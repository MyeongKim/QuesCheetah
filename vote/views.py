from datetime import timezone
from http.cookiejar import request_path
from django.core import serializers
from django.core.exceptions import ValidationError
from django.db.models import F
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST
from main.models import ApiKey
from vote.models import Question, Answer, UserAnswer, Url

# Create your views here.


def new(request, api_key):
    context = {
        'api_key': api_key
    }

    if request.method == 'POST':

        # save question first
        create_question(request)

        # save answers
        create_answer(request)

        messages.add_message(request, messages.INFO, '투표가 저장되었습니다.')

        return redirect('vote:select_question', api_key=api_key)

    return render(request, 'vote/pages/new.html', context)


def select_question(request, api_key):
    context = {
        'api_key': api_key
    }

    q_api_key = ApiKey.objects.get(key=api_key)

    try:
        question = Question.objects.filter(api_key=q_api_key)

    except Question.DoesNotExist:
        return render(request, 'vote/pages/question_select.html', context)

    answers = Answer.objects.filter(question=question)
    context.update({'question': question, 'answers': answers})

    return render(request, 'vote/pages/question_select.html', context)


def get_vote(request, api_key, question_title):
    context = {
        'api_key' : api_key
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
    # use to_dict?
    pass


def delete(request, api_key, question_title):
    question = Question.objects.get(api_key=api_key, question_title=question_title)
    question.delete()

    return JsonResponse({})

# todo update 하는 api 는 PUT method로.

# todo url 맨 처음 /v1/ 붙이기.

# todo question - list, update, delete
# todo answer -  update, delete, simple_view, full_view
# todo useranswer -  update,
# todo api - get, create,

# ======================================

'''
question management
'''


@require_POST
def to_private(request):
    """
    POST - /v1/question/private

    question을 private으로 전환합니다.

    :parameter - api_key, ( question_title / question_id )
    :return -
    """
    api_key = request.POST.get('api_key')
    question_title = request.POST.get('question_title')
    question_id = request.POST.get('question_id')

    response_dict = {}

    a = ApiKey.objects.get(key=api_key)

    if question_title and question_id:
        q = Question.objects.get(api_key=a, question_title=question_title, id=question_id)

    elif question_id:
        q = Question.objects.get(api_key=a, id=question_id)
    elif question_title:
        q = Question.objects.get(api_key=a, question_title=question_title)

    if q:

        q.is_private = True
        q.save()

    else:
        response_dict.update({
            'error': "Can't find the question."
        })

    return JsonResponse(response_dict)


@require_POST
def to_public(request):
    """
    POST - /v1/question/public

    question을 public으로 전환합니다.

    :parameter - api_key, ( question_title / question_id )
    :return -
    """
    api_key = request.POST.get('api_key')
    question_title = request.POST.get('question_title')
    question_id = request.POST.get('question_id')

    response_dict = {}

    a = ApiKey.objects.get(key=api_key)

    if question_title and question_id:
        q = Question.objects.get(api_key=a, question_title=question_title, id=question_id)

    elif question_id:
        q = Question.objects.get(api_key=a, id=question_id)
    elif question_title:
        q = Question.objects.get(api_key=a, question_title=question_title)

    if q:

        q.is_private = False
        q.save()

    else:
        response_dict.update({
            'error': "Can't find the question."
        })

    return JsonResponse(response_dict)


@require_POST
def get_url_list(request):
    """
    POST - /v1/question/url/list

    허용하는 url list 를 return 합니다.

    :parameter - api_key, ( question_title / question_id )
    :return - urls
    """
    api_key = request.POST.get('api_key')
    question_title = request.POST.get('question_title')
    question_id = request.POST.get('question_id')

    response_dict = {}

    a = ApiKey.objects.get(key=api_key)

    if question_title and question_id:
        q = Question.objects.get(api_key=a, question_title=question_title, id=question_id)

    elif question_id:
        q = Question.objects.get(api_key=a, id=question_id)
    elif question_title:
        q = Question.objects.get(api_key=a, question_title=question_title)

    if q:

        u = q.authenticated_urls
        if u:
            response_dict.update({
                'urls': [url.full_url for url in u]
            })
        else:
            response_dict.update({
                'error': "no urls in this question"
            })
    else:
        response_dict.update({
            'error': "Can't find the question."
        })

    return JsonResponse(response_dict)


@require_POST
def add_url(request):
    """
    POST - /v1/question/url/add

    허용하는 url을 추가합니다.

    :parameter - api_key, ( question_title / question_id ), [urls]
    :return - urls
    """
    api_key = request.POST.get('api_key')
    question_title = request.POST.get('question_title')
    question_id = request.POST.get('question_id')
    new_urls = request.POST.get('urls')

    response_dict = {}

    a = ApiKey.objects.get(key=api_key)

    if question_title and question_id:
        q = Question.objects.get(api_key=a, question_title=question_title, id=question_id)

    elif question_id:
        q = Question.objects.get(api_key=a, id=question_id)
    elif question_title:
        q = Question.objects.get(api_key=a, question_title=question_title)

    if q:
        if new_urls:
            for url in new_urls:
                new_u = Url(question=q, full_url=url)
                new_u.save()

            u = q.authenticated_urls
            response_dict.update({
                'urls': [url.full_url for url in u]
            })
        else:
            response_dict.update({
                'error': "requested url is none"
            })
    else:
        response_dict.update({
            'error': "Can't find the question."
        })

    return JsonResponse(response_dict)


@require_POST
def create_question(request):
    """
    POST - /v1/question/create

    새 question을 생성합니다.

    :parameter - api_key, question_title, question_text, (start_dt, end_dt, is_editable, is_private)
    :return - question
    """
    api_key = request.POST.get('api_key')
    question_title = request.POST.get('question_title')
    question_text = request.POST.get('question_text')
    start_dt = request.POST.get('start_dt')
    end_dt = request.POST.get('end_dt')
    is_editable = request.POST.get('is_editable')
    is_private = request.POST.get('is_private')

    if is_editable:
        is_editable = True
    else:
        is_editable = True

    if is_private:
        is_private = True
    else:
        is_private = False

    response_dict = {}

    a = ApiKey.objects.get(key=api_key)

    new_question = Question(
        api_key=a,
        question_title=question_title,
        question_text=question_text,
        start_dt=start_dt,
        end_dt=end_dt,
        is_editable=is_editable,
        is_private=is_private
    )

    new_question.save()

    q = Question.objects.get(api_key=a, id=new_question.id)

    response_dict.update({
        'question': serializers.serialize('json', [q])
    })

    return JsonResponse(response_dict)


@require_POST
def create_answer(request):
    """
    POST - /v1/answer/create

    새 answer 를 생성합니다.
    answer_num은 list index 순서로 지정됩니다.
    :parameter - api_key, ( question_title / question_id ), answer1, answer2, answer3, ...
    :return - answers
    """
    api_key = request.POST.get('api_key')
    question_title = request.POST.get('question_title')
    question_id = request.POST.get('question_id')

    response_dict = {}

    a = ApiKey.objects.get(key=api_key)

    if question_title and question_id:
        q = Question.objects.get(api_key=a, question_title=question_title, id=question_id)

    elif question_id:
        q = Question.objects.get(api_key=a, id=question_id)
    elif question_title:
        q = Question.objects.get(api_key=a, question_title=question_title)

    for i in range(9):
        answer_text = request.POST.get('answer'+str(i))
        if answer_text:
            new_answer = Answer(question=q, answer_text=answer_text, answer_num=i)
            new_answer.save()

        for index, answer in enumerate(q.answers.all(), start=1):
            response_dict['answer'+str(index)] = serializers.serialize('json', [answer])
    else:
        response_dict.update({
            'error': "Can't find the answer_text."
        })

    return JsonResponse(response_dict)


@require_POST
def get_question(request):
    """
    POST - /v1/question/get

    question을 가져옵니다.
    :parameter - api_key, ( question_title / question_id )
    :return - question
    """
    api_key = request.POST.get('api_key')
    question_title = request.POST.get('question_title')
    question_id = request.POST.get('question_id')

    response_dict = {}

    a = ApiKey.objects.get(key=api_key)

    if question_title and question_id:
        q = Question.objects.get(api_key=a, question_title=question_title, id=question_id)

    elif question_id:
        q = Question.objects.get(api_key=a,id=question_id)
    elif question_title:
        q = Question.objects.get(api_key=a, question_title=question_title)

    if q:
        response_dict.update({
            'question': serializers.serialize('json', [q])
        })
    else:
        response_dict.update({
            'error': "Can't find the question."
        })

    return JsonResponse(response_dict)


@require_POST
def get_answer(request):
    """
    POST - /v1/answer/get

    answer 들을 가져옵니다.
    :parameter - api_key, ( question_title / question_id )
    :return - answer
    """
    api_key = request.POST.get('api_key')
    question_title = request.POST.get('question_title')
    question_id = request.POST.get('question_id')
    response_dict = {}

    a = ApiKey.objects.get(key=api_key)

    if question_title and question_id:
        q = Question.objects.get(api_key=a, question_title=question_title, id=question_id)

    elif question_id:
        q = Question.objects.get(api_key=a, id=question_id)
    elif question_title:
        q = Question.objects.get(api_key=a, question_title=question_title)

    if q:
        if q.answers:
            response_dict.update({
                'answer': serializers.serialize('json', [q.answers.all()])
            })
        else:
            response_dict.update({
                'error': "Can't find the answer"
            })
    else:
        response_dict.update({
            'error': "Can't find the question."
        })

    return JsonResponse(response_dict)


@require_POST
def create_useranswer(request):
    """
    POST - /v1/useranswer/create

    새로운 useranswer instance 를 만듭니다.
    :parameter - api_key, ( question_title / question_id ), update_num, unique_user
    :return - useranswer
    """
    api_key = request.POST.get('api_key')
    question_title = request.POST.get('question_title')
    question_id = request.POST.get('question_id')
    update_num = request.POST.get('update_num')
    unique_user = request.POST.get('unique_user')

    response_dict = {}

    a = ApiKey.objects.get(key=api_key)

    if question_title and question_id:
        q = Question.objects.get(api_key=a, question_title=question_title, id=question_id)

    elif question_id:
        q = Question.objects.get(api_key=a, id=question_id)
    elif question_title:
        q = Question.objects.get(api_key=a, question_title=question_title)

    if q:
        if q.answers:
            a = Answer.objects.get(question=q, answer_num=update_num)
            new_useranswer = UserAnswer(answer=a, unique_user=unique_user)
            new_useranswer.save()

            response_dict.update({
                'useranswer': serializers.serialize('json', [UserAnswer.objects.get(id=new_useranswer.id)])
            })
        else:
            response_dict.update({
                'error': "Can't find the answer"
            })

    else:
        response_dict.update({
            'error': "Can't find the question."
        })

    return JsonResponse(response_dict)



# def update(request):
#
#     q_id = request.POST.get('q_id')
#     update_num = request.POST.get('update_num')
#     unique_id = request.POST.get('uniqueId')
#
#     question = Question.objects.get(id=q_id)
#     answer = Answer.objects.get(question=question, answer_num=update_num)
#
#     response_dict = {}
#
#     try:
#         new_answer = UserAnswer(answer=answer, unique_user=unique_id)
#         new_answer.save()
#     except Exception as e:
#         response_dict.update({'exception_msg': "theres a problem."})
#         response_dict.update({'msg': e.message})
#
#     return JsonResponse(response_dict)
