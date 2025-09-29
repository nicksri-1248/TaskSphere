from django import forms
from django.utils.text import slugify
from .models import Task
from .models import Project
from register.models import Company
from django.contrib.auth.models import User

status = (
    ('1', 'Stuck'),
    ('2', 'Working'),
    ('3', 'Done'),
)

due = (
    ('1', 'On Due'),
    ('2', 'Overdue'),
    ('3', 'Done'),
)


class TaskRegistrationForm(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Project.objects.all())
    assign = forms.ModelMultipleChoiceField(queryset=User.objects.all())
    task_name = forms.CharField(max_length=80)
    status = forms.ChoiceField(choices=status)
    due = forms.ChoiceField(choices=due)

    class Meta:
        model = Task
        fields = '__all__'


    def save(self, commit=True):
        task = super(TaskRegistrationForm, self).save(commit=False)
        task.project = self.cleaned_data['project']
        task.task_name = self.cleaned_data['task_name']
        task.status = self.cleaned_data['status']
        task.due = self.cleaned_data['due']
        
        if commit:
            task.save()
            # Save many-to-many relationships after the object is saved
            assigns = self.cleaned_data['assign']
            task.assign.set(assigns)  # Use set() instead of add() for multiple objects

        return task


    def __init__(self, *args, **kwargs):
        super(TaskRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['project'].widget.attrs['class'] = 'form-control'
        self.fields['project'].widget.attrs['placeholder'] = 'Select project for this task'
        self.fields['task_name'].widget.attrs['class'] = 'form-control'
        self.fields['task_name'].widget.attrs['placeholder'] = 'e.g., Design User Interface'
        self.fields['status'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['placeholder'] = 'Select task status'
        self.fields['due'].widget.attrs['class'] = 'form-control'
        self.fields['due'].widget.attrs['placeholder'] = 'Select due status'
        self.fields['assign'].widget.attrs['class'] = 'form-control'
        self.fields['assign'].widget.attrs['placeholder'] = 'Select team members'


class ProjectRegistrationForm(forms.ModelForm):
    name = forms.CharField(max_length=80)
    # slug = forms.SlugField('shortcut')
    assign = forms.ModelMultipleChoiceField(queryset=User.objects.all())
    efforts = forms.DurationField()
    status = forms.ChoiceField(choices=status)
    dead_line = forms.DateField()
    company = forms.ModelChoiceField(queryset=Company.objects.all())
    complete_per = forms.FloatField(min_value=0, max_value=100)
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Project
        fields = '__all__'


    def save(self, commit=True):
        project = super(ProjectRegistrationForm, self).save(commit=False)
        project.name = self.cleaned_data['name']
        project.efforts = self.cleaned_data['efforts']
        project.status = self.cleaned_data['status']
        project.dead_line = self.cleaned_data['dead_line']
        project.company = self.cleaned_data['company']
        project.complete_per = self.cleaned_data['complete_per']
        project.description = self.cleaned_data['description']
        project.slug = slugify(str(self.cleaned_data['name']))
        
        if commit:
            project.save()
            # Save many-to-many relationships after the object is saved
            assigns = self.cleaned_data['assign']
            project.assign.set(assigns)  # Use set() instead of add() for multiple objects

        return project


    def __init__(self, *args, **kwargs):
        super(ProjectRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'e.g., E-Commerce Website Development'
        self.fields['efforts'].widget.attrs['class'] = 'form-control'
        self.fields['efforts'].widget.attrs['placeholder'] = 'e.g., 30 days (format: 30 00:00:00)'
        self.fields['status'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['placeholder'] = 'Select project status'
        self.fields['dead_line'].widget.attrs['class'] = 'form-control'
        self.fields['dead_line'].widget.attrs['placeholder'] = 'e.g., 2025-12-31 (YYYY-MM-DD format)'
        self.fields['dead_line'].widget.attrs['type'] = 'date'
        self.fields['company'].widget.attrs['class'] = 'form-control'
        self.fields['company'].widget.attrs['placeholder'] = 'Select company'
        self.fields['complete_per'].widget.attrs['class'] = 'form-control'
        self.fields['complete_per'].widget.attrs['placeholder'] = 'e.g., 25 (percentage 0-100)'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['placeholder'] = 'e.g., Develop a modern e-commerce platform with user authentication, shopping cart, payment integration...'
        self.fields['assign'].widget.attrs['class'] = 'form-control'