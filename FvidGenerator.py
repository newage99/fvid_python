from symbols.Symbol import Symbol
from symbols.Variable import Variable
from symbols.Function import Function

symbols = Symbol.symbols()
functions = Function.symbols()
functions_strs = Function.symbols_strs()
variables = Variable.symbols()
variables_strs = Variable.symbols_strs()


class FvidGenerator:

    @staticmethod
    def __get_next_symbol(symbol):
        str_symbol = str(symbol)
        get_next_symbol = False
        for s in symbols:
            s_str = str(s)
            if get_next_symbol:
                return s
            if str_symbol == s_str:
                get_next_symbol = True
        return None

    @staticmethod
    def __get_symbol_type(str_symbol):
        if str_symbol in variables_strs:
            return 'v'
        elif str_symbol in functions_strs:
            return 'f'
        elif str_symbol == '(':
            return '('
        elif str_symbol == ')':
            return ')'

    @staticmethod
    def __check_fvid(fvid):

        currently_open_parenthesis = 0
        last_open_parenthesis_pos = -1
        last_symbol_type = None
        last_fvid_str = ''
        first_symbol_str = str(fvid[0])
        current_variables = []
        are_current_variables_ordered = True

        if first_symbol_str == ')' or first_symbol_str in functions_strs:
            return False

        fvid_str = ''
        for f in fvid:
            fvid_str += str(f) + ' '

        if fvid_str == '2 1 + ':
            a = 0

        for i in range(len(fvid)):

            current_fvid = fvid[i]
            current_fvid_str = str(current_fvid)
            current_symbol_type = FvidGenerator.__get_symbol_type(current_fvid_str)

            if current_symbol_type == 'v':
                current_variables.append(current_fvid_str)
                if len(current_variables) > 1 and (len(current_fvid_str) < len(last_fvid_str) or
                        (len(current_fvid_str) == len(last_fvid_str) and current_fvid_str < last_fvid_str)):
                    are_current_variables_ordered = False
            elif len(current_variables) > 0:
                fun = getattr(current_fvid, 'does_parameters_order_affects_result', None)
                if fun and not fun() and not are_current_variables_ordered:
                    return False
                current_variables.clear()
                are_current_variables_ordered = True

            if current_symbol_type == ')' and \
                    (last_symbol_type == 'v' or (last_open_parenthesis_pos > -1 and last_open_parenthesis_pos > i - 3)):
                return False

            if current_symbol_type == 'f' and last_symbol_type == '(':
                return False

            if current_symbol_type == "(":
                last_open_parenthesis_pos = i
                currently_open_parenthesis += 1
            elif current_symbol_type == ")":
                currently_open_parenthesis -= 1
                if currently_open_parenthesis < 0:
                    return False

            last_symbol_type = current_symbol_type
            last_fvid_str = current_fvid_str

        if currently_open_parenthesis != 0 or last_symbol_type != 'f':
            return False

        return True

    @staticmethod
    def __fvid_str_to_symbols_list(fvid_str: str):

        fvid_str_split = fvid_str.split(" ")
        symbols_list = []

        for symbol_str in fvid_str_split:
            symbol = Symbol.get_symbol_by_str(symbol_str)
            if symbol:
                symbols_list.append(symbol)
            else:
                return None

        return symbols_list

    @staticmethod
    def generate(length, start_fvid=None):

        if start_fvid:
            first_fvid = FvidGenerator.__fvid_str_to_symbols_list(start_fvid)
            if not first_fvid:
                print(f"Error converting 'start_fvid'={start_fvid} to symbols list.")
        else:
            first_fvid = None

        if not first_fvid:
            first_fvid = []
            for i in range(length):
                first_fvid.append(symbols[0])
        fvids = []
        not_exit = True
        last_fvid = first_fvid
        possible_fvids = 0

        while not_exit:

            if FvidGenerator.__check_fvid(last_fvid):
                fvids.append(last_fvid)

            fvid = last_fvid.copy()
            not_modified = True

            for i in range(length - 1, -1, -1):
                str_symbol = str(fvid[i])
                if str_symbol != str(symbols[-1]):
                    next_symbol = FvidGenerator.__get_next_symbol(fvid[i])
                    fvid[i] = next_symbol
                    for j in range(i + 1, length):
                        fvid[j] = symbols[0]
                    not_modified = False
                    break

            last_fvid = fvid

            if not_modified:
                not_exit = False

            possible_fvids += 1

        print(f"Possible fvids: {possible_fvids - 1}")
        print(f"Generated fvids: {len(fvids)}")

        return fvids


if __name__ == '__main__':
    results = FvidGenerator.generate(5)
    for result in results:
        fvid_str = ""
        for s in result:
            fvid_str += f"{str(s)} "
        fvid_str = fvid_str[:-1]
        # print(fvid_str)
