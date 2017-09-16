from django.db import models


class Tick(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    spread = models.FloatField(blank=True)
    # price of BTC in ZAR
    XBTZAR = models.FloatField()
    # price of BTC in ZAR
    XBTUSD = models.FloatField()
    # price of USD in ZAR
    USDZAR = models.FloatField()

    def calc_spread(self):
        spread = (((1/self.XBTUSD) * self.XBTZAR) / self.USDZAR) - 1
        return round(spread, 5)

    def save(self, *args, **kwargs):
        self.spread = self.calc_spread()
        super(Tick, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Tick"
        verbose_name_plural = "Ticks"
