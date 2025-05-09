from django.db import models
from django.utils.translation import gettext as _


class Record(models.Model):
    image = models.ImageField(_("Image"), upload_to="art/img", max_length=255)
    album = models.CharField(_("Album"), max_length=255, db_index=True)

    def __str__(self):
        return ("{}").format(self.image)

    class Meta:
        verbose_name_plural = "Records"
        ordering = ["album", "image"]
