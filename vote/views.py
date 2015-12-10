from django.shortcuts import render
from main.models import ApiKey
from vote.models import Question, Answer
# Create your views here.


def new(request, api_key):
    context = {
        api_key : api_key
    }

    if request.method == 'POST':

        # save question first
        question_text = request.POST.get('question')

        q_api_key = ApiKey.objects.get(key=api_key)

        new_question = Question(api_key=q_api_key, question_text=question_text)
        new_question.save()

        # save answers
        for i in range(9):
            name = 'answer'+str(i)
            if request.POST.get(name):
                new_answer = Answer(question=new_question, answer_text=request.POST.get(name), answer_num=i)
                new_answer.save()

        context.update({'msg': '투표가 저장되었습니다.'})

    return render(request, 'vote/pages/new.html', context)