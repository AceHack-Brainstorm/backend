# CloudSense Backend

### Tech Stack : 
- Django Rest framework
- 5 minute interval CRON job using django-cron and crontab
- Website status checks using python requests library
- OpenAI for recommendation

### How to Configure : 
Please setup a virtual environment prior to installing any dependencies

```bash
git clone https://github.com/AceHack-Brainstorm/backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Optionally, for setting up CRON for a 5 minute status check, setup the following CRON tab entry using `crontab -e`
```sh
*/5 * * * *  source /home/monitor-backend/env/bin/activate && python3 /home/monintor-backend/backend/manage.py runcrons > /var/log/cronjob.log
```