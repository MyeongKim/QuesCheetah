from django.db import models
from main.models import ApiKey
# Create your models here.


class Question(models.Model):
    api_key = models.ForeignKey(ApiKey, related_name='question_key')
    question_text = models.CharField(max_length=100)
    question_title = models.CharField(max_length=30)
    is_closed = models.BooleanField(default=False)

    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)

    start_dt = models.DateTimeField(auto_now_add=True)
    end_dt = models.DateTimeField()


    def __str__(self):
        return 'id:{},{}'.format(self.id, self.question_text)


@property
class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='object_question')
    answer_text = models.CharField(max_length=50)
    answer_num = models.IntegerField()

    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}-({})'.format(self.answer_text, self.count)
    #
    # def get_answer_num(self):
    #     return 0
    