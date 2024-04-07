from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=30)
    url = models.URLField(max_length=120)
    architecture = models.TextField()
    recommendation = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name

class Monitor_Log(models.Model):
    datetime = models.DateTimeField()
    status_code = models.IntegerField()
    ping = models.IntegerField()
    service = models.ForeignKey("Service", on_delete=models.CASCADE)
    def __str__(self):
        return self.datetime.__str__()