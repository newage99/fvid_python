from django.db import models


class FVID(models.Model):

    value = models.TextField(null=False, blank=False, primary_key=True)
