from django.db import models
from django.utils import timezone


class Mytest(models.Model):
    title = models.CharField(max_length=200)
    date1 = models.DateTimeField(
            default=timezone.now)
    date2 = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
