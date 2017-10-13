import csv

from django.contrib import admin
from django.utils.encoding import smart_str
from django.http import HttpResponse

from homepage.models import Tick


class TickAdmin(admin.ModelAdmin):
    list_display = ['created', 'spread']
    actions = ['export_csv']

    def export_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=tickdata.csv'
        writer = csv.writer(response, csv.excel)
        writer.writerow([
            smart_str(u"Date"),
            smart_str(u"Spread"),
            smart_str(u"XBTUSD"),
            smart_str(u"XBTZAR"),
            smart_str(u"USDZAR"),
        ])
        for obj in queryset:
            writer.writerow([
                smart_str(obj.created),
                smart_str(obj.spread),
                smart_str(obj.XBTUSD),
                smart_str(obj.XBTZAR),
                smart_str(obj.USDZAR),
            ])
        return response


admin.site.register(Tick, TickAdmin)
