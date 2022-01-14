from django.views import generic

from quiz.services import get_quiz_data


class QuizView(generic.ListView):
    template_name = "quiz/index.html"

    def get_queryset(self):
        return get_quiz_data()
