from django.core.validators import MinValueValidator
from django.db import models


class AnalyzeRun(models.Model):

    fvid_length = models.PositiveIntegerField(null=False, blank=False, validators=[MinValueValidator(1)])

    number_of_nodes = models.PositiveIntegerField(null=False, blank=False, validators=[MinValueValidator(1)])

    upload_frequency = models.PositiveIntegerField(null=False, blank=False, validators=[MinValueValidator(1)],
                                                   default=1000)

    next_fvid_to_analyze = models.TextField(null=True, blank=True)

    percentage = models.FloatField(null=False, blank=False, default=0.0)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    completed_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):

        arguments_dict = {
            "fvid_length": self.fvid_length,
            "number_of_nodes": self.number_of_nodes,
            "upload_frequency": self.upload_frequency
        }
        if self.next_fvid_to_analyze:
            arguments_dict["start_fvid"] = self.next_fvid_to_analyze
        from commands.Analyze1Command import Analyze1Command
        Analyze1Command.execute(arguments_dict)
