from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from django.http import JsonResponse
from .models import *
from .forms import HabitForm


# =========================
# DASHBOARD
# =========================

@login_required(login_url='login')

def dashboard(request):

    today = timezone.now().date()

    habits = Habit.objects.filter(
        user=request.user
    ).order_by('-streak')

    total_habits = habits.count()

    completed_today = HabitCompletion.objects.filter(
        habit__user=request.user,
        completed_at=today
    ).count()

    # water tracking

    water, created = WaterIntake.objects.get_or_create(
        user=request.user,
        date=today
    )

    # steps tracking

    step_tracker, created = StepTracker.objects.get_or_create(
        user=request.user,
        date=today
    )

    context = {

        'habits': habits,

        'total_habits': total_habits,

        'completed_today': completed_today,

        'water': water,

        'steps': step_tracker,
    }

    return render(
        request,
        'dashboard.html',
        context
    )


# =========================
# ADD HABIT
# =========================

@login_required(login_url='login')

def add_habit(request):

    if request.method == 'POST':

        form = HabitForm(request.POST)

        if form.is_valid():

            habit = form.save(commit=False)

            habit.user = request.user

            habit.save()

            return redirect('dashboard')

    else:

        form = HabitForm()

    return render(
        request,
        'add_habit.html',
        {
            'form': form
        }
    )


# =========================
# COMPLETE HABIT
# =========================

@login_required(login_url='login')

def complete_habit(request, habit_id):

    habit = get_object_or_404(
        Habit,
        id=habit_id,
        user=request.user
    )

    today = timezone.now().date()

    already_completed = HabitCompletion.objects.filter(
        habit=habit,
        completed_at=today
    ).exists()

    if not already_completed:

        HabitCompletion.objects.create(
            habit=habit,
            completed_at=today
        )

        habit.total_completed += 1

        habit.streak += 1

        habit.save()

    return redirect('dashboard')


# =========================
# WATER TRACKING
# =========================

@login_required(login_url='login')

def add_water(request):

    today = timezone.now().date()

    water, created = WaterIntake.objects.get_or_create(
        user=request.user,
        date=today
    )

    if water.glasses < 8:

        water.glasses += 1

        water.save()

    return redirect('dashboard')


# =========================
# STEP TRACKING
# =========================

@login_required(login_url='login')

def add_steps(request):

    today = timezone.now().date()

    step_tracker, created = StepTracker.objects.get_or_create(
        user=request.user,
        date=today
    )

    step_tracker.steps += 500

    step_tracker.save()

    return redirect('dashboard')


# =========================
# ANALYTICS
# =========================

@login_required(login_url='login')

def analytics(request):

    habits = Habit.objects.filter(
        user=request.user
    )

    return render(
        request,
        'analytics.html',
        {
            'habits': habits
        }
    )


# =========================
# STREAKS
# =========================

@login_required(login_url='login')

def streaks(request):

    habits = Habit.objects.filter(
        user=request.user
    ).order_by('-streak')

    return render(
        request,
        'streaks.html',
        {
            'habits': habits
        }
    )


# =========================
# SETTINGS
# =========================

@login_required(login_url='login')

def settings_page(request):

    user = request.user

    success = False

    if request.method == 'POST':

        name = request.POST.get('name')

        email = request.POST.get('email')

        if name:
            user.username = name

        if email:
            user.email = email

        user.save()

        success = True

    return render(
        request,
        'settings.html',
        {
            'user_data': user,
            'success': success
        }
    )

# =========================
# REGISTER
# =========================

def register_page(request):

    error = ''

    if request.method == 'POST':

        username = request.POST.get('username')

        email = request.POST.get('email')

        password = request.POST.get('password')

        if User.objects.filter(
            username=username
        ).exists():

            error = 'Username already exists'

        else:

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            login(request, user)

            return redirect('dashboard')

    return render(
        request,
        'register.html',
        {
            'error': error
        }
    )


# =========================
# LOGIN
# =========================

def login_page(request):

    error = ''

    if request.method == 'POST':

        username = request.POST.get('username')

        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('dashboard')

        else:

            error = 'Invalid username or password'

    return render(
        request,
        'login.html',
        {
            'error': error
        }
    )


# =========================
# LOGOUT
# =========================

def logout_page(request):

    logout(request)

    return redirect('login')

def ai_chat(request):

    if request.method == "POST":

        message = request.POST.get("message")

        message = message.lower()

        if "focus" in message:

            reply = "🚀 Try deep work sessions between 9 AM and 11 AM."

        elif "water" in message:

            reply = "💧 Drink at least 8 glasses daily for better focus."

        elif "stress" in message:

            reply = "🧘 Meditation and short breaks reduce stress."

        elif "motivation" in message:

            reply = "🔥 Small daily consistency beats motivation."

        elif "sleep" in message:

            reply = "😴 7-8 hours sleep improves productivity."

        elif "gym" in message:

            reply = "💪 Strength training improves energy and discipline."

        elif "coding" in message:

            reply = "👨‍💻 Practice coding daily for faster growth."

        else:

            reply = "🤖 Keep improving your habits daily!"

        return JsonResponse({
            "reply": reply
        })