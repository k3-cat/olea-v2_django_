from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework import routers

from commits.views import CommitsView
from projects.views import ProjectView
from users.views import UserView
from works.views import WorkView

router = routers.SimpleRouter()

router.register(r'^users', UserView, basename='users')
router.register(r'^projects', ProjectView)
router.register(r'^works', WorkView, basename='works')
router.register(r'^commits', CommitsView, basename='commits')

urlpatterns = router.get_urls()
if settings.DEBUG:
    urlpatterns += static(settings.AP_URL, document_root=settings.AP_ROOT)
    urlpatterns += static(settings.CF_URL, document_root=settings.CF_ROOT)
