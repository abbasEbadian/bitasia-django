class IsAdminRequestMixin:

    def has_admin_header(self, META, *args, **kwargs):
        return META.get("HTTP_X_AMGEZI", "ABI") == "GERMEZI"
