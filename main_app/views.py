from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, Job, Event
from .forms import JobForm, EventForm, ProfileForm
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.mixins import UserPassesTestMixin
from django.forms import Textarea


# Create your views here.
def home(request):
  return render(request, 'home.html')

# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     try:
#        if created:
#           Profile.objects.create(user=instance).save()
#     except Exception as err:
#        print(f'Error creating user profile!\n{err}')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      # create_profile()
      login(request, user)
      return redirect('profileform')
    else:
      error_message = 'Invalid signup. Please try again.'
  form = UserCreationForm()

  context = {
    'form': form,
    'error_message': error_message,
  }
  return render(request, 'registration/signup.html', context)


class ProfileCreate(LoginRequiredMixin, CreateView):
  model = Profile
  fields = ['full_name', 'picture_url', 'linkedin_url', 'industry', 'number_connections']
  # success_url = '/profiles'
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)



class ProfileUpdate(UserPassesTestMixin, UpdateView):
  model = Profile
  fields = ['full_name', 'picture_url', 'linkedin_url', 'industry', 'number_connections',]
  def test_func(self):
    profile = get_object_or_404(Profile, pk = self.kwargs['pk'])
    return self.request.user == profile.user

  def form_valid(self, form):
    form.instance.user = self.request.user  # form.instance is the cat
    return super().form_valid(form)


# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     try:
#        if created:
#           Profile.objects.create(user=instance).save()
#     except Exception as err:
#        print(f'Error creating user profile!\n{err}')

@login_required
def profiles_index(request):
  profiles = Profile.objects.all()
  
  return render(request, 'profiles/index.html', {
    'profiles': profiles
  })

@login_required
def profiles_detail(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    jobs = Job.objects.filter(profile =profile_id)
    time_spent = 0
    for job in jobs:
      events = job.event_set.all()
      for event in events:
        time_spent += event.time_spent
    job_form = JobForm()
    return render(request, 'profiles/detail.html', {
        'jobs': jobs,
        'job_form': job_form,
        'profile_id': profile_id,
        'full_name':profile.full_name,
        'profile': profile,
        'time_spent': time_spent,
    })

@login_required
def jobs_detail(request, job_id):
  job = Job.objects.get(id=job_id)
  events = Event.objects.filter(job=job_id)
  profile = Profile.objects.get(id=job.profile.id)
  time_spent = 0
  for event in events:
    time_spent += event.time_spent
  event_form = EventForm()
  return render(request, 'profiles/jobs/detail.html', {
    'events': events,
    'event_form': event_form,
    'job': job,
    'job_id': job_id,
    'time_spent': time_spent,
    'profile': profile,
  })

class JobDelete(LoginRequiredMixin, DeleteView):
  model = Job
  success_url = '/profiles/{profile_id}'


  def get_job_profile(self, **kwargs):
    context = super().get_context_data(**kwargs)
    return f"{self.profile.id}"

  # def get_job_profile(self):
  #   profile = self.profile_id
  #   return profile
  # profile_id = get_job_profile(Job)


class JobUpdate(LoginRequiredMixin, UpdateView):
  model = Job
  # form = JobForm()
  fields = ['position_applied_for', 'company_name', 'salary_range', 'status', 'type_of_resume', 'dates', 'time_spent', 'confidence_bar', 'desirability_bar']
#   success_url = '/profiles/<int:pk>'

@login_required
def add_job(request, profile_id):
  form = JobForm(request.POST)
  print('ANY KIND OF STRING')
  if form.is_valid():
    new_job = form.save(commit=False)
    new_job.profile_id = profile_id
    new_job.save()
  return redirect('detail', profile_id=profile_id)

@login_required
def add_event(request, job_id):
  form = EventForm(request.POST)
  if form.is_valid():
    new_event = form.save(commit=False)
    new_event.job_id = job_id
    new_event.save()
  return redirect('job_detail', job_id=job_id)


class EventDelete(LoginRequiredMixin, DeleteView):
  model = Event
  success_url = '/jobs/{job_id}'



class EventDelete(LoginRequiredMixin, DeleteView):
  model = Event
  success_url = '/profiles'

class EventUpdate(LoginRequiredMixin, UpdateView):
  model = Event
  fields = ['date', 'type_of_event', 'time_spent', 'comment']

