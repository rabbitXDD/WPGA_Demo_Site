import logging
import json

from django import forms
from django.shortcuts import render, redirect 
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib.auth import authenticate
from django.db import IntegrityError

import Handler

from .forms import Register, CreateStudent, Valuations
from .models import Student, Grade, EvaluationQuestion, EvaluationAnswer

studentHandler = Handler.StudentHandler()
userHandler = Handler.UserHandler()

import pandas as pd
import matplotlib.pyplot as plt
import plotly.plotly as py 
plt.rcdefaults()
import numpy as np
import mpld3
from matplotlib.pyplot import figure, title, bar
import numpy.random as rnd

# Create your views here.
def index(request):
    return render(request, 'students/Index.html')

def getVisualization(request):
    
    student_grades = pd.read_csv('Exam_1_Exam_1 (copy).csv')

    id = int(request.user.username)
    studentGrades = student_grades.loc[student_grades['Student ID']==id].iloc[0]

    average = [
        student_grades['Question1'].mean(),
        student_grades['Question2'].mean(),
        student_grades['Question3'].mean(),
        student_grades['Question4'].mean(),
        student_grades['Question5'].mean(),
        student_grades['Question6-12'].mean(),
    ]
    student_questionslist = list(studentGrades.values[3:9].astype('float64'))
    df = pd.DataFrame(dict(graph=['Question1', 'Question2', 'Question3', 'Question4', 'Question5', 'Question6-12'],
                            n=student_questionslist, m=average)) 
    ind = np.arange(len(df))
    width = 0.4

    fig, ax = plt.subplots()
    ax.barh(ind + width, df.m, width, color='green', label='Class average')
    ax.barh(ind, df.n, width, color='red', label='Your score')


    ax.set(yticks=ind + width, yticklabels=df.graph, ylim=[2*width - 1, len(df)])
    ax.legend()

    fig_html = mpld3.fig_to_html(fig)

    return fig_html, student_questionslist, average


def thankyou(request):
    return render(request, 'students/Thanks.html')

@login_required
def getVisualization_2(request, qid):
    import plotly.offline as opy

    student_grades = pd.read_csv('Exam_1_Exam_1.csv')

    id = int(request.user.username)
    studentGrades = student_grades.loc[student_grades['Student ID']==id].iloc[0]

    average = [
        student_grades['Question1'].mean(),
        student_grades['Question2'].mean(),
        student_grades['Question3'].mean(),
        student_grades['Question4'].mean(),
        student_grades['Question5'].mean(),
        student_grades['Question6-12'].mean(),
    ]
    student_questionslist = list(studentGrades.values[3:9].astype('float64'))

    base_chart = {
    "values": [40, 10, 10, 10, 10, 10, 10],
    "labels": ["-", "0", "20", "40", "60", "80", "100%"],
    "domain": {"x": [0, .48]},
    "marker": {
        "colors": [
            'rgb(255, 255, 255)',
            'rgb(255, 255, 255)',
            'rgb(255, 255, 255)',
            'rgb(255, 255, 255)',
            'rgb(255, 255, 255)',
            'rgb(255, 255, 255)',
            'rgb(255, 255, 255)'
        ],
        "line": {
            "width": 1
        }
    },
    "name": "Gauge",
    "hole": .4,
    "type": "pie",
    "direction": "clockwise",
    "rotation": 108,
    "showlegend": False,
    "hoverinfo": "none",
    "textinfo": "label",
    "textposition": "outside"
    }
    questionDict = {
        1: 'Question1',
        2: 'Question2',
        3: 'Question3',
        4: 'Question4',
        5: 'Question5',
        6: 'Question6-12',
    }
    meter_chart = {
        "values": [50, 16.6, 16.6,16.6,],
        "labels": [questionDict[qid], 
                student_grades[questionDict[qid]].describe()['25%'],
                student_grades[questionDict[qid]].describe()['50%'],
                student_grades[questionDict[qid]].describe()['75%']
                ],
        "marker": {
            'colors': [
                'rgb(255, 255, 255)',
                'rgb(232,226,202)',
                'rgb(226,210,172)',
                'rgb(223,189,139)',
                'rgb(223,162,103)',
                'rgb(226,126,64)'
            ]
        },
        "domain": {"x": [0, 0.48]},
        "name": "Gauge",
        "hole": .3,
        "type": "pie",
        "direction": "clockwise",
        "rotation": 90,
        "showlegend": False,
        "textinfo": "label",
        "textposition": "inside",
        "hoverinfo": "none"
    }

    svgPath_Q1 = 'M 0.235 0.5 L 0.178 0.547 L 0.237 0.505 Z'
    svgPath_medium = 'M 0.235 0.5 L 0.24 0.65 L 0.245 0.5 Z'
    svgPath_Q3 = 'M 0.237 0.505 L 0.292 0.547 L 0.245 0.5 Z'

    if studentGrades[questionDict[qid]] < student_grades[questionDict[qid]].describe()['25%']:
        svgPath = svgPath_Q1
    elif studentGrades[questionDict[qid]] > student_grades[questionDict[qid]].describe()['25%'] and studentGrades['Question1'] < student_grades['Question1'].describe()['75%']:
        svgPath = svgPath_medium
    else:
        svgPath = svgPath_Q3

    layout = {
        'xaxis': {
            'showticklabels': False,
            'autotick': False,
            'showgrid': False,
            'zeroline': False,
        },
        'yaxis': {
            'showticklabels': False,
            'autotick': False,
            'showgrid': False,
            'zeroline': False,
        },
        'shapes': [
            {
                'type': 'path',
                'path': svgPath,
                'fillcolor': 'rgba(44, 160, 101, 0.5)',
                'line': {
                    'width': 0.5
                },
                'xref': 'paper',
                'yref': 'paper'
            }
        ],
        'annotations': [
            {
                'xref': 'paper',
                'yref': 'paper',
                'x': 0.23,
                'y': 0.45,
                'text': str(studentGrades[questionDict[qid]]),
                'showarrow': False
            }
        ]
    }

    # we don't want the boundary now
    base_chart['marker']['line']['width'] = 0

    fig = {"data": [base_chart, meter_chart],
        "layout": layout}
    div = opy.plot(fig, auto_open=False, output_type='div')

    return div, student_questionslist, average

