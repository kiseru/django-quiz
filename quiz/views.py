from django.http import Http404, HttpRequest
from django.shortcuts import redirect
from django.views.generic import TemplateView

from quiz.services import get_quiz_data


class QuizListView(TemplateView):
    template_name = "quiz/index.html"

    def get_context_data(self, **kwargs):
        return {"quizzes": get_quiz_data()}


def check_is_empty(quizzes):
    if len(quizzes) == 0:
        raise Http404()


class QuizDetailView(TemplateView):
    template_name = "quiz/quiz_detail.html"

    def get_context_data(self, uuid):
        quizzes = get_quiz_data()
        filtered_quizzes = [quiz for quiz in quizzes if quiz.uuid == uuid]
        check_is_empty(quizzes)
        return {
            "quiz": filtered_quizzes[0],
            "question": self.get_question(filtered_quizzes[0]),
        }

    def get_question(self, quiz):
        self.check_has_question_id()
        return quiz.questions[self.request.session["question_index"]]

    def check_has_question_id(self):
        if "question_index" not in self.request.session:
            self.request.session["question_index"] = 0

    def post(self, request, uuid):
        print(request.POST['test'])
        return redirect('quiz_detailed', uuid)
