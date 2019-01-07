from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from profile_app.models import Profile, City, Gender
from django.contrib.auth import authenticate, login, logout
from profile_app.forms import SignupForm, LoginForm, UserForm, ProfileForm, ExtraInfoForm


def index(request):
  users = User.objects.all().filter(is_superuser=False)
  return render(request, 'index.html', context={ 'users': users })


def signup(request):
  if request.method == 'POST':
    User.objects.create_user(
      username=request.POST.get('username'),
      password=request.POST.get('password'),
      first_name=request.POST.get('first_name'),
      last_name=request.POST.get('last_name'),
      email=request.POST.get('email'),
    )

    user = authenticate(request, username=username, password=password)

    Profile.objects.get_or_create(
      user=user,
      bio='',
      city=City.objects.get(id=request.POST.get('city')),
      gender=Gender.objects.get(id=request.POST.get('gender')),
    )

    if user is not None:
      login(request, user)
      return redirect('/profile_app/')

  return render(request, 'signup.html', context={
      'signup_form': SignupForm(),
      'extra_info_form': ExtraInfoForm(),
    })


def login_auth(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      return redirect('/profile_app/')

  return render(request, 'login.html', context={ 'login_form': LoginForm() })


def logout_auth(request):
  logout(request)
  return redirect('/profile_app/')


def profile(request, user_id):
  user = User.objects.get(id=user_id)
  return render(request, 'profile.html', context={ 'user': user })


def profile_edit(request, user_id):
  user = User.objects.get(id=user_id)

  try:
    profile = Profile.objects.get(user=user)
  except Profile.DoesNotExist:
    profile = Profile.objects.get_or_create(user=user, bio='')[0]

  redirect_profile_link = '/profile_app/profile/{}'.format(user_id)

  if user_id != request.user.id:
    return redirect(redirect_profile_link)

  if request.method == 'POST':
    user.first_name = request.POST.get('first_name')
    user.last_name = request.POST.get('last_name')
    user.email = request.POST.get('email')
    user.save()

    profile.bio = request.POST.get('bio')
    profile.save()

    return redirect(redirect_profile_link)

  return render(request, 'profile_edit.html', context={
    'user': user,
    'profile_form': ProfileForm(initial={
      'bio': profile.bio,
    }),
    'user_form': UserForm(initial={
      'first_name': user.first_name,
      'last_name': user.last_name,
      'email': user.email,
    })
  })








