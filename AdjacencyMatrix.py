class AdjacencyMatrix:

    def __init__(self, number_of_nodes):
        self.__number_of_nodes = number_of_nodes
        self.__matrix = []
        for i in range(number_of_nodes):
            self.__matrix.append([0] * number_of_nodes)

    def connect(self, x, y):
        if x != y:
            self.__matrix[x][y] = 1
            self.__matrix[y][x] = 1

    def print(self):
        for i in range(self.__number_of_nodes):
            for j in range(self.__number_of_nodes):
                if i < j:
                    print(self.__matrix[i][j], end='')
            print('')

    def get_matrix(self):
        return self.__matrix
