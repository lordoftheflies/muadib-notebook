from django.conf.urls import url
from django.contrib.staticfiles.views import serve
from django.views.generic import TemplateView

urlpatterns = [

    url(r'^service-worker.js$', serve, kwargs={
        'path': 'service-worker.js'
    }, name='service-worker'),

    url(r'^src/(?P<path>/.html)$', serve),

    url(r'^$', TemplateView.as_view(template_name="presentation/spa.html"), name='home'),

]
