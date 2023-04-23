from django.db import models


class Form(models.Model):
    slug = models.SlugField(max_length=100, db_comment="slug")
    title = models.CharField(max_length=255, db_comment="title")
    start_date = models.DateTimeField(db_comment="start date")
    end_date = models.DateTimeField(db_comment="end date")
    created_at = models.DateTimeField(auto_now_add=True, null=True, db_comment="created at")
    update_at = models.DateTimeField(auto_now=True, null=True, db_comment="updated at")

    class Meta:
        db_table = "form"


class Component(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, db_comment="form FK")
    type = models.CharField(max_length=20, db_comment="type")
    title = models.CharField(max_length=255, db_comment="title")
    note = models.CharField(max_length=500, db_comment="note")
    order = models.SmallIntegerField(db_comment="order")

    class Meta:
        db_table = "component"


class Question(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE, db_comment="component FK")
    title = models.CharField(max_length=255, db_comment="title")
    note = models.CharField(max_length=500, db_comment="note")
    type = models.CharField(max_length=20, db_comment="type")
    allowed_size = models.SmallIntegerField(db_comment="allowed_size")
    is_required = models.BooleanField(db_comment="is required")

    class Meta:
        db_table = "question"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, db_comment="question FK")
    title = models.CharField(max_length=255, db_comment="title")
    order = models.SmallIntegerField(db_comment="order")

    class Meta:
        db_table = "choice"
