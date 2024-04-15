from api.const import MODERATOR_VALUE, MODERATOR_FIELD


class IsModeratorMixin:

    def is_moderator(self, request):
        admin = request.user and request.user.is_staff
        return admin and request.headers.get(MODERATOR_FIELD, None) == MODERATOR_VALUE


class IsModeratorMixin:

    def is_moderator(self, request):
        admin = request.user and request.user.is_staff
        return admin and request.headers.get(MODERATOR_FIELD, None) == MODERATOR_VALUE
