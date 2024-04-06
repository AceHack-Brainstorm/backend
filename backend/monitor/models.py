from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=30)
    url = models.URLField(max_length=120)
    architecture = models.TextField()
    recommendation = models.TextField(blank=True)

class Monitor_Log(models.Model):
    datetime = models.DateTimeField()
    status = models.BooleanField()
    ping = models.IntegerField()
    service = models.ForeignKey("Service", on_delete=models.CASCADE)