from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from api.models import *
from faculty.forms import ClassForm, SurveyQuestionForm, SurveyForm, ClassEnrollmentForm
from django.db.utils import IntegrityError
from django.contrib.admin.views.decorators import staff_member_required


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/accounts/login')
def dashboard(request):
    classes = Class.objects.filter(admin=request.user)
    students = Student.objects.filter()
    students_enrolled = ClassEnrollment.objects.get_queryset()
    return render(request, 'faculty/dashboard.html',
                  {'students_enrolled': students_enrolled, 'students': students, 'classes': classes,
                   'class_form': ClassForm(), 'student_form': ClassEnrollmentForm()})


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/accounts/login')
def student_view_table(request, class_id):
    current_class = Class.objects.filter(id=class_id)
    students = current_class.classenrollment_set.all()
    students_enrolled = ClassEnrollment.student.get_object(
        instance=ClassEnrollment.objects.get(class_enrolled=class_id))
    return render(request, 'faculty/student_view_table.html',
                  {'class': current_class, 'students': students, 'students_enrolled': students_enrolled})


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/accounts/login')
def positions_dashboard(request):
    positions = Position.objects.filter()
    return render(request, 'faculty/positions_dashboard.html', {'positions': positions})


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/accounts/login')
def survey_dashboard(request):
    responses = SurveyResponse.objects.filter()
    surveys = Survey.objects.filter(admin=request.user)
    questions = SurveyQuestion.objects.filter()
    if 'survey' in request.GET:
        survey_form = SurveyForm(request.user.id, instance=Survey.objects.get(id=request.GET['survey']))
    else:
        survey_form = SurveyForm(request.user.id, initial={'admin': request.user})

    return render(request, 'faculty/survey_dashboard.html',
                  {'responses': responses, 'questions': questions, 'surveys': surveys, 'survey_form': survey_form,
                   'survey_question_form': SurveyQuestionForm()})


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/accounts/login')
def survey_questions(request, survey_id):
    questions = SurveyQuestion.objects.filter()
    survey = Survey.objects.get(id=survey_id)
    survey_for_class = survey.associated_class.objects.all()
    return_data = {'survey': survey, 'survey_for_class': survey_for_class, 'questions': questions}

    if 'error' in request.GET:
        return_data['error_message'] = request.GET['error']
    return render(request, 'faculty/survey_questions.html', return_data)


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/accounts/login')
def survey_responses(request, survey_id):
    responses = SurveyResponse.objects.filter()
    survey = Survey.objects.get(id=survey_id)
    survey_for_class = survey.associated_class.objects.all()
    return_data = {'survey': survey, 'survey_for_class': survey_for_class, 'responses': responses}

    if 'error' in request.GET:
        return_data['error_message'] = request.GET['error']
    return render(request, 'faculty/survey_responses.html', return_data)


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/accounts/login')
def feedback(request):
    feed = Feedback.objects.filter()
    return render(request, 'faculty/feedback.html', {'feed': feed})


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/accounts/login')
def register(request):
    return render(request, 'faculty/register.html')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/accounts/login')
def forgot_password(request):
    return render(request, 'faculty/forgot_password.html')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/accounts/login')
def class_overview(request, class_id):
    classes = Class.objects.filter(id=class_id)
    return_data = {'classes': classes}

    if 'error' in request.GET:
        return_data['error_message'] = request.GET['error']

    return render(request, 'faculty/dashboard.html', return_data)


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/accounts/login')
def class_edit(request, class_id):
    current_class = Class.objects.get(id=class_id)
    class_form = ClassForm(instance=current_class)
    return render(request, 'faculty/class_edit_form.html', {'class_form': class_form, 'class': current_class})


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/accounts/login')
def class_remove(request, class_id):
    current_class = Class.objects.get(id=class_id)
    current_class.delete()
    return redirect('dashboard')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/accounts/login')
def class_create(request):
    return render(request, 'faculty/dashboard.html', {'form': ClassForm()})


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/accounts/login')
def survey_question_create(request):
    return render(request, 'faculty/survey_dashboard.html', {'survey_form': SurveyQuestionForm()})


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/accounts/login')
def student_enrollment_create(request):
    return render(request, 'faculty/dashboard.html', {'student_form': ClassEnrollmentForm()})


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/accounts/login')
def survey_save_form(request):
    if 'survey' in request.GET:
        survey_form = SurveyForm(request.user.id, request.POST, instance=Survey.objects.get(id=request.GET['survey']))
    else:
        survey_form = SurveyForm(request.user.id, request.POST)

    if not survey_form.is_valid():
        print(survey_form.errors)

    current_survey = survey_form.save(commit=False)
    current_survey.admin = request.user

    try:
        current_survey.save()
        survey_form.save_m2m()
    except IntegrityError:
        return redirect('survey_dashboard')

    return redirect('survey_dashboard')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/accounts/login')