def showVisualizations(request):
    answer = EvaluationAnswer.objects.filter(user=request.user)
    if answer:
        return HttpResponseRedirect('/thanks/')
    if request.method == 'POST':
        form = Valuations.ValuationsForm(request.POST)
        
        question = EvaluationQuestion.objects.all()[0]
        
        if form.is_valid():
            answer = form.cleaned_data['answer']
            answer = EvaluationAnswer(question=question, answer=answer, user=request.user)
            answer.save()
            return HttpResponseRedirect('/thanks/')
        else:
            fig_html, student_questionslist, average = getVisualization(request)
    else:
        form = Valuations.ValuationsForm
        question = EvaluationQuestion.objects.all()[0]

        if request.user.MondayClass:
            fig_html, student_questionslist, average = getVisualization(request)
            div = ''

            context = {
                'figure': fig_html,
                'studentGrades': student_questionslist,
                'classAverages': average,
                'form': form,
                'question': question,
            }
        else:
            fig_html_list = []
            for i in range(1,7):
                fig_html_list.append(getVisualization_2(request, i)[0])
            fig_html, student_questionslist, average = getVisualization_2(request, 1)

            context = {
                'figure': fig_html,
                'figure_2': fig_html_list[1],
                'figure_3': fig_html_list[2],
                'figure_4': fig_html_list[3],
                'figure_5': fig_html_list[4],
                'figure_6': fig_html_list[5],
                'studentGrades': student_questionslist,
                'classAverages': average,
                'form': form,
                'question': question,
            }

    # try:
    # except:
    #     logging.exception('Got exception on main handler')
    #     raise Http404("Something goes wrong")
        
    return render(request, 'students/Visualizations.html', context)

@login_required
def getAllStudents(request):
    try:
        studentsList = studentHandler.getStudentsQuerySet()
        context = {
            'studentsList': studentsList,
        }
    except:
        logging.exception('Got exception on main handler')
        raise Http404("Something goes wrong")
    
    return render(request, 'students/AllStudentsGrade.html', context)

@login_required
def getSubjects(request):
    try:
        subjectsList = studentHandler.getSubjects()
        context = {
            'subjectsList': subjectsList,
        }
    except:
        logging.exception('Got exception on main handler')
        raise Http404("Something goes wrong")
    
    return render(request, 'students/SubjectGrades.html', context)

