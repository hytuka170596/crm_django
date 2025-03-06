from django.db import models
from django.db.models import BooleanField
from django.utils.translation import gettext_lazy as _

from utils.mixins import TimestampMixin, ActorMixin
from leads.models import Lead


# Менеджер может создавать, просматривать и редактировать контракты, смотреть потенциальных клиентов и переводить их в активных.
class Customer(TimestampMixin, ActorMixin, models.Model):
    """Активный клиент пользующийся услугами компаний."""

    lead: Lead = models.OneToOneField(
        to=Lead,
        on_delete=models.PROTECT,
        related_name="customer",
        verbose_name=_("Lead"),
    )
    archived: bool = models.BooleanField(
        default=False, verbose_name=_("Archived"), db_default=None
    )

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")
        ordering = (
            "pk",
            "-created_at",
        )

    def __str__(self) -> str:
        return f"Customer: {self.lead.full_name}"
