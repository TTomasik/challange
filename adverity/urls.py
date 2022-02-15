"""adverity URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework import routers

from star_wars.views import CSVFileDataView, PeopleView, StarWarsView, ValueCountView

router = routers.SimpleRouter()
router.register(r'api/fetch_newest_collection', StarWarsView, 'fetch-newest-collection')
router.register(r'api/csv_files', CSVFileDataView, 'csv-files')
router.register(r'api/people', PeopleView, 'people')
router.register(r'api/value_count', ValueCountView, 'people')

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += router.urls
