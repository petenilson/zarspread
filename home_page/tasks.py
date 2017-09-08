from __future__ import absolute_import, unicode_literals
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from home_page.utils import update_prices


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="update_prices",
    ignore_result=True
)
def update():
    update_prices()
