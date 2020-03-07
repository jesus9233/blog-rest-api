from rest_framework import serializers

from .models import Question, Answer

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model


###################### User ########################
User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(label='Email Address')
    email2 = serializers.EmailField(label='Confirm Email')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password',
            
        ]
        extra_kwargs = {
            "password":{"write_only": True}
        }

    def validate(self, data):
        return data

    def validate_email(self, value):
        data = self.get_initial()
        email1 = data.get("email2")
        email2 = value
        if email1 != email2:
            raise serializers.ValidationError("Emails must match.")
        
        user_qs = User.objects.filter(email=email2)
        if user_qs.exists():
            raise serializers.ValidationError("This user has already registered.")

        return value

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get("email")
        email2 = value
        if email1 != email2:
            raise serializers.ValidationError("Emails must match.")
        return value

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
            username = username,
            email = email
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserLoginSerializer(serializers.ModelSerializer):
    token = serializers.CharField(allow_blank=True, read_only=True)
    username = serializers.CharField()
    email = serializers.EmailField(label='Email Address')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'token',
        ]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate(self, data):
        return data


###################### Question ###########################
class QuestionCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            'id',
            'title',
            'content'
        )


question_detail_url = serializers.HyperlinkedIdentityField(
    view_name='question_detail',
    lookup_field='pk'
)


class QuestionDetailSerializer(serializers.ModelSerializer):
    url = question_detail_url
    user = UserDetailSerializer(read_only=True)
    image = serializers.SerializerMethodField()
    answers = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = (
            'id',
            'user',
            'image',
            'url',
            'title',
            'slug',
            'content',
            'answers'
        )

    def get_image(self, obj):
        try:
            image = obj.image.path
        except:
            image = None
        return image

    def get_answers(self, obj):
        a_qs = Answer.objects.filter_by_instance(obj)
        answers = AnswerSerializer(a_qs, many=True).data
        return answers


class QuestionListSerializer(serializers.ModelSerializer):
    url = question_detail_url
    user = UserDetailSerializer(read_only=True)
    class Meta:
        model = Question
        fields = [
            'id',
            'url',
            'user',
            'title',
            'content',
        ]


####################### Answer Serializers ###############################
def create_answer_serializer(model_type='post', pk=None, parent_id=None, user=None):
    class AnswerCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Answer
            fields = [
                'id',
                'parent',
                'content',
                'timestamp'
            ]

        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.pk = pk
            self.parent_obj = None
            if parent_id:
                parent_qs = Answer.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    self.parent_obj = parent_qs.first()
            return super(AnswerCreateSerializer, self).__init__(*args, **kwargs)

        def validate(self, data):
            model_type = self.model_type
            model_qs = ContentType.objects.filter(model=model_type)
            if not model_qs.exists() or model_qs.count() != 1:
                raise serializers.ValidationError("This is not a valid content type.")
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(pk=self.pk)
            if not obj_qs.exists() or obj_qs.count() != 1:
                raise serializers.ValidationError("This is not a pk for this content type.")
            return data

        def create(self, validated_data):
            content = validated_data.get("content")
            if user:
                main_user = user
            else:
                main_user = User.objects.all().first()
            model_type = self.model_type
            pk = self.pk
            parent_obj = self.parent_obj
            answer = Answer.objects.create_by_model_type(
                model_type=model_type,
                pk=pk,
                content=content,
                user=main_user,
                parent_obj=parent_obj
            )
            return answer

    return AnswerCreateSerializer


class AnswerSerializer(serializers.ModelSerializer):
    reply_count = serializers.SerializerMethodField()
    class Meta:
        model = Answer
        fields = (
            'id',
            'content_type',
            'object_id',
            'parent',
            'content',
            'reply_count',
            'timestamp'
        )

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0


class AnswerListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='answer_detail')
    reply_count = serializers.SerializerMethodField()
    class Meta:
        model = Answer
        fields = [
            'url',
            'id',
            'content',
            'reply_count',
            'timestamp',
        ]
    
    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0


class AnswerChildSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    class Meta:
        model = Answer
        fields = (
            'id',
            'user',
            'content',
            'timestamp'
        )


class AnswerDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='answer_detail')
    reply_count = serializers.SerializerMethodField()
    content_object_url = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    class Meta:
        model = Answer
        fields = [
            'id',
            'user',
            'url',
            'content',
            'reply_count',
            'replies',
            'timestamp',
            'content_object_url',
        ]
        read_only_fields = [
            'reply_count',
            'replies',
        ]

    def get_content_object_url(self, obj):
        try:
            return obj.content_object.get_api_url()
        except:
            return None

    def get_replies(self, obj):
        if obj.is_parent:
            return AnswerChildSerializer(obj.children(), many=True).data
        return None

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0
