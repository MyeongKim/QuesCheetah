from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page, never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.utils.decorators import method_decorator
from django.views.generic.base import View
import urllib.request, urllib.error, urllib.parse
from urllib.error import HTTPError
import json
from main.models import ApiKey, Domain
from vote.models import Question, Answer, UserAnswer, MultiQuestion
from django.conf import settings

import jwt

"""
Get host domain variable which is
different with execution environment.
Default local address is "127.0.0.1:8000".
"""
HOST_HOME = getattr(settings, "HOST_HOME", None)


"""
QueesCheetah Web Server view function
Functions includes several activities in quescheetah.com.
Dashboard page rendering function included.
"""


# Render question select page for a account
@never_cache
def select_question(request):
    context = {
    }
    if not hasattr(request.user, 'api_keys'):
        messages.add_message(request, messages.ERROR, 'You should create api key first.')
        return redirect('main:user_mypage', request.user.id)
    else:
        api_key = request.user.api_keys.key
        context.update({
            'api_key': api_key
        })

    try:
        api_key_instance = ApiKey.objects.get(key=api_key)
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, 'This api_key is not valid.')
        return redirect('main:user_mypage', request.user.id)

    single_question_set = Question.objects.filter(api_key=api_key_instance, multi_question=None, is_removed=False)
    multi_question_set = MultiQuestion.objects.filter(api_key=api_key_instance, is_removed=False)
    context.update({'multi_question': multi_question_set, 'single_question': single_question_set})

    return render(request, 'vote/pages/question_select.html', context)


# Render creating a new question page
def new(request, api_key):
    context = {
        'api_key': api_key
    }

    return render(request, 'vote/pages/new.html', context)


# Show a dashboard related page for a user
def dashboard_select(request):
    context = {

    }
    if not hasattr(request.user, 'api_keys'):
        messages.add_message(request, messages.ERROR, 'You should create api key first.')
        return redirect('main:user_mypage', request.user.id)
    else:
        api_key = request.user.api_keys.key
        context.update({
            'api_key': api_key
        })

    if MultiQuestion.objects.filter(api_key__key=api_key):
        multi_question_id = MultiQuestion.objects.filter(api_key__key=api_key)[0].id

        return redirect('v1:dashboard_group_overview', multi_question_id)

    elif Question.objects.filter(api_key__key=api_key):
        question_id = Question.objects.filter(api_key__key=api_key)[0].id

        return redirect('v1:dashboard_overview', question_id)

    else:
        # If user didn't make any question or group question, redirect to create page.
        return redirect('v1:new', api_key)


# Render dashboard overview page for a single question.
def dashboard_overview(request, question_id):
    context = {

    }

    if not hasattr(request.user, 'api_keys'):
        messages.add_message(request, messages.ERROR, 'You should create api key first.')
        return redirect('main:user_mypage', request.user.id)
    else:
        api_key = request.user.api_keys.key
        context.update({
            'api_key': api_key
        })

    '''
    request question data to rest api
    '''
    url = 'http://'+HOST_HOME+'v1/questions/'+str(question_id)

    req = urllib.request.Request(url)
    req.add_header('api-key', api_key)
    req.add_header('Origin', HOST_HOME)

    try:
        response_json = urllib.request.urlopen(req).read()
        response_json = json.loads(response_json.decode('utf-8'))
    except HTTPError:
        messages.add_message(request, messages.ERROR, 'Fail to get data.')
        return HttpResponse(HTTPError.reason, HTTPError)

    context.update(response_json)

    '''
    request useranswer data to rest api
    '''
    url = 'http://'+HOST_HOME+'v1/questions/'+str(question_id)+'/answers/useranswers'

    req = urllib.request.Request(url)
    req.add_header('api-key', api_key)
    req.add_header('Origin', HOST_HOME)

    try:
        response_json = urllib.request.urlopen(req).read()
        response_json = json.loads(response_json.decode('utf-8'))
    except HTTPError:
        messages.add_message(request, messages.ERROR, 'Fail to get data.')
        return HttpResponse(HTTPError.reason, HTTPError)

    context.update(response_json)

    '''
    provide other question/group info for navigation
    '''
    context.update({
        'nav_group': [],
        'nav_question': []
    })

    try:
        multi_question_instance_set = MultiQuestion.objects.filter(api_key__key=api_key)
    except ObjectDoesNotExist:
        pass
    else:
        for multi_question in multi_question_instance_set:
            context['nav_group'].append({
                "group_name": multi_question.group_name,
                "id": multi_question.id
            })

    try:
        question_instance_set = Question.objects.filter(api_key__key=api_key)
    except ObjectDoesNotExist:
        pass
    else:
        for question in question_instance_set:
            context['nav_question'].append({
                "question_title": question.question_title,
                "id": question.id
            })

    context.update({
        'HOST_HOME': HOST_HOME
    })
    return render(request, 'vote/pages/dashboard_overview.html', context)


# Render dashboard analysis page for a single question.
def dashboard_filter(request, question_id):
    context = {

    }
    if not hasattr(request.user, 'api_keys'):
        messages.add_message(request, messages.ERROR, 'You should create api key first.')
        return redirect('main:user_mypage', request.user.id)
    else:
        api_key = request.user.api_keys.key
        context.update({
            'api_key': api_key
        })

    '''
    request question data to rest api
    '''
    url = 'http://'+HOST_HOME+'v1/questions/'+str(question_id)

    req = urllib.request.Request(url)
    req.add_header('api-key', api_key)
    req.add_header('Origin', HOST_HOME)

    try:
        response_json = urllib.request.urlopen(req).read()
        response_json = json.loads(response_json.decode('utf-8'))
    except HTTPError:
        messages.add_message(request, messages.ERROR, 'Fail to get data.')
        return HttpResponse(HTTPError.reason, HTTPError)

    context.update(response_json)

    '''
    request useranswer data to rest api
    '''
    url = 'http://'+HOST_HOME+'v1/questions/'+str(question_id)+'/answers/useranswers'

    req = urllib.request.Request(url)
    req.add_header('api-key', api_key)
    req.add_header('Origin', HOST_HOME)

    try:
        response_json = urllib.request.urlopen(req).read()
        response_json = json.loads(response_json.decode('utf-8'))
    except HTTPError:
        messages.add_message(request, messages.ERROR, 'Fail to get data.')
        return HttpResponse(HTTPError.reason, HTTPError)

    context.update(response_json)

    '''
    provide other question/group info for navigation
    '''
    context.update({
        'nav_group': [],
        'nav_question': []
    })

    try:
        multi_question_instance_set = MultiQuestion.objects.filter(api_key__key=api_key)
    except ObjectDoesNotExist:
        pass
    else:
        for multi_question in multi_question_instance_set:
            context['nav_group'].append({
                "group_name": multi_question.group_name,
                "id": multi_question.id
            })

    try:
        question_instance_set = Question.objects.filter(api_key__key=api_key)
    except ObjectDoesNotExist:
        pass
    else:
        for question in question_instance_set:
            context['nav_question'].append({
                "question_title": question.question_title,
                "id": question.id
            })

    context.update({
        'HOST_HOME': HOST_HOME
    })
    return render(request, 'vote/pages/dashboard_filter.html', context)


# Render dashboard users page for a single question.
def dashboard_users(request, question_id):
    context = {

    }
    if not hasattr(request.user, 'api_keys'):
        messages.add_message(request, messages.ERROR, 'You should create api key first.')
        return redirect('main:user_mypage', request.user.id)
    else:
        api_key = request.user.api_keys.key
        context.update({
            'api_key': api_key
        })

    '''
    request question data to rest api
    '''
    url = 'http://'+HOST_HOME+'v1/questions/'+str(question_id)

    req = urllib.request.Request(url)
    req.add_header('api-key', api_key)
    req.add_header('Origin', HOST_HOME)

    try:
        response_json = urllib.request.urlopen(req).read()
        response_json = json.loads(response_json.decode('utf-8'))
    except HTTPError:
        messages.add_message(request, messages.ERROR, 'Fail to get data.')
        return HttpResponse(HTTPError.reason, HTTPError)

    context.update(response_json)

    '''
    request useranswer data to rest api
    '''
    url = 'http://'+HOST_HOME+'v1/questions/'+str(question_id)+'/answers/useranswers'

    req = urllib.request.Request(url)
    req.add_header('api-key', api_key)
    req.add_header('Origin', HOST_HOME)

    try:
        response_json = urllib.request.urlopen(req).read()
        response_json = json.loads(response_json.decode('utf-8'))
    except HTTPError:
        messages.add_message(request, messages.ERROR, 'Fail to get data.')
        return HttpResponse(HTTPError.reason, HTTPError)

    context.update(response_json)

    '''
    provide other question/group info for navigation
    '''
    context.update({
        'nav_group': [],
        'nav_question': []
    })

    try:
        multi_question_instance_set = MultiQuestion.objects.filter(api_key__key=api_key)
    except ObjectDoesNotExist:
        pass
    else:
        for multi_question in multi_question_instance_set:
            context['nav_group'].append({
                "group_name": multi_question.group_name,
                "id": multi_question.id
            })

    try:
        question_instance_set = Question.objects.filter(api_key__key=api_key)
    except ObjectDoesNotExist:
        pass
    else:
        for question in question_instance_set:
            context['nav_question'].append({
                "question_title": question.question_title,
                "id": question.id
            })
    return render(request, 'vote/pages/dashboard_users.html', context)


# Render dashboard overview page for a group question.
def dashboard_group_overview(request, group_id):
    context = {

    }
    if not hasattr(request.user, 'api_keys'):
        messages.add_message(request, messages.ERROR, 'You should create api key first.')
        return redirect('main:user_mypage', request.user.id)
    else:
        api_key = request.user.api_keys.key
        context.update({
            'api_key': api_key
        })

    '''
    request group data to rest api
    '''
    url = 'http://'+HOST_HOME+'v1/groups/'+str(group_id)

    req = urllib.request.Request(url)
    req.add_header('api-key', api_key)
    req.add_header('Origin', HOST_HOME)

    try:
        response_json = urllib.request.urlopen(req).read()
        response_json = json.loads(response_json.decode('utf-8'))
    except HTTPError:
        messages.add_message(request, messages.ERROR, 'Fail to get data.')
        return HttpResponse(HTTPError.reason, HTTPError)

    context.update(response_json)

    '''
    request useranswer data to rest api
    '''
    url = 'http://'+HOST_HOME+'v1/groups/'+str(group_id)+'/answers/useranswers'

    req = urllib.request.Request(url)
    req.add_header('api-key', api_key)
    req.add_header('Origin', HOST_HOME)

    try:
        response_json = urllib.request.urlopen(req).read()
        response_json = json.loads(response_json.decode('utf-8'))
    except HTTPError:
        messages.add_message(request, messages.ERROR, 'Fail to get data.')
        return HttpResponse(HTTPError.reason, HTTPError)

    context.update(response_json)

    '''
    provide other question/group info for navigation
    '''
    context.update({
        'nav_group': [],
        'nav_question': []
    })

    try:
        multi_question_instance_set = MultiQuestion.objects.filter(api_key__key=api_key)
    except ObjectDoesNotExist:
        pass
    else:
        for multi_question in multi_question_instance_set:
            context['nav_group'].append({
                "group_name": multi_question.group_name,
                "id": multi_question.id
            })

    try:
        question_instance_set = Question.objects.filter(api_key__key=api_key)
    except ObjectDoesNotExist:
        pass
    else:
        for question in question_instance_set:
            context['nav_question'].append({
                "question_title": question.question_title,
                "id": question.id
            })

    context.update({
        'HOST_HOME': HOST_HOME
    })
    return render(request, 'vote/pages/dashboard_overview.html', context)


