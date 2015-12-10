from django.db import models
from main.models import ApiKey
# Create your models here.


class Question(models.Model):
    api_key = models.OneToOneField(ApiKey, related_name='question_key', primary_key=True)
    question_text = models.CharField(max_length=100)
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='object_question')
    answer_text = models.CharField(max_length=50)
    answer_num = models.IntegerField()
    count = models.IntegerField(default=0)

    def __str__(self):
        return '{}-({})'.format(self.answer_text, self.count)

