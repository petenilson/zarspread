from __future__ import absolute_import
from celery.task.schedules import crontab
from celery.decorators import periodic_task, task
from celery.utils.log import get_task_logger

from home_page.utils import update_prices

logger = get_task_logger(__name__)


"""@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="task_update_prices",
    ignore_re   sult=True,
)
def task_update_prices():
    """
    Saves latest image from Flickr
    """
    update_prices()"""


@task(name='update_prices')
def task_update_prices():
    """
    Saves latest image from Flickr
    """
    update_prices()
