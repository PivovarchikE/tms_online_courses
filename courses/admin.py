from django.contrib import admin
from courses import models
from django.utils.html import format_html


class TopicDocumentInline(admin.StackedInline):
    model = models.TopicDocument
    extra = 1
    fields = ('name', 'file', 'deleted_at')
    readonly_fields = ('created_at', 'updated_at')


class CourseTopicInline(admin.StackedInline):
    model = models.CourseTopic
    extra = 1
    fields = ('title', 'description', 'deleted_at')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [TopicDocumentInline]


class CoursePartInline(admin.StackedInline):
    model = models.CoursePart
    extra = 1
    fields = ('title', 'description', 'deleted_at')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [CourseTopicInline]


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at', 'parts_count')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'description')
    fields = ('title', 'description', 'deleted_at', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [CoursePartInline]

    def parts_count(self, obj):
        return obj.parts.count()

    parts_count.short_description = 'Количество частей'


@admin.register(models.CoursePart)
class CoursePartAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'created_at', 'topics_count')
    list_filter = ('course', 'created_at')
    search_fields = ('title', 'description', 'course__title')
    fields = ('course', 'title', 'description', 'deleted_at', 'created_at',
              'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [CourseTopicInline]

    def topics_count(self, obj):
        return obj.topics.count()

    topics_count.short_description = 'Количество тем'


@admin.register(models.CourseTopic)
class CourseTopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'part', 'course', 'created_at', 'documents_count')
    list_filter = ('part__course', 'created_at')
    search_fields = ('title', 'description', 'part__title',
                     'part__course__title')
    fields = ('part', 'title', 'description', 'deleted_at', 'created_at',
              'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [TopicDocumentInline]

    def course(self, obj):
        return obj.part.course

    course.short_description = 'Курс'

    def documents_count(self, obj):
        return obj.documents.count()

    documents_count.short_description = 'Количество документов'


@admin.register(models.TopicDocument)
class TopicDocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'topic', 'part', 'course', 'created_at',
                    'file_link')
    list_filter = ('topic__part__course', 'created_at')
    search_fields = ('name', 'topic__title', 'topic__part__title',
                     'topic__part__course__title')
    fields = ('topic', 'name', 'file', 'deleted_at', 'created_at',
              'updated_at')
    readonly_fields = ('created_at', 'updated_at', 'file_link')

    def part(self, obj):
        return obj.topic.part

    part.short_description = 'Часть'

    def course(self, obj):
        return obj.topic.part.course

    course.short_description = 'Курс'

    def file_link(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">{}</a>',
                               obj.file.url, obj.file.url)
        return '-'

    file_link.short_description = 'Файл'
