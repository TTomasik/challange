from django.contrib import admin
from star_wars.models import CSVFileData


class AdminCSVFileData(admin.ModelAdmin):
    list_display = ('filename', 'date')


admin.site.register(CSVFileData, AdminCSVFileData)
