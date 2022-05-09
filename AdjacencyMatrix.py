from backend.adjacency_matrix.models import AdjacencyMatrix


class AdjacencyMatrixClass:

    def __init__(self, number_of_nodes):
        self.__number_of_nodes = number_of_nodes
        self.__matrix = []
        triangular_number = (number_of_nodes * (number_of_nodes - 1)) / 2
        self.__connections = [0 for i in range(triangular_number)]
        for i in range(number_of_nodes):
            self.__matrix.append([0] * number_of_nodes)

    def connect(self, x, y):
        if x != y and self.__matrix[x][y] != 1:
            self.__matrix[x][y] = 1
            self.__matrix[y][x] = 1

            small_index = x if x < y else y
            big_index = x if small_index != x else y
            index = 0

            for i in range(self.__number_of_nodes - 1):
                for j in range(i + 1, self.__number_of_nodes):
                    if i == small_index and j == big_index:
                        self.__connections[index] = 1
                        break

    def print(self):
        for i in range(self.__number_of_nodes):
            for j in range(self.__number_of_nodes):
                if i < j:
                    print(self.__matrix[i][j], end='')
            print('')

    def get_matrix(self):
        return self.__matrix

    def get_connections_str(self):
        return ','.join(self.__connections)

    @staticmethod
    def upload_adjacency_matrices(adjacency_matrices_dict, number_of_nodes):

        uploaded_matrices = []

        for key in adjacency_matrices_dict:

            element = adjacency_matrices_dict[key]

            if element and "matrix_uploaded" in element and not element["matrix_uploaded"]:

                obj, created = AdjacencyMatrix.objects.get_or_create(value=key, number_of_nodes=number_of_nodes)
                if created:
                    uploaded_matrices.append({
                        "django_object": obj,
                        "adjacency_matrix": element
                    })

        return uploaded_matrices
