# 직접 개발한 코드
from django.core import serializers
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST
from django.views.generic.base import View
import urllib.request, urllib.error, urllib.parse
from urllib.error import HTTPError
import json
from main.models import ApiKey, Domain
from vote.models import Question, Answer, UserAnswer, Url, MultiQuestion

import jwt

''' server view function '''


def select_question(request, api_key):
    context = {
        'api_key': api_key
    }
    try:
        q_api_key = ApiKey.objects.get(key=api_key)
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, 'This api_key is not valid.')
        return redirect('main:user_mypage', request.user.id)

    single_question = Question.objects.filter(api_key=q_api_key, multi_question=None, is_removed=False)
    m = MultiQuestion.objects.filter(api_key=q_api_key, is_removed=False)
    context.update({'multi_question': m, 'single_question': single_question})

    return render(request, 'vote/pages/question_select.html', context)


def new(request, api_key):
    context = {
        'api_key': api_key
    }

    return render(request, 'vote/pages/new.html', context)


def get_vote(request, api_key, question_id):
    context = {
        'api_key': api_key
    }

    '''
    request to rest api
    '''
    url = 'http://127.0.0.1:8000/v1/questions/'+str(question_id)+'/SimpleResult'

    req = urllib.request.Request(url)
    req.add_header('api-key', api_key)

    try:
        response_json = urllib.request.urlopen(req).read()
        response_json = json.loads(response_json.decode('utf-8'))
    except HTTPError:
        messages.add_message(request, messages.ERROR, 'Fail to get data.')
        return HttpResponse(HTTPError.reason, HTTPError)

    context.update(response_json)

    return render(request, 'vote/pages/action.html', context)


def get_multiple_vote(request, api_key, group_name):
    context = {
        'api_key': api_key
    }

    try:
        a = ApiKey.objects.get(key=api_key)
        m = MultiQuestion.objects.get(api_key=a, group_name=group_name, is_removed=False)
    except ObjectDoesNotExist:
        desc = 'The MultiQuestion does not exist in followed api key.'
        messages.add_message(request, messages.ERROR, desc)
        return redirect('main:user_mypage', request.user.id)

    '''
    request to rest api
    '''
    url = 'http://127.0.0.1:8000/v1/groups/'+str(m.id)

    req = urllib.request.Request(url)
    req.add_header('api-key', api_key)

    try:
        response_json = urllib.request.urlopen(req).read()
        response_json = json.loads(response_json.decode('utf-8'))
    except HTTPError:
        messages.add_message(request, messages.ERROR, 'Fail to get data.')
        return HttpResponse(HTTPError.reason, HTTPError)

    context.update(response_json)

    return render(request, 'vote/pages/multi_action.html', context)


def dashboard(request, api_key, question_id):
    context = {
        'api_key': api_key
    }
    '''
    request to full_view_answer rest api
    '''
    url = 'http://127.0.0.1:8000/v1/questions/'+str(question_id)+'/SimpleResult'

    req = urllib.request.Request(url)
    req.add_header('api-key', api_key)

    try:
        response_json = urllib.request.urlopen(req).read()
        response_json = json.loads(response_json.decode('utf-8'))
    except HTTPError:
        messages.add_message(request, messages.ERROR, 'Fail to get data.')
        return HttpResponse(HTTPError.reason, HTTPError)

    context.update(response_json)
    return render(request, 'vote/pages/dashboard.html', context)


def multiple_dashboard(request, api_key, group_name):
    context = {
        'api_key': api_key
    }

    try:
        a = ApiKey.objects.get(key=api_key)
        m = MultiQuestion.objects.get(api_key=a, group_name=group_name, is_removed=False)
    except ObjectDoesNotExist:
        desc = 'The MultiQuestion does not exist in followed api key.'
        messages.add_message(request, messages.ERROR, desc)
        return redirect('main:user_mypage', request.user.id)

    questions = m.question_elements.filter(is_removed=False)
    length = questions.count()

    '''
    request to simple_view_answer rest api
    '''
    url = 'http://127.0.0.1:8000/v1/groups/'+str(m.id)

    req = urllib.request.Request(url)
    req.add_header('api-key', api_key)

    try:
        response_json = urllib.request.urlopen(req).read()
        response_json = json.loads(response_json.decode('utf-8'))
    except HTTPError:
        messages.add_message(request, messages.ERROR, 'Fail to get data.')
        return HttpResponse(HTTPError.reason, HTTPError)

    context.update(response_json)
    context.update({'length': length})

    return render(request, 'vote/pages/multi_dashboard.html', context)


def match_domain(request):
    api_key = get_api_key(request)
    if api_key:
        request_domain = request.get_host()
        if request_domain[:4] == 'www.':
            request_domain = request_domain[4:]
        try:
            a = ApiKey.objects.get(key=api_key)
            d = Domain.objects.get(domain=request_domain, api_key=a)
        except ObjectDoesNotExist:
            return False
        return True
    else:
        return False

# ======================================

''' rest api function '''


@csrf_exempt
@require_POST
def to_public(request):
    """
    POST - /v1/question/public

    question을 public으로 전환합니다.

    :parameter - api_key, ( question_title / question_id )
    :return -
    """
    if match_domain(request):
        data = json.loads(request.body.decode('utf-8'))
        api_key = data.get('api_key')
        question_title = data.get('question_title')
        question_id = data.get('question_id')

        response_dict = {}

        try:
            a = ApiKey.objects.get(key=api_key)

            if question_title and question_id:
                q = Question.objects.get(api_key=a, question_title=question_title, id=question_id, is_removed=False)
            elif question_id:
                q = Question.objects.get(api_key=a, id=question_id, is_removed=False)
            elif question_title:
                q = Question.objects.get(api_key=a, question_title=question_title, is_removed=False)
        except ObjectDoesNotExist:
            desc = 'The Question does not exist in followed api key.'
            return error_return(desc)

        q.is_private = False
        q.save()

        return JsonResponse(response_dict)
    else:
        desc = 'This request url is not authenticated in followed api_key.'
        return error_return(desc)


@require_POST
def get_url_list(request):
    """
    POST - /v1/question/url/list

    허용하는 url list 를 return 합니다.

    :parameter - api_key, ( question_title / question_id )
    :return - urls
    """
    if match_domain(request):
        data = json.loads(request.body.decode('utf-8'))
        api_key = data.get('api_key')
        question_title = data.get('question_title')
        question_id = data.get('question_id')

        response_dict = {}

        try:
            a = ApiKey.objects.get(key=api_key)

            if question_title and question_id:
                q = Question.objects.get(api_key=a, question_title=question_title, id=question_id, is_removed=False)
            elif question_id:
                q = Question.objects.get(api_key=a, id=question_id, is_removed=False)
            elif question_title:
                q = Question.objects.get(api_key=a, question_title=question_title, is_removed=False)
        except ObjectDoesNotExist:
            desc = 'The Question does not exist in followed api key.'
            return error_return(desc)

        u = q.authenticated_urls
        if u:
            response_dict.update({
                'urls': [url.full_url for url in u]
            })
        else:
            desc = 'No urls in this question'
            return error_return(desc)

        return JsonResponse(response_dict)
    else:
        desc = 'This request url is not authenticated in followed api_key.'
        return error_return(desc)

@require_POST
def add_url(request):
    """
    POST - /v1/question/url/add

    허용하는 url을 추가합니다.

    :parameter - api_key, ( question_title / question_id ), urls
    :return - urls
    """
    if match_domain(request):
        data = json.loads(request.body.decode('utf-8'))
        api_key = data.get('api_key')
        question_title = data.get('question_title')
        question_id = data.get('question_id')
        new_urls = data.get('urls')

        response_dict = {}

        try:
            a = ApiKey.objects.get(key=api_key)

            if question_title and question_id:
                q = Question.objects.get(api_key=a, question_title=question_title, id=question_id, is_removed=False)
            elif question_id:
                q = Question.objects.get(api_key=a, id=question_id, is_removed=False)
            elif question_title:
                q = Question.objects.get(api_key=a, question_title=question_title, is_removed=False)
        except ObjectDoesNotExist:
            desc = 'The Question does not exist in followed api key.'
            return error_return(desc)

        if new_urls:
            for url in new_urls:
                new_u = Url(question=q, full_url=url, is_removed=False)
                new_u.save()

            u = q.authenticated_urls
            response_dict.update({
                'urls': [url.full_url for url in u]
            })
        else:
            desc = 'requested url is none'
            return error_return(desc)

        return JsonResponse(response_dict)
    else:
        desc = 'This request url is not authenticated in followed api_key.'
        return error_return(desc)


