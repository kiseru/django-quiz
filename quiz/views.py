from django.views.generic import TemplateView

from quiz.services import get_quiz_data


class QuizListView(TemplateView):
    template_name = "quiz/index.html"

    def get_context_data(self, **kwargs):
        return {"quizzes": get_quiz_data()}
