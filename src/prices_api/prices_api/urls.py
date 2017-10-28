from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^profiles/', include('profiles.urls')),
    url(r'^prices/', include('prices.urls'))
]