@csrf_exempt
@require_POST
def create_question(request):
    """
    POST - /v1/question/create

    새 question을 생성합니다.

    :parameter - api_key, question_title, question_text, (start_dt, end_dt, is_editable, is_private)
    :return - question
    """
    if match_domain(request):
        data = json.loads(request.body.decode('utf-8'))

        api_key = data.get('api_key')
        question_title = data.get('question_title')
        question_text = data.get('question_text')
        start_dt = data.get('start_dt')
        end_dt = data.get('end_dt')
        is_editable = data.get('is_editable') == 'True'
        is_private = data.get('is_private') == 'True'

        response_dict = {}

        try:
            a = ApiKey.objects.get(key=api_key)
        except ObjectDoesNotExist:
            desc = 'The ApiKey instance does not exist in followed key.'
            return error_return(desc)

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

        try:
            q = Question.objects.get(api_key=a, id=new_question.id, is_removed=False)
        except ObjectDoesNotExist:
            desc = 'The Question does not exist in followed api key.'
            return error_return(desc)

        response_dict.update({
            'question': serializers.serialize('json', [q])
        })

        return JsonResponse(response_dict)
    else:
        desc = 'This request url is not authenticated in followed api_key.'
        return error_return(desc)


@csrf_exempt
@require_POST
def create_answer(request):
    """
    POST - /v1/answer/create

    새 answer 를 생성합니다.
    answer_num은 list index 순서로 지정됩니다.
    :parameter - api_key, ( question_title / question_id ), answers(answer_text, answer_num)
    :return - answers
    """
    if match_domain(request):
        data = json.loads(request.body.decode('utf-8'))

        api_key = data.get('api_key')
        question_title = data.get('question_title')
        question_id = data.get('question_id')

        response_dict = {}

        try:
            a = ApiKey.objects.get(key=api_key)

            if question_title and question_id:
                q = Question.objects.get(api_key=a, question_title=question_title, id=question_id, is_removed=False)
            elif question_id:
                q = Question.objects.get(api_key=a, id=question_id, is_removed=False)
            elif question_title:
                q = Question.objects.get(api_key=a, question_title=question_title, is_removed=False)
        except ObjectDoesNotExist:
            desc = 'The Question does not exist in followed api key.'
            return error_return(desc)

        for key, value in data.get('answers').items():
            answer_text = value.get('answer_text')
            if answer_text:
                new_answer = Answer(question=q, answer_text=answer_text, answer_num=key)
                new_answer.save()

                for index, answer in enumerate(q.answers.all(), start=1):
                    response_dict['answer'+str(index)] = serializers.serialize('json', [answer])
            else:
                desc = 'answer_text is None'
                return error_return(desc)

        return JsonResponse(response_dict)
    else:
        desc = 'This request url is not authenticated in followed api_key.'
        return error_return(desc)


@csrf_exempt
@require_POST
def get_group(request):
    """
    POST - /v1/question/get

    question을 가져옵니다.
    :parameter - api_key, group_name
    :return - question, answers
    """
    if match_domain(request):
        data = json.loads(request.body.decode('utf-8'))
        api_key = data.get('api_key')
        group_name = data.get('group_name')

        response_dict = {}
        response_dict['question'] = {}

        try:
            a = ApiKey.objects.get(key=api_key)
            m = MultiQuestion.objects.get(group_name=group_name)
        except ObjectDoesNotExist:
            desc = 'The MultiQuestion doees not exist in follwed api key'
            return error_return(desc)

        for index, q in enumerate(m.question_elements.all()):

            response_dict['question']['answers'] = []

            for a in q.answers.all():
                response_dict['question']['answers'].append({
                    'answer_num': a.answer_num,
                    'answer_text': a.answer_text,
                    'answer_count': a.get_answer_count
                })

            response_dict['question'].update({
                'question_title': q.question_title,
                'question_text': q.question_text,
                'question_id': q.id,
            })

        return JsonResponse(response_dict)
    else:
        desc = 'This request url is not authenticated in followed api_key.'
        return error_return(desc)


@csrf_exempt
@require_POST
def get_question(request):
    """
    POST - /v1/question/get

    question을 가져옵니다.
    :parameter - api_key, ( question_title / question_id )
    :return - question
    """
    data = json.loads(request.body.decode('utf-8'))
    api_key = data.get('api_key')
    question_title = data.get('question_title')
    question_id = data.get('question_id')

    response_dict = {}

    try:
        a = ApiKey.objects.get(key=api_key)

        if question_title and question_id:
            q = Question.objects.get(api_key=a, question_title=question_title, id=question_id, is_removed=False)
        elif question_id:
            q = Question.objects.get(api_key=a,id=question_id, is_removed=False)
        elif question_title:
            q = Question.objects.get(api_key=a, question_title=question_title, is_removed=False)
    except ObjectDoesNotExist:
        desc = 'The Question does not exist in followed api key.'
        return error_return(desc)

    if q:
        response_dict.update({
            # 'question': serializers.serialize('json', [q])
            'question_title': q.question_title,
            'question_text': q.question_text,
            'question_id': q.id,
        })
    else:
        desc = 'The Question does not exist.'
        return error_return(desc)

    return JsonResponse(response_dict)


@csrf_exempt
@require_POST
def get_answer(request):
    """
    POST - /v1/answer/get

    한 question의 모든 answer 들을 가져옵니다.
    :parameter - api_key, ( question_title / question_id )
    :return - answer
    """
    data = json.loads(request.body.decode('utf-8'))
    api_key = data.get('api_key')
    question_title = data.get('question_title')
    question_id = data.get('question_id')

    response_dict = {}
    answer_list = []

    try:
        a = ApiKey.objects.get(key=api_key)

        if question_title and question_id:
            q = Question.objects.get(api_key=a, question_title=question_title, id=question_id, is_removed=False)
        elif question_id:
            q = Question.objects.get(api_key=a, id=question_id, is_removed=False)
        elif question_title:
            q = Question.objects.get(api_key=a, question_title=question_title, is_removed=False)
    except ObjectDoesNotExist:
        desc = 'The Question does not exist in followed api key.'
        return error_return(desc)

    a = q.answers.all()
    if a:
        print(a)
        print("sdf")
        print("sdf")
        for answer in a:
            print("sdf1212")
            answer_list.append({
                'answer_num': answer.answer_num,
                'answer_text': answer.answer_text,
                'answer_count': answer.get_answer_count()
            })
            print(answer.get_answer_count())
        response_dict.update({
            'answers': answer_list
        })
        print("sdf")

        print(response_dict)
        return JsonResponse(response_dict, safe=False)
    else:
        desc = 'The Answer does not exist.'
        return error_return(desc)



@csrf_exempt
@require_POST
def create_useranswer(request):
    """
    POST - /v1/useranswer/create

    새로운 useranswer instance 를 만듭니다.
    :parameter - api_key, ( question_title / question_id ), update_num, unique_user
    :return - useranswer
    """
    if match_domain(request):
        data = json.loads(request.body.decode('utf-8'))
        api_key = data.get('api_key')
        question_title = data.get('question_title')
        question_id = data.get('question_id')
        update_num = data.get('update_num')
        unique_user = data.get('unique_user')

        response_dict = {}

        try:
            a = ApiKey.objects.get(key=api_key)

            if question_title and question_id:
                q = Question.objects.get(api_key=a, question_title=question_title, id=question_id, is_removed=False)
            elif question_id:
                q = Question.objects.get(api_key=a, id=question_id, is_removed=False)
            elif question_title:
                q = Question.objects.get(api_key=a, question_title=question_title, is_removed=False)
        except ObjectDoesNotExist:
            desc = 'The Question does not exist in followed api key.'
            return error_return(desc)

        if q.answers:
            try:
                a = Answer.objects.get(question=q, answer_num=update_num, is_removed=False)
            except ObjectDoesNotExist:
                desc = 'The Answer does not exist in followed answer_num.'
                return error_return(desc)

            new_useranswer = UserAnswer(answer=a, unique_user=unique_user)
            new_useranswer.save()

            try:
                curr_useranswer = UserAnswer.objects.get(id=new_useranswer.id, is_removed=False)
            except ObjectDoesNotExist:
                desc = 'The UserAnswer does not exist in followed id.'
                return error_return(desc)

            response_dict.update({
                'useranswer': serializers.serialize('json', [curr_useranswer])
            })
        else:
            desc = 'The Answer does not exist.'
            return error_return(desc)

        return JsonResponse(response_dict)
    else:
        desc = 'This request url is not authenticated in followed api_key.'
        return error_return(desc)




