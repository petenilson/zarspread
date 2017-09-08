from django.views.generic import TemplateView
from home_page.models import Tick

class HomeView(TemplateView):
    template_name = 'home_page.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        # Get the List of Habits for a User
        recent_tick = Tick.objects.order_by('-id')[0]

        context['USDZAR'] = recent_tick.USDZAR
        context['XBTZAR'] = recent_tick.XBTZAR
        context['XBTUSD'] = recent_tick.XBTUSD

        # calculate the spread
        spread = (((1/recent_tick.XBTUSD) * recent_tick.XBTZAR) / recent_tick.USDZAR) - 1
        context['SPREAD'] = round(spread*100, 1)
        return context
