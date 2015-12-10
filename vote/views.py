from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render, redirect
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


def action(request, api_key):
    context = {

    }

    a = ApiKey.objects.get(key=api_key)

    if not a.question_key:
        return redirect('vote:new')

    question = Question.objects.get(api_key=a)
    answers = Answer.objects.filter(question=question)

    context.update({'question':question, 'answers':answers})
    return render(request, 'vote/pages/action.html', context)


def update(request):

    q_key = request.POST.get('q_key')
    update_num = request.POST.get('update_num')

    a = ApiKey.objects.get(key=q_key)
    question = Question.objects.get(api_key=a)

    Answer.objects.filter(question=question, answer_num=update_num).update(count=F('count')+1)

    return JsonResponse({})