@csrf_exempt
@require_POST
def full_view_answer(request):
    """
    POST - /v1/answer/view/full

    useranswer를 포함한 자세한 정보를 제공합니다.
    :parameter - api_key, ( question_title / question_id )
    :return - question_title, question_text, answer({answer_num, answer_text, answer_count, useranswer({unique_user, created_dt})})
    """
    if match_domain(request):
        data = json.loads(request.body.decode('utf-8'))
        api_key = data.get('api_key')
        question_title = data.get('question_title')
        question_id = data.get('question_id')

        response_dict = {}
        answer_list = []

        try:
            a = ApiKey.objects.get(key=api_key)

            if question_title and question_id:
                q = Question.objects.get(api_key=a, question_title=question_title, id=question_id, is_removed=False)
            elif question_id:
                q = Question.objects.get(api_key=a, id=question_id, is_removed=False)
            elif question_title:
                q = Question.objects.get(api_key=a, question_title=question_title, is_removed=False)
        except ObjectDoesNotExist:
                desc = 'The Question does not exist in followed api_key.'
                return error_return(desc)

        response_dict.update({
            'question_title': q.question_title,
            'question_text': q.question_text
        })
        a = q.answers.all()
        if a:
            for answer in a:
                answer_list.append({
                    'answer_num': answer.answer_num,
                    'answer_text': answer.answer_text,
                    'answer_count': answer.get_answer_count,
                    'useranswer': []
                })
                for useranswer in answer.user_answers.all():
                    answer_list[-1]['useranswer'].append({
                        'unique_user': useranswer.unique_user,
                        'created_dt': useranswer.created_dt
                    })

            response_dict.update({
                'answer': answer_list
            })
        else:
            desc = 'The Answer does not exist.'
            return error_return(desc)

        return JsonResponse(response_dict)
    else:
        desc = 'This request url is not authenticated in followed api_key.'
        return error_return(desc)


@csrf_exempt
@require_POST
def create_multiple_question(request):
    """
    POST - /v1/multiple/create

    multiquestion 그룹을 생성하고
    같이 생성된 복수 질문들을 그룹에 추가합니다.
    질문의 보기들도 같이 저장됩니다.
    :parameter - api_key, group_name, questions({question_title, question_text, (start_dt, end_dt, is_editable, is_private)}), answers({answer_text, answer_num})
    :return - multiquestion, question
    """
    if match_domain(request):
        data = json.loads(request.body.decode('utf-8'))
        api_key = data.get('api_key')
        group_name = data.get('group_name')

        response_dict = {}

        try:
            a = ApiKey.objects.get(key=api_key)
        except ObjectDoesNotExist:
                desc = 'The ApiKey does not exist in followed key.'
                return error_return(desc)

        new_multiq = MultiQuestion(api_key=a, group_name=group_name)
        new_multiq.save()

        for question_key, question_value in data.get('questions').items():
            question_title = question_value.get('question_title')
            question_text = question_value.get('question_text')
            start_dt = question_value.get('start_dt')
            end_dt = question_value.get('end_dt')
            is_editable = question_value.get('is_editable') == 'True'
            is_private = question_value.get('is_private') == 'True'

            if question_title:
                new_question = Question(
                    api_key=a,
                    multi_question=new_multiq,
                    question_title=question_title,
                    question_text=question_text,
                    start_dt=start_dt,
                    end_dt=end_dt,
                    is_editable=is_editable,
                    is_private=is_private
                )
                new_question.save()

                for answer_key, answer_value in data.get('answers').get(question_key).items():
                    answer_text = answer_value.get('answer_text')
                    answer_num = answer_value.get('answer_num')

                    if answer_text:
                        new_answer = Answer(question=new_question, answer_text=answer_text, answer_num=answer_num)
                        new_answer.save()

        try:
            mq = MultiQuestion.objects.get(id=new_multiq.id, is_removed=False)
            q = mq.question_elements.all()

            response_dict.update({
                'multiquestion': serializers.serialize('json', [mq]),
                'question': serializers.serialize('json', q),
            })

            return JsonResponse(response_dict)
        except ObjectDoesNotExist:
            desc = 'MultiQuestion does not exist by new_multiq.id'
            return error_return(desc)
    else:
        desc = 'This request url is not authenticated in followed api_key.'
        return error_return(desc)

@csrf_exempt
@require_POST
def create_single_question(request):
    """
    POST - /v1/single/create

    복수 질문이 아닌 하나의 질문에 따른 보기들을 저장합니다.
    :parameter - api_key, questions(question_title, question_text, (start_dt, end_dt, is_editable, is_private)), answers(answer_text, answer_num)
    :return - question
    """
    if match_domain(request):
        '''
        request to create_question, create_answer rest api
        '''
        data = json.loads(request.body.decode('utf-8'))
        api_key = data['api_key']
        question_data = data['questions']['1']
        answers_data = data['answers']['1']

        url = 'http://localhost:8000/vote/question/create'
        data = {
            'question_title': question_data['question_title'],
            'question_text': question_data['question_text'],
            'is_editable': question_data['is_editable'],
            'is_private': question_data['is_private'],
            'start_dt': question_data['start_dt'],
            'end_dt': question_data['end_dt'],
            'api_key': api_key
        }

        data = json.dumps(data).encode("utf-8")
        req = urllib.request.Request(url)

        try:
            question_response_json = urllib.request.urlopen(req, data=data).read().decode("utf-8")
            question_response_json = json.loads(question_response_json)
        except HTTPError as e:
            content = e.read()
            return HttpResponse(content)

        url = 'http://localhost:8000/vote/answer/create'

        data = {
            'api_key': api_key,
            'question_title': question_data['question_title'],
            'answers': answers_data
        }

        data = json.dumps(data).encode("utf-8")
        req = urllib.request.Request(url)

        try:
            answer_response_json = urllib.request.urlopen(req, data=data).read().decode("utf-8")
            answer_response_json = json.loads(answer_response_json)
        except HTTPError as e:
            content = e.read()
            return HttpResponse(content)

        return JsonResponse({
            'question': question_response_json,
            'answers': answer_response_json
        })
    else:
        desc = 'This request url is not authenticated in followed api_key.'
        return error_return(desc)

@require_POST
def delete_question(request):
    """
    POST - /v1/question/delete

    해당하는 question 을 삭제합니다.
    :parameter - api_key, ( question_title / question_id )
    :return -
    """
    if match_domain(request):
        data = json.loads(request.body.decode('utf-8'))
        api_key = data.get('api_key')
        question_title = data.get('question_title')
        question_id = data.get('question_id')

        response_dict = {}

        try:
            a = ApiKey.objects.get(key=api_key)
            if question_title and question_id:
                q = Question.objects.get(api_key=a, question_title=question_title, id=question_id, is_removed=False)
            elif question_id:
                q = Question.objects.get(api_key=a, id=question_id, is_removed=False)
            elif question_title:
                q = Question.objects.get(api_key=a, question_title=question_title, is_removed=False)

        except ObjectDoesNotExist:
                desc = 'The Question does not exist in followed api_key.'
                return error_return(desc)
        q.is_removed = True
        q.save()

        return JsonResponse(response_dict)
    else:
        desc = 'This request url is not authenticated in followed api_key.'
        return error_return(desc)


