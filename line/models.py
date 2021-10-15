from django.db import models

# Create your models here.


class Line(models.Model):
    description = models.CharField(max_length=200)
    uid = models.CharField(max_length=200, unique=True)
    cycle_time = models.IntegerField()
    goal_time = models.IntegerField()

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
    actual = models.IntegerField()
    reason = models.ForeignKey(Reason, on_delete=models.SET_NULL, null=True)
    comment = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return f"{self.line.description} - {self.date}"