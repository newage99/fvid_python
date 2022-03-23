import sys
from commands.Command import Command
from symbols.Symbol import Symbol
from symbols.Variable import Variable
from symbols.Function import Function
from AdjacencyMatrix import AdjacencyMatrix


def __get_symbols_list(fvid) -> list:
    fvid_str_list = fvid.split(" ")
    symbols = Symbol.symbols_dict()
    str_symbols = symbols.keys()
    fvid_symbols = []
    for str_symbol in fvid_str_list:
        if str_symbol not in str_symbols:
            raise Exception(f"Invalid symbol: {str_symbol}")
        fvid_symbols.append(symbols[str_symbol] if str_symbol in str_symbols else str_symbol)
    return fvid_symbols


def __compute_connection(symbols, variables_strs, functions_strs, x, y, number_of_nodes) -> bool:
    dimensional_results = [[]]
    for symbol in symbols:
        symbol_str = symbol.symbol()
        if symbol_str in variables_strs:
            dimensional_results[-1].append(symbol.compute(x, y, number_of_nodes))
        elif symbol_str in functions_strs:
            dimensional_results[-1] = [symbol.compute(dimensional_results[-1])]
        elif symbol_str == "(":
            dimensional_results.append([])
        elif symbol_str == ")":
            dimensional_results[-2].append(dimensional_results[-1][0])
            dimensional_results.pop()
    return dimensional_results[0][0] > 0


def __generate_adjacency_matrix(fvid, number_of_nodes) -> AdjacencyMatrix:
    symbols = __get_symbols_list(fvid)
    variables = Variable.symbols_strs()
    functions = Function.symbols_strs()
    adjacency_matrix = AdjacencyMatrix(number_of_nodes)
    for x in range(number_of_nodes - 1):
        for y in range(x + 1, number_of_nodes):
            are_nodes_connected = __compute_connection(symbols, variables, functions, x, y, number_of_nodes)
            if are_nodes_connected:
                adjacency_matrix.connect(x, y)
    return adjacency_matrix


def interpret(fvid, number_of_nodes):
    adjacency_matrix = __generate_adjacency_matrix(fvid, number_of_nodes)
    from DegreeDiameterCalculator import DegreeDiameterCalculator
    result = DegreeDiameterCalculator.calculate(adjacency_matrix.get_matrix())

    if result:
        print()


class Analyze1Command(Command):

    @staticmethod
    def str_to_execute_command():
        return "analyze1"

    @staticmethod
    def description():
        return "Analyzes degree and diameter properties of topologies."

    @staticmethod
    def print_help():
        pass

    @staticmethod
    def execute(arguments):
        interpret("x ( x y % ) n +", 4)


if __name__ == '__main__':
    Analyze1Command.execute(sys.argv[1:])
