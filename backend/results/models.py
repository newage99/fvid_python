from django.db import models


class DegreeDiameterResult(models.Model):

    adjacency_matrix = models.OneToOneField("adjacency_matrix.AdjacencyMatrix", null=False, blank=False,
                                            on_delete=models.CASCADE)

    connected = models.BooleanField(null=False, blank=False, default=False)

    degree = models.PositiveIntegerField(null=True, blank=True)

    diameter = models.PositiveIntegerField(null=True, blank=True)

    total_degree = models.PositiveIntegerField(null=True, blank=True)

    total_diameter = models.PositiveIntegerField(null=True, blank=True)
