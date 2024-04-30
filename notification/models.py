from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

from exchange.models import BaseModel

User = get_user_model()


class NotificationManger(models.Manager):
    def _create_global(self, title, content):
        return self.create(title=title, content=content, type=Notification.NotificationType.GLOBAL)

    def _create_for_user(self, user, title, content):
        return self.create(user_id=user, title=title, content=content)

    def create_for_users(self, users, title, content):
        if not users:
            return self._create_global(title=title, content=content)
        for user in users:
            self._create_for_user(user, title, content)

    def for_user(self, user, exclude_seen=False):
        user_qs = user.notifications.all()
        all_qs = Notification.objects.filter(type=Notification.NotificationType.GLOBAL)
        if exclude_seen:
            user_qs = user_qs.exclude(seen_user_ids=user)
            all_qs = all_qs.exclude(seen_user_ids=user)
        return user_qs | all_qs


class Notification(BaseModel):
    class NotificationType(models.TextChoices):
        GLOBAL = 'global', "Global Notification"
        USER = 'user', "User Notification"

    type = models.CharField(choices=NotificationType.choices, default=NotificationType.USER)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications", blank=True, null=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    # to handle `seen` for both of types, we use many2many
    seen_user_ids = models.ManyToManyField(User, related_name='seen_users', blank=True)

    objects = NotificationManger()

    def __str__(self):
        return f"{self.title}"

    class Meta:
        ordering = ("-id",)
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
