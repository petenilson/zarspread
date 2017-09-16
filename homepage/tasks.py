from __future__ import absolute_import, unicode_literals
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from homepage.utils import update_prices, wake_site


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="update_prices",
    ignore_result=True
)
def update():
    update_prices()

# keep the heroku app running
@periodic_task(
    run_every=(crontab(minute='*/25')),
    name="keep_awake",
    ignore_result=True
)
def wake():
    wake_site()
