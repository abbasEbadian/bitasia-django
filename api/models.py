import decimal

from django.db import models


class RoundedDecimalField(models.DecimalField):

    def __init__(self, *args, **kwargs):
        super(RoundedDecimalField, self).__init__(*args, **kwargs)
        self.decimal_ctx = decimal.Context(prec=self.decimal_places, rounding=decimal.ROUND_HALF_UP)

    def pre_save(self, model_instance, add):
        """Return field's value just before saving."""
        value = getattr(model_instance, self.attname)
        if isinstance(value, decimal.Decimal):
            return decimal.Decimal(value).quantize(decimal.Decimal("0.00001"), rounding=decimal.ROUND_HALF_UP)
        return getattr(model_instance, self.attname)
