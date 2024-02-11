from django.db import models
from django.utils.translation import gettext as _

from authority.models import BaseModelWithDate


def get_file_path_for_icon(instance, filename):
    ext = filename.split('.')[-1]
    filename = "images/avatars/%s.%s" % (instance.name, ext)
    return filename


class CurrencyKey:
    IRT = "IRT"
    

class Currency(BaseModelWithDate):
    name = models.CharField(_('Name'))
    symbol = models.CharField(_('Symbol'))
    icon = models.ImageField(_('Icon'), upload_to=get_file_path_for_icon)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')
