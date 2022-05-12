from django.contrib import admin

from core.services import create_admin_change_link

from .models import DegreeDiameterResult


@admin.register(DegreeDiameterResult)
class DegreeDiameterResultAdmin(admin.ModelAdmin):

    list_display = ['_adjacency_matrix', '_fvids', 'connected', 'degree', 'diameter', 'simple_score', 'total_score',
                    '_runs']
    list_filter = ['connected']

    def _adjacency_matrix(self, obj):
        if obj and obj.adjacency_matrix:
            matrix = obj.adjacency_matrix
            return create_admin_change_link("adjacency_matrix_adjacencymatrix_change", matrix.id, matrix.value)
        return "-"

    def _fvids(self, obj):
        if obj and obj.adjacency_matrix:
            from adjacency_matrix.models import FVIDAdjacencyMatrix
            matrix = obj.adjacency_matrix
            fvids = FVIDAdjacencyMatrix.objects.filter(adjacency_matrix=matrix).values_list('fvid', flat=True)
            max_fvids = 2
            return_fvids = fvids[:max_fvids]
            return_value = ', '.join(return_fvids)
            len_fvids = len(fvids)
            if len_fvids > max_fvids:
                return_value += f" ... ({str(len_fvids - max_fvids)} more)"
            return return_value
        return ''

    def _runs(self, obj):
        if obj and obj.adjacency_matrix:
            from runs.models import AdjacencyMatrixDiscoveredOnRun
            values = AdjacencyMatrixDiscoveredOnRun.objects.filter(adjacency_matrix=obj.adjacency_matrix) \
                .values_list('run', flat=True)
            if len(values) > 0:
                values = [str(value) for value in values]
                return f"#{', #'.join(values)}"
        return ''
