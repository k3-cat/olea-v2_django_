from users.models import User as UserModel


class CBackend:
    def authenticate(self, request, name=None, password=None):
        try:
            user = UserModel.objects.get(name)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and user.is_active:
                return user
        raise PermissionError

    def get_user(self, uid):
        try:
            user = UserModel.objects.get(uid=uid)
        except UserModel.DoesNotExist:
            return None
        if user.is_active:
            return user
