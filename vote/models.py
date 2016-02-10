# 직접 개발한 코드
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import ManyToManyField
from django.utils.translation import ugettext as _
import re
from main.models import ApiKey

from datetime import datetime, timedelta
from django.utils import timezone
# Create your models here.


class MultiQuestion(models.Model):
    api_key = models.ForeignKey(ApiKey, related_name='multiquestions')
    group_name = models.CharField(max_length=100, unique=True)

    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return 'id:{},{}'.format(self.id, self.group_name)

    @property
    def get_question_count(self):
        return self.question_elements.filter(is_removed=False).count()


class Question(models.Model):
    TYPE_SURVEY = 'SURV'
    TYPE_VOTE = 'VOTE'
    TYPE_CHOICE = (
        (TYPE_SURVEY, 'Survey'),
        (TYPE_VOTE, 'Vote'),
    )

    api_key = models.ForeignKey(ApiKey, related_name='questions')

    type = models.CharField(max_length=60, choices=TYPE_CHOICE, default=TYPE_VOTE)

    ''' is checked group question '''
    multi_question = models.ForeignKey(MultiQuestion, related_name='question_elements', null=True)

    ''' question '''
    question_title = models.CharField(max_length=50)
    question_text = models.CharField(max_length=100)
    question_num = models.CharField(max_length=10, null=True)

    ''' question available '''
    is_closed = models.BooleanField(default=False)
    start_dt = models.DateTimeField()
    end_dt = models.DateTimeField()
    is_editable = models.BooleanField(default=True)  # if answer can be changed
    is_private = models.BooleanField(default=False)
    is_removed = models.BooleanField(default=False)

    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'id:{},{}'.format(self.id, self.question_text)

    @classmethod
    def check_same_title(cls, api_key, new_title):
        if cls.objects.filter(api_key=api_key, question_title=new_title):
            return True
        return False

    def clean(self):
        # clean question_title
        # if self.check_same_title(self.api_key, self.question_title):
            # raise ValidationError({'question_title': _('This question_title is already exist in same api_key')})

        # clean start_dt
        if self.start_dt:
            if datetime.strptime(self.start_dt, '%Y-%m-%dT%H:%M') < datetime.now():
                raise ValidationError({'start_dt': _('Start date should be later than now')})
        else:
            self.start_dt = timezone.now()

        # clean end_dt
        if self.end_dt:
            if datetime.strptime(self.end_dt, '%Y-%m-%dT%H:%M') <= datetime.strptime(self.start_dt, '%Y-%m-%dT%H:%M'):
                raise ValidationError({'end_dt': _('End date should be later than start date')})
        else:
            self.end_dt = timezone.now() + timezone.timedelta(days=30)

        if not re.match(r'[a-zA-Z0-9]*$', self.question_title):
            raise ValidationError({
                'question_title': _('question_title has to be consisted of characters and numbers with no whitespace.')
            })

    def save(self, **kwargs):
        my_value = kwargs.pop('is_update', None)
        if my_value:
            return super(Question, self).save(**kwargs)
        else:
            self.clean()
            return super(Question, self).save(**kwargs)


class Url(models.Model):
    question = models.ForeignKey(Question, related_name='authenticated_urls')
    url_name = models.CharField(max_length=100, null=True, blank=True)
    full_url = models.CharField(max_length=200)

    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return '{}-({})'.format(self.url_name, self.full_url)


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers')
    answer_text = models.CharField(max_length=50)
    answer_num = models.IntegerField(null=True)

    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return '{}-({})'.format(self.answer_text, self.answer_num)

    @property
    def get_answer_count(self):
        return self.answer.count()


# user vote info 따로 관리
class UserAnswer(models.Model):
    answer = models.ForeignKey(Answer, related_name='answer')
    unique_user = models.CharField(max_length=100, unique=True)  # api_key+unique Id
    # survey_text = models.TextField()

    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return '{}-{}'.format(self.answer, self.unique_user)


# make a dictionary which includes editable fields
def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in opts.concrete_fields + opts.many_to_many:
        if isinstance(f, ManyToManyField):
            if instance.pk is None:
                data[f.name] = []
            else:
                data[f.name] = list(f.value_from_object(instance).values_list('pk', flat=True))
        else:
            data[f.name] = f.value_from_object(instance)
    return data
