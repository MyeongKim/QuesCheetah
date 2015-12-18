from django.db import models
from main.models import ApiKey

from datetime import datetime, timedelta
# Create your models here.


class Question(models.Model):
    api_key = models.ForeignKey(ApiKey, related_name='question_key')
    question_text = models.CharField(max_length=100)
    question_title = models.CharField(max_length=50)
    is_closed = models.BooleanField(default=False)

    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)

    # todo check date is later than now ==> in forms.py
    start_dt = models.DateTimeField(auto_now_add=True)
    end_dt = models.DateTimeField(default=datetime.now()+timedelta(days=365))

    def __str__(self):
        return 'id:{},{}'.format(self.id, self.question_text)

    def check_end_dt(self):
        if self.end_dt < datetime.now():
            self.is_closed = True
            return False
        return True


class AnswerManager(models.Manager):

    def get_answer_num(self, question, answer_num):
        return self.filter(question=question, answer_num=answer_num).count()


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='object_question')
    answer_text = models.CharField(max_length=50)
    answer_num = models.IntegerField()
    unique_user = models.CharField(max_length=255, unique=True)  # apikey + unique ID

    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)

    objects = AnswerManager()

    def __str__(self):
        return '{}-({})'.format(self.answer_text, self.count)
