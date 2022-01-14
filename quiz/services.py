import json

from .dto import QuizDTO, AnswersDTO, QuestionDTO, ChoiceDTO


class QuizResultService:
    def __init__(self, quiz_dto: QuizDTO, answers_dto: AnswersDTO):
        self.quiz_dto = quiz_dto
        self.answers_dto = answers_dto

    def get_result(self) -> float:
        pass


def get_quiz_data():
    raw_quiz = load_data_quiz_json()
    quiz = parse_quiz(**raw_quiz)
    return quiz


def load_data_quiz_json():
    with open('quiz.json') as quiz_json:
        return json.load(quiz_json)


def parse_quiz(uuid, title, questions):
    return QuizDTO(uuid, title, [parse_question(**raw_question) for raw_question in questions])


def parse_question(uuid, text, choices):
    return QuestionDTO(uuid, text, [parse_choice(**raw_choice) for raw_choice in choices])


def parse_choice(**kwargs):
    return ChoiceDTO(**kwargs)
