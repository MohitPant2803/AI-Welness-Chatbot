from celery import Celery
from celery.schedules import crontab

app = Celery('proj',
            broker='redis://redis-main:6379/0',
            backend='redis://redis-main:6379/1',
            include=['proj.tasks'])

app.conf.update(
    result_expires=3600,
    broker_connection_retry_on_startup=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)

app.conf.timezone = "Asia/Kolkata"
app.conf.enable_utc = False

app.conf.beat_schedule = {
    "send-mails": {
        "task": "proj.tasks.sendMailFromQueue",
        "schedule": crontab(hour=10, minute=00),
    },
    "analyze-emps":{
        "task": "proj.tasks.analyseEmps",
        "schedule": crontab(hour=23, minute=59)
    }
}

if __name__ == '__main__':
    app.start()
