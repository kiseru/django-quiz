from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import TemplateView

from quiz.dto import AnswersDTO, AnswerDTO
from quiz.services import get_quiz_data, QuizResultService

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
        quizzes = get_quiz_data()
        filtered_quizzes = [quiz for quiz in quizzes if quiz.uuid == kwargs["uuid"]]
        quiz = filtered_quizzes[0]
        if self.request.session[QUESTION_INDEX_KEY] >= len(quiz.questions):
            return redirect("quiz_result", kwargs["uuid"])
        check_is_empty(quizzes)
        question = self.get_question(quiz)
        context = {
            "quiz": quiz,
            "question": question,
        }
        return self.render_to_response(context)

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

        if ANSWERS_KEY not in self.request.session:
            self.request.session[ANSWERS_KEY] = []

        new_answer = {
            "question_uuid": question_uuid,
            "answers": answers,
        }
        answers = [answer for answer in self.request.session[ANSWERS_KEY] if answer["question_uuid"] != question_uuid]
        answers.append(new_answer)
        self.request.session[ANSWERS_KEY] = answers
        self.request.session[QUESTION_INDEX_KEY] += 1
        return redirect('quiz_detailed', uuid)


class QuizResultView(TemplateView):
    template_name = "quiz/quiz_result.html"

    def get(self, request, *args, **kwargs):
        answers = [AnswerDTO(answer["question_uuid"], answer["answers"]) for answer in request.session[ANSWERS_KEY]]
        quizzes = get_quiz_data()
        filtered_quizzes = [quiz for quiz in quizzes if quiz.uuid == kwargs["uuid"]]
        quiz = filtered_quizzes[0]
        if len(self.request.session[ANSWERS_KEY]) != len(quiz.questions):
            return redirect("quiz_detailed", kwargs["uuid"])
        answers = AnswersDTO(quiz.uuid, answers)
        quiz_result_service = QuizResultService(quiz, answers)
        result = quiz_result_service.get_result()
        self.request.session[QUESTION_INDEX_KEY] = 0
        self.request.session[ANSWERS_KEY] = []
        return self.render_to_response({
            "result": int(result * 100),
            "quiz_name": quiz.title,
        })
