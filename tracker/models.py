from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Habit Model

class Habit(models.Model):

    CATEGORY_CHOICES = [
        ('Fitness', 'Fitness'),
        ('Coding', 'Coding'),
        ('Study', 'Study'),
        ('Health', 'Health'),
        ('Reading', 'Reading'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)

    description = models.TextField()

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    streak = models.IntegerField(default=0)

    total_completed = models.IntegerField(default=0)

    def __str__(self):
        return self.title


# Habit Completion Model

class HabitCompletion(models.Model):

    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE
    )

    completed_at = models.DateField(
        default=timezone.now
    )

    def __str__(self):
        return f"{self.habit.title} - {self.completed_at}"
    

class WaterIntake(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    glasses = models.IntegerField(default=0)

    date = models.DateField(auto_now_add=True)


class StepTracker(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    steps = models.IntegerField(default=0)

    goal = models.IntegerField(default=10000)

    date = models.DateField(auto_now_add=True)

class MoodTracker(models.Model):

    MOODS = [
        ('Happy', 'Happy'),
        ('Focused', 'Focused'),
        ('Tired', 'Tired'),
        ('Stressed', 'Stressed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    mood = models.CharField(max_length=20, choices=MOODS)

    date = models.DateField(auto_now_add=True)