def enrollment_save_form(request):
    if 'class' in request.GET:
        student_form = ClassEnrollmentForm(request.POST, instance=ClassEnrollment.objects.get(id=request.GET['class']))
    else:
        student_form = ClassEnrollmentForm(request.POST)

    if not student_form.is_valid():
        print(student_form.errors)

    current_enrollment = student_form.save(commit=False)
    current_enrollment.admin = request.user

    current_enrollment.save()
    student_form.save_m2m()

    return redirect('dashboard')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/accounts/login')
def class_save_form(request):
    if 'class' in request.GET:
        class_form = ClassForm(request.POST, instance=Class.objects.get(id=request.GET['class']))
    else:
        class_form = ClassForm(request.POST)

    current_class = class_form.save(commit=False)
    current_class.admin = request.user

    if current_class.start_time > current_class.end_time:
        return redirect('dashboard?%s' % 'error=Start time after end time')

    current_class.save()
    class_form.save_m2m()

    return redirect('dashboard')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/accounts/login')
def question_save_form(request):
    if 'survey' in request.GET:
        survey_form = SurveyQuestionForm(request.POST, instance=SurveyQuestion.objects.get(id=request.GET['survey']))
    else:
        survey_form = SurveyQuestionForm(request.POST)

    if not survey_form.is_valid():
        print(survey_form.errors)

    current_survey = survey_form.save(commit=False)
    current_survey.admin = request.user

    current_survey.save()
    survey_form.save_m2m()

    return redirect('survey_dashboard')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/accounts/login')
def question_form(request):
    if 'survey' in request.GET:
        survey_question_form = SurveyQuestionForm(instance=SurveyQuestion.objects.get(id=request.GET['survey']))
    else:
        survey_question_form = SurveyQuestionForm()
    return render(request, 'faculty/survey_question_form.html', {'survey_question_form': survey_question_form})


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/accounts/login')
def add_students_specific_class(request, class_id, first_name, last_name):
    try:
        current_class = Class.objects.get(id=class_id)
        add_student = ClassEnrollment.objects.get(student__user__first_name=first_name,
                                                  student__user__last_name=last_name)
        current_class.classenrollment_set.add(add_student)

        return redirect('/faculty/' + str(class_id) + '/view_student')
    except ClassEnrollment.DoesNotExist:
        return redirect('/faculty/' + str(
            class_id) + '/view_student?%s' % 'error=Student does not exist: ' + first_name + ' ' + last_name)


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/accounts/login')
def class_view(request, class_id):
    current_class = Class.objects.get(id=class_id)
    students = current_class.classenrollment_set.all()
    return_data = {'class': current_class, 'students': students}
    return render(request, 'faculty/student_view_table.html', return_data)


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/accounts/login')
def questions_view(request, survey_id):
    question_object = SurveyQuestion.objects.filter(survey_id=survey_id)
    questions = question_object.all()
    return_data = {'questions': questions}
    return render(request, 'faculty/survey_questions.html', return_data)


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/accounts/login')
def responses_view(request, survey_id):
    survey_instances = SurveyInstance.objects.filter(survey=survey_id)
    survey_entry_instances = []
    for survey_instance in survey_instances:
        survey_entry_instances.extend([x for x in SurveyEntryInstance.objects.filter(survey_instance=survey_instance)])

    responses = []
    for survey_entry_instance in survey_entry_instances:
        responses.extend([x for x in SurveyResponse.objects.filter(survey_entry=survey_entry_instance)])

    question_responses = []
    for response in responses:
        try:
            test_survey_entry = SurveyQuestionInstance.objects.get(id=response.survey_entry.id)
            response.prompt = test_survey_entry.question.prompt_text
            question_responses.append(response)
        except SurveyQuestionInstance.DoesNotExist:
            pass

    return_data = {'responses': question_responses}
    return render(request, 'faculty/survey_responses.html', return_data)


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/accounts/login')
def add_survey_question(request, survey_id):
    survey = Survey.objects.get(survey_id=survey_id)
    add_question = SurveyQuestion.objects.get(survey_id=survey_id)
    survey.associated_class.add(add_question)
    return redirect('/faculty/' + str(survey_id) + '/view_survey')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/accounts/login')
def survey_view(request, survey_id):
    survey = Survey.objects.get(id=survey_id)
    survey_for_class = survey.associated_class.objects.all()
    return_data = {'survey': survey, 'survey_for_class': survey_for_class}

    if 'error' in request.GET:
        return_data['error_message'] = request.GET['error']

    return render(request, 'faculty/survey_dashboard.html', return_data)


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/accounts/login')
def student_view_form(request):
    if 'student' in request.GET:
        student_form = ClassEnrollmentForm(instance=ClassEnrollment.objects.get(id=request.GET['student']))
    else:
        student_form = ClassEnrollmentForm()
    return render(request, 'faculty/student_enrollment_form.html', {'student_form': student_form})


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/accounts/login')
def class_remove_student(request, class_id):
    remove_student = ClassEnrollment.objects.get(class_enrolled=class_id)
    remove_student.delete()
    return redirect('/faculty/' + str(class_id) + '/view_student')
