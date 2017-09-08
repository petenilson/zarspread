from __future__ import absolute_import, unicode_literals
import random
from celery.decorators import task
from utils import update_prices

@task(name="update_prices")
def update():
    update_prices()
