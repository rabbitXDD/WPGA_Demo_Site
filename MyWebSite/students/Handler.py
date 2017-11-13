from django.db.models import Q, Max, Sum, Avg

from .models import Student, Grade, User

class StudentHandler(object):
    def getStudentsTupleList(self, students):
        studentsTupleList = []

        for ele in students:
            if ele.gradeList == []:
                studentsTupleList.append((
                    ele.firstName,
                    ele.lastName,
                    ele.phoneNumber,
                    '',
                    '',
                    '',
                    '',
                ))
            else:   
                for index, grade in enumerate(ele.gradeList):
                    if grade.examNumber > 1:
                        if index == 0:
                            studentsTupleList.append((
                            ele.firstName,
                            ele.lastName,
                            ele.phoneNumber,
                            grade.examNumber,
                            grade.subject1Score,
                            grade.subject2Score,
                            grade.subject3Score,
                        ))
                        else:
                            studentsTupleList.append((
                            '',
                            '',
                            '',
                            grade.examNumber,
                            grade.subject1Score,
                            grade.subject2Score,
                            grade.subject3Score,
                        ))
                    else:
                        studentsTupleList.append((
                            ele.firstName,
                            ele.lastName,
                            ele.phoneNumber,
                            grade.examNumber,
                            grade.subject1Score,
                            grade.subject2Score,
                            grade.subject3Score,
                        ))
                    
        studentTuple = ()
        return studentsTupleList

    def getAllStudents(self):
        students = []
        
        for s in Student.objects.all():
            s.gradeList = []
            for g in s.grade.all():
                s.addGrade(g)

            students.append(s)
        return self.getStudentsTupleList(students)

    def getStudentsQuerySet(self):
        s = Student.objects.all()
        return s

    def getSubjects(self):
        index = 1
        subjectList = []
        examNumberMax = Grade.objects.all().aggregate(
                            Max('examNumber'))['examNumber__max']
        
        while index <= examNumberMax:
            subject1Sum = Grade.objects.filter(examNumber=index).aggregate(
                            Sum('subject1Score'))['subject1Score__sum']
            subject2Sum = Grade.objects.filter(examNumber=index).aggregate(
                            Sum('subject2Score'))['subject2Score__sum']
            subject3Sum = Grade.objects.filter(examNumber=index).aggregate(
                            Sum('subject3Score'))['subject3Score__sum']
            subject1Avg = Grade.objects.filter(examNumber=index).aggregate(
                            Avg('subject1Score'))['subject1Score__avg']
            subject2Avg = Grade.objects.filter(examNumber=index).aggregate(
                            Avg('subject2Score'))['subject2Score__avg']
            subject3Avg = Grade.objects.filter(examNumber=index).aggregate(
                            Avg('subject3Score'))['subject3Score__avg']
            studentNumInExam = Grade.objects.filter(examNumber=index).count()
            subjectTmp = (index, 
                          subject1Sum, subject2Sum, subject3Sum,
                          subject1Avg, subject2Avg, subject3Avg,
                          studentNumInExam)
            subjectList.append(subjectTmp)
            index = index + 1
            print index, examNumberMax

        return subjectList

    def search(self, keyword):
        students = Student.objects.all().filter(
            Q(firstName__contains=keyword) | Q(lastName__contains=keyword))

        searchResult = self.getStudentsTupleList(students)
        return searchResult

    def rank(self, compareNum):
        grade = Grade.objects.extra(
            select={
                'gradeSum': 'subject1Score + subject2Score + subject3Score'
            },
            where=["examNumber=%s"],
            params=[compareNum],
            order_by=('-gradeSum',)
        )

        return grade

    def createStudent(self, firstName, lastName, phoneNumber):
        student = Student(
            firstName=firstName,
            lastName=lastName,
            phoneNumber=phoneNumber
        )
        student.save()
        return student

class UserHandler(object):
    
    def createUser(self, userName, password, 
                   firstName=None, lastName=None, 
                   email=None, phoneNumber=None):
        user = User.objects.create_user(userName, email=email, password=password)
        
        if firstName:
            user.first_name = firstName
        if lastName:
            user.last_name = lastName
        if phoneNumber:
            user.phoneNumber = phoneNumber
        user.save()

        return user
        
    def authenticateUser(userName, password):
        user = authenticate(username=userName, password=password)
        if user is not None:
            # A backend authenticated the credentials
            return user
        else:
            # No backend authenticated the credentials
            return None