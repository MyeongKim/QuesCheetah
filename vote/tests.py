from django.test import TestCase, Client
from main.models import User, Domain, ApiKey

import json

class ApiTestCase(TestCase):
    @classmethod
    def setUp(cls):
        """Make api key for request header"""
        cls.u = User.objects.create(email="test@test.com", username="test")
        cls.u.set_password("123")
        cls.a = ApiKey.objects.generate(cls.u)
        cls.a.secret_key = ApiKey.objects.generate_secret()
        cls.a.save()
        cls.d = Domain.objects.create(domain="127.0.0.1", api_key=cls.a)

        cls.c = Client(HTTP_API_KEY=cls.a.key, HTTP_HOST="127.0.0.1")

    def test_create_group_question(self):
        """Make a new group question"""
        request_json = {
            "group_name": "This Group name",
            "questions": {
                "1": {
                    "question_title": "Yourquestiontitle1",
                    "question_text": "How did this test go?",
                    "start_dt": "",
                    "end_dt": "",
                    "is_editable": False,
                    "is_private": False
                },
                "2": {
                    "question_title": "Yourquestiontitle2",
                    "question_text": "Are you hungry?",
                    "start_dt": "",
                    "end_dt": "",
                    "is_editable": False,
                    "is_private": False
                }
            },
            "answers": {
                "1": {
                    "1": {
                        "answer_text": "Answer 1"
                    },
                    "2": {
                        "answer_text": "Answer 2"
                    },
                },
                "2": {
                    "1": {
                        "answer_text": "Answer 1"
                    },
                    "2": {
                        "answer_text": "Answer 2"
                    },
                },
            }
        }
        response = self.c.post('/v1/groups', json.dumps(request_json), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_create_single_question(self):
        """Make a new question"""
        request_json = {
            "group_name": "",
            "questions": {
                "1": {
                    "question_title": "Yourquestiontitle1",
                    "question_text": "How did this test go?",
                    "start_dt": "",
                    "end_dt": "",
                    "is_editable": False,
                    "is_private": False
                }
            },
            "answers": {
                "1": {
                    "1": {
                        "answer_text": "Answer 1"
                    },
                    "2": {
                        "answer_text": "Answer 2"
                    },
                }
            }
        }
        response = self.c.post('/v1/questions', json.dumps(request_json), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # get question_id to request answer and useranswer
        response_json = json.loads(str(response.content, encoding='utf8'))
        ApiTestCase.qid = response_json['questions']['1']['question_id']

    def test_get_list_of_answers(self):
        """Get answers info from question that we just created"""
        # response = self.c.get('/v1/questions/3/answers')
        # print(response)
        # self.assertEqual(response.status_code, 200)

    def test_get_list_of_useranswers(self):
        """Get useranswer info from question that we just created"""
        # response = self.c.get('/v1/questions/'+str(self.qid)+'/answers/1/useranswers')
        # self.assertEqual(response.status_code, 200)