@require_POST
def delete_answer(request):
    """
    POST - /v1/answer/delete

    해당하는 answer 를 삭제합니다.
    :parameter - api_key, ( question_title / question_id ), answer_num
    :return -
    """
    if match_domain(request):
        data = json.loads(request.body.decode('utf-8'))
        api_key = data.get('api_key')
        question_title = data.get('question_title')
        question_id = data.get('question_id')
        answer_num = data.get('answer_num')

        response_dict = {}

        try:
            a = ApiKey.objects.get(key=api_key)
            if question_title and question_id:
                q = Question.objects.get(api_key=a, question_title=question_title, id=question_id, is_removed=False)
            elif question_id:
                q = Question.objects.get(api_key=a, id=question_id, is_removed=False)
            elif question_title:
                q = Question.objects.get(api_key=a, question_title=question_title, is_removed=False)

        except ObjectDoesNotExist:
                desc = 'The Question does not exist in followed api_key.'
                return error_return(desc)

        answer = q.answers.filter(answer_num=answer_num, is_removed=False)
        for a in answer:
            a.is_removed = True
            a.save()

        return JsonResponse(response_dict)
    else:
        desc = 'This request url is not authenticated in followed api_key.'
        return error_return(desc)


@require_POST
def delete_useranswer(request):
    """
    POST - /v1/useranswer/delete

    해당하는 useranswer 를 삭제합니다.
    :parameter - api_key, ( question_title / question_id ), answer_num, unique_user
    :return -
    """
    if match_domain(request):
        data = json.loads(request.body.decode('utf-8'))
        api_key = data.get('api_key')
        question_title = data.get('question_title')
        question_id = data.get('question_id')
        answer_num = data.get('answer_num')
        unique_user = data.get('unique_user')

        response_dict = {}

        try:
            a = ApiKey.objects.get(key=api_key)
            if question_title and question_id:
                q = Question.objects.get(api_key=a, question_title=question_title, id=question_id, is_removed=False)
            elif question_id:
                q = Question.objects.get(api_key=a, id=question_id, is_removed=False)
            elif question_title:
                q = Question.objects.get(api_key=a, question_title=question_title, is_removed=False)

        except ObjectDoesNotExist:
                desc = 'The Question does not exist in followed api_key.'
                return error_return(desc)

        answer = q.answers.get(answer_num=answer_num, is_removed=False)
        unique_user = str(unique_user) + api_key

        try:
            useranswer = UserAnswer.objects.get(answer=answer, unique_user=unique_user, is_removed=False)
            useranswer.is_removed = True
            useranswer.save()

        except ObjectDoesNotExist:
                desc = 'The UserAnswer does not exist in followed unique_user.'
                return error_return(desc)

        return JsonResponse(response_dict)
    else:
        desc = 'This request url is not authenticated in followed api_key.'
        return error_return(desc)


@csrf_exempt
@require_POST
def delete_question_set(request):
    """
    POST - /v1/question/set/delete

    question 의 answer 와 useranswer 를 모두 삭제합니다.
    :parameter - api_key, ( question_title / question_id )
    :return -
    """
    if match_domain(request):
        data = json.loads(request.body.decode('utf-8'))
        api_key = data.get('api_key')
        question_title = data.get('question_title')
        question_id = data.get('question_id')

        response_dict = {}

        try:
            a = ApiKey.objects.get(key=api_key)
            if question_title and question_id:
                q = Question.objects.get(api_key=a, question_title=question_title, id=question_id, is_removed=False)
            elif question_id:
                q = Question.objects.get(api_key=a, id=question_id, is_removed=False)
            elif question_title:
                q = Question.objects.get(api_key=a, question_title=question_title, is_removed=False)

        except ObjectDoesNotExist:
                desc = 'The Question does not exist in followed api_key.'
                return error_return(desc)

        answers = q.answers.all()
        for answer in answers:
            useranswers = answer.user_answers.all()
            for useranswer in useranswers:
                useranswer.is_removed = True
                useranswer.save()

            answer.is_removed = True
            answer.save()

        q.is_removed = True
        q.save(is_update=True)

        return JsonResponse(response_dict)
    else:
        desc = 'This request url is not authenticated in followed api_key.'
        return error_return(desc)


@require_POST
def delete_multi_question_set(request):
    """
    POST - /v1/multiple/delete

    한 group 에 속한 모든 question 을 삭제합니다.
    question 에 속하는 answer, useranswer 도 모두 삭제됩니다.
    :parameter - api_key, group_name
    :return -
    """
    if match_domain(request):
        data = json.loads(request.body.decode('utf-8'))
        api_key = data.get('api_key')
        group_name = data.get('group_name')

        response_dict = {}

        try:
            a = ApiKey.objects.get(key=api_key)
            m = MultiQuestion.objects.get(api_key=a, group_name=group_name, is_removed=False)
        except ObjectDoesNotExist:
                desc = 'The Question does not exist in followed api_key.'
                return error_return(desc)

        questions = m.question_elements.all()
        for q in questions:
            answers = q.answers.all()
            for answer in answers:
                useranswers = answer.user_answers.all()
                for useranswer in useranswers:
                    useranswer.is_removed = True
                    useranswer.save()

                answer.is_removed = True
                answer.save()

            q.is_removed = True
            q.save()

        m.is_removed = True
        m.save()

        return JsonResponse(response_dict)
    else:
        desc = 'This request url is not authenticated in followed api_key.'
        return error_return(desc)


@csrf_exempt
@require_POST
def update_useranswer(request):
    """
    POST - /v1/useranswer/update

    생성된 useranswer 의 answer field를 변경합니다.
    :parameter - api_key, ( question_title / question_id ), pre_answer_num, post_answer_num, unique_user
    :return - useranswer
    """
    if match_domain(request):
        data = json.loads(request.body.decode('utf-8'))
        api_key = data.get('api_key')
        question_title = data.get('question_title')
        question_id = data.get('question_id')
        pre_answer_num = data.get('pre_answer_num')
        post_answer_num = data.get('post_answer_num')
        unique_user = data.get('unique_user')

        response_dict = {}

        try:
            a = ApiKey.objects.get(key=api_key)
            if question_title and question_id:
                q = Question.objects.get(api_key=a, question_title=question_title, id=question_id, is_removed=False)
            elif question_id:
                q = Question.objects.get(api_key=a, id=question_id, is_removed=False)
            elif question_title:
                q = Question.objects.get(api_key=a, question_title=question_title, is_removed=False)

        except ObjectDoesNotExist:
                desc = 'The Question does not exist in followed api_key.'
                return error_return(desc)

        if q.is_editable:
            answer = q.answers.get(answer_num=pre_answer_num, is_removed=False)
            unique_user = str(unique_user) + api_key

            try:
                useranswer = UserAnswer.objects.get(answer=answer, unique_user=unique_user, is_removed=False)
                new_answer = q.answers.get(answer_num=post_answer_num, is_removed=False)
                useranswer.answer = new_answer
                useranswer.save()

            except ObjectDoesNotExist:
                    desc = 'The UserAnswer does not exist in followed unique_user.'
                    return error_return(desc)

            return JsonResponse(response_dict)
        else:
            desc = 'Property "is_editable" of this question is currently False. Set True for this request.'
            return error_return(desc)
    else:
        desc = 'This request url is not authenticated in followed api_key.'
        return error_return(desc)


def error_return(desc, status=400):
    return JsonResponse({
        'error': True,
        'description': desc
    }, status=status)


def get_api_key(request):
    api_key = request.META.get('HTTP_API_KEY')
    if api_key:
        return api_key
    else:
        secret = ApiKey.objects.get(id=request.META.get('HTTP_KID')).secret_key
        try:
            decoded = jwt.decode(request.META.get('HTTP_JWT'), secret, algorithms=['HS256', 'HS512', 'HS384'])
        except jwt.InvalidTokenError:
            return False
        return decoded.get('api-key')


