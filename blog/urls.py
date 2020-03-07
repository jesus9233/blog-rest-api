from django.urls import path, include
from .views import (
    UserCreateAPIView,
    UserLoginAPIView,
    QuestionCreateAPIView,
    QuestionDetailAPIView,
    QuestionUpdateAPIView,
    QuestionDeleteAPIView,
    QuestionListAPIView,
    AnswerCreateAPIView,
    AnswerDetailAPIView,
    AnswerListAPIView
)


urlpatterns = [
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('users/login/', UserLoginAPIView.as_view(), name='login'),
    path('users/register/', UserCreateAPIView.as_view(), name='register'),

    path('questions/', QuestionListAPIView.as_view(), name='question_list'),
    path('questions/create/', QuestionCreateAPIView.as_view(), name='question_create'),
    path('questions/<int:pk>/', QuestionDetailAPIView.as_view(), name='question_detail'),
    path('questions/<int:pk>/edit/', QuestionUpdateAPIView.as_view(), name='question_update'),
    path('questions/<int:pk>/delete/', QuestionDeleteAPIView.as_view(), name='question_delete'),

    path('answers/', AnswerListAPIView.as_view(), name='answer_list'),
    path('answers/create/', AnswerCreateAPIView.as_view(), name='answer_create'),
    path('answers/<int:pk>/', AnswerDetailAPIView.as_view(), name='answer_detail')
]