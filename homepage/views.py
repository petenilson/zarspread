from django.views.generic import TemplateView
from django.utils import timezone

from datetime import timedelta
from itertools import groupby
import json

from homepage.models import Tick


class HomeView(TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        recent_tick = Tick.objects.order_by('-id')[0]

        rates = {
            'usdzar': recent_tick.USDZAR,
            'xbtzar': recent_tick.XBTZAR,
            'xbtusd': recent_tick.XBTUSD,
        }
        spread = recent_tick.spread
        last_24hrs = Tick.objects.filter(
            created__gte=timezone.now() - timedelta(hours=24)
        )
        time_frmt = '%Y-%m-%d-%HT'
        historical = []
        for date, group in groupby(last_24hrs, lambda x: x.created.strftime(time_frmt)):
            historical.append(
                {
                    'date': date,
                    'high': max([e.spread for e in group]),
                }
            )

        context['data'] = rates
        context['data'].update(
            {
                'spread': round(spread*100, 1),
                'historical': historical,
            }
        )

        return context
