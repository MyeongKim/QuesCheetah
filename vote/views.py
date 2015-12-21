from datetime import timezone
from django.core.exceptions import ValidationError
from django.db.models import F
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from main.models import ApiKey
from vote.models import Question, Answer, UserAnswer

# Create your views here.


def new(request, api_key):
    context = {
        'api_key': api_key
    }

    if request.method == 'POST':

        # save question first
        question_text = request.POST.get('question_text')
        question_title = request.POST.get('question_title')

        q_api_key = ApiKey.objects.get(key=api_key)

        new_question = Question(api_key=q_api_key, question_text=question_text, question_title=question_title)
        new_question.save()

        # save answers
        for i in range(9):
            name = 'answer'+str(i)
            if request.POST.get(name):
                new_answer = Answer(question=new_question, answer_text=request.POST.get(name), answer_num=i)
                new_answer.save()

        messages.add_message(request, messages.INFO, '투표가 저장되었습니다.')
        return redirect('vote:select_question', api_key= api_key)

    return render(request, 'vote/pages/new.html', context)


def select_question(request, api_key):
    context = {
        'api_key' : api_key
    }

    q_api_key = ApiKey.objects.get(key=api_key)

    try:
        question = Question.objects.filter(api_key=q_api_key)

    except Question.DoesNotExist:
        return render(request, 'vote/pages/question_select.html', context)

    answers = Answer.objects.filter(question=question)
    context.update({'question': question, 'answers': answers})

    return render(request, 'vote/pages/question_select.html', context)


def update(request):

    q_id = request.POST.get('q_id')
    update_num = request.POST.get('update_num')
    unique_id = request.POST.get('uniqueId')

    question = Question.objects.get(id=q_id)
    answer = Answer.objects.get(question=question, answer_num=update_num)

    response_dict = {}

    try:
        new_answer = UserAnswer(answer=answer, unique_user=unique_id)
        new_answer.save()
    except Exception as e:
        response_dict.update({'exception_msg': "theres a problem."})
        response_dict.update({'msg': e.message})

    return JsonResponse(response_dict)


def get_vote(request, api_key, question_title):
    context = {

    }
    question = Question.objects.get(api_key=ApiKey.objects.get(key=api_key), question_title=question_title)
    if question:
        answers = Answer.objects.filter(question=question)
        context.update({'question': question, 'answers': answers})

        return render(request, 'vote/pages/action.html', context)

    else:
        return HttpResponse("question is not exist")


# todo bring graph data.. etc
def get_result(request, api_key, question_title):

    a = ApiKey.objects.get(key=api_key)
    pass


def delete(request, api_key, question_title):
    question = Question.objects.get(api_key=api_key, question_title=question_title)
    question.delete()

    return JsonResponse({})
