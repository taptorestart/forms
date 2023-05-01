from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.forms.models import Form, Component, Choice, Submit


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "slug",
        "title",
        "start_date",
        "end_date",
        "updated_by",
        "created_at",
        "update_at",
    )
    readonly_fields = ("updated_by",)

    def save_model(self, request, obj: Form, form, change):
        obj.updated_by_id = request.user.id
        super().save_model(request, obj, form, change)


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
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
    readonly_fields = (
        "updated_by",
        "is_question",
    )
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
class ChoiceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "component_title",
        "text",
        "order",
        "updated_by",
        "created_at",
        "update_at",
    )
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
class SubmitAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "form_slug",
        "form_title",
        "user",
        "answer",
    )

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
