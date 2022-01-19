import json

from .dto import QuizDTO, AnswersDTO, QuestionDTO, ChoiceDTO

quiz_memorization: list[QuizDTO] | None = None


class QuizResultService:
    def __init__(self, quiz_dto: QuizDTO, answers_dto: AnswersDTO):
        self.quiz_dto = quiz_dto
        self.answers_dto = answers_dto

    def get_result(self) -> float:
        questions_count = len(self.quiz_dto.questions)
        right_answers_count = 0
        for question in self.quiz_dto.questions:
            for answer in self.answers_dto.answers:
                if answer.question_uuid == question.uuid:
                    flag = True
                    for choice_uuid in answer.choices:
                        for choice in question.choices:
                            if flag and choice.uuid == choice_uuid and not choice.is_correct:
                                flag = False
                    if flag:
                        right_answers_count += 1
        return right_answers_count / questions_count


def get_quiz(uuid: str) -> QuizDTO:
    quizzes = get_quiz_data()
    filtered_quizzes = [quiz for quiz in quizzes if quiz.uuid == uuid]
    return filtered_quizzes[0]


def get_quiz_data() -> list[QuizDTO]:
    load_data_if_not_loaded()
    return quiz_memorization


def load_data_if_not_loaded():
    if quiz_memorization is None:
        load_data_quiz_json()


def load_data_quiz_json():
    with open('quiz.json', encoding="utf-8") as quiz_json:
        global quiz_memorization
        quiz_memorization = [parse_quiz(**raw_quiz) for raw_quiz in json.load(quiz_json)]


def parse_quiz(uuid, title, questions):
    return QuizDTO(uuid, title, [parse_question(**raw_question) for raw_question in questions])


def parse_question(uuid, text, choices):
    return QuestionDTO(uuid, text, [parse_choice(**raw_choice) for raw_choice in choices])


def parse_choice(**kwargs):
    return ChoiceDTO(**kwargs)
