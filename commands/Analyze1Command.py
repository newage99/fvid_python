import sys
import time
from commands.Command import Command
from symbols.Symbol import Symbol
from symbols.Variable import Variable
from symbols.Function import Function
from AdjacencyMatrix import AdjacencyMatrix
from FvidGenerator import FvidGenerator
from DegreeDiameterCalculator import DegreeDiameterCalculator


class Analyze1Command(Command):

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def __generate_adjacency_matrix(symbols, number_of_nodes) -> AdjacencyMatrix:
        # symbols = __get_symbols_list(fvid)
        variables = Variable.symbols_strs()
        functions = Function.symbols_strs()
        adjacency_matrix = AdjacencyMatrix(number_of_nodes)
        for x in range(number_of_nodes - 1):
            for y in range(x + 1, number_of_nodes):
                are_nodes_connected = Analyze1Command.__compute_connection(symbols, variables, functions, x, y, number_of_nodes)
                if are_nodes_connected:
                    adjacency_matrix.connect(x, y)
        return adjacency_matrix

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
        length = 7
        print("")
        print(f"FVid length: {length}")
        fvids = FvidGenerator.generate(length)
        number_of_nodes_list = [10]
        for number_of_nodes in number_of_nodes_list:
            print("")
            print(f"Testing for {number_of_nodes} nodes...")
            results = []
            percentage = 0
            len_fvids = len(fvids)
            for i in range(len(fvids)):
                fvid = fvids[i]
                current_percentage = int((i / len_fvids) * 100)
                if current_percentage > percentage:
                    print(f"{current_percentage}%")
                    percentage = current_percentage
                fvid_str = " ".join([str(s) for s in fvid])
                adjacency_matrix = Analyze1Command.__generate_adjacency_matrix(fvid, number_of_nodes)
                scores = DegreeDiameterCalculator.calculate(adjacency_matrix.get_matrix())
                if scores:
                    simple_score = scores[0] + scores[1]
                    total_score = scores[2] + scores[3]
                    inserted = False
                    for i in range(len(results)):
                        result = results[i]
                        list_simple = result[2] + result[3]
                        list_total = result[4] + result[5]
                        if simple_score < list_simple  or (simple_score == list_simple and total_score < list_total):
                            results.insert(i, [fvid_str, total_score, scores[0], scores[1], scores[2], scores[3]])
                            inserted = True
                            break
                    if not inserted:
                        results.append([fvid_str, total_score, scores[0], scores[1], scores[2], scores[3]])
                time.sleep(0.001)
            print(f"Connected fvids: {len(results)}")
            print("")
            len_results = len(results)
            for i in range(20):
                if i - 1 > len_results:
                    break
                result = results[i]
                result = [str(r) for r in result]
                print(' | '.join(result))


if __name__ == '__main__':
    Analyze1Command.execute(sys.argv[1:])
