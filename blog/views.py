from django.contrib.auth import get_user_model

from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin

from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView,
    DestroyAPIView
)

from rest_framework.permissions import (
    AllowAny,
)

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from .permissions import IsOwnerOrReadOnly
from .pagination import QuestionPageNumberPagination

from .models import Question, Answer
from .serializers import (
    UserCreateSerializer,
    UserLoginSerializer,
    QuestionCreateUpdateSerializer,
    QuestionDetailSerializer,
    QuestionListSerializer,
    AnswerListSerializer,
    AnswerDetailSerializer,
    create_answer_serializer
)


User = get_user_model()

####################### User Login/Register ##############################
class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer
    
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


####################### Question Serializers #############################
class QuestionCreateAPIView(CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class QuestionDetailAPIView(RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionDetailSerializer
    permission_classes = [AllowAny]
    # lookup_field = 'slug'


class QuestionUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionCreateUpdateSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class QuestionDeleteAPIView(DestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]


class QuestionListAPIView(ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionListSerializer
    permission_classes = [AllowAny]
    pagination_class = QuestionPageNumberPagination


# ####################### Answer Serializers #############################
# class AnswerCreateAPIView(CreateAPIView):
#     queryset = Answer.objects.all()

#     def get_serializer_class(self):
#         model_type = self.request.GET.get("type")
#         pk = self.request.GET.get("pk")
#         parent_id = self.request.GET.get("parent_id", None)
#         return create_answer_serializer(model_type=model_type, pk=pk, parent_id=parent_id, user=self.request.user)


# class AnswerDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
#     queryset = Answer.objects.filter(id__gte=0)
#     serializer_class = AnswerDetailSerializer
#     permission_classes = [IsOwnerOrReadOnly]

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


# class AnswerListAPIView(ListAPIView):
#     queryset = Answer.objects.filter(id__gte=0)
#     serializer_class = AnswerListSerializer
#     permission_classes = [AllowAny]
#     pagination_class = QuestionPageNumberPagination