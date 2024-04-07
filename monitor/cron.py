from django_cron import CronJobBase, Schedule
from .models import Service, Monitor_Log
import requests
import datetime

class PingHosts(CronJobBase):
    RUN_EVERY_MINS = 5 # every 5 mins

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'monitor.ping_hosts'    # a unique code

    def do(self):
        pass    # do your thing here
    services = Service.objects.all()
    for service in services:
        response = requests.get(service.url)
        http_code = response.status_code
        milliseconds = int(response.elapsed.total_seconds() * 1000)
        print('Request was succesful')
        print(http_code)
        print(milliseconds)

        # Log to DB
        status = True if http_code == 200 else False
        monitor_log = Monitor_Log(datetime = datetime.datetime.now(), status = status, ping = milliseconds, service = service)
        monitor_log.save()