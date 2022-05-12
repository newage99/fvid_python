import threading

from django.core.validators import MinValueValidator
from django.db import models


class AnalyzeRun(models.Model):

    fvid_length = models.PositiveIntegerField(null=False, blank=False, validators=[MinValueValidator(1)])

    number_of_nodes = models.PositiveIntegerField(null=False, blank=False, validators=[MinValueValidator(1)])

    upload_frequency = models.PositiveIntegerField(null=False, blank=False, validators=[MinValueValidator(1)],
                                                   default=1000)

    number_of_analyzed_fvids = models.PositiveIntegerField(null=False, blank=False, default=0)

    next_fvid_to_analyze = models.TextField(null=True, blank=True)

    percentage = models.FloatField(null=False, blank=False, default=0.0)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    completed_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        from .services import run_analyze
        t = threading.Thread(target=run_analyze, args=[self])
        t.setDaemon(True)
        t.start()


class AdjacencyMatrixDiscoveredOnRun(models.Model):

    adjacency_matrix = models.ForeignKey("adjacency_matrix.AdjacencyMatrix", null=False, blank=False,
                                         on_delete=models.CASCADE)

    run = models.ForeignKey("runs.AnalyzeRun", null=False, blank=False, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('adjacency_matrix', 'run')
