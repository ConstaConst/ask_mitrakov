from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class ProfileManager(models.Manager):
    def create_user(self, username, email, password, nickname, avatar):
        user = User.objects.create_user(username, email, password)
        return self.create(user=user, nickname=nickname, avatar=avatar)

    def best_members(self):
        return self.all()


class Profile(models.Model):
    objects = ProfileManager()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=32)
    avatar = models.ImageField(default='default_ava.png')

    def __str__(self):
        return self.user.username


class QuestionManager(models.Manager):
    def fresh(self):
        return self.all()

    def hot(self):
        return self.order_by()


class Question(models.Model):
    objects = QuestionManager()
    title = models.CharField(max_length=128)
    text = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.author.user.username + " - " + self.title


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField()
    is_correct = models.BooleanField(default=False)


class TagManager(models.Manager):
    def most_popular(self):
        return self.order_by('questions')#как поулчить количество вопросов?


class Tag(models.Model):
    objects = TagManager()
    name = models.CharField(max_length=16)
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return self.name
