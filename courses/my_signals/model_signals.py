from django.db.models.signals import post_save
from django.dispatch import receiver
from courses import models


@receiver(post_save, sender=models.Course)
def course_created(sender, instance, created, **kwargs):
    if created:
        print('++++++++++New course created')
    else:
        print('++++++++++Course updated')


# @receiver(pre_save, sender=models.Course)
# def course_created(sender, instance, created, **kwargs):
#     if created:
#         instance['title'] = 'PRE SAVE TITLE'
#         print('++++++++++New course created')
#     else:
#         print('++++++++++Course updated')
