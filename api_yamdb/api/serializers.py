import datetime as dt

from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from api.validators import UserDataValidation
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

MAX_SCORE = 10


class UserSerializer(serializers.ModelSerializer, UserDataValidation):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class SignupSerializer(serializers.Serializer, UserDataValidation):

    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True, max_length=150)


class GetTokenSerializer(serializers.Serializer, UserDataValidation):

    username = serializers.CharField(required=True, max_length=150)
    confirmation_code = serializers.CharField(required=True)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id', )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id', )


class TitleWriteSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        required=False,
        queryset=Genre.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        current_year = dt.date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                f'Год должен быть меньше {current_year}')
        return value


class TitleReadSerializer(serializers.ModelSerializer):

    category = CategorySerializer(required=True)
    genre = GenreSerializer(many=True, required=False)
    rating = serializers.IntegerField()

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title
        read_only_fields = ('id', 'name', 'year', 'rating',
                            'description', 'genre', 'category')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title', )

    def validate(self, data):
        title = get_object_or_404(
            Title.objects.prefetch_related(
                models.Prefetch(
                    "reviews", queryset=Review.objects.select_related("author")
                )
            ),
            id=self.context["view"].kwargs["title_id"],
        )
        author = self.context["request"].user
        if not self.instance and title.reviews.filter(author=author).exists():
            raise serializers.ValidationError(
                f'Ревью на "{title}" от "{author}" уже существует'
            )
        return data

    def validate_score(self, value):
        if 0 >= value or value > MAX_SCORE:
            raise serializers.ValidationError(
                f'Оценка может быть только числом от 1 до {MAX_SCORE}')
        return value


class CommentSerializer(serializers.ModelSerializer):

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
