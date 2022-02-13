from django.conf import settings
from django.db import models
from django.utils.dateformat import format


class CSVFileData(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=50)

    @property
    def representation_name(self):
        return format(self.date, settings.DATETIME_FORMAT)

    @property
    def csv_name(self):
        return f'{self.filename}_{self.id}.csv'
