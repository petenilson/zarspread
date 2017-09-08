from django.db import models


class Tick(models.Model):
    date_time = models.DateTimeField(auto_now_add=True)
    # price of BTC in ZAR
    XBTZAR = models.FloatField()
    # price of BTC in ZAR
    XBTUSD = models.FloatField()
    # price of USD in ZAR
    USDZAR = models.FloatField()

    class Meta:
        verbose_name = "Tick"
        verbose_name_plural = "Ticks"