class Groups(View):
    def post(self, request):
        if match_domain(request):
            data = json.loads(request.body.decode('utf-8'))
            group_name = data.get('group_name')
            api_key = get_api_key(request)
            if not api_key:
                desc = "Can't get a valid api key."
                return error_return(desc)

            response_dict = {
                'questions': {},
                'answers': {}
            }

            try:
                a = ApiKey.objects.get(key=api_key)
            except ObjectDoesNotExist:
                desc = 'The ApiKey does not exist in followed key.'
                return error_return(desc, 404)

            new_multiq = MultiQuestion(api_key=a, group_name=group_name)
            new_multiq.save()

            for question_key, question_value in data.get('questions').items():
                question_title = question_value.get('question_title')
                question_text = question_value.get('question_text')
                start_dt = question_value.get('start_dt')
                end_dt = question_value.get('end_dt')
                is_editable = question_value.get('is_editable') == 'True'
                is_private = question_value.get('is_private') == 'True'

                if question_title:
                    new_question = Question(
                        api_key=a,
                        multi_question=new_multiq,
                        question_title=question_title,
                        question_text=question_text,
                        question_num=question_key,
                        start_dt=start_dt,
                        end_dt=end_dt,
                        is_editable=is_editable,
                        is_private=is_private
                    )
                    new_question.save()

                    for answer_key, answer_value in data.get('answers').get(question_key).items():
                        answer_text = answer_value.get('answer_text')
                        answer_num = answer_key

                        if answer_text:
                            new_answer = Answer(question=new_question, answer_text=answer_text, answer_num=answer_num)
                            new_answer.save()

            try:
                mq = MultiQuestion.objects.get(id=new_multiq.id, is_removed=False)
                q = mq.question_elements.filter(is_removed=False).order_by('question_num')

            except ObjectDoesNotExist:
                desc = 'MultiQuestion does not exist by new_multiq.id'
                return error_return(desc, 404)

            response_dict.update({
                "group_id": mq.id,
                "group_name": mq.group_name
            })

            for question in q:
                response_dict['questions'].update({
                    question.question_num : {
                        'question_title': question.question_title,
                        'question_text': question.question_text,
                        'start_dt': question.start_dt,
                        'end_dt': question.end_dt,
                        'is_editable': question.is_editable,
                        'is_private': question.is_private
                    }
                })

                a = question.answers.filter(is_removed=False).order_by('answer_num')
                response_dict['answers'].update({
                    question.question_num : {}
                })

                for answer in a:
                    response_dict['answers'][question.question_num].update({
                        answer.answer_num : {
                            'answer_text': answer.answer_text,
                        }
                    })

            return JsonResponse(response_dict)
        else:
            desc = 'This request url is not authenticated in followed api_key.'
            return error_return(desc, 401)

    def get(self, request, group_id):
        if match_domain(request):
            api_key = get_api_key(request)
            if not api_key:
                desc = "Can't get a valid api key."
                return error_return(desc)

            response_dict = {
                'questions': {},
                'answers': {}
            }

            try:
                m = MultiQuestion.objects.get(id=group_id, is_removed=False)
                q = m.question_elements.filter(is_removed=False).order_by('question_num')
            except ObjectDoesNotExist:
                desc = 'The MultiQuestion does not exist in follwed api key'
                return error_return(desc, 404)

            response_dict.update({
                "group_id": m.id,
                "group_name": m.group_name
            })

            for question in q:
                response_dict['questions'].update({
                    question.question_num : {
                        'id': question.id,
                        'question_title': question.question_title,
                        'question_text': question.question_text,
                        'start_dt': question.start_dt,
                        'end_dt': question.end_dt,
                        'is_editable': question.is_editable,
                        'is_private': question.is_private
                    }
                })

                a = question.answers.filter(is_removed=False).order_by('answer_num')
                response_dict['answers'].update({
                    question.question_num : {}
                })

                for answer in a:
                    response_dict['answers'][question.question_num].update({
                        answer.answer_num : {
                            'id': answer.id,
                            'answer_text': answer.answer_text,
                            'answer_count': answer.get_answer_count
                        }
                    })

            return JsonResponse(response_dict)
        else:
            desc = 'This request url is not authenticated in followed api_key. / Or api key is not valid.'
            return error_return(desc, 401)

    def put(self, request, group_id):
        if match_domain(request):
            data = json.loads(request.body.decode('utf-8'))
            api_key = get_api_key(request)
            if not api_key:
                desc = "Can't get a valid api key."
                return error_return(desc)

            response_dict = {
                'questions': {},
                'answers': {}
            }
            update_question_dict = {}
            update_answer_dict = {}

            try:
                a = ApiKey.objects.get(key=api_key)
            except ObjectDoesNotExist:
                desc = 'The ApiKey does not exist in followed key.'
                return error_return(desc, 404)

            m = MultiQuestion.objects.get(api_key=a, id=group_id, is_removed=False)
            group_name = data.get('group_name')

            if group_name:
                m.group_name = group_name
                m.save()

            if data.get('questions'):
                for question_key, question_value in data.get('questions').items():
                    question_title = question_value.get('question_title')
                    question_text = question_value.get('question_text')
                    start_dt = question_value.get('start_dt')
                    end_dt = question_value.get('end_dt')
                    is_editable = question_value.get('is_editable') == 'True'
                    is_private = question_value.get('is_private') == 'True'

                    try:
                        selected_q = m.question_elements.get(question_num=question_key, is_removed=False)
                    except ObjectDoesNotExist:
                        desc = 'Question does not exist.'
                        return error_return(desc, 404)

                    if question_title:
                        update_question_dict.update({
                            'question_title': question_title
                        })
                    if question_text:
                        update_question_dict.update({
                            'question_text': question_text
                        })
                    if start_dt:
                        update_question_dict.update({
                            'start_dt': start_dt
                        })
                    if end_dt:
                        update_question_dict.update({
                            'end_dt': end_dt
                        })
                    if question_value.get('is_editable'):
                        update_question_dict.update({
                            'is_editable': is_editable
                        })
                    if question_value.get('is_private'):
                        update_question_dict.update({
                            'is_private': is_private
                        })

                    for key in update_question_dict:
                        setattr(selected_q, key, update_question_dict[key])
                    selected_q.save(is_update=True)

                    '''
                    update answer instance
                    '''
                    if data.get('answers').get(question_key):
                        for answer_key, answer_value in data.get('answers').get(question_key).items():
                            answer_text = answer_value.get('answer_text')

                            try:
                                selected_a = selected_q.answers.get(answer_num=answer_key, is_removed=False)
                            except ObjectDoesNotExist:
                                desc = 'Answer does not exist.'
                                return error_return(desc, 404)

                            if answer_text:
                                update_answer_dict.update({
                                    'answer_text': answer_text
                                })

                            for key in update_answer_dict:
                                setattr(selected_a, key, update_answer_dict[key])
                            selected_a.save()

            '''
            load data for response json
            '''
            try:
                mq = MultiQuestion.objects.get(id=m.id, is_removed=False)
                q = mq.question_elements.filter(is_removed=False).order_by('question_num')
            except ObjectDoesNotExist:
                desc = 'MultiQuestion does not exist by new_multiq.id'
                return error_return(desc, 404)

            response_dict.update({
                "group_id": mq.id,
                "group_name": mq.group_name
            })

            for question in q:
                response_dict['questions'].update({
                    question.question_num : {
                        'question_title': question.question_title,
                        'question_text': question.question_text,
                        'start_dt': question.start_dt,
                        'end_dt': question.end_dt,
                        'is_editable': question.is_editable,
                        'is_private': question.is_private
                    }
                })

                a = question.answers.filter(is_removed=False).order_by('answer_num')
                response_dict['answers'].update({
                    question.question_num : {}
                })

                for answer in a:
                    response_dict['answers'][question.question_num].update({
                        answer.answer_num : {
                            'answer_text': answer.answer_text,
                        }
                    })

            return JsonResponse(response_dict)

        else:
            desc = 'This request url is not authenticated in followed api_key.'
            return error_return(desc, 401)

    def delete(self, request, group_id):
        if match_domain(request):
            api_key = get_api_key(request)
            if not api_key:
                desc = "Can't get a valid api key."
                return error_return(desc)

            response_dict = {}

            try:
                a = ApiKey.objects.get(key=api_key)
                m = MultiQuestion.objects.get(api_key=a, id=group_id, is_removed=False)
            except ObjectDoesNotExist:
                    desc = 'The Question does not exist in followed api_key.'
                    return error_return(desc, 404)

            questions = m.question_elements.filter(is_removed=False)
            for q in questions:
                answers = q.answers.filter(is_removed=False)
                for answer in answers:
                    useranswers = answer.user_answers.filter(is_removed=False)
                    for useranswer in useranswers:
                        useranswer.is_removed = True
                        useranswer.save()

                    answer.is_removed = True
                    answer.save()

                questions.update(is_removed = True)

            m.is_removed = True
            m.save()

            response_dict.update({
                "result": "success",
                "description": "Deleted this group"
            })
            return JsonResponse(response_dict)
        else:
            desc = 'This request url is not authenticated in followed api_key.'
            return error_return(desc, 401)


