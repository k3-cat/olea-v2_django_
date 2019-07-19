from django.urls import path
from rest_framework import routers

from users.views import UserView
from works.views import WorkView
from projects.views import ProjectView
from commits.views import CommitsView

router = routers.SimpleRouter()

router.register(r'^users', UserView, basename='users')
router.register(r'^projects', ProjectView)
router.register(r'^works', WorkView, basename='works')
router.register(r'^commits', CommitsView, basename='commits')

urlpatterns = router.get_urls()
