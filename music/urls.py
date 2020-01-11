from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.urls import reverse

urlpatterns = [

    path('',views.welcome,name='music'),#remove this line just checking something
]


if settings.DEBUG:
    urlpatterns +=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)