from rest_framework import routers
from users.views import UserAPIViewSet
from works.views import WorkAPIViewSet
from projects.views import ProjectAPIViewSet
from storages.views import StorageAPIViewSet

router = routers.DefaultRouter()

router.register(r'users', UserAPIViewSet)
router.register(r'projects', ProjectAPIViewSet)
router.register(r'works', WorkAPIViewSet)
router.register(r'storages', StorageAPIViewSet)

urlpatterns = router.get_urls()
