import csv

from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth import get_user_model
User = get_user_model()

class Command(BaseCommand):
    help = 'Create students automatically by given numbers with built-in random name list'

    def handle(self, *args, **options):
        csvfile = open('Exam_1_Exam_1.csv', 'rb')
        looptimes = 0
        for row in csv.reader(csvfile):
            user = User.objects.create_user(username=row[2],
                                 email='%s@nccu.edu.tw' % (row[2], ),
                                 MondayClass=False,
                                 password=row[2])
            looptimes += 1

        self.stdout.write('Successfully create %s students' % looptimes)
