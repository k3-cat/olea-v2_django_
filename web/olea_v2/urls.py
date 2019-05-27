from django.urls import path
from rest_framework import routers

from users.views import UserAPIView
from works.views import WorkAPIView
from projects.views import ProjectAPIView
from o3o_auth.views import login_views

router = routers.SimpleRouter()

router.register(r'users', UserAPIView)
router.register(r'projects', ProjectAPIView)
router.register(r'works', WorkAPIView)

urlpatterns = router.get_urls() + [path('auth/login', login_views)]
