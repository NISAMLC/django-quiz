
# View for Homepage
from django.shortcuts import render
from .models import QuizSet


def home(request):
    quiz_sets = QuizSet.objects.all()
    return render(request, 'quiz/home.html', {'quiz_sets': quiz_sets})


#view for questions
from django.shortcuts import render, get_object_or_404,redirect
from .models import QuizSet, Question
from django.urls import reverse
#
#
# def start_quiz(request, quiz_id):
#     quiz_set = get_object_or_404(QuizSet, id=quiz_id)
#     questions = quiz_set.questions.all()  # get all questions for that quiz set
#
#     # Get current question index from URL (or default to 0)
#     question_index = int(request.GET.get('q', 0))
#
#     # If index is out of range, quiz is over
#     if question_index >= len(questions):
#         score = request.session.get('score', 0)
#         total = len(questions)
#         # Clear score for next attempt
#         request.session['score'] = 0
#         return render(request, 'quiz/quiz_result.html', {
#             'quiz_set': quiz_set,
#             'score': score,
#             'total': total
#         })
#
#     # Get current question
#     question = questions[question_index]
#
#     # Check if an answer was submitted
#     if request.method == 'POST':
#         selected_option = int(request.POST.get('option'))
#         correct_option = question.correct_option
#
#         # Initialize score in session
#         if 'score' not in request.session:
#             request.session['score'] = 0
#
#         # Update score if correct
#         if selected_option == correct_option:
#             request.session['score'] += 1
#
#         # Redirect to next question
#         next_question = question_index + 1
#         quiz_url = reverse('start_quiz', args=[quiz_id])
#         return redirect(f"{quiz_url}?q={next_question}")
#
#     return render(request, 'quiz/quiz_question.html', {
#         'quiz_set': quiz_set,
#         'question': question,
#         'question_index': question_index,
#         'total_questions': len(questions),
#     })


def start_quiz(request, quiz_id):
    quiz_set = get_object_or_404(QuizSet, id=quiz_id)
    questions = quiz_set.questions.all()

    # Get current question index from query param
    question_index = int(request.GET.get('q', 0))

    # Initialize session data if not already set
    if 'score' not in request.session:
        request.session['score'] = 0
        request.session['answers'] = []  # store user answers

    # If quiz is finished
    if question_index >= len(questions):
        score = request.session.get('score', 0)
        user_answers = request.session.get('answers', [])
        total = len(questions)

        # Clear session for next attempt
        request.session['score'] = 0
        request.session['answers'] = []

        # Combine questions, user answers, and correctness
        results = []
        for idx, question in enumerate(questions):
            user_answer = user_answers[idx]
            results.append({
                'question': question,
                'user_answer': user_answer,
                'is_correct': (user_answer == question.correct_option)
            })

        return render(request, 'quiz/quiz_result.html', {
            'quiz_set': quiz_set,
            'score': score,
            'total': total,
            'results': results
        })

    # Get current question
    question = questions[question_index]

    # If user submitted an answer
    if request.method == 'POST':
        selected_option = int(request.POST.get('option'))
        correct_option = question.correct_option

        # Update score
        if selected_option == correct_option:
            request.session['score'] += 1

        # Save answer
        answers = request.session.get('answers', [])
        answers.append(selected_option)
        request.session['answers'] = answers

        # Redirect to next question
        next_question = question_index + 1
        quiz_url = reverse('start_quiz', args=[quiz_id])
        return redirect(f"{quiz_url}?q={next_question}")

    return render(request, 'quiz/quiz_question.html', {
        'quiz_set': quiz_set,
        'question': question,
        'question_index': question_index,
        'total_questions': len(questions),
    })