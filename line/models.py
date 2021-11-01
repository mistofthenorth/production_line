from django.db import models

# Create your models here.


class Line(models.Model):
    description = models.CharField(max_length=200)
    uid = models.CharField(max_length=200, unique=True)
    cycle_time = models.IntegerField()
    goal_time = models.IntegerField()
    default_headcount = models.IntegerField(default=2)
    colorChoices = (
        ('Grey', 'Grey'),
        ('Gold', 'Yellow'),
        ('DodgerBlue', 'Light Blue'),
        ('Green', 'Green'),
        ('Orange', 'Orange'),
        ('Purple', 'Purple'),
        ('White', 'White'),
        ('Red', 'Red'),
        ('DodgerBlue', 'Medium Blue'),
        ('CornflowerBlue', 'Light Blue')
        )
    color = models.CharField(
        max_length=16,
        choices=colorChoices,
        default='Grey',
        null=True)

    def __str__(self):
        return self.description


class Reason(models.Model):
    code = models.IntegerField()
    description = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.code} - {self.description}"


class Goal(models.Model):
    date = models.DateTimeField()
    line = models.ForeignKey(Line, on_delete=models.CASCADE)
    goal = models.IntegerField()
    real_time_goal = models.IntegerField(null=True)
    actual = models.IntegerField()
    cycle_time = models.IntegerField()
    headcount = models.IntegerField()
    reason = models.ForeignKey(Reason, on_delete=models.SET_NULL, null=True)
    comment = models.CharField(max_length=1000, null=True)
    is_active = models.BooleanField()

    def __str__(self):
        return f"{self.line.description} - {self.date}"