from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.views import generic
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Choice, Question
from .forms import QuestionForm, ChoiceForm

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

class PollDetailsPageView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsPageView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

class CreatePageView(generic.ListView):
    model = Question
    template_name = 'polls/create.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

# def poll_create(request):
#     if request.method == "POST":
#         Qform = QuestionForm(request.POST)
#         Cform = ChoiceForm(request.POST)
#         if Qform.is_valid() and Cform.is_valid:
#             question = Qform.save(commit=False)
#             question.author = request.user
#             question.pub_date = timezone.now()
#             question.save()
#             choice = Cform.save(commit=False)
#             choice.author = request.user
#             choice.question = question
#             choice.save()
#             return redirect('polls:detail', pk=question.pk)
#     else:
#         Qform = QuestionForm()
#         Cform = ChoiceForm()
#     return render(request, 'polls/create.html', {'Qform': Qform, 'Cform': Cform})


def poll_create(request):
    if request.method == "POST":
        Qform = QuestionForm(request.POST)
        Cform = [ChoiceForm(request.POST, prefix=str(x)) for x in range(0,3)]
        if Qform.is_valid() and all([x.is_valid for x in Cform]):
            question = Qform.save(commit=False)
            question.author = request.user
            question.pub_date = timezone.now()
            question.save()
            for x in Cform:
                choice = x.save(commit=False)
                choice.author = request.user
                choice.question = question
                choice.save()
                return redirect('polls:detail', pk=question.pk)
    else:
        Qform = QuestionForm()
        Cform = [ChoiceForm(prefix=str(x)) for x in range(0,3)]
    return render(request, 'polls/create.html', {'Qform': Qform, 'Cform': Cform})