class Questions(View):
    def post(self, request):
        if match_domain(request):
            data = json.loads(request.body.decode('utf-8'))
            api_key = get_api_key(request)
            if not api_key:
                desc = "Can't get a valid api key."
                return error_return(desc)

            question_data = data.get('questions').get("1")
            question_title = question_data.get('question_title')
            question_text = question_data.get('question_text')
            start_dt = question_data.get('start_dt')
            end_dt = question_data.get('end_dt')
            is_editable = question_data.get('is_editable') == 'True'
            is_private = question_data.get('is_private') == 'True'

            answer_data = data.get('answers').get("1")

            response_dict = {
                'questions': {},
                'answers': {}
            }

            try:
                a = ApiKey.objects.get(key=api_key)
            except ObjectDoesNotExist:
                desc = 'The ApiKey instance does not exist in followed key.'
                return error_return(desc, 404)

            new_question = Question(
                api_key=a,
                question_title=question_title,
                question_text=question_text,
                question_num="1",
                start_dt=start_dt,
                end_dt=end_dt,
                is_editable=is_editable,
                is_private=is_private
            )

            new_question.save()

            try:
                q = Question.objects.get(api_key=a, id=new_question.id, is_removed=False)
            except ObjectDoesNotExist:
                desc = 'The Question does not exist in followed api key.'
                return error_return(desc, 404)

            for key, value in answer_data.items():
                answer_text = value.get('answer_text')
                if answer_text:
                    new_answer = Answer(question=q, answer_text=answer_text, answer_num=key)
                    new_answer.save()
                else:
                    pass

            '''
            load data for response json
            '''
            response_dict['questions'].update({
                q.question_num : {
                    'question_title': q.question_title,
                    'question_text': q.question_text,
                    'start_dt': q.start_dt,
                    'end_dt': q.end_dt,
                    'is_editable': q.is_editable,
                    'is_private': q.is_private
                }
            })

            a = q.answers.filter(is_removed=False).order_by('answer_num')
            response_dict['answers'].update({
                q.question_num : {}
            })

            for answer in a:
                response_dict['answers'][q.question_num].update({
                    answer.answer_num : {
                        'answer_text': answer.answer_text,
                    }
                })

            return JsonResponse(response_dict)
        else:
            desc = 'This request url is not authenticated in followed api_key.'
            return error_return(desc, 401)

    def get(self, request, question_id):
        if match_domain(request):
            api_key = get_api_key(request)
            if not api_key:
                desc = "Can't get a valid api key."
                return error_return(desc)

            response_dict = {
                'questions': {},
                'answers': {}
            }

            try:
                a = ApiKey.objects.get(key=api_key)
                q = Question.objects.get(api_key=a, id=question_id, is_removed=False)
            except ObjectDoesNotExist:
                    desc = 'The Question does not exist in followed api_key.'
                    return error_return(desc, 404)

            '''
            load data for response json
            '''
            response_dict['questions'].update({
                q.question_num : {
                    'id': q.id,
                    'question_title': q.question_title,
                    'question_text': q.question_text,
                    'start_dt': q.start_dt,
                    'end_dt': q.end_dt,
                    'is_editable': q.is_editable,
                    'is_private': q.is_private
                }
            })

            a = q.answers.filter(is_removed=False).order_by('answer_num')
            response_dict['answers'].update({
                q.question_num : {}
            })

            for answer in a:
                response_dict['answers'][q.question_num].update({
                    answer.answer_num : {
                        'id': answer.id,
                        'answer_count': answer.get_answer_count,
                        'answer_text': answer.answer_text,
                    }
                })

            return JsonResponse(response_dict)
        else:
            desc = 'This request url is not authenticated in followed api_key.'
            return error_return(desc, 401)

    def put(self, request, question_id):
        if match_domain(request):
            data = json.loads(request.body.decode('utf-8'))
            api_key = get_api_key(request)
            if not api_key:
                desc = "Can't get a valid api key."
                return error_return(desc)

            response_dict = {
                'questions': {},
                'answers': {}
            }
            update_question_dict = {}
            update_answer_dict = {}

            try:
                a = ApiKey.objects.get(key=api_key)
            except ObjectDoesNotExist:
                desc = 'The ApiKey instance does not exist in followed key.'
                return error_return(desc, 404)

            if data.get('questions').get('1'):
                question_data = data.get('questions').get('1')
                question_title = question_data.get('question_title')
                question_text = question_data.get('question_text')
                start_dt = question_data.get('start_dt')
                end_dt = question_data.get('end_dt')
                is_editable = question_data.get('is_editable') == 'True'
                is_private = question_data.get('is_private') == 'True'

                try:
                    selected_q = Question.objects.get(api_key=a, id=question_id, is_removed=False)
                except ObjectDoesNotExist:
                    desc = 'Question does not exist.'
                    return error_return(desc, 404)

                if question_title:
                    update_question_dict.update({
                        'question_title': question_title
                    })
                if question_text:
                    update_question_dict.update({
                        'question_text': question_text
                    })
                if start_dt:
                    update_question_dict.update({
                        'start_dt': start_dt
                    })
                if end_dt:
                    update_question_dict.update({
                        'end_dt': end_dt
                    })
                if question_data.get('is_editable'):
                    update_question_dict.update({
                        'is_editable': is_editable
                    })
                if question_data.get('is_private'):
                    update_question_dict.update({
                        'is_private': is_private
                    })

                for key in update_question_dict:
                    setattr(selected_q, key, update_question_dict[key])
                selected_q.save(is_update=True)

                '''
                update answer instance
                '''
                if data.get('answers').get('1'):
                    for answer_key, answer_value in data.get('answers').get('1').items():
                        answer_text = answer_value.get('answer_text')

                        try:
                            selected_a = selected_q.answers.get(answer_num=answer_key, is_removed=False)
                        except ObjectDoesNotExist:
                            desc = 'Answer does not exist.'
                            return error_return(desc, 404)

                        if answer_text:
                            update_answer_dict.update({
                                'answer_text': answer_text
                            })

                        for key in update_answer_dict:
                            setattr(selected_a, key, update_answer_dict[key])
                        selected_a.save()

            try:
                updated_q = Question.objects.get(api_key=a, id=question_id, is_removed=False)
            except ObjectDoesNotExist:
                desc = 'The Question does not exist in followed api key.'
                return error_return(desc, 404)

            response_dict['questions'].update({
                updated_q.question_num : {
                    'question_title': updated_q.question_title,
                    'question_text': updated_q.question_text,
                    'start_dt': updated_q.start_dt,
                    'end_dt': updated_q.end_dt,
                    'is_editable': updated_q.is_editable,
                    'is_private': updated_q.is_private
                }
            })

            a = updated_q.answers.filter(is_removed=False).order_by('answer_num')
            response_dict['answers'].update({
                updated_q.question_num : {}
            })

            for answer in a:
                response_dict['answers'][updated_q.question_num].update({
                    answer.answer_num : {
                        'answer_text': answer.answer_text,
                    }
                })

            return JsonResponse(response_dict)
        else:
            desc = 'This request url is not authenticated in followed api_key.'
            return error_return(desc, 401)

    def delete(self, request, question_id):
        if match_domain(request):
            data = json.loads(request.body.decode('utf-8'))
            api_key = get_api_key(request)
            if not api_key:
                desc = "Can't get a valid api key."
                return error_return(desc)

            response_dict = {}

            try:
                a = ApiKey.objects.get(key=api_key)
                q = Question.objects.get(api_key=a, id=question_id, is_removed=False)

            except ObjectDoesNotExist:
                    desc = 'The Question does not exist in followed api_key.'
                    return error_return(desc, 404)

            answers = q.answers.filter(is_removed=False)
            for answer in answers:
                useranswers = answer.user_answers.filter(is_removed=False)
                for useranswer in useranswers:
                    useranswer.is_removed = True
                    useranswer.save()

                answer.is_removed = True
                answer.save()

            q.is_removed = True
            q.save(is_update=True)

            response_dict.update({
                "result": "success",
                "description": "Deleted a question."
            })
            return JsonResponse(response_dict)
        else:
            desc = 'This request url is not authenticated in followed api_key.'
            return error_return(desc, 401)