# Render dashboard analysis page for a group question.
def dashboard_group_filter(request, group_id):
    context = {

    }
    if not hasattr(request.user, 'api_keys'):
        messages.add_message(request, messages.ERROR, 'You should create api key first.')
        return redirect('main:user_mypage', request.user.id)
    else:
        api_key = request.user.api_keys.key
        context.update({
            'api_key': api_key
        })

    '''
    request group data to rest api
    '''
    url = 'http://'+HOST_HOME+'v1/groups/'+str(group_id)

    req = urllib.request.Request(url)
    req.add_header('api-key', api_key)
    req.add_header('Origin', HOST_HOME)

    try:
        response_json = urllib.request.urlopen(req).read()
        response_json = json.loads(response_json.decode('utf-8'))
    except HTTPError:
        messages.add_message(request, messages.ERROR, 'Fail to get data.')
        return HttpResponse(HTTPError.reason, HTTPError)

    context.update(response_json)

    '''
    request useranswer data to rest api
    '''
    url = 'http://'+HOST_HOME+'v1/groups/'+str(group_id)+'/answers/useranswers'

    req = urllib.request.Request(url)
    req.add_header('api-key', api_key)
    req.add_header('Origin', HOST_HOME)

    try:
        response_json = urllib.request.urlopen(req).read()
        response_json = json.loads(response_json.decode('utf-8'))
    except HTTPError:
        messages.add_message(request, messages.ERROR, 'Fail to get data.')
        return HttpResponse(HTTPError.reason, HTTPError)

    context.update(response_json)

    '''
    provide other question/group info for navigation
    '''
    context.update({
        'nav_group': [],
        'nav_question': []
    })

    try:
        multi_question_instance_set = MultiQuestion.objects.filter(api_key__key=api_key)
    except ObjectDoesNotExist:
        pass
    else:
        for multi_question in multi_question_instance_set:
            context['nav_group'].append({
                "group_name": multi_question.group_name,
                "id": multi_question.id
            })

    try:
        question_instance_set = Question.objects.filter(api_key__key=api_key)
    except ObjectDoesNotExist:
        pass
    else:
        for question in question_instance_set:
            context['nav_question'].append({
                "question_title": question.question_title,
                "id": question.id
            })

    context.update({
        'HOST_HOME': HOST_HOME
    })
    return render(request, 'vote/pages/dashboard_filter.html', context)


# Render dashboard users page for a group question.
def dashboard_group_users(request, group_id):
    context = {

    }
    if not hasattr(request.user, 'api_keys'):
        messages.add_message(request, messages.ERROR, 'You should create api key first.')
        return redirect('main:user_mypage', request.user.id)
    else:
        api_key = request.user.api_keys.key
        context.update({
            'api_key': api_key
        })

    '''
    request group data to rest api
    '''
    url = 'http://'+HOST_HOME+'v1/groups/'+str(group_id)

    req = urllib.request.Request(url)
    req.add_header('api-key', api_key)
    req.add_header('Origin', HOST_HOME)

    try:
        response_json = urllib.request.urlopen(req).read()
        response_json = json.loads(response_json.decode('utf-8'))
    except HTTPError:
        messages.add_message(request, messages.ERROR, 'Fail to get data.')
        return HttpResponse(HTTPError.reason, HTTPError)

    context.update(response_json)

    '''
    request useranswer data to rest api
    '''
    url = 'http://'+HOST_HOME+'v1/groups/'+str(group_id)+'/answers/useranswers'

    req = urllib.request.Request(url)
    req.add_header('api-key', api_key)
    req.add_header('Origin', HOST_HOME)

    try:
        response_json = urllib.request.urlopen(req).read()
        response_json = json.loads(response_json.decode('utf-8'))
    except HTTPError:
        messages.add_message(request, messages.ERROR, 'Fail to get data.')
        return HttpResponse(HTTPError.reason, HTTPError)

    context.update(response_json)

    '''
    provide other question/group info for navigation
    '''
    context.update({
        'nav_group': [],
        'nav_question': []
    })

    try:
        multi_question_instance_set = MultiQuestion.objects.filter(api_key__key=api_key)
    except ObjectDoesNotExist:
        pass
    else:
        for multi_question in multi_question_instance_set:
            context['nav_group'].append({
                "group_name": multi_question.group_name,
                "id": multi_question.id
            })

    try:
        question_instance_set = Question.objects.filter(api_key__key=api_key)
    except ObjectDoesNotExist:
        pass
    else:
        for question in question_instance_set:
            context['nav_question'].append({
                "question_title": question.question_title,
                "id": question.id
            })
    return render(request, 'vote/pages/dashboard_users.html', context)


# Render dashboard sample page that anyone can access
@never_cache
def dashboard_sample(request, page):
    context = {

    }

    api_key = 'b3e9d78456671bd24be1041c16d6e689afec27d6'
    context.update({
        'api_key': api_key
    })

    '''
    request group data to rest api
    '''
    url = 'http://'+HOST_HOME+'v1/groups/5'

    req = urllib.request.Request(url)
    req.add_header('api-key', api_key)

    try:
        response_json = urllib.request.urlopen(req).read()
        response_json = json.loads(response_json.decode('utf-8'))
    except HTTPError:
        messages.add_message(request, messages.ERROR, 'Fail to get data.')
        return HttpResponse(HTTPError.reason, HTTPError)

    context.update(response_json)

    '''
    request useranswer data to rest api
    '''
    url = 'http://'+HOST_HOME+'v1/groups/5/answers/useranswers'

    req = urllib.request.Request(url)
    req.add_header('api-key', api_key)

    try:
        response_json = urllib.request.urlopen(req).read()
        response_json = json.loads(response_json.decode('utf-8'))
    except HTTPError:
        messages.add_message(request, messages.ERROR, 'Fail to get data.')
        return HttpResponse(HTTPError.reason, HTTPError)

    context.update(response_json)

    '''
    provide other question/group info for navigation
    '''
    context.update({
        'nav_group': [],
        'nav_question': []
    })

    try:
        multi_question_instance_set = MultiQuestion.objects.filter(api_key__key=api_key)
    except ObjectDoesNotExist:
        pass
    else:
        for multi_question in multi_question_instance_set:
            context['nav_group'].append({
                "group_name": multi_question.group_name,
                "id": multi_question.id
            })

    try:
        question_instance_set = Question.objects.filter(api_key__key=api_key)
    except ObjectDoesNotExist:
        pass
    else:
        for question in question_instance_set:
            context['nav_question'].append({
                "question_title": question.question_title,
                "id": question.id
            })

    context.update({
        'is_sample': True
    })

    if page == 'users':
        return render(request, 'vote/pages/dashboard_users.html', context)
    if page == 'filter':
        return render(request, 'vote/pages/dashboard_filter.html', context)
    return render(request, 'vote/pages/dashboard_overview.html', context)



