from django.db import models
from django.utils.translation import gettext as _


class Record(models.Model):
    code = models.CharField(_("Code"), max_length=255, primary_key=True)
    title = models.CharField(_("Title"), max_length=255)
    text = models.TextField(_("Text"))

    def __str__(self):
        return ("{}").format(self.title)

    class Meta:
        verbose_name_plural = "Records"
        ordering = ["code"]
