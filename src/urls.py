"""
URL configuration for src project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from courses import views
from src import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.courses, name='courses'),
    path('create-course', views.create_course, name='create-course'),
    path('course_details/<int:course_id>', views.course_details, name='course-details'),
    path('update-course/<int:course_id>', views.update_course, name='update-course'),
    path('delete-course', views.delete_course, name='delete-course'),
    path('create/<int:course_id>/part/<int:part_id>/create-topic', views.create_course_topic, name='create-course-topic'),
    path('course/<int:course_id>/part/<int:part_id>/topic/<int:topic_id>/update', views.update_course_topic, name='update-course-topic'),
    path('course/<int:course_id>/part/<int:part_id>/topic/<int:topic_id>/delete', views.delete_course_topic, name='delete-course-topic'),
    path('course/<int:course_id>/create-part', views.create_course_part, name='create-course-part'),
    path('course/<int:course_id>/part/<int:part_id>/update', views.update_course_part, name='update-course-part'),
    path('course/<int:course_id>/part/<int:part_id>/delete', views.delete_course_part, name='delete-course-part'),
    path('course/<int:course_id>/part/<int:part_id>/topic/<int:topic_id>/create-document', views.create_topic_document, name='create-topic-document'),
    path('course/<int:course_id>/part/<int:part_id>/topic/<int:topic_id>/document/<int:document_id>/update', views.update_topic_document, name='update-topic-document'),
    path('course/<int:course_id>/part/<int:part_id>/topic/<int:topic_id>/document/<int:document_id>/delete', views.delete_topic_document, name='delete-topic-document'),

    # registration
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
