from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Form(models.Model):
    slug = models.SlugField(verbose_name=_("slug"), max_length=100, db_comment="slug")
    title = models.CharField(verbose_name=_("title"), max_length=255, db_comment="title")
    start_date = models.DateTimeField(verbose_name=_("start date"), db_comment="start date")
    end_date = models.DateTimeField(verbose_name=_("end date"), db_comment="end date")
    updated_by = models.ForeignKey(
        User,
        verbose_name=_("updated by"),
        related_name="+",
        on_delete=models.SET_NULL,
        null=True,
        db_comment="last user who updated",
    )
    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True, db_comment="created at")
    update_at = models.DateTimeField(verbose_name=_("updated at"), auto_now=True, db_comment="updated at")

    class Meta:
        db_table = "form"
        verbose_name = _("form")
        verbose_name_plural = _("forms")


class Component(models.Model):
    TITLE = 100
    TEXT, TEXTAREA = 200, 201
    RADIO, CHECKBOX, SELECT = 300, 301, 302
    TYPE_CHOICES = (
        (TITLE, "TITLE"),
        (TEXT, "TEXT"),
        (TEXTAREA, "TEXTAREA"),
        (RADIO, "RADIO"),
        (CHECKBOX, "CHECKBOX"),
        (SELECT, "SELECT"),
    )
    QUESTION_TYPES = (TEXT, TEXTAREA, RADIO, CHECKBOX, SELECT)
    QUESTION_SELECT_TYPES = (RADIO, CHECKBOX, SELECT)

    form = models.ForeignKey(Form, related_name="+", on_delete=models.CASCADE, db_comment="form FK")
    type = models.SmallIntegerField(verbose_name=_("type"), choices=TYPE_CHOICES, db_comment="type")
    max_allowed_size = models.SmallIntegerField(
        verbose_name=_("max allowed size"), null=True, blank=True, db_comment="max allowed size"
    )
    title = models.CharField(verbose_name=_("title"), blank=True, max_length=255, db_comment="title")
    description = models.CharField(verbose_name=_("description"), blank=True, max_length=500, db_comment="description")
    order = models.SmallIntegerField(verbose_name=_("order"), default=0, db_comment="order")
    updated_by = models.ForeignKey(
        User,
        verbose_name=_("updated by"),
        related_name="+",
        on_delete=models.SET_NULL,
        null=True,
        db_comment="last user who updated",
    )
    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True, db_comment="created at")
    update_at = models.DateTimeField(verbose_name=_("updated at"), auto_now=True, db_comment="updated at")

    class Meta:
        db_table = "component"
        verbose_name = _("component")
        verbose_name_plural = _("components")

    @property
    def is_question(self) -> bool:
        result = False
        if self.type in self.QUESTION_TYPES:
            result = True
        return result


class Choice(models.Model):
    component = models.ForeignKey(Component, related_name="+", on_delete=models.CASCADE, db_comment="question FK")
    text = models.CharField(verbose_name=_("text"), max_length=255, db_comment="title")
    order = models.SmallIntegerField(verbose_name=_("order"), default=0, db_comment="order")
    updated_by = models.ForeignKey(
        User,
        verbose_name=_("updated by"),
        related_name="+",
        on_delete=models.SET_NULL,
        null=True,
        db_comment="last user who updated",
    )
    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True, db_comment="created at")
    update_at = models.DateTimeField(verbose_name=_("updated at"), auto_now=True, db_comment="updated at")

    class Meta:
        db_table = "choice"
        verbose_name = _("choice")
        verbose_name_plural = _("choices")


class Submit(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, db_comment="form FK")
    form_title = models.CharField(verbose_name=_("form title"), max_length=255, db_comment="title")
    user = models.ForeignKey(
        User, verbose_name=_("user"), on_delete=models.SET_NULL, null=True, db_comment="user who submitted"
    )
    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True, db_comment="created at")

    class Meta:
        db_table = "submit"
        verbose_name = _("submit")
        verbose_name_plural = _("submits")


class Answer(models.Model):
    submit = models.ForeignKey(
        Submit, verbose_name=_("submit"), related_name="+", on_delete=models.CASCADE, db_comment="submit FK"
    )
    component = models.ForeignKey(
        Component, verbose_name=_("component"), related_name="+", on_delete=models.DO_NOTHING, db_comment="component FK"
    )
    question_title = models.CharField(
        verbose_name=_("question title"), max_length=255, blank=True, db_comment="component title"
    )
    answer = models.CharField(verbose_name=_("answer"), blank=True, max_length=1000, db_comment="text")
    choice = models.ForeignKey(
        Choice,
        verbose_name=_("choice"),
        related_name="+",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        db_comment="choice FK",
    )
    choice_text = models.CharField(verbose_name=_("choice text"), max_length=255, blank=True, db_comment="choice text")
    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True, db_comment="created at")

    class Meta:
        db_table = "answer"
        verbose_name = _("answer")
        verbose_name_plural = _("answers")
