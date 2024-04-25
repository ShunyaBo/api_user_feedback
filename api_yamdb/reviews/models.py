import datetime as dt

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User

COMMENT_SIZE = 30


def validate_year(year):
    now_year = dt.date.today()
    if year > now_year.year:
        raise ValueError(f'некорректный год {year}')


class Category(models.Model):
    name = models.CharField(verbose_name="название", max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(verbose_name="название", max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        return self.name


class Title(models.Model):

    name = models.CharField(verbose_name='название', max_length=256)
    year = models.IntegerField(
        'год релиза',
        validators=[validate_year],
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='категория',
        null=True,
        blank=True,
        related_name='titles'
    )
    description = models.TextField(
        null=True,
        verbose_name='описание'
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'

    def __str__(self) -> str:
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.genre} {self.title}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='заголовок'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='дата отзыва'
    )
    text = models.TextField()
    score = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)],
        verbose_name='оценка'
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name="unique_review")
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='дата комментария'
    )
    text = models.TextField()

    class Meta:
        verbose_name = 'коментарий'
        verbose_name_plural = 'коментарии'

    def __str__(self):
        return self.text[:COMMENT_SIZE]
