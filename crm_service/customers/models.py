from django.db import models
from django.db.models import BooleanField
from django.utils.translation import gettext_lazy as _

from utils.mixins import TimestampMixin
from leads.models import Lead


class Customer(TimestampMixin, models.Model):
    """Активный клиент пользующийся услугами компаний."""

    lead: Lead = models.OneToOneField(
        to=Lead,
        on_delete=models.PROTECT,
        related_name="customer",
        verbose_name=_("Lead"),
    )
    is_active: BooleanField = models.BooleanField(
        default=True,
        verbose_name=_("Is Active"),
    )

    def __str__(self) -> str:
        return f"Customer: {self.lead.full_name}"
