from django.contrib import admin
from .models import Reader, Day, Mess


class ReaderAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'wants_lection',
        'wants_psalm',
        'wants_believers_pray',
        'owner'
    ]


class DayAdmin(admin.ModelAdmin):
    fields = [
        'date',
        'second_lection_exist',
        'owner'
    ]


class MessAdmin(admin.ModelAdmin):
    fields = [
        'day',
        'hour',
        'first_lection',
        'second_lection',
        'psalm',
        'believers_pray'
    ]


admin.site.register(Reader, ReaderAdmin)
admin.site.register(Day, DayAdmin)
admin.site.register(Mess, MessAdmin)
