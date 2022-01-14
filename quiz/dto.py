from typing import NamedTuple


class ChoiceDTO(NamedTuple):
    uuid: str
    text: str
    is_correct: bool


class QuestionDTO(NamedTuple):
    uuid: str
    text: str
    choices: list[ChoiceDTO]


class QuizDTO(NamedTuple):
    uuid: str
    title: str
    questions: list[QuestionDTO]


class AnswerDTO(NamedTuple):
    question_uuid: str
    choices: list[str]


class AnswersDTO(NamedTuple):
    quiz_uuid: str
    answers: list[AnswerDTO]
