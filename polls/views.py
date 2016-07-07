from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.views import generic
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from .models import Choice, Question


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

class test(generic.ListView):
    model = Question
    template_name = 'polls/test.html'

class test2(generic.ListView):
    model = Question
    template_name = 'polls/your-name.html'

# def hello(request):
#     return HttpResponse("Hello world")


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


# def InputCreation(request, question_id):
#     questionTitle = models.CharField(max_length=200)
#     # question = get_object_or_404(Question, pk=question_id)
#     # return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))