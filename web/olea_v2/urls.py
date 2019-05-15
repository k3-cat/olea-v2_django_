from django.urls import path
from rest_framework import routers

from users.views import UserAPIView, UserNAPIView
from works.views import WorkAPIView, WorkCAPIView
from projects.views import ProjectAPIView, ProjectNAPIView
from storages.views import StorageAPIViewSet
from o3o_auth.views import login_views

router = routers.DefaultRouter()

router.register(r'users', UserAPIView)
router.register(r'users_', UserNAPIView)
router.register(r'projects', ProjectAPIView)
router.register(r'projects_', ProjectNAPIView)
router.register(r'works', WorkAPIView)
router.register(r'works-', WorkCAPIView)
router.register(r'storages', StorageAPIViewSet)

urlpatterns = router.get_urls() + [path('auth/login', login_views)]