@login_required
def search(request):
    if request.method == 'GET':
        context = {
            'searchResult': ' ',
        }
    elif request.method == 'POST':
        name = request.POST['keyword']
        if name:
            try:
                searchResult = studentHandler.search(name)
                context = {
                    'searchResult': searchResult,
                }
            except:
                logging.exception('Got exception on main handler')
                raise Http404("Something goes wrong")
        else:
            context = {
                'searchResult': ' ',
            }
        
    return render(request, 'students/Search.html', context)

@login_required
def rank(request):
    if request.method == 'GET':
        context = {
            'rankResult': ' ',
        }

    elif request.method == 'POST':
        examNumber = request.POST['examNumber']

        if examNumber:
            try:
                rankResult = studentHandler.rank(examNumber)
                rankList = range(1, len(rankResult) + 1)

                context = {
                    'rankResult': rankResult,
                    'examNumber': examNumber,
                    'rankList': rankList,
                }
            except ValueError:
                context = {
                    'errorMessage': 'You have typed in invalid value'
                }
                return render(request, 'students/ErrorPage.html', context)

            except:
                logging.exception('Got exception on main handler')
                raise Http404("Something goes wrong")
        else:
            context = {
                'rankResult': ' ',
            }
        
    return render(request, 'students/Rank.html', context)

def signup(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Register.RegistrationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            cleanData = form.clean()

            try:
                userHandler.createUser(
                    cleanData['userName'],
                    cleanData['password'],
                    cleanData['firstName'],
                    cleanData['lastName'],
                    cleanData['email'],
                    cleanData['phoneNumber']
                )

                user = authenticate(
                    username=cleanData['userName'], 
                    password=cleanData['password']
                )

                login(request, user)
                return redirect('/students/')

            except:
                logging.exception('Got exception on main handler')
                raise Http404("Something goes wrong")
            
    else:
        form = Register.RegistrationForm()

    return render(request, 'students/SignupPage.html', {'form': form})

def signin(request):
    if request.method == 'GET':
        context = {
            }
        return render(request, 'students/SigninPage.html', context)
    elif request.method == 'POST':
        username = request.POST['accountName']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('/students/')
        else:
            # Return an 'invalid login' error message.
            pass

def logoutView(request):
    logout(request)
    # Redirect to a success page.
    return render(request, 'students/Index.html')

def createStudent(request):
    if request.method == 'POST':
        form = CreateStudent.StudentForm(request.POST)

        if form.is_valid():
            cleanData = form.clean()

            student = studentHandler.createStudent(
                cleanData['firstName'],
                cleanData['lastName'],
                cleanData['phoneNumber']
                #cleanData.get('phoneNumber', ' ')
                #if phoneNumber is none, return ' '
            )

            url = reverse('students')
            return HttpResponseRedirect(url)
    else:
        form = CreateStudent.StudentForm()

    return render(request, 'students/CreateStudentPage.html', {'form': form})

def paginateStudentsByAjax(request):
    students = studentHandler.getStudentsQuerySet()
    studentsPaginator = Paginator(students, 10)

    page = request.GET.get('page')

    try:
        results = studentsPaginator.page(page)    
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        results = studentsPaginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        results = None

    studentsList = []
        
    for ele in results.object_list:
        studentsTmp = {}
        gradeList = []
        studentsTmp['firstName'] = ele.firstName
        studentsTmp['lastName'] = ele.lastName
        studentsTmp['phoneNumber'] = ele.phoneNumber

        for grade in ele.grade.all():
            gradeTmp = {}
            gradeTmp['examNumber'] = grade.examNumber
            gradeTmp['subject1Score'] = grade.subject1Score
            gradeTmp['subject2Score'] = grade.subject2Score
            gradeTmp['subject3Score'] = grade.subject3Score
            gradeList.append(gradeTmp)
        studentsTmp['grade'] = gradeList

        studentsList.append(studentsTmp)

    return HttpResponse(
        json.dumps(studentsList), 
        content_type='application/json'
    )

def ajaxView(request):
    return render(request, 'students/StudentsListAjaxScrollUp.html')

class StudentsList(ListView):
    queryset = Student.objects.all()
    template_name = 'students/StudentsList.html'
    paginate_by = 10

class InfiniteScrollStudentsList(ListView):
    queryset = Student.objects.all()
    template_name = 'students/StudentsListInfiniteScrollUp.html'
    paginate_by = 10

