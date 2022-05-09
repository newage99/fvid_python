import sys
import time
from commands.Command import Command
from symbols.Symbol import Symbol
from symbols.Variable import Variable
from symbols.Function import Function
from AdjacencyMatrix import AdjacencyMatrixClass
from FvidGenerator import FvidGenerator
from DegreeDiameterCalculator import DegreeDiameterCalculator

from backend.adjacency_matrix.models import AdjacencyMatrix
from backend.adjacency_matrix.models import FVIDAdjacencyMatrix
from backend.fvid.models import FVID
from backend.results.models import DegreeDiameterResult


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
    def __generate_adjacency_matrix(symbols, number_of_nodes) -> AdjacencyMatrixClass:
        variables = Variable.symbols_strs()
        functions = Function.symbols_strs()
        adjacency_matrix = AdjacencyMatrixClass(number_of_nodes)
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
    def upload_degree_diameter_results(uploaded_matrices):

        for uploaded_matrix in uploaded_matrices:

            django_object = uploaded_matrix["django_object"]
            adjacency_matrix = uploaded_matrix["adjacency_matrix"]
            connected = adjacency_matrix["connected"] if "connected" in adjacency_matrix else False
            degree = diameter = total_degree = total_diameter = None

            if connected and "scores" in adjacency_matrix:
                scores = adjacency_matrix["scores"]
                degree = scores["degree"] if "degree" in scores else None
                diameter = scores["diameter"] if "diameter" in scores else None
                total_degree = scores["total_degree"] if "total_degree" in scores else None
                total_diameter = scores["total_diameter"] if "total_diameter" in scores else None

            DegreeDiameterResult.objects.get_or_create(adjacency_matrix=django_object, connected=connected,
                                                       degree=degree, diameter=diameter, total_degree=total_degree,
                                                       total_diameter=total_diameter)

    @staticmethod
    def upload_fvids(results):

        for key in results:
            element = results[key]
            adjacency_matrix_obj = AdjacencyMatrix.objects.get(value=key)
            if element and "fvids" in element:
                for fvid in element["fvids"]:
                    fvid, created = FVID.objects.get_or_create(value=fvid)
                    FVIDAdjacencyMatrix.objects.get_or_create(fvid=fvid, adjacency_matrix=adjacency_matrix_obj)

    @staticmethod
    def upload_results(results, number_of_nodes):

        # Step 1: Upload 'AdjacencyMatrix' objects
        uploaded_matrices = AdjacencyMatrixClass.upload_adjacency_matrices(results, number_of_nodes)

        # Step 2: Upload 'DegreeDiameterResult' objects
        Analyze1Command.upload_degree_diameter_results(uploaded_matrices)

        # Step 3: Upload
        Analyze1Command.upload_fvids(results)

    @staticmethod
    def execute(arguments):
        if arguments is None or "fvid_length" not in arguments or "number_of_nodes" not in arguments or \
                "upload_frequency" not in arguments:
            print("Invalid arguments.")
            return

        fvid_length = arguments["fvid_length"]
        number_of_nodes = arguments["number_of_nodes"]
        upload_frequency = arguments["upload_frequency"]
        start_fvid = arguments["start_fvid"] if "start_fvid" in arguments else None
        print("")
        print(f"FVid length: {fvid_length}")

        fvids = FvidGenerator.generate(fvid_length, start_fvid)

        print("")
        print(f"Testing for {number_of_nodes} nodes...")
        results = []
        percentage = 0
        len_fvids = len(fvids)

        ams = {}
        ams_to_upload = {}
        fvids_to_upload_counter = 0

        for i in range(len(fvids)):
            fvid = fvids[i]
            current_percentage = int((i / len_fvids) * 100)
            if current_percentage > percentage:
                print(f"{current_percentage}%")
                percentage = current_percentage

            fvid_str = " ".join([str(s) for s in fvid])
            fvids_to_upload_counter += 1

            adjacency_matrix = Analyze1Command.__generate_adjacency_matrix(fvid, number_of_nodes)
            connections = adjacency_matrix.get_connections_str()

            if connections in ams_to_upload:
                ams_to_upload[connections]["fvids"].append(fvid_str)
            else:
                ams_to_upload[connections] = {"fvids": [fvid_str]}
                ams_to_upload[connections]["matrix_uploaded"] = connections in ams and "matrix_uploaded" in ams and ams[connections]["matrix_uploaded"]

            if connections in ams:
                is_new_matrix = False
                ams[connections]["fvids"].append(fvid_str)
            else:
                is_new_matrix = True
                ams[connections] = {"fvids": [fvid_str]}

            if is_new_matrix:
                scores = DegreeDiameterCalculator.calculate(adjacency_matrix.get_matrix())
                if scores:
                    scores = {
                        "degree": scores[0],
                        "diameter": scores[1],
                        "total_degree": scores[2],
                        "total_diameter": scores[3]
                    }
                    ams[connections]["connected"] = True
                    ams[connections]["scores"] = scores
                    ams_to_upload[connections]["connected"] = True
                    ams_to_upload[connections]["scores"] = scores
                else:
                    ams[connections]["connected"] = False
                    ams_to_upload[connections]["connected"] = False

            if fvids_to_upload_counter >= upload_frequency:
                Analyze1Command.upload_results(ams_to_upload, number_of_nodes)
                for key in ams_to_upload:
                    ams[key]["matrix_uploaded"] = True
                ams_to_upload = {}

            time.sleep(0.0001)

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
