from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import TemplateView

from quiz.dto import AnswersDTO, AnswerDTO
from quiz.services import get_quiz_data, QuizResultService, get_quiz

ANSWERS_KEY = "answers"
QUESTION_INDEX_KEY = "question_index"


class QuizListView(TemplateView):
    template_name = "quiz/index.html"

    def get_context_data(self, **kwargs):
        return {"quizzes": get_quiz_data()}


def check_is_empty(quizzes):
    if len(quizzes) == 0:
        raise Http404()


class QuizDetailView(TemplateView):
    template_name = "quiz/quiz_detail.html"

    def get(self, request, *args, **kwargs):
        quiz = get_quiz(kwargs["uuid"])
        if self.request.session[QUESTION_INDEX_KEY] >= len(quiz.questions):
            return redirect("quiz_result", kwargs["uuid"])
        return self.render_to_response({
            "quiz": quiz,
            "question": self.get_question(quiz),
        })

    def get_question(self, quiz):
        self.check_has_question_id()
        return quiz.questions[self.request.session[QUESTION_INDEX_KEY]]

    def check_has_question_id(self):
        if QUESTION_INDEX_KEY not in self.request.session:
            self.request.session[QUESTION_INDEX_KEY] = 0

    def post(self, request, uuid):
        question_uuid = request.POST["question_uuid"]
        answers = request.POST.getlist("answers")
        if len(answers) == 0:
            return redirect('quiz_detailed', uuid)
        self.check_session_has_answers()
        self.update_answers_storage(question_uuid, {"question_uuid": question_uuid, "answers": answers})
        return redirect('quiz_detailed', uuid)

    def check_session_has_answers(self):
        if ANSWERS_KEY not in self.request.session:
            self.request.session[ANSWERS_KEY] = []

    def update_answers_storage(self, question_uuid, answer):
        answers = [answer for answer in self.request.session[ANSWERS_KEY] if answer["question_uuid"] != question_uuid]
        answers.append(answer)
        self.request.session[ANSWERS_KEY] = answers
        self.request.session[QUESTION_INDEX_KEY] += 1


class QuizResultView(TemplateView):
    template_name = "quiz/quiz_result.html"

    def get(self, request, *args, **kwargs):
        answers = [AnswerDTO(answer["question_uuid"], answer["answers"]) for answer in request.session[ANSWERS_KEY]]
        quiz = get_quiz(kwargs["uuid"])
        if len(self.request.session[ANSWERS_KEY]) != len(quiz.questions):
            return redirect("quiz_detailed", kwargs["uuid"])
        result = QuizResultService(quiz, AnswersDTO(quiz.uuid, answers)).get_result()
        self.clear_session()
        return self.render_to_response({
            "result": int(result * 100),
            "quiz_name": quiz.title,
        })

    def clear_session(self):
        self.request.session[QUESTION_INDEX_KEY] = 0
        self.request.session[ANSWERS_KEY] = []