@csrf_exempt
@require_GET
def simple_view_answer(request, question_id):
    """
    POST - /v1/answer/view/simple

    answer 의 중요 정보만을 제공합니다.
    :parameter - api_key, ( question_title / question_id )
    :return - question_title, question_text, answer({answer_num, answer_text, answer_count})
    """
    if match_domain(request):
        api_key = get_api_key(request)
        if not api_key:
            desc = "Can't get a valid api key."
            return error_return(desc)
        response_dict = {}
        answer_list = []

        try:
            a = ApiKey.objects.get(key=api_key)
            q = Question.objects.get(api_key=a, id=question_id, is_removed=False)
        except ObjectDoesNotExist:
                desc = 'The Question does not exist in followed api_key.'
                return error_return(desc, 404)

        response_dict.update({
            'id': q.id,
            'question_title': q.question_title,
            'question_text': q.question_text
        })
        a = q.answers.filter(is_removed=False)
        if a:
            for answer in a:
                answer_list.append({
                    'id': answer.id,
                    'answer_num': answer.answer_num,
                    'answer_text': answer.answer_text,
                    'answer_count': answer.get_answer_count
                })
            response_dict.update({
                'answers': answer_list
            })
        else:
            desc = 'The Answer does not exist.'
            return error_return(desc, 404)
        return JsonResponse(response_dict)
    else:
        desc = 'This request url is not authenticated in followed api_key.'
        return error_return(desc, 401)


@csrf_exempt
@require_GET
def to_private(request, question_id):
    if match_domain(request):
        api_key = get_api_key(request)
        if not api_key:
            desc = "Can't get a valid api key."
            return error_return(desc)

        response_dict = {}

        try:
            a = ApiKey.objects.get(key=api_key)
            q = Question.objects.get(api_key=a, id=question_id, is_removed=False)
        except ObjectDoesNotExist:
            desc = 'The Question does not exist in followed api key.'
            return error_return(desc, 404)

        q.is_private = True
        q.save(is_update=True)
        response_dict.update({
            "result": "success",
            "description": "Switched to the private question."
        })
        return JsonResponse(response_dict)
    else:
        desc = 'This request url is not authenticated in followed api_key.'
        return error_return(desc, 401)


class Answers(View):
    def post(self, request, question_id):
        if match_domain(request):
            data = json.loads(request.body.decode('utf-8'))
            api_key = get_api_key(request)
            if not api_key:
                desc = "Can't get a valid api key."
                return error_return(desc)

            response_dict = {
                'answers': {}
            }

            try:
                a = ApiKey.objects.get(key=api_key)
                q = Question.objects.get(api_key=a, id=question_id, is_removed=False)
            except ObjectDoesNotExist:
                desc = 'The Question does not exist in followed api key.'
                return error_return(desc, 404)

            for key, value in data.get('answers').items():
                answer_text = value.get('answer_text')
                if answer_text:
                    new_answer = Answer(question=q, answer_text=answer_text, answer_num=key)
                    new_answer.save()
                else:
                    pass

            '''
            load data for response json
            '''
            a = q.answers.filter(is_removed=False).order_by('answer_num')

            for answer in a:
                response_dict['answers'].update({
                    answer.answer_num : {
                        'id': answer.id,
                        'answer_text': answer.answer_text,
                        'answer_count': answer.get_answer_count
                    }
                })

            return JsonResponse(response_dict)
        else:
            desc = 'This request url is not authenticated in followed api_key.'
            return error_return(desc, 401)

    def get(self, request, *args, **kwargs):
        question_id=kwargs['question_id']
        answer_num=kwargs.get('answer_num')
        if match_domain(request):
            api_key = get_api_key(request)
            if not api_key:
                desc = "Can't get a valid api key."
                return error_return(desc)

            response_dict = {
                'answers':{}
            }

            '''
            logic for get answer list
            '''
            if not answer_num:
                try:
                    a = ApiKey.objects.get(key=api_key)
                    q = Question.objects.get(api_key=a, id=question_id, is_removed=False)
                except ObjectDoesNotExist:
                    desc = 'The Question does not exist in followed api key.'
                    return error_return(desc, 404)

                a = q.answers.filter(is_removed=False)
                if a:
                    for answer in a:
                        response_dict['answers'].update({
                            answer.answer_num : {}
                        })
                        response_dict['answers'][answer.answer_num].update({
                            'id': answer.id,
                            'answer_text': answer.answer_text,
                            'answer_count': answer.get_answer_count
                        })
                else:
                    desc = 'The Answer does not exist.'
                    return error_return(desc, 404)

                return JsonResponse(response_dict)
            '''
            logic for get one answer
            '''
            if answer_num:
                try:
                    a = ApiKey.objects.get(key=api_key)
                    q = Question.objects.get(api_key=a, id=question_id, is_removed=False)
                except ObjectDoesNotExist:
                    desc = 'The Question does not exist in followed api key.'
                    return error_return(desc, 404)

                a = q.answers.get(answer_num=answer_num, is_removed=False)
                if a:
                    response_dict['answers'].update({
                        a.answer_num : {}
                    })
                    response_dict['answers'][a.answer_num].update({
                        'id': a.id,
                        'answer_text': a.answer_text,
                        'answer_count': a.get_answer_count
                    })
                else:
                    desc = 'The Answer does not exist.'
                    return error_return(desc, 404)

                return JsonResponse(response_dict)
        else:
            desc = 'This request url is not authenticated in followed api_key.'
            return error_return(desc, 401)

    def delete(self, request, question_id, answer_num):
        if match_domain(request):
            api_key = get_api_key(request)
            if not api_key:
                desc = "Can't get a valid api key."
                return error_return(desc)
            response_dict = {}

            try:
                a = ApiKey.objects.get(key=api_key)
                q = Question.objects.get(api_key=a, id=question_id, is_removed=False)
            except ObjectDoesNotExist:
                    desc = 'The Question does not exist in followed api_key.'
                    return error_return(desc, 404)

            answer = q.answers.filter(answer_num=answer_num, is_removed=False)
            for a in answer:
                a.is_removed = True
                a.save()

            response_dict.update({
                "result": "success",
                "description": "Deleted this answer."
            })
            return JsonResponse(response_dict)
        else:
            desc = 'This request url is not authenticated in followed api_key.'
            return error_return(desc, 401)

    def put(self, request, question_id):
        if match_domain(request):
            data = json.loads(request.body.decode('utf-8'))
            api_key = get_api_key(request)
            if not api_key:
                desc = "Can't get a valid api key."
                return error_return(desc)
            response_dict = {
                'answers': {}
            }

            try:
                a = ApiKey.objects.get(key=api_key)
                q = Question.objects.get(api_key=a, id=question_id, is_removed=False)
            except ObjectDoesNotExist:
                desc = 'The Question does not exist in followed api key.'
                return error_return(desc, 404)

            for key, value in data.get('answers').items():
                update_a = Answer.objects.get(question=q, answer_num=key, is_removed=False)
                answer_text = value.get('answer_text')
                if answer_text:
                    update_a.answer_text = answer_text
                    update_a.save()
                else:
                    pass

            '''
            load data for response json
            '''
            a = q.answers.filter(is_removed=False).order_by('answer_num')

            for answer in a:
                response_dict['answers'].update({
                    answer.answer_num : {
                        'id': answer.id,
                        'answer_text': answer.answer_text,
                        'answer_count': answer.get_answer_count
                    }
                })

            return JsonResponse(response_dict)
        else:
            desc = 'This request url is not authenticated in followed api_key.'
            return error_return(desc, 401)


