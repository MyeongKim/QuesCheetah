from django.contrib import admin
from vote.models import Question, Answer, MultiQuestion, UserAnswer

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(MultiQuestion)
admin.site.register(UserAnswer)
