from django.contrib import admin

from core.services import create_admin_change_link

from .models import AdjacencyMatrix
from .models import FVIDAdjacencyMatrix


@admin.register(AdjacencyMatrix)
class AdjacencyMatrixAdmin(admin.ModelAdmin):

    list_display = ['value', 'number_of_nodes']


@admin.register(FVIDAdjacencyMatrix)
class FVIDAdjacencyMatrixAdmin(admin.ModelAdmin):

    list_display = ['_fvid', '_adjacency_matrix']

    def _fvid(self, obj):
        if obj and obj.adjacency_matrix:
            fvid = obj.fvid
            return create_admin_change_link("fvid_fvid_change", fvid.value, fvid.value)
        return "-"

    def _adjacency_matrix(self, obj):
        if obj and obj.adjacency_matrix:
            matrix = obj.adjacency_matrix
            return create_admin_change_link("adjacency_matrix_adjacencymatrix_change", matrix.id, matrix.value)
        return "-"
