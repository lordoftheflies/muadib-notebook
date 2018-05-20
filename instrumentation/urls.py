from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from instrumentation import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'equipments', views.EquipmentViewSet)
router.register(r'processes', views.ProcessViewSet)
router.register(r'executions', views.ExecutionViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    url(r'^api/', include(router.urls)),
    # url(r'^api/resources/active/$', views.active_resources_view),
    # url(r'^api/ping/(?P<resource_name>[a-z0-9]+)/$', views.ping_view),
]