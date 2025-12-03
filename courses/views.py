from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET, require_POST, \
    require_http_methods

from courses import models
from courses import forms
from courses.signals.custom_signals import course_published


@require_GET
@login_required
def courses(request):
    paginator = Paginator(models.Course.objects.all().order_by('title'), 5)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return render(request, 'course_list.html', {'page_obj': page_object})


@require_GET
@login_required
def course_details(request, course_id):
    # course --> parts ---> topics ---> documents
    course = models.Course.objects.prefetch_related(
        'parts__topics__documents').get(id=course_id)
    return render(request, 'course_details.html', {'course': course})


@require_http_methods(['GET', 'POST'])
@login_required
def create_course(request):
    if request.method == "POST":
        form = forms.CourseForm(request.POST)

        if form.is_valid():
            form.save()

            course_published.send(sender='1', course=form.instance,
                                  user=request.user)
            course_published.send(sender='2')

            return redirect('courses')

    else:
        form = forms.CourseForm()
        return render(request, 'course_form.html', {'form': form})


@require_http_methods(['GET', 'POST'])
@login_required
def update_course(request, course_id):
    course = models.Course.objects.get(id=course_id)

    if request.method == "POST":
        form = forms.CourseForm(request.POST, instance=course)

        if form.is_valid():
            form.save()
            return redirect('course-details', course_id=course.id)
    else:
        form = forms.CourseForm(instance=course)
        return render(request, 'course_form.html',
                      {'form': form, 'course': course})


@require_POST
@login_required
def delete_course(request):
    course_id = request.POST.get('course_id')
    course = models.Course.objects.get(id=course_id)
    course.delete()
    return redirect('courses')


@require_http_methods(['GET', 'POST'])
@login_required
def create_course_part(request, course_id):
    course = models.Course.objects.get(id=course_id)
    if request.method == 'POST':
        form = forms.CoursePartForm(request.POST)
        if form.is_valid():
            course.parts.create(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description']
            )
            return redirect('course-details', course_id=course_id)
        else:
            return render(request, 'course_part_form.html',
                          {'form': form, 'course_id': course_id})
    else:
        form = forms.CoursePartForm()
        return render(request, 'course_part_form.html',
                      {'form': form, 'course_id': course_id})


@require_http_methods(['GET', 'POST'])
@login_required
def update_course_part(request, course_id, part_id):
    part = models.CoursePart.objects.get(id=part_id)
    if request.method == 'POST':
        form = forms.CoursePartForm(request.POST)
        if form.is_valid():
            part.title = form.cleaned_data['title']
            part.description = form.cleaned_data['description']
            part.save()
            return redirect('course-details', course_id=course_id)
        else:
            return render(request, 'course_part_form.html',
                          {'form': form, 'course_id': course_id,
                           'part_id': part_id})
    else:
        form = forms.CoursePartForm(
            initial={'title': part.title, 'description': part.description})
        return render(request, 'course_part_form.html',
                      {'form': form, 'course_id': course_id,
                       'part_id': part_id, 'is_edit': True})


@require_POST
@login_required
def delete_course_part(request, course_id, part_id):
    part = models.CoursePart.objects.get(id=part_id)
    part.delete()
    return redirect('course-details', course_id=course_id)


@require_http_methods(['GET', 'POST'])
@login_required
def create_course_topic(request, course_id, part_id):
    part = models.CoursePart.objects.get(id=part_id)
    if request.method == 'POST':
        form = forms.CourseTopicForm(request.POST)
        if form.is_valid():
            part.topics.create(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description']
            )
            return redirect('course-details', course_id=course_id)
        else:
            return render(request, 'course_topic_form.html',
                          {'form': form, 'course_id': course_id,
                           'part_id': part_id})
    else:
        form = forms.CourseTopicForm()
        return render(request, 'course_topic_form.html',
                      {'form': form, 'course_id': course_id,
                       'part_id': part_id})


@require_http_methods(['GET', 'POST'])
@login_required
def update_course_topic(request, course_id, part_id, topic_id):
    topic = models.CourseTopic.objects.get(id=topic_id)
    if request.method == 'POST':
        form = forms.CourseTopicForm(request.POST)
        if form.is_valid():
            topic.title = form.cleaned_data['title']
            topic.description = form.cleaned_data['description']
            topic.save()
            return redirect('course-details', course_id=course_id)
        else:
            return render(request, 'course_topic_form.html',
                          {'form': form, 'course_id': course_id,
                           'part_id': part_id, 'topic_id': topic_id})
    else:
        form = forms.CourseTopicForm(
            initial={'title': topic.title, 'description': topic.description})
        return render(request, 'course_topic_form.html',
                      {'form': form, 'course_id': course_id,
                       'part_id': part_id, 'topic_id': topic_id,
                       'is_edit': True})


@require_POST
@login_required
def delete_course_topic(request, course_id, part_id, topic_id):
    topic = models.CourseTopic.objects.get(id=topic_id)
    topic.delete()
    return redirect('course-details', course_id=course_id)


@require_http_methods(['GET', 'POST'])
@login_required
def create_topic_document(request, course_id, part_id, topic_id):
    topic = models.CourseTopic.objects.get(id=topic_id)
    if request.method == 'POST':
        form = forms.TopicDocument(request.POST, request.FILES)
        # При создании файл обязателен
        if form.is_valid():
            if not form.cleaned_data.get('file'):
                form.add_error('file',
                               'Файл обязателен при создании документа')
                return render(request, 'topic_document_form.html',
                              {'form': form, 'course_id': course_id,
                               'part_id': part_id, 'topic_id': topic_id})
            topic.documents.create(
                name=form.cleaned_data['name'],
                file=form.cleaned_data['file']
            )
            return redirect('course-details', course_id=course_id)
        else:
            return render(request, 'topic_document_form.html',
                          {'form': form, 'course_id': course_id,
                           'part_id': part_id, 'topic_id': topic_id})
    else:
        form = forms.TopicDocument()
        return render(request, 'topic_document_form.html',
                      {'form': form, 'course_id': course_id,
                       'part_id': part_id, 'topic_id': topic_id})


@require_http_methods(['GET', 'POST'])
@login_required
def update_topic_document(request, course_id, part_id, topic_id, document_id):
    document = models.TopicDocument.objects.get(id=document_id)
    if request.method == 'POST':
        form = forms.TopicDocument(request.POST, request.FILES)
        if form.is_valid():
            document.name = form.cleaned_data['name']
            if form.cleaned_data.get('file'):
                document.file = form.cleaned_data['file']
            document.save()
            return redirect('course-details', course_id=course_id)
        else:
            return render(request, 'topic_document_form.html',
                          {'form': form, 'course_id': course_id,
                           'part_id': part_id, 'topic_id': topic_id,
                           'document_id': document_id, 'document': document,
                           'is_edit': True})
    else:
        form = forms.TopicDocument(initial={'name': document.name})
        return render(request, 'topic_document_form.html',
                      {'form': form, 'course_id': course_id,
                       'part_id': part_id, 'topic_id': topic_id,
                       'document_id': document_id, 'document': document,
                       'is_edit': True})


@require_POST
@login_required
def delete_topic_document(request, course_id, part_id, topic_id, document_id):
    document = models.TopicDocument.objects.get(id=document_id)
    document.delete()
    return redirect('course-details', course_id=course_id)


@require_http_methods(['GET', 'POST'])
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('courses')
    else:
        form = UserCreationForm
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('courses')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('courses')
