from django.core.management.base import BaseCommand
from courses import models
from django.conf import settings
from pathlib import Path
import shutil


class Command(BaseCommand):
    help = "Flush all data from the database"

    def handle(self, *args, **options):
        self.stdout.write("Flushing all data from the database...")
        self.stdout.write("This action is irreversible and will delete all data from the database.")
        self.stdout.write("Are you sure you want to continue? (y/n)")
        answer = input()

        if answer == "y":
            models.Course.objects.all().delete()
            self.stdout.write("Courses deleted")
            models.CoursePart.objects.all().delete()
            self.stdout.write("Course parts deleted")
            models.CourseTopic.objects.all().delete()
            self.stdout.write("Course topics deleted")
            models.TopicDocument.objects.all().delete()
            self.stdout.write("Course topic documents deleted")

            path = Path(settings.MEDIA_ROOT)
            if path.exists():
                shutil.rmtree(path)
                self.stdout.write("Media directory deleted")

            self.stdout.write("All data flushed")

        else:
            self.stdout.write("Canceled")
