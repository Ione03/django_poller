from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from itertools import chain
from .models import Question, Category, UserAnswer, Answer
from .tools.helper import get_questions, generate_safe_forms


class FormTestCase(TestCase):

    def setUp(self):
        c1 = Category.objects.create(name='Default')
        c2 = Category.objects.create(name='limit2', display_all=False,
            display_factor=2)
        q1 = Question.objects.create(question='Test1', is_active=True,
            category=c1, required=True)
        q2 = Question.objects.create(question='Test2', is_active=True,
            category=c2, required=True)
        Question.objects.create(question='Test3', is_active=True, category=
            c2, required=True)
        Question.objects.create(question='Test4', is_active=True, category=
            c2, required=True)
        UserAnswer.objects.create(question=q2, answer='Test answer')
        self.factory = RequestFactory()

    def test_form_creation(self):
        client = Client()
        response = client.get(reverse('poll'))
        self.assertEqual(response.status_code, 200, msg='Response error poll')

    def test_question_limitation(self):
        ques = Question.objects.filter(is_active=True).order_by('count')
        questions = get_questions()
        questions = list(chain(questions))
        pre_def = list(chain(ques.filter(question='Test1'), ques.filter(
            question='Test2'), ques.filter(question='Test3')))
        self.assertEqual(questions, pre_def, msg='Generator error')

    def test_json_response(self):
        client = Client()
        response = client.get(reverse('get_data'))
        self.assertEqual(response.status_code, 200, msg=
            'Request error get_data')

    def test_empty_json_response(self):
        client = Client()
        response = client.get(reverse('get_data'))
        question = response.get('question')
        x = response.get('_x')
        y = response.get('_y')
        self.assertEqual(question, None, msg=
            'Response error JSON obj question wrong')
        self.assertEqual(x, None, msg='Response error JSON obj x wrong')
        self.assertEqual(y, None, msg='Response error JSON obj y wrong')

    def test_filled_json_response(self):
        client = Client()
        question = Question.objects.get(question='Test1')
        response = client.get(path=reverse('get_data'), data={'id':
            question.pk})
        ua = UserAnswer.objects.filter(question=question)
        x = list()
        y = list()
        for t in ua:
            x.append(t.answer)
            y.append(str(round(ua.filter(answer=t).count() / ua.count(),
                ndigits=2) * 100))
        data = {'_x': x, '_y': y, 'question': question.question}
        self.assertJSONEqual(str(response.content, encoding='utf8'),
            expected_data=data, msg=
            'Response error get_data wrong created JSON obj')


class PollTestCase(TestCase):

    def setUp(self):
        c = Category.objects.create(name='Default')
        a1 = Answer.objects.create(answer='predefined 1')
        a2 = Answer.objects.create(answer='predefined 2')
        q2 = Question.objects.create(question='Test2', is_active=True,
            category=c, required=True, type=Question.QUESTION_TYPE_SINGLE)
        q3 = Question.objects.create(question='Test3', is_active=True,
            category=c, required=False)
        q3.answers.set([a1])
        q2.answers.set([a1, a2])
        UserAnswer.objects.create(question=q2, answer=a1)
        UserAnswer.objects.create(question=q2, answer=[a1, a2])

    def test_objects(self):
        question = Question.objects.get(question='Test3')
        answer = Answer.objects.filter(answer='predefined 1')
        answers = question.get_answers()
        self.assertEqual(answers[0], answer[0])
