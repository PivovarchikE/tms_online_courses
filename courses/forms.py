from django import forms
from courses import models


class CourseForm(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = ['title', 'description']


class CoursePartForm(forms.Form):
    title = forms.CharField(max_length=255, label='Название части')
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        label='Описание'
    )


class CourseTopicForm(forms.Form):
    title = forms.CharField(max_length=255, label='Название темы')
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        label='Описание'
    )


class TopicDocument(forms.Form):
    name = forms.CharField(max_length=255, label='Название файла')
    file = forms.FileField(label='Файл', required=False)


# Переопределение полей формы регистрации (расширение)
# class RegisterForm(UserCreationForm):
#     email = forms.EmailField(required=True, label='Email')
#     first_name = forms.CharField(max_length=30, required=False, label='Name')
#     last_name = forms.CharField(max_length=30, required=False, label='Last Name')
#
#     class Meta:
#         model=User
#         fields=('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
#
#         def __init__(self, *args, **kwargs):
#             super().__init__(*args, **kwargs)
#
#             for field_name, field in self.fields.items():
#                 field.widget.attrs['class'] = 'form-control'
