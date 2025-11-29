import random
from django.core.files.base import ContentFile, File
from django.core.management.base import BaseCommand
from django_seed import Seed
from faker import Faker

from courses import models


class Command(BaseCommand):
    help = 'Generate test data using faker or django-seed'
    num_parts = random.randint(2, 4)
    num_topics = random.randint(2, 5)
    num_documents = random.randint(1, 3)

    def add_arguments(self, parser):
        parser.add_argument(
            'count',
            type=int,
            help='Count of Entities to create'
        )
        parser.add_argument(
            '--method',
            type=str,
            choices=['faker', 'seeder'],
            default='faker',
            help='Use faker or seeder'
        )
        parser.add_argument(
            '--locale',
            type=str,
            default='en_US',
            help='Locale for faker'
        )

    def handle(self, *args, **options):
        count = options['count']
        method = options['method']
        locale = options['locale']

        self.stdout.write(self.style.SUCCESS(f'Starting generation of {count} test data using {method} method...'))

        if method == 'faker':
            self.generate_with_faker(count, locale)

        elif method == 'seeder':
            self.generate_with_seeder(count, locale)

        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} test courses!'))

    def generate_with_faker(self, count, locale):
        fake = Faker(locale)

        for i in range(count):
            course = models.Course.objects.create(
                title=fake.catch_phrase(),
                description=fake.text(max_nb_chars=500)
            )

            for _ in range(self.num_parts):
                part = models.CoursePart.objects.create(
                    course=course,
                    title=fake.sentence(nb_words=3).rstrip('.'),
                    description=fake.text(max_nb_chars=300)
                )

                for _ in range(self.num_topics):
                    topic = models.CourseTopic.objects.create(
                        part=part,
                        title=fake.sentence(nb_words=4).rstrip('.'),
                        description=fake.text(max_nb_chars=200)
                    )

                    for _ in range(self.num_documents):
                        file_name = fake.file_name(extension='txt')
                        models.TopicDocument.objects.create(
                            topic=topic,
                            name=file_name,
                            file=ContentFile(fake.text(), f'seed_documents/{file_name}')
                        )

            self.stdout.write(f'Course created: {course.title}')

    def generate_with_seeder(self, count, locale):
        from django.utils import timezone

        seeder = Seed.seeder()
        seeder.faker = Faker(locale)

        seeder.add_entity(models.Course, count, {
            'title': lambda x: seeder.faker.sentence(),
            'description': lambda x: seeder.faker.text(),
            'created_at': lambda x: timezone.now(),
            'updated_at': lambda x: timezone.now(),
            'deleted_at': lambda x: None,
        }
        )

        course_ids = seeder.execute()[models.Course]
        courses = models.Course.objects.filter(id__in=course_ids).all()

        for course in courses:
            seeder.add_entity(models.CoursePart, self.num_parts, {
                'course': lambda x: course,
                'title': lambda x: seeder.faker.sentence(),
                'description': lambda x: seeder.faker.text(),
                'created_at': lambda x: timezone.now(),
                'updated_at': lambda x: timezone.now(),
                'deleted_at': lambda x: None,
            })

            part_ids = seeder.execute()[models.CoursePart]
            parts = models.CoursePart.objects.filter(id__in=part_ids).all()

            for part in parts:
                seeder.add_entity(models.CourseTopic, self.num_topics, {
                    'part': lambda x: part,
                    'title': lambda x: seeder.faker.sentence(),
                    'description': lambda x: seeder.faker.text(),
                    'created_at': lambda x: timezone.now(),
                    'updated_at': lambda x: timezone.now(),
                    'deleted_at': lambda x: None,
                })

                topic_ids = seeder.execute()[models.CourseTopic]
                topics = models.CourseTopic.objects.filter(id__in=topic_ids).all()

                for topic in topics:
                    for _ in range(self.num_documents):
                        file_name = seeder.faker.file_name(extension='txt')
                        seeder.add_entity(models.TopicDocument, count, {
                            'topic': lambda x: topic,
                            'name': lambda x: file_name,
                            'file': lambda x: File(
                                ContentFile(seeder.faker.text(), f'seed_documents/{file_name}')
                            ),
                            'created_at': lambda x: timezone.now(),
                            'updated_at': lambda x: timezone.now(),
                            'deleted_at': None
                        })

                    seeder.execute()

            self.stdout.write(f'Course created: {course}')
