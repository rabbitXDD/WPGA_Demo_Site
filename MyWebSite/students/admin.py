from django.contrib import admin

from .models import Student, Grade, User, EvaluationScheme, EvaluationQuestion, EvaluationAnswer
# Register your models here.

class GradeInline(admin.TabularInline):
    model = Grade
    extra = 1

class StudentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('user information', {'fields': ['firstName']}),
        (None, {'fields': ['lastName']}),
        (None, {'fields': ['phoneNumber']}),
    ]

    inlines = [GradeInline]

    list_display = ('firstName', 'lastName', 'phoneNumber')
    list_filter = ['firstName']

class UserAdmin(admin.ModelAdmin):
    """docstring for UserAdmin"""
    fieldsets = [
        ('user information', {'fields': ['username']}),
        (None, {'fields': ['phoneNumber']}),
        (None, {'fields': ['email']}),
    ]
    list_display = ('username', 'phoneNumber', 'email')

class EvaluationSchemeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('title', {'fields': ['title']}),
    ]
    list_display = ('title', )
        
admin.site.register(Grade)
admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(EvaluationScheme, EvaluationSchemeAdmin)
admin.site.register(EvaluationQuestion)
admin.site.register(EvaluationAnswer)
