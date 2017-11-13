import random

from django.core.management.base import BaseCommand, CommandError

from students.models import Student

firstName = ['Abbyabbie', 'Alina', 'Betty', 'Catherine', 'Francis', 'Gloria', 
             'Laura']
lastName = ['Lin', 'Lee', 'Liou', 'Chen', 'Shiua', 'Hunag', 'New', 'Chou']
phoneNumberList = list('0900000000')

class Command(BaseCommand):
    help = 'Create students automatically by given numbers with built-in random name list'

    def add_arguments(self, parser):
        message = 'Type the students number you want to add.'
        parser.add_argument('studentNumbers', type=int, help=message)

    def handle(self, *args, **options):
        phoneNumberLength = len(phoneNumberList)
        
        if options['studentNumbers']:
            looptimes = int(options['studentNumbers'])
        else:
            looptimes = 10

        for ele in range(looptimes):

            for i in range(2, phoneNumberLength):
                phoneNumberList[i] = str(random.randint(0, 9))

            phoneNumber = ''.join(phoneNumberList)

            student = Student(
                firstName='%s%d' % (random.choice(firstName), ele),
                lastName=random.choice(lastName),
                phoneNumber=phoneNumber
            )
            student.save()

        self.stdout.write('Successfully create %s students' % looptimes)
