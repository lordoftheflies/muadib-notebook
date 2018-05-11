from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from instrumentation import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'schemas', views.SchemaViewSet)
router.register(r'equipments', views.EquipmentViewSet)
router.register(r'terminal', views.ConsoleViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/resources/active/$', views.active_resources_view),
]