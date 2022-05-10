from django.db import models


class AdjacencyMatrix(models.Model):

    value = models.TextField(null=False, blank=False)

    number_of_nodes = models.PositiveIntegerField(null=False, blank=False)


class FVIDAdjacencyMatrix(models.Model):

    fvid = models.ForeignKey("fvid.FVID", null=False, blank=False, on_delete=models.CASCADE)

    adjacency_matrix = models.ForeignKey(AdjacencyMatrix, null=False, blank=False, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('fvid', 'adjacency_matrix')