"""
Our view functions for REST API request
Every functions check if this request has correct authentication.
If request method is 'GET', we don't need to check authentication.
All response format is all JSON format. (also in error case)
"""

"""
Domain matching process is only needed
when request method is not 'GET'.
We check request header 'Origin' to match user's domain instance value.
This proccess inhibits Cross Origin Request Sharing.
"""


def match_domain(request):
    if request.method == 'GET':
        return True
    api_key = get_api_key(request)
    if api_key:
        request_domain = request.META.get('HTTP_ORIGIN')
        if request_domain[:7] == 'http://':
            request_domain = request_domain[7:]
        if request_domain[:4] == 'www.':
       	    request_domain = request_domain[4:]
        try:
            api_key_instance = ApiKey.objects.get(key=api_key)
            domain_instance = Domain.objects.get(domain=request_domain, api_key=api_key_instance)
        except ObjectDoesNotExist:
            return False
        return True
    else:
        return False


# Make JSON object for response
def error_return(desc, status=400):
    return JsonResponse({
        'error': True,
        'description': desc
    }, status=status)


"""
Parse request header 'api-key' and get information.
If the value is not exist, check the authentication can be done by JWT.
"""


def get_api_key(request):
    api_key = request.META.get('HTTP_API_KEY')
    if api_key:
        return api_key
    else:
        secret_key = ApiKey.objects.get(id=request.META.get('HTTP_KID')).secret_key
        try:
            decoded_value = jwt.decode(request.META.get('HTTP_JWT'), secret_key, algorithms=['HS256', 'HS512', 'HS384'])
        except jwt.InvalidTokenError:
            return False
        return decoded_value.get('api-key')


"""
Actions about MultiQuestion model.
Correct request format can be accessed in following url.
https://mingkim.gitbooks.io/quescheetah-document/content/Group/index.html
"""
class Groups(View):
    # Create a new MultiQuestion instance.
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
                api_key_instance = ApiKey.objects.get(key=api_key)
            except ObjectDoesNotExist:
                desc = 'The ApiKey does not exist in followed key.'
                return error_return(desc, 404)

            new_multiq = MultiQuestion(api_key=api_key_instance, group_name=group_name)
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
                        api_key=api_key_instance,
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
                multi_question_instance = MultiQuestion.objects.get(id=new_multiq.id, is_removed=False)
                question_instance_set = multi_question_instance.question_elements.filter(is_removed=False).order_by('question_num')

            except ObjectDoesNotExist:
                desc = 'MultiQuestion does not exist by new_multiq.id'
                return error_return(desc, 404)

            response_dict.update({
                "group_id": multi_question_instance.id,
                "group_name": multi_question_instance.group_name
            })

            for question in question_instance_set:
                response_dict['questions'].update({
                    question.question_num : {
                        'question_id': question.id,
                        'question_title': question.question_title,
                        'question_text': question.question_text,
                        'start_dt': question.start_dt,
                        'end_dt': question.end_dt,
                        'is_editable': question.is_editable,
                        'is_private': question.is_private
                    }
                })

                answer_instance_set = question.answers.filter(is_removed=False).order_by('answer_num')
                response_dict['answers'].update({
                    question.question_num : {}
                })

                for answer in answer_instance_set:
                    response_dict['answers'][question.question_num].update({
                        answer.answer_num : {
                            'answer_text': answer.answer_text,
                        }
                    })

            return JsonResponse(response_dict)
        else:
            desc = 'This request url is not authenticated in followed api_key.'
            return error_return(desc, 401)

    # Send a MultiQuestion info
    @method_decorator(never_cache)
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
                multi_question_instance = MultiQuestion.objects.get(id=group_id, is_removed=False)
                question_instance_set = multi_question_instance.question_elements.filter(is_removed=False).order_by('question_num')
            except ObjectDoesNotExist:
                desc = 'The MultiQuestion does not exist in follwed api key'
                return error_return(desc, 404)

            response_dict.update({
                "group_id": multi_question_instance.id,
                "group_name": multi_question_instance.group_name
            })

            for question in question_instance_set:
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

                answer_instance_set = question.answers.filter(is_removed=False).order_by('answer_num')
                response_dict['answers'].update({
                    question.question_num : {}
                })

                for answer in answer_instance_set:
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

    # Update a MultiQuestion value
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
                api_key_instance = ApiKey.objects.get(key=api_key)
            except ObjectDoesNotExist:
                desc = 'The ApiKey does not exist in followed key.'
                return error_return(desc, 404)

            multi_question_instance = MultiQuestion.objects.get(api_key=api_key_instance, id=group_id, is_removed=False)
            group_name = data.get('group_name')

            if group_name:
                multi_question_instance.group_name = group_name
                multi_question_instance.save()

            if data.get('questions'):
                for question_key, question_value in data.get('questions').items():
                    question_title = question_value.get('question_title')
                    question_text = question_value.get('question_text')
                    start_dt = question_value.get('start_dt')
                    end_dt = question_value.get('end_dt')
                    is_editable = question_value.get('is_editable') == 'True'
                    is_private = question_value.get('is_private') == 'True'

                    try:
                        selected_question_instance = multi_question_instance.question_elements.get(question_num=question_key, is_removed=False)
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
                        setattr(selected_question_instance, key, update_question_dict[key])
                    selected_question_instance.save(is_update=True)

                    '''
                    update answer instance
                    '''
                    if data.get('answers').get(question_key):
                        for answer_key, answer_value in data.get('answers').get(question_key).items():
                            answer_text = answer_value.get('answer_text')

                            try:
                                selected_answer_instance = selected_question_instance.answers.get(answer_num=answer_key, is_removed=False)
                            except ObjectDoesNotExist:
                                desc = 'Answer does not exist.'
                                return error_return(desc, 404)

                            if answer_text:
                                update_answer_dict.update({
                                    'answer_text': answer_text
                                })

                            for key in update_answer_dict:
                                setattr(selected_answer_instance, key, update_answer_dict[key])
                            selected_answer_instance.save()

            '''
            load data for response json
            '''
            try:
                multi_question_created = MultiQuestion.objects.get(id=multi_question_instance.id, is_removed=False)
                question_created_set = multi_question_created.question_elements.filter(is_removed=False).order_by('question_num')
            except ObjectDoesNotExist:
                desc = 'MultiQuestion does not exist by new_multiq.id'
                return error_return(desc, 404)

            response_dict.update({
                "group_id": multi_question_created.id,
                "group_name": multi_question_created.group_name
            })

            for question in question_created_set:
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

                answer_created_set = question.answers.filter(is_removed=False).order_by('answer_num')
                response_dict['answers'].update({
                    question.question_num : {}
                })

                for answer in answer_created_set:
                    response_dict['answers'][question.question_num].update({
                        answer.answer_num : {
                            'answer_text': answer.answer_text,
                        }
                    })

            return JsonResponse(response_dict)

        else:
            desc = 'This request url is not authenticated in followed api_key.'
            return error_return(desc, 401)

    # Delete a MultiQuestion and all related Queston, Answer, Useranswer
    def delete(self, request, group_id):
        if match_domain(request):
            api_key = get_api_key(request)
            if not api_key:
                desc = "Can't get a valid api key."
                return error_return(desc)

            response_dict = {}

            try:
                api_key_instance = ApiKey.objects.get(key=api_key)
                multi_question_instance = MultiQuestion.objects.get(api_key=api_key_instance, id=group_id, is_removed=False)
            except ObjectDoesNotExist:
                    desc = 'The Question does not exist in followed api_key.'
                    return error_return(desc, 404)

            question_instance_set = multi_question_instance.question_elements.filter(is_removed=False)
            for question in question_instance_set:
                answer_instance_set = question.answers.filter(is_removed=False)
                for answer in answer_instance_set:
                    if hasattr(answer, 'user_answers'):
                        useranswer_instance_set = answer.user_answers.filter(is_removed=False)
                        for useranswer in useranswer_instance_set:
                            useranswer.is_removed = True
                            useranswer.save()

                    answer.is_removed = True
                    answer.save()

                question.is_removed = True
                question.save(is_update=True)

            multi_question_instance.is_removed = True
            multi_question_instance.save()

            response_dict.update({
                "result": "success",
                "description": "Deleted this group"
            })
            return JsonResponse(response_dict)
        else:
            desc = 'This request url is not authenticated in followed api_key.'
            return error_return(desc, 401)

