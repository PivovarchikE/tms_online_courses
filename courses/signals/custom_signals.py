from django.dispatch import Signal, receiver


course_published = Signal()


@receiver(course_published, sender='1')
def notify_course_published(sender, course, user, **kwargs):
    print("+++++sender", sender)
    print("+++++course", course)
    print("+++++user", user)
    print("+++++kwargs", kwargs)


@receiver(course_published, sender='2')
def notify_course_published2(**kwargs):
    print("+++++++++2")
