import sys
import time
from datetime import datetime

from adjacency_matrix.AdjacencyMatrix import AdjacencyMatrixClass
from adjacency_matrix.models import AdjacencyMatrix
from adjacency_matrix.models import FVIDAdjacencyMatrix

from fvid.FvidGenerator import FvidGenerator
from fvid.models import FVID

from results.models import DegreeDiameterResult

from runs.commands.Command import Command
from runs.DegreeDiameterCalculator import DegreeDiameterCalculator
from runs.models import AnalyzeRun

from symbols.Symbol import Symbol
from symbols.Variable import Variable
from symbols.Function import Function


class Analyze1Command(Command):

    am_total = 0
    dd_total = 0
    fv_total = 0
    up_total = 0

    gam_1 = 0
    gam_2 = 0
    gam_3 = 0
    gam_4 = 0
    gam_5 = 0

    cc_1 = 0
    cc_2 = 0
    cc_3 = 0
    cc_4 = 0
    cc_5 = 0

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
            # cc_1_1 = datetime.now()
            symbol_str = symbol.symbol()
            # cc_2_1 = datetime.now()
            # Analyze1Command.cc_1 += (cc_2_1 - cc_1_1).total_seconds()
            if symbol_str in variables_strs:
                dimensional_results[-1].append(symbol.compute(x, y, number_of_nodes))
                # cc_3_1 = datetime.now()
                # Analyze1Command.cc_2 += (cc_3_1 - cc_2_1).total_seconds()
            elif symbol_str in functions_strs:
                dimensional_results[-1] = [symbol.compute(dimensional_results[-1])]
                # cc_4_1 = datetime.now()
                # Analyze1Command.cc_3 += (cc_4_1 - cc_2_1).total_seconds()
            elif symbol_str == "(":
                dimensional_results.append([])
                # cc_5_1 = datetime.now()
                # Analyze1Command.cc_4 += (cc_5_1 - cc_2_1).total_seconds()
            elif symbol_str == ")":
                dimensional_results[-2].append(dimensional_results[-1][0])
                dimensional_results.pop()
                # cc_6_1 = datetime.now()
                # Analyze1Command.cc_5 += (cc_6_1 - cc_2_1).total_seconds()
        return dimensional_results[0][0] > 0

    @staticmethod
    def __generate_adjacency_matrix(symbols, number_of_nodes) -> AdjacencyMatrixClass:

        # gam_1_1 = datetime.now()

        variables = Variable.symbols_strs()

        # gam_2_1 = datetime.now()
        # Analyze1Command.gam_1 += (gam_2_1 - gam_1_1).total_seconds()

        functions = Function.symbols_strs()

        # gam_3_1 = datetime.now()
        # Analyze1Command.gam_2 += (gam_3_1 - gam_2_1).total_seconds()

        adjacency_matrix = AdjacencyMatrixClass(number_of_nodes)

        # gam_4_1 = datetime.now()
        # Analyze1Command.gam_3 += (gam_4_1 - gam_3_1).total_seconds()

        for x in range(number_of_nodes - 1):
            for y in range(x + 1, number_of_nodes):
                # gam_5_0 = datetime.now()
                are_nodes_connected = Analyze1Command.__compute_connection(symbols, variables, functions, x, y, number_of_nodes)
                # gam_5_1 = datetime.now()
                # Analyze1Command.gam_4 += (gam_5_1 - gam_5_0).total_seconds()
                if are_nodes_connected:
                    adjacency_matrix.connect(x, y)
                # gam_6_1 = datetime.now()
                # Analyze1Command.gam_5 += (gam_6_1 - gam_5_1).total_seconds()
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
            degree = diameter = simple_score = total_degree = total_diameter = total_score = None

            if connected and "scores" in adjacency_matrix:
                scores = adjacency_matrix["scores"]
                degree = scores["degree"] if "degree" in scores else None
                diameter = scores["diameter"] if "diameter" in scores else None
                simple_score = degree + diameter
                total_degree = scores["total_degree"] if "total_degree" in scores else None
                total_diameter = scores["total_diameter"] if "total_diameter" in scores else None
                total_score = total_degree + total_diameter

            DegreeDiameterResult.objects.get_or_create(adjacency_matrix=django_object, connected=connected,
                                                       degree=degree, diameter=diameter, simple_score=simple_score,
                                                       total_degree=total_degree, total_diameter=total_diameter,
                                                       total_score=total_score)

    @staticmethod
    def upload_fvids(results):

        first_total = 0
        second_total = 0
        third_total = 0
        fourth_total = 0
        uploaded_fvids = 0
        # am_keys = list(results.keys())
        # ams = AdjacencyMatrix.objects.filter(value__in=am_keys)
        # ams_dict = {}
        # for am in ams:
        #     ams_dict[am.value] = am

        fvids = []
        fvid_ams = []

        for key in results:
            element = results[key]
            first_1 = datetime.now()
            adjacency_matrix_obj = AdjacencyMatrix.objects.get(value=key)
            second_1 = datetime.now()
            first_total += (second_1 - first_1).total_seconds()
            if element and "fvids" in element:
                for fvid in element["fvids"]:
                    fvid_ins = FVID(value=fvid)
                    fvids.append(fvid_ins)
                    fvid_ams.append(FVIDAdjacencyMatrix(fvid=fvid_ins, adjacency_matrix=adjacency_matrix_obj))
                    # fvid, created = FVID.objects.get_or_create(value=fvid)
                    # FVIDAdjacencyMatrix.objects.get_or_create(fvid=fvid, adjacency_matrix=adjacency_matrix_obj)
                    uploaded_fvids += 1

            # try:
            #     third_1 = datetime.now()
            #     second_total += (third_1 - second_1).total_seconds()
            #     if len(fvids) > 0:
            #         FVID.objects.bulk_create(fvids, ignore_conflicts=True)
            #     fourth_1 = datetime.now()
            #     third_total += (fourth_1 - third_1).total_seconds()
            #     if len(fvid_ams) > 0:
            #         FVIDAdjacencyMatrix.objects.bulk_create(fvid_ams, ignore_conflicts=True)
            #     fourth_2 = datetime.now()
            #     fourth_total += (fourth_2 - fourth_1).total_seconds()
            # except Exception as e:
            #     print(f"upload_fvids exception: {str(e)}")

        # print(f"first_total: {first_total}")
        # print(f"second_total: {second_total}")
        # print(f"third_total: {third_total}")
        # print(f"fourth_total: {fourth_total}")

        return uploaded_fvids

    @staticmethod
    def upload_results(results, number_of_nodes, next_fvid_to_analyze, number_of_analyzed_fvids,
                       number_of_analyzed_matrices, analyze_run_obj_f):

        am_1 = datetime.now()

        # Step 1: Upload 'AdjacencyMatrix' and 'AdjacencyMatrixDiscoveredOnRun' objects
        uploaded_matrices = AdjacencyMatrixClass.upload_adjacency_matrices(results, number_of_nodes, analyze_run_obj_f)

        dd_1 = datetime.now()
        Analyze1Command.am_total += (dd_1 - am_1).total_seconds()

        # Step 2: Upload 'DegreeDiameterResult' objects
        Analyze1Command.upload_degree_diameter_results(uploaded_matrices)

        fv_1 = datetime.now()
        Analyze1Command.dd_total += (fv_1 - dd_1).total_seconds()

        # Step 3: Upload 'FVID' and 'FVIDAdjacencyMatrix' objects
        Analyze1Command.upload_fvids(results)

        up_1 = datetime.now()
        Analyze1Command.fv_total += (up_1 - fv_1).total_seconds()

        analyze_run_obj_f.update(next_fvid_to_analyze=next_fvid_to_analyze,
                                 number_of_analyzed_fvids=number_of_analyzed_fvids,
                                 number_of_analyzed_matrices=number_of_analyzed_matrices)

        up_2 = datetime.now()
        Analyze1Command.up_total += (up_2 - up_1).total_seconds()

    @staticmethod
    def execute(arguments):
        try:
            mandatory_arguments = ["fvid_length", "number_of_nodes", "upload_frequency", "number_of_analyzed_fvids",
                                   "run_id"]
            for mandatory_argument in mandatory_arguments:
                if mandatory_argument not in arguments:
                    print(f"Missing argument: {mandatory_argument}")
                    return

            fvid_length = arguments["fvid_length"]
            number_of_nodes = arguments["number_of_nodes"]
            upload_frequency = arguments["upload_frequency"]
            # number_of_analyzed_fvids = arguments["number_of_analyzed_fvids"]
            run_id = arguments["run_id"]
            fvid_generator = FvidGenerator(length=fvid_length)
            start_fvid_str = arguments["start_fvid"] if "start_fvid" in arguments else None
            if start_fvid_str:
                fvid = fvid_generator.fvid_str_to_symbols_list(start_fvid_str)
            else:
                fvid = fvid_generator.get_first_fvid()
            ams = {}
            ams_to_upload = {}
            fvids_to_upload_counter = 0
            analyze_run_django_obj_f = AnalyzeRun.objects.filter(id=run_id)

            generate_am_total = 0
            misc_total = 0
            dd_calc_total = 0
            upload_total = 0
            get_next_fvid_total = 0
            lowest_simple_score = None
            lowest_total_score = None
            number_of_analyzed_fvids = analyze_run_django_obj_f[0].number_of_analyzed_fvids
            number_of_analyzed_matrices = analyze_run_django_obj_f[0].number_of_analyzed_matrices

            while fvid:

                generate_am_1 = datetime.now()

                fvid_str = " ".join([str(s) for s in fvid])
                fvids_to_upload_counter += 1
                adjacency_matrix = Analyze1Command.__generate_adjacency_matrix(fvid, number_of_nodes)
                connections = adjacency_matrix.get_connections_str()

                misc_1 = datetime.now()
                generate_am_total += (misc_1 - generate_am_1).total_seconds()

                number_of_analyzed_fvids += 1

                if connections in ams_to_upload:
                    if "scores" in ams_to_upload[connections]:
                        scores = ams_to_upload[connections]["scores"]
                        if scores["simple_score"] == lowest_simple_score and scores["total_score"] == lowest_total_score:
                            ams_to_upload[connections]["fvids"].append(fvid_str)
                else:
                    # ams_to_upload[connections] = {"fvids": [fvid_str]}
                    ams_to_upload[connections] = {
                        "matrix_uploaded": connections in ams and "matrix_uploaded" in ams[connections] and ams[connections]["matrix_uploaded"]
                    }

                if connections in ams:
                    is_new_matrix = False
                    ams[connections]["fvids"].append(fvid_str)
                else:
                    is_new_matrix = True
                    number_of_analyzed_matrices += 1
                    ams[connections] = {"fvids": [fvid_str]}

                dd_calc_1 = datetime.now()
                misc_total += (dd_calc_1 - misc_1).total_seconds()

                if is_new_matrix:
                    scores = DegreeDiameterCalculator.calculate(adjacency_matrix.get_matrix())
                    if scores:
                        simple_score = scores[0] + scores[1]
                        total_score = scores[2] + scores[3]
                        scores = {
                            "degree": scores[0],
                            "diameter": scores[1],
                            "total_degree": scores[2],
                            "total_diameter": scores[3],
                            "simple_score": simple_score,
                            "total_score": total_score
                        }
                        ams[connections]["connected"] = True
                        ams[connections]["scores"] = scores
                        ams_to_upload[connections]["connected"] = True
                        ams_to_upload[connections]["scores"] = scores
                        if lowest_simple_score is None or simple_score < lowest_simple_score or \
                                (simple_score == lowest_simple_score and total_score <= lowest_total_score):
                            ams_to_upload[connections]["fvids"] = [fvid_str]
                    else:
                        ams[connections]["connected"] = False
                        ams_to_upload[connections]["connected"] = False

                upload_1 = datetime.now()
                dd_calc_total += (upload_1 - dd_calc_1).total_seconds()

                if fvids_to_upload_counter >= upload_frequency:
                    fvids_to_upload_counter = 0

                    print(f"generate_am_total: {generate_am_total}")
                    print(f"misc_total: {misc_total}")
                    print(f"dd_calc_total: {dd_calc_total}")
                    print(f"upload_total: {upload_total}")
                    print(f"get_next_fvid_total: {get_next_fvid_total}")
                    # print(f"am_total: {Analyze1Command.am_total}")
                    # print(f"dd_total: {Analyze1Command.dd_total}")
                    # print(f"fv_total: {Analyze1Command.fv_total}")
                    # print(f"up_total: {Analyze1Command.up_total}")
                    # print(f"gam_1: {Analyze1Command.gam_1}")
                    # print(f"gam_2: {Analyze1Command.gam_2}")
                    # print(f"gam_3: {Analyze1Command.gam_3}")
                    # print(f"gam_4: {Analyze1Command.gam_4}")
                    # print(f"gam_5: {Analyze1Command.gam_5}")
                    # print(f"cc_1: {Analyze1Command.cc_1}")
                    # print(f"cc_2: {Analyze1Command.cc_2}")
                    # print(f"cc_3: {Analyze1Command.cc_3}")
                    # print(f"cc_4: {Analyze1Command.cc_4}")
                    # print(f"cc_5: {Analyze1Command.cc_5}")
                    print(f"fvid_str: {fvid_str}")
                    print("")

                    Analyze1Command.upload_results(
                        ams_to_upload,
                        number_of_nodes,
                        fvid_str,
                        number_of_analyzed_fvids,
                        number_of_analyzed_matrices,
                        analyze_run_django_obj_f)
                    for key in ams_to_upload:
                        ams[key]["matrix_uploaded"] = True
                    ams_to_upload = {}

                get_next_fvid_1 = datetime.now()
                upload_total += (get_next_fvid_1 - upload_1).total_seconds()

                fvid = fvid_generator.get_next_fvid(fvid)

                sleep_1 = datetime.now()
                get_next_fvid_total += (sleep_1 - get_next_fvid_1).total_seconds()

                # time.sleep(0.0001)
                # sleep_2 = datetime.now()
                # sleep_total += (sleep_2 - sleep_1).total_seconds()

            print(f"generate_am_total: {generate_am_total}")
            print(f"misc_total: {misc_total}")
            print(f"dd_calc_total: {dd_calc_total}")
            print(f"upload_total: {upload_total}")
            print(f"get_next_fvid_total: {get_next_fvid_total}")
            print("")

            Analyze1Command.upload_results(
                ams_to_upload,
                number_of_nodes,
                fvid_str,
                number_of_analyzed_fvids,
                number_of_analyzed_matrices,
                analyze_run_django_obj_f)
            for key in ams_to_upload:
                ams[key]["matrix_uploaded"] = True

            now = datetime.now()
            analyze_run_django_obj_f.update(percentage=100.0, completed_at=now)
        except Exception as e:
            line_no = '<Not found>'
            try:
                import sys
                exc_type, exc_obj, exc_tb = sys.exc_info()
                line_no = str(exc_tb.tb_lineno)
            except:
                pass
            print(f"Analyze1Command.execute exception at line {str(line_no)}: {str(e)}")
