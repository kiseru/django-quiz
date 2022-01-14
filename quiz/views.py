from django.shortcuts import render

from quiz.services import get_quiz_data


def quiz(request):
    parsed_quiz = get_quiz_data()
    return render(request, 'quiz/index.html', context={'quiz': parsed_quiz})