class Useranswers(View):
    def post(self, request, question_id, answer_num):
        if match_domain(request):
            data = json.loads(request.body.decode('utf-8'))
            api_key = get_api_key(request)
            if not api_key:
                desc = "Can't get a valid api key."
                return error_return(desc)
            unique_user = data['useranswer'].get('unique_user')
            response_dict = {
                'useranswer': {}
            }

            try:
                a = ApiKey.objects.get(key=api_key)
                q = Question.objects.get(api_key=a, id=question_id, is_removed=False)
            except ObjectDoesNotExist:
                desc = 'The Question does not exist in followed api key.'
                return error_return(desc, 404)

            if q.answers:
                try:
                    a = Answer.objects.get(question=q, answer_num=answer_num, is_removed=False)
                except ObjectDoesNotExist:
                    desc = 'The Answer does not exist in followed answer_num.'
                    return error_return(desc, 404)

                new_useranswer = UserAnswer(answer=a, unique_user=unique_user)
                new_useranswer.save()

                try:
                    curr_useranswer = UserAnswer.objects.get(id=new_useranswer.id, is_removed=False)
                except ObjectDoesNotExist:
                    desc = 'The UserAnswer does not exist in followed id.'
                    return error_return(desc, 404)

                response_dict['useranswer'].update({
                    'id': curr_useranswer.id,
                    'created_dt': curr_useranswer.created_dt,
                    'unique_user': curr_useranswer.unique_user,
                    'answer_num': curr_useranswer.answer.answer_num
                })
            else:
                desc = 'The Answer does not exist.'
                return error_return(desc, 404)

            return JsonResponse(response_dict)
        else:
            desc = 'This request url is not authenticated in followed api_key.'
            return error_return(desc, 401)

    def get(self, request, question_id, *args, **kwargs):
        unique_user = kwargs.get('unique_user')
        answer_num = kwargs.get('answer_num')
        if match_domain(request):
            api_key = get_api_key(request)
            if not api_key:
                desc = "Can't get a valid api key."
                return error_return(desc)

            response_dict = {
                'useranswers': {}
            }

            try:
                a = ApiKey.objects.get(key=api_key)
                q = Question.objects.get(api_key=a, id=question_id, is_removed=False)
            except ObjectDoesNotExist:
                desc = 'The Question does not exist in followed api key.'
                return error_return(desc, 404)

            '''
            case 1. get all useranswers
            '''
            if not unique_user and not answer_num:
                try:
                    answers = Answer.objects.filter(question=q, is_removed=False)
                except ObjectDoesNotExist:
                    desc = 'The Answer does not exist in followed answer_num.'
                    return error_return(desc, 404)

                for a in answers:
                    response_dict['useranswers'].update({
                        a.answer_num : []
                    })
                    try:
                        useranswers = UserAnswer.objects.filter(answer=a, is_removed=False)
                    except UserAnswer.DoesNotExist:
                        desc = 'No such user answered this question.'
                        return error_return(desc, 404)
                    for u in useranswers:
                        response_dict['useranswers'][a.answer_num].append({
                            "unique_user": u.unique_user,
                            "id": u.id,
                            "created_dt": u.created_dt
                        })
                return JsonResponse(response_dict)
            '''
            case 2. get all useranswers of one answer
            '''
            if answer_num and (not unique_user):
                try:
                    answer = Answer.objects.get(question=q, answer_num=answer_num, is_removed=False)
                except ObjectDoesNotExist:
                    desc = 'The Answer does not exist in followed answer_num.'
                    return error_return(desc, 404)

                response_dict['useranswers'].update({
                    answer.answer_num: []
                })

                try:
                    useranswers = UserAnswer.objects.filter(answer=answer, is_removed=False)
                except ObjectDoesNotExist:
                    desc = 'No such user answered this question.'
                    return error_return(desc, 404)

                for u in useranswers:
                    response_dict['useranswers'][answer.answer_num].append({
                        "unique_user": u.unique_user,
                        "id": u.id,
                        "created_dt": u.created_dt
                    })
                return JsonResponse(response_dict)

            '''
            case 3. get one useranswer
            '''
            if unique_user:
                try:
                    answers = Answer.objects.filter(question=q, is_removed=False)
                except ObjectDoesNotExist:
                    desc = 'The Answer does not exist in followed answer_num.'
                    return error_return(desc, 404)

                try:
                    useranswer = UserAnswer.objects.get(answer__in=answers, unique_user=unique_user, is_removed=False)
                except ObjectDoesNotExist:
                    desc = 'No such user answered this question.'
                    return error_return(desc, 404)

                response_dict['useranswers'].update({
                    useranswer.answer.answer_num: {}
                })

                response_dict['useranswers'][useranswer.answer.answer_num].update({
                    "unique_user": useranswer.unique_user,
                    "id": useranswer.id,
                    "created_dt": useranswer.created_dt
                })
                return JsonResponse(response_dict)
        else:
            desc = 'This request url is not authenticated in followed api_key.'
            return error_return(desc, 401)

    def delete(self, request, question_id, unique_user):
        if match_domain(request):
            api_key = get_api_key(request)
            if not api_key:
                desc = "Can't get a valid api key."
                return error_return(desc)
            response_dict = {}

            try:
                a = ApiKey.objects.get(key=api_key)
                q = Question.objects.get(api_key=a, id=question_id, is_removed=False)
            except ObjectDoesNotExist:
                    desc = 'The Question does not exist in followed api_key.'
                    return error_return(desc, 404)

            try:
                answers = Answer.objects.filter(question=q, is_removed=False)
                useranswer = UserAnswer.objects.get(answer__in=answers, unique_user=unique_user, is_removed=False)
                useranswer.is_removed = True
                useranswer.save()
            except ObjectDoesNotExist:
                    desc = 'The UserAnswer does not exist in followed unique_user.'
                    return error_return(desc, 404)

            response_dict.update({
                "result": "success",
                "description": "Deleted this useranswer."
            })
            return JsonResponse(response_dict)
        else:
            desc = 'This request url is not authenticated in followed api_key.'
            return error_return(desc, 401)

    def put(self, request, question_id, unique_user):
        if match_domain(request):
            data = json.loads(request.body.decode('utf-8'))
            api_key = get_api_key(request)
            if not api_key:
                desc = "Can't get a valid api key."
                return error_return(desc)
            answer_num = data.get('answer_num')
            response_dict = {
                'useranswer':{}
            }

            try:
                a = ApiKey.objects.get(key=api_key)
                q = Question.objects.get(api_key=a, id=question_id, is_removed=False)
            except ObjectDoesNotExist:
                desc = 'The Question does not exist in followed api_key.'
                return error_return(desc, 404)

            if q.is_editable:
                try:
                    answers = Answer.objects.filter(question=q, is_removed=False)
                    u = UserAnswer.objects.get(answer__in=answers, unique_user=unique_user, is_removed=False)
                except ObjectDoesNotExist:
                    desc = 'The UserAnswer does not exist in followed unique_user.'
                    return error_return(desc, 404)

                try:
                    new_answer = Answer.objects.get(question=q, answer_num=answer_num, is_removed=False)
                except ObjectDoesNotExist:
                    desc = 'The new Answer instance does not exist in followed unique_user.'
                    return error_return(desc, 404)

                u.answer = new_answer
                u.save()

                response_dict['useranswer'].update({
                    "answer_num": u.answer.answer_num,
                    "unique_user": u.unique_user,
                    "created_dt": u.created_dt,
                    'id': u.id
                })
                return JsonResponse(response_dict)
            else:
                desc = 'Property [is_editable] of this question is currently False. Set True for this request.'
                return error_return(desc)
        else:
            desc = 'This request url is not authenticated in followed api_key.'
            return error_return(desc, 401)