"""
Actions about Question model.
Question related data can be requested by 2 format in 'GET' method.
One is short simple information response,
and the other one is full response that contains all informations.
Correct request format can be accessed in following url.
https://mingkim.gitbooks.io/quescheetah-document/content/Question/index.html
"""
class Questions(View):
    # Make a new Question
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
                api_key_instance = ApiKey.objects.get(key=api_key)
            except ObjectDoesNotExist:
                desc = 'The ApiKey instance does not exist in followed key.'
                return error_return(desc, 404)

            new_question = Question(
                api_key=api_key_instance,
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
                question_instance = Question.objects.get(api_key=api_key_instance, id=new_question.id, is_removed=False)
            except ObjectDoesNotExist:
                desc = 'The Question does not exist in followed api key.'
                return error_return(desc, 404)

            for key, value in answer_data.items():
                answer_text = value.get('answer_text')
                if answer_text:
                    new_answer = Answer(question=question_instance, answer_text=answer_text, answer_num=key)
                    new_answer.save()
                else:
                    pass

            '''
            load data for response json
            '''
            response_dict['questions'].update({
                question_instance.question_num: {
                    'question_id': question_instance.id,
                    'question_title': question_instance.question_title,
                    'question_text': question_instance.question_text,
                    'start_dt': question_instance.start_dt,
                    'end_dt': question_instance.end_dt,
                    'is_editable': question_instance.is_editable,
                    'is_private': question_instance.is_private
                }
            })

            answer_instance_set = question_instance.answers.filter(is_removed=False).order_by('answer_num')
            response_dict['answers'].update({
                question_instance.question_num: {}
            })

            for answer in answer_instance_set:
                response_dict['answers'][question_instance.question_num].update({
                    answer.answer_num: {
                        'answer_text': answer.answer_text,
                    }
                })

            return JsonResponse(response_dict)
        else:
            desc = 'This request url is not authenticated in followed api_key.'
            return error_return(desc, 401)

    # Send a Question data.
    @method_decorator(never_cache)
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
                api_key_instance = ApiKey.objects.get(key=api_key)
                question_instance = Question.objects.get(api_key=api_key_instance, id=question_id, is_removed=False)
            except ObjectDoesNotExist:
                    desc = 'The Question does not exist in followed api_key.'
                    return error_return(desc, 404)

            '''
            load data for response json
            '''
            response_dict['questions'].update({
                question_instance.question_num : {
                    'id': question_instance.id,
                    'question_title': question_instance.question_title,
                    'question_text': question_instance.question_text,
                    'start_dt': question_instance.start_dt,
                    'end_dt': question_instance.end_dt,
                    'is_editable': question_instance.is_editable,
                    'is_private': question_instance.is_private
                }
            })

            answer_instance_set = question_instance.answers.filter(is_removed=False).order_by('answer_num')
            response_dict['answers'].update({
                question_instance.question_num : {}
            })

            for answer in answer_instance_set:
                response_dict['answers'][question_instance.question_num].update({
                    answer.answer_num: {
                        'id': answer.id,
                        'answer_count': answer.get_answer_count,
                        'answer_text': answer.answer_text,
                    }
                })

            return JsonResponse(response_dict)
        else:
            desc = 'This request url is not authenticated in followed api_key.'
            return error_return(desc, 401)

    # Updates a Question.
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
                api_key_instance = ApiKey.objects.get(key=api_key)
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
                    selected_question = Question.objects.get(api_key=api_key_instance, id=question_id, is_removed=False)
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
                    setattr(selected_question, key, update_question_dict[key])
                selected_question.save(is_update=True)

                '''
                update answer instance
                '''
                if data.get('answers').get('1'):
                    for answer_key, answer_value in data.get('answers').get('1').items():
                        answer_text = answer_value.get('answer_text')

                        try:
                            selected_answer = selected_question.answers.get(answer_num=answer_key, is_removed=False)
                        except ObjectDoesNotExist:
                            desc = 'Answer does not exist.'
                            return error_return(desc, 404)

                        if answer_text:
                            update_answer_dict.update({
                                'answer_text': answer_text
                            })

                        for key in update_answer_dict:
                            setattr(selected_answer, key, update_answer_dict[key])
                        selected_answer.save()

            try:
                updated_question = Question.objects.get(api_key=api_key_instance, id=question_id, is_removed=False)
            except ObjectDoesNotExist:
                desc = 'The Question does not exist in followed api key.'
                return error_return(desc, 404)

            response_dict['questions'].update({
                updated_question.question_num: {
                    'question_title': updated_question.question_title,
                    'question_text': updated_question.question_text,
                    'start_dt': updated_question.start_dt,
                    'end_dt': updated_question.end_dt,
                    'is_editable': updated_question.is_editable,
                    'is_private': updated_question.is_private
                }
            })

            answer_updated_set = updated_question.answers.filter(is_removed=False).order_by('answer_num')
            response_dict['answers'].update({
                updated_question.question_num: {}
            })

            for answer in answer_updated_set:
                response_dict['answers'][updated_question.question_num].update({
                    answer.answer_num: {
                        'answer_text': answer.answer_text,
                    }
                })

            return JsonResponse(response_dict)
        else:
            desc = 'This request url is not authenticated in followed api_key.'
            return error_return(desc, 401)

    # Delete a Question and related Answer, Useranswer
    def delete(self, request, question_id):
        if match_domain(request):
            data = json.loads(request.body.decode('utf-8'))
            api_key = get_api_key(request)
            if not api_key:
                desc = "Can't get a valid api key."
                return error_return(desc)

            response_dict = {}

            try:
                api_key_instance = ApiKey.objects.get(key=api_key)
                question_instance = Question.objects.get(api_key=api_key_instance, id=question_id, is_removed=False)

            except ObjectDoesNotExist:
                    desc = 'The Question does not exist in followed api_key.'
                    return error_return(desc, 404)

            answer_instance_set = question_instance.answers.filter(is_removed=False)
            for answer in answer_instance_set:
                if hasattr(answer, 'user_answers'):
                    useranswer_instance_set = answer.user_answers.filter(is_removed=False)
                    for useranswer in useranswer_instance_set:
                        useranswer.is_removed = True
                        useranswer.save()

                answer.is_removed = True
                answer.save()

            question_instance.is_removed = True
            question_instance.save(is_update=True)

            response_dict.update({
                "result": "success",
                "description": "Deleted a question."
            })
            return JsonResponse(response_dict)
        else:
            desc = 'This request url is not authenticated in followed api_key.'
            return error_return(desc, 401)


"""
Sends abridged information about
the question and following answers.
"""
@csrf_exempt
@require_GET
def simple_view_answer(request, question_id):
    if match_domain(request):
        api_key = get_api_key(request)
        if not api_key:
            desc = "Can't get a valid api key."
            return error_return(desc)
        response_dict = {}
        answer_list = []

        try:
            api_key_instance = ApiKey.objects.get(key=api_key)
            question_instance = Question.objects.get(api_key=api_key_instance, id=question_id, is_removed=False)
        except ObjectDoesNotExist:
                desc = 'The Question does not exist in followed api_key.'
                return error_return(desc, 404)

        response_dict.update({
            'id': question_instance.id,
            'question_title': question_instance.question_title,
            'question_text': question_instance.question_text
        })
        answer_instance_set = question_instance.answers.filter(is_removed=False)
        if answer_instance_set:
            for answer in answer_instance_set:
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


# Change question state to private
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
            api_key_instance = ApiKey.objects.get(key=api_key)
            question_instance = Question.objects.get(api_key=api_key_instance, id=question_id, is_removed=False)
        except ObjectDoesNotExist:
            desc = 'The Question does not exist in followed api key.'
            return error_return(desc, 404)

        question_instance.is_private = True
        question_instance.save(is_update=True)
        response_dict.update({
            "result": "success",
            "description": "Switched to the private question."
        })
        return JsonResponse(response_dict)
    else:
        desc = 'This request url is not authenticated in followed api_key.'
        return error_return(desc, 401)



"""
Actions about Answer model.
Answer related data can be requested by 2 format in 'GET' method.
One is specific to the requested answer number,
and the other one is full response that contains all informations.
Correct request format can be accessed in following url.
https://mingkim.gitbooks.io/quescheetah-document/content/Answer/index.html
"""
class Answers(View):
    # Make a new Answer
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
                api_key_instance = ApiKey.objects.get(key=api_key)
                question_instance = Question.objects.get(api_key=api_key_instance, id=question_id, is_removed=False)
            except ObjectDoesNotExist:
                desc = 'The Question does not exist in followed api key.'
                return error_return(desc, 404)

            for key, value in data.get('answers').items():
                answer_text = value.get('answer_text')
                if answer_text:
                    new_answer = Answer(question=question_instance, answer_text=answer_text, answer_num=key)
                    new_answer.save()
                else:
                    pass

            '''
            load data for response json
            '''
            answer_instance_set = question_instance.answers.filter(is_removed=False).order_by('answer_num')

            for answer in answer_instance_set:
                response_dict['answers'].update({
                    answer.answer_num: {
                        'id': answer.id,
                        'answer_text': answer.answer_text,
                        'answer_count': answer.get_answer_count
                    }
                })

            return JsonResponse(response_dict)
        else:
            desc = 'This request url is not authenticated in followed api_key.'
            return error_return(desc, 401)

    # Send a Answer data
    @method_decorator(never_cache)
    def get(self, request, *args, **kwargs):
        question_id=kwargs['question_id']
        answer_num=kwargs.get('answer_num')
        if match_domain(request):
            api_key = get_api_key(request)
            if not api_key:
                desc = "Can't get a valid api key."
                return error_return(desc)

            response_dict = {
                'answers': {}
            }

            """
            case 1.
            logic for get_answer_list
            Send all information
            """
            if not answer_num:
                try:
                    api_key_instance = ApiKey.objects.get(key=api_key)
                    question_instance = Question.objects.get(api_key=api_key_instance, id=question_id, is_removed=False)
                except ObjectDoesNotExist:
                    desc = 'The Question does not exist in followed api key.'
                    return error_return(desc, 404)

                answer_instance_set = question_instance.answers.filter(is_removed=False)
                if answer_instance_set:
                    for answer in answer_instance_set:
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

            """
            case 2.
            logic for get_one_answer
            Send specific one answer_num information.
            """
            if answer_num:
                try:
                    api_key_instance = ApiKey.objects.get(key=api_key)
                    question_instance = Question.objects.get(api_key=api_key_instance, id=question_id, is_removed=False)
                except ObjectDoesNotExist:
                    desc = 'The Question does not exist in followed api key.'
                    return error_return(desc, 404)

                answer_instance_set = question_instance.answers.get(answer_num=answer_num, is_removed=False)
                if answer_instance_set:
                    response_dict['answers'].update({
                        answer_instance_set.answer_num : {}
                    })
                    response_dict['answers'][answer_instance_set.answer_num].update({
                        'id': answer_instance_set.id,
                        'answer_text': answer_instance_set.answer_text,
                        'answer_count': answer_instance_set.get_answer_count
                    })
                else:
                    desc = 'The Answer does not exist.'
                    return error_return(desc, 404)

                return JsonResponse(response_dict)
        else:
            desc = 'This request url is not authenticated in followed api_key.'
            return error_return(desc, 401)

    # Delete a Answer and related Useranswer
    def delete(self, request, question_id, answer_num):
        if match_domain(request):
            api_key = get_api_key(request)
            if not api_key:
                desc = "Can't get a valid api key."
                return error_return(desc)
            response_dict = {}

            try:
                api_key_instance = ApiKey.objects.get(key=api_key)
                question_instance = Question.objects.get(api_key=api_key_instance, id=question_id, is_removed=False)
            except ObjectDoesNotExist:
                    desc = 'The Question does not exist in followed api_key.'
                    return error_return(desc, 404)

            answer_instance_set = question_instance.answers.filter(answer_num=answer_num, is_removed=False)
            for answer in answer_instance_set:
                answer.is_removed = True
                answer.save()

            response_dict.update({
                "result": "success",
                "description": "Deleted this answer."
            })
            return JsonResponse(response_dict)
        else:
            desc = 'This request url is not authenticated in followed api_key.'
            return error_return(desc, 401)

    # Update a Answer data
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
                api_key_instance = ApiKey.objects.get(key=api_key)
                question_instance = Question.objects.get(api_key=api_key_instance, id=question_id, is_removed=False)
            except ObjectDoesNotExist:
                desc = 'The Question does not exist in followed api key.'
                return error_return(desc, 404)

            for key, value in data.get('answers').items():
                updated_answer = Answer.objects.get(question=question_instance, answer_num=key, is_removed=False)
                answer_text = value.get('answer_text')
                if answer_text:
                    updated_answer.answer_text = answer_text
                    updated_answer.save()
                else:
                    pass

            '''
            load data for response json
            '''
            answer_instance_set = question_instance.answers.filter(is_removed=False).order_by('answer_num')

            for answer in answer_instance_set:
                response_dict['answers'].update({
                    answer.answer_num: {
                        'id': answer.id,
                        'answer_text': answer.answer_text,
                        'answer_count': answer.get_answer_count
                    }
                })

            return JsonResponse(response_dict)
        else:
            desc = 'This request url is not authenticated in followed api_key.'
            return error_return(desc, 401)


"""
Actions about Useranswer model.
Useranswer related data can be requested by 3 format in 'GET' method.
One is specific to the requested unique user,
and another one is specific to the one answer.
and the last one is full response that contains all useranswers in the group.
Correct request format can be accessed in following url.
https://mingkim.gitbooks.io/quescheetah-document/content/Useranswer/index.html
"""
class Useranswers(View):
    # Make a new Useranswer
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
                api_key_instance = ApiKey.objects.get(key=api_key)
                question_instance = Question.objects.get(api_key=api_key_instance, id=question_id, is_removed=False)
            except ObjectDoesNotExist:
                desc = 'The Question does not exist in followed api key.'
                return error_return(desc, 404)

            if question_instance.answers:
                try:
                    a = Answer.objects.get(question=question_instance, answer_num=answer_num, is_removed=False)
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

    # Send a Useranswer data
    @method_decorator(never_cache)
    def get(self, request, *args, **kwargs):
        question_id = kwargs.get('question_id')
        unique_user = kwargs.get('unique_user')
        answer_num = kwargs.get('answer_num')
        group_id = kwargs.get('group_id')
        if match_domain(request):
            api_key = get_api_key(request)
            if not api_key:
                desc = "Can't get a valid api key."
                return error_return(desc)

            response_dict = {
                'useranswers': {}
            }

            if not group_id:
                try:
                    api_key_instance = ApiKey.objects.get(key=api_key)
                    question_instance = Question.objects.get(api_key=api_key_instance, id=question_id, is_removed=False)
                except ObjectDoesNotExist:
                    desc = 'The Question does not exist in followed api key.'
                    return error_return(desc, 404)

            """
            case 1.
            get all useranswers of one question.
            """
            if not unique_user and not answer_num and not group_id:
                try:
                    answer_instance_set = Answer.objects.filter(question=question_instance, is_removed=False)
                except ObjectDoesNotExist:
                    desc = 'The Answer does not exist in followed answer_num.'
                    return error_return(desc, 404)

                for answer in answer_instance_set:
                    response_dict['useranswers'].update({
                        answer.answer_num : []
                    })
                    try:
                        useranswer_instance_set = UserAnswer.objects.filter(answer=answer, is_removed=False)
                    except UserAnswer.DoesNotExist:
                        desc = 'No such user answered this question.'
                        return error_return(desc, 404)
                    for useranswer in useranswer_instance_set:
                        response_dict['useranswers'][answer.answer_num].append({
                            "unique_user": useranswer.unique_user,
                            "id": useranswer.id,
                            "created_dt": useranswer.created_dt
                        })
                return JsonResponse(response_dict)

            """
            case 2.
            get all useranswers of one answer
            """
            if answer_num and (not unique_user):
                try:
                    answer_instance = Answer.objects.get(question=question_instance, answer_num=answer_num, is_removed=False)
                except ObjectDoesNotExist:
                    desc = 'The Answer does not exist in followed answer_num.'
                    return error_return(desc, 404)

                response_dict['useranswers'].update({
                    answer_instance.answer_num: []
                })

                try:
                    useranswer_instance_set = UserAnswer.objects.filter(answer=answer_instance, is_removed=False)
                except ObjectDoesNotExist:
                    desc = 'No such user answered this question.'
                    return error_return(desc, 404)

                for useranswer in useranswer_instance_set:
                    response_dict['useranswers'][answer_instance.answer_num].append({
                        "unique_user": useranswer.unique_user,
                        "id": useranswer.id,
                        "created_dt": useranswer.created_dt
                    })
                return JsonResponse(response_dict)

            """
            case 3.
            get one useranswer by unique user name.
            """
            if unique_user:
                try:
                    answer_instance_set = Answer.objects.filter(question=question_instance, is_removed=False)
                except ObjectDoesNotExist:
                    desc = 'The Answer does not exist in followed answer_num.'
                    return error_return(desc, 404)

                try:
                    useranswer_instance = UserAnswer.objects.get(answer__in=answer_instance_set, unique_user=unique_user, is_removed=False)
                except ObjectDoesNotExist:
                    desc = 'No such user answered this question.'
                    return error_return(desc, 404)

                response_dict['useranswers'].update({
                    useranswer_instance.answer.answer_num: {}
                })

                response_dict['useranswers'][useranswer_instance.answer.answer_num].update({
                    "unique_user": useranswer_instance.unique_user,
                    "id": useranswer_instance.id,
                    "created_dt": useranswer_instance.created_dt
                })
                return JsonResponse(response_dict)

            """
            case 4.
            get all useranswers of one group
            """
            if group_id:
                try:
                    question_instance_set = Question.objects.filter(multi_question_id=group_id)
                except ObjectDoesNotExist:
                    desc = 'The question does not exist in followed group_id.'
                    return error_return(desc, 404)

                for question_instance in question_instance_set:
                    response_dict['useranswers'].update({
                            question_instance.question_num : {}
                        })

                    try:
                        answer_instance_set = Answer.objects.filter(question=question_instance, is_removed=False)
                    except ObjectDoesNotExist:
                        continue

                    for answer_instance in answer_instance_set:
                        response_dict['useranswers'][question_instance.question_num].update({
                            answer_instance.answer_num : []
                        })
                        try:
                            useranswer_instance_set = UserAnswer.objects.filter(answer=answer_instance, is_removed=False)
                        except UserAnswer.DoesNotExist:
                            continue

                        for useranswer_instance in useranswer_instance_set:
                            response_dict['useranswers'][question_instance.question_num][answer_instance.answer_num].append({
                                "unique_user": useranswer_instance.unique_user,
                                "id": useranswer_instance.id,
                                "created_dt": useranswer_instance.created_dt
                            })
                return JsonResponse(response_dict)

        else:
            desc = 'This request url is not authenticated in followed api_key.'
            return error_return(desc, 401)

    # Delete a Useranswer
    def delete(self, request, question_id, unique_user):
        if match_domain(request):
            api_key = get_api_key(request)
            if not api_key:
                desc = "Can't get a valid api key."
                return error_return(desc)
            response_dict = {}

            try:
                api_key_instance = ApiKey.objects.get(key=api_key)
                question_instance = Question.objects.get(api_key=api_key_instance, id=question_id, is_removed=False)
            except ObjectDoesNotExist:
                    desc = 'The Question does not exist in followed api_key.'
                    return error_return(desc, 404)

            try:
                answer_instance_set = Answer.objects.filter(question=question_instance, is_removed=False)
                useranswer_instance = UserAnswer.objects.get(answer__in=answer_instance_set, unique_user=unique_user, is_removed=False)
                useranswer_instance.is_removed = True
                useranswer_instance.save()
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

    # Update a Useranswer
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
                api_key_instance = ApiKey.objects.get(key=api_key)
                question_instance = Question.objects.get(api_key=api_key_instance, id=question_id, is_removed=False)
            except ObjectDoesNotExist:
                desc = 'The Question does not exist in followed api_key.'
                return error_return(desc, 404)

            if question_instance.is_editable:
                try:
                    answer_instance_set = Answer.objects.filter(question=question_instance, is_removed=False)
                    useranswer_instance = UserAnswer.objects.get(answer__in=answer_instance_set, unique_user=unique_user, is_removed=False)
                except ObjectDoesNotExist:
                    desc = 'The UserAnswer does not exist in followed unique_user.'
                    return error_return(desc, 404)

                try:
                    new_answer = Answer.objects.get(question=question_instance, answer_num=answer_num, is_removed=False)
                except ObjectDoesNotExist:
                    desc = 'The new Answer instance does not exist in followed unique_user.'
                    return error_return(desc, 404)

                useranswer_instance.answer = new_answer
                useranswer_instance.save()

                response_dict['useranswer'].update({
                    "answer_num": useranswer_instance.answer.answer_num,
                    "unique_user": useranswer_instance.unique_user,
                    "created_dt": useranswer_instance.created_dt,
                    'id': useranswer_instance.id
                })
                return JsonResponse(response_dict)
            else:
                desc = 'Property [is_editable] of this question is currently False. Set True for this request.'
                return error_return(desc)
        else:
            desc = 'This request url is not authenticated in followed api_key.'
            return error_return(desc, 401)

