class AdjacencyMatrix:

    def __init__(self, number_of_nodes):
        self.__number_of_nodes = number_of_nodes
        self.__matrix = []
        for i in range(number_of_nodes):
            self.__matrix.append([0] * number_of_nodes)

    def connect(self, x, y):
        first_access = x
        second_access = y
        if x > y:
            first_access = y
            second_access = x
        self.__matrix[first_access][second_access] = 1

    def print(self):
        for i in range(self.__number_of_nodes):
            for j in range(self.__number_of_nodes):
                if i < j:
                    print(self.__matrix[i][j], end='')
            print('')
