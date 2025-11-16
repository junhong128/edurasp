from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import Questions
import random

def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def test(request):
    # Get subject from query parameter if it exists
    subject = request.GET.get('subject', None)
    grade = 7  # Always set to grade 7

    if subject:
        # Get 10 random questions for the selected subject and grade
        questions = list(Questions.objects.filter(subject=subject, grade=grade))

        if questions:
            # Store question IDs in session for looping
            question_ids = [q.id for q in questions[:10]]
            request.session['question_ids'] = question_ids
            request.session['current_index'] = 0
            request.session['answered_questions'] = []  # Track answered questions
            request.session['subject'] = subject
            request.session['grade'] = grade

            # Get the first question
            current_question = questions[0]
            context = {
                'question': current_question,
                'subject': subject,
                'grade': grade,
                'question_number': 1,
                'total_questions': min(len(questions), 10)
            }
            template = loader.get_template('practice.html')
            return HttpResponse(template.render(context, request))

    # Show subject selection page
    # Get unique subjects from database for grade 7
    subjects = Questions.objects.filter(grade=7).values_list('subject', flat=True).distinct()

    context = {
        'subjects': subjects,
        'show_selection': True
    }
    template = loader.get_template('practice.html')
    return HttpResponse(template.render(context, request))

def check_answer(request):
    """API endpoint to check if the selected answer is correct"""
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        selected_answer = data.get('answer')

        question_ids = request.session.get('question_ids', [])
        current_index = request.session.get('current_index', 0)

        if question_ids:
            # Get the current question
            question = Questions.objects.get(id=question_ids[current_index])
            correct_answer = question.correctAnswer

            is_correct = (selected_answer == correct_answer)

            return JsonResponse({
                'success': True,
                'is_correct': is_correct,
                'correct_answer': correct_answer,
                'explanation': question.explanation
            })

    return JsonResponse({'success': False, 'error': 'Invalid request'})

def next_question(request):
    """API endpoint to get the next question in the loop"""
    if request.method == 'POST':
        question_ids = request.session.get('question_ids', [])
        current_index = request.session.get('current_index', 0)
        answered_questions = request.session.get('answered_questions', [])

        if question_ids:
            # Mark current question as answered
            if current_index not in answered_questions:
                answered_questions.append(current_index)
                request.session['answered_questions'] = answered_questions

            # Check if all questions have been answered
            if len(answered_questions) >= len(question_ids):
                # All questions completed, signal to redirect
                return JsonResponse({
                    'success': True,
                    'completed': True,
                    'redirect_url': '/practice/'
                })

            # Move to next question
            current_index = (current_index + 1) % len(question_ids)
            request.session['current_index'] = current_index

            # Get the question
            question = Questions.objects.get(id=question_ids[current_index])

            return JsonResponse({
                'success': True,
                'completed': False,
                'question': {
                    'text': question.questionText,
                    'optionA': question.optionA,
                    'optionB': question.optionB,
                    'optionC': question.optionC,
                    'optionD': question.optionD,
                },
                'question_number': current_index + 1,
                'total_questions': len(question_ids)
            })

    return JsonResponse({'success': False, 'error': 'Invalid request'})