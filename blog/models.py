from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.urls import reverse


# ######################## Question ####################
# class Question(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=120)
#     slug = models.SlugField(unique=True)
#     image = models.ImageField(
#         upload_to='images/',
#         null=True,
#         blank=True,
#         width_field="width_field",
#         height_field="height_field"
#     )
#     height_field = models.IntegerField(default=50)
#     width_field = models.IntegerField(default=50)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def get_api_url(self):
#         return reverse("question_detail", kwargs={"slug": self.slug})

#     class Meta:
#         ordering = ['-created_at']

#     def __unicode__(self):
#         return self.title

#     def __str__(self):
#         return self.title

#     @property
#     def answers(self):
#         instance = self
#         qs = Answer.objects.filter_by_instance(instance)
#         return qs

#     @property
#     def get_content_type(self):
#         instance = self
#         content_type = ContentType.objects.get_for_model(instance.__class__)
#         return content_type


# ########################### Answer ###################
# class AnswerManager(models.Manager):
#     def all(self):
#         qs = super(AnswerManager, self).filter(parent=None)
#         return qs

#     def filter_by_instance(self, instance):
#         content_type = ContentType.objects.get_for_model(instance.__class__)
#         obj_id = instance.id
#         qs = super(AnswerManager, self).filter(content_type=content_type, object_id=obj_id).filter(parent=None)
#         return qs

#     def create_by_model_type(self, model_type, pk, content, user, parent_obj=None):
#         model_qs = ContentType.objects.filter(model=model_type)
#         if model_qs.exists():
#             SomeModel = model_qs.first().model_class()
#             obj_qs = SomeModel.objects.filter(pk=pk)
#             if obj_qs.exists() and obj_qs.count() == 1:
#                 instance = self.model()
#                 instance.content = content
#                 instance.user = user
#                 instance.content_type = model_qs.first()
#                 instance.object_id = obj_qs.first().id
#                 if parent_obj:
#                     instance.parent = parent_obj
#                 instance.save()
#                 return instance
#         return None


# class Answer(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')
#     parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)

#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     objects = AnswerManager()

#     class Meta:
#         ordering = ['-timestamp']

#     def __unicode__(self):
#         return str(self.user.username)

#     def __str__(self):
#         return str(self.user.username)

#     def children(self):
#         return Answer.objects.filter(parent=self)

#     @property
#     def is_parent(self):
#         if self.parent is not None:
#             return False
#         return True