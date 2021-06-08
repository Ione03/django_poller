from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from .models import UserAnswer, Question, Answer
from .tools.helper import get_questions, generate_safe_forms
from django.utils.translation import ugettext_lazy as _
from .utils import get_ip


def poll_over(request):
    raise Http404('Umfrage nicht gefunden')


def poll_index(request):
    questions = get_questions()
    if request.method == 'POST':
        forms = generate_safe_forms(questions, request)
        if not forms.is_valid():
            return render(request, 'polls.html', {'questions': questions,
                'form': forms, 'invalid': True})
        else:
            q = 0
            ip = get_ip(request)
            domain = request.get_host()
            for i in questions:
                try:
                    current_question = i
                    current_answer = forms.cleaned_data['answer' + str(q + 1)]
                    if current_question.type == Question.QUESTION_TYPE_TEXT:
                        obj, created = UserAnswer.objects.get_or_create(
                            question=current_question, ip=ip, domain=domain,
                            defaults={'answer': current_answer})
                    else:
                        try:
                            if len(current_answer) > 1:
                                for j in range(len(current_answer)):
                                    a, created = (UserAnswer.objects.
                                        get_or_create(question=
                                        current_question, ip=ip, domain=
                                        domain, defaults={'answer':
                                        current_answer[j].answer}))
                                    if created:
                                        current_question = (Question.objects.
                                            get(pk=current_question.pk))
                                        current_question.count += 1
                                        current_question.save()
                        except TypeError:
                            a, created = UserAnswer.objects.get_or_create(
                                question=current_question, ip=ip, domain=
                                domain, defaults={'answer': current_answer})
                            if created:
                                current_question = Question.objects.get(pk=
                                    current_question.pk)
                                current_question.count += 1
                                current_question.save()
                except MultiValueDictKeyError:
                    print('not saved')
                q += 1
        messages.success(request, _('Thanks for your participation'))
        return render(request, 'polls.html', {'questions': questions})
    else:
        forms = generate_safe_forms(questions, request)
    return render(request, 'polls.html', {'questions': questions, 'form':
        forms})


def statistics(request):
    questions = Question.objects.filter(is_active=True)
    answers = UserAnswer.objects.all().values('answer')
    q_a = list()
    for i in range(questions.count()):
        pre = list()
        v = answers.filter(question=questions[i])
        pre.append(questions[i])
        pre.append(v)
        pre.append(v.count())
        q_a.append(pre)
    content = {'questions': questions, 'answers': answers, 'q_a': q_a}
    return render(request, 'poll/statistics.html', context=content)


def get_data(request):
    id = request.GET.get('id', None)
    data = {}
    if id:
        question = Question.objects.get(pk=id).question
        answers = UserAnswer.objects.filter(question__id=id)
        x = list()
        y = list()
        for t in answers:
            x.append(t.answer)
            y.append(str(round(answers.filter(answer=t).count() / answers.
                count(), ndigits=2) * 100))
        data = {'_x': x, '_y': y, 'question': question}
    return JsonResponse(data)
