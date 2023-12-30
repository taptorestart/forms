from celery.result import AsyncResult
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, User
from django.http import Http404, JsonResponse, FileResponse
from django.urls import path
from django.utils.safestring import mark_safe
from rest_framework import status
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from apps.forms.models import Form, Component, Choice, Submit
from apps.forms.tasks import download_xlsx

admin.site.unregister(Group)
admin.site.unregister(User)


@admin.register(Group)
class GroupAdmin(GroupAdmin, ModelAdmin):
    list_display = ("name",)


@admin.register(User)
class UserAdmin(UserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    list_display = ("id", "username", "email", "is_superuser", "is_staff", "is_active")
    list_display_links = ("id", "username")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("id", "username", "email")
    filter_horizontal = ("groups", "user_permissions")


@admin.register(Form)
class FormAdmin(ModelAdmin):
    list_display = ("id", "slug", "title", "start_date", "end_date", "updated_by", "created_at", "update_at")
    readonly_fields = ("updated_by",)

    def save_model(self, request, obj: Form, form, change):
        obj.updated_by_id = request.user.id
        super().save_model(request, obj, form, change)


@admin.register(Component)
class ComponentAdmin(ModelAdmin):
    list_display = (
        "id",
        "form_slug",
        "form_title",
        "type",
        "is_question",
        "max_allowed_size",
        "title",
        "description",
        "order",
        "updated_by",
        "created_at",
        "update_at",
    )
    readonly_fields = ("updated_by", "is_question")
    raw_id_fields = ("form",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related("form", "updated_by")
        return queryset

    def form_slug(self, obj: Component) -> str:
        return obj.form.slug

    def form_title(self, obj: Component) -> str:
        return obj.form.title

    def save_model(self, request, obj: Component, form, change):
        obj.updated_by_id = request.user.id
        if not change:
            order_list = Component.objects.filter(form_id=obj.form_id).values_list("order", flat=True)
            obj.order = max(order_list) + 1 if order_list else 1
        super().save_model(request, obj, form, change)


@admin.register(Choice)
class ChoiceAdmin(ModelAdmin):
    list_display = ("id", "component_title", "text", "order", "updated_by", "created_at", "update_at")
    readonly_fields = ("updated_by",)
    raw_id_fields = ("component",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related("component", "updated_by")
        return queryset

    def component_title(self, obj: Choice) -> str:
        return obj.component.title

    def save_model(self, request, obj: Choice, form, change):
        obj.updated_by_id = request.user.id
        if not change:
            order_list = Choice.objects.filter(component_id=obj.component_id).values_list("order", flat=True)
            obj.order = max(order_list) + 1 if order_list else 1
        super().save_model(request, obj, form, change)


@admin.register(Submit)
class SubmitAdmin(ModelAdmin):
    list_display = ("id", "form_slug", "form_title", "user", "answer")
    list_filter = ("form__slug",)

    change_list_template = "list.html"

    def form_slug(self, obj: Submit) -> str:
        return obj.form.slug

    def answer(self, obj: Submit) -> str:
        answers = obj.answer_set.all()
        answer_html = ""
        for i, answer in enumerate(answers):
            answer_html += f"Q. {answer.question_title}<br>"
            if answer.component.type in Component.QUESTION_SELECT_TYPES:
                answer_html += f"A. {answer.choice_text}"
            else:
                answer_html += f"A. {answer.answer}"
            if i != len(answers) - 1:
                answer_html += "<br>"
        return mark_safe(answer_html)

    def get_urls(self):
        urls = [
            path("download/", self.download, name="download"),
            path("download-status/", self.download_status, name="download_status"),
            path("download-file/", self.download_file, name="download_file"),
        ]
        return urls + super().get_urls()

    def download(self, request):
        if not request.user.is_staff:
            raise Http404()
        slug = request.GET.get("form__slug")
        task = download_xlsx.delay(slug)
        return JsonResponse({"task": task.id}, status=status.HTTP_202_ACCEPTED)

    def download_status(self, request):
        if not request.user.is_staff:
            raise Http404()
        task = request.GET.get("task")
        task_result = AsyncResult(task)
        payload = {
            "task": task,
            "status": task_result.status,
            "result": task_result.result,
        }
        return JsonResponse(payload, status=status.HTTP_200_OK)

    def download_file(self, request):
        if not request.user.is_staff:
            raise Http404()
        filename = request.GET.get("filename")
        filepath = f"/tmp/forms/{filename}"
        response = FileResponse(open(filepath, "rb"))
        response["Content-Disposition"] = f"attachment; filename={filename}"
        return response
