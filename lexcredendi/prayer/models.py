from django.db import models
from django.utils.translation import gettext as _


class Record(models.Model):
    code = models.CharField(_("Code"), max_length=255, primary_key=True)
    title = models.CharField(_("Title"), max_length=255)
    text = models.TextField(_("Text"))
    latin_title = models.CharField(
        _("Latin Title"), max_length=255, blank=True, null=True
    )
    latin_text = models.TextField(
        _("Latin Text"), blank=True, null=True
    )  # Using TextField

    def __str__(self):
        return ("{}").format(self.title)

    class Meta:
        verbose_name_plural = "Records"
        ordering = ["code"]
