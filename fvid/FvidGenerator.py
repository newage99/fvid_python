from symbols.Symbol import Symbol
from symbols.Variable import Variable
from symbols.Function import Function


class FvidGenerator:

    def __init__(self, length):
        self.symbols = Symbol.symbols()
        self.functions = Function.symbols()
        self.functions_strs = Function.symbols_strs()
        self.variables = Variable.symbols()
        self.variables_strs = Variable.symbols_strs()
        self.length = length

    def __get_next_symbol(self, symbol):
        str_symbol = str(symbol)
        get_next_symbol = False
        for s in self.symbols:
            s_str = str(s)
            if get_next_symbol:
                return s
            if str_symbol == s_str:
                get_next_symbol = True
        return None

    def __get_symbol_type(self, str_symbol):
        if str_symbol in self.variables_strs:
            return 'v'
        elif str_symbol in self.functions_strs:
            return 'f'
        elif str_symbol == '(':
            return '('
        elif str_symbol == ')':
            return ')'

    def __check_fvid(self, fvid):

        currently_open_parenthesis = 0
        last_open_parenthesis_pos = -1
        last_symbol_type = None
        last_fvid_str = ''
        first_symbol_str = str(fvid[0])
        current_variables = []
        are_current_variables_ordered = True

        if first_symbol_str == ')' or first_symbol_str in self.functions_strs:
            return False

        fvid_str = ''
        for f in fvid:
            fvid_str += str(f) + ' '

        if fvid_str == '2 1 + ':
            a = 0

        for i in range(len(fvid)):

            current_fvid = fvid[i]
            current_fvid_str = str(current_fvid)
            current_symbol_type = self.__get_symbol_type(current_fvid_str)

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
    def fvid_str_to_symbols_list(fvid_str: str):

        fvid_str_split = fvid_str.split(" ")
        symbols_list = []

        for symbol_str in fvid_str_split:
            symbol = Symbol.get_symbol_by_str(symbol_str)
            if symbol:
                symbols_list.append(symbol)
            else:
                return None

        return symbols_list

    def get_next_fvid(self, fvid):

        fvid_copy = fvid.copy()
        length = len(fvid_copy)
        not_modified = False

        while not not_modified:

            not_modified = True

            for i in range(0, length):
                str_symbol = str(fvid_copy[i])
                if str_symbol != str(self.symbols[-1]):
                    next_symbol = self.__get_next_symbol(fvid_copy[i])
                    fvid_copy[i] = next_symbol
                    for j in range(i - 1, -1, -1):
                        fvid_copy[j] = self.symbols[0]
                    not_modified = False
                    break

            # for i in range(length - 1, -1, -1):
            #     str_symbol = str(fvid_copy[i])
            #     if str_symbol != str(self.symbols[-1]):
            #         next_symbol = self.__get_next_symbol(fvid_copy[i])
            #         fvid_copy[i] = next_symbol
            #         for j in range(i + 1, length):
            #             fvid_copy[j] = self.symbols[0]
            #         not_modified = False
            #         break

            if not not_modified and self.__check_fvid(fvid_copy):
                return fvid_copy

        return None

    def get_first_fvid(self):

        fvid = []
        for i in range(self.length):
            fvid.append(self.symbols[0])

        if self.__check_fvid(fvid):
            return fvid

        return self.get_next_fvid(fvid)

    def generate(self, start_fvid=None):

        if start_fvid:
            first_fvid = self.fvid_str_to_symbols_list(start_fvid)
            if not first_fvid:
                print(f"Error converting 'start_fvid'={start_fvid} to symbols list.")
        else:
            first_fvid = None

        if not first_fvid:
            first_fvid = self.get_first_fvid()
        fvids = []
        not_exit = True
        last_fvid = first_fvid
        possible_fvids = 0

        while not_exit:

            if self.__check_fvid(last_fvid):
                fvids.append(last_fvid)

            fvid = last_fvid.copy()
            not_modified = True

            for i in range(self.length - 1, -1, -1):
                str_symbol = str(fvid[i])
                if str_symbol != str(self.symbols[-1]):
                    next_symbol = self.__get_next_symbol(fvid[i])
                    fvid[i] = next_symbol
                    for j in range(i + 1, self.length):
                        fvid[j] = self.symbols[0]
                    not_modified = False
                    break

            last_fvid = fvid

            if not_modified:
                not_exit = False

            possible_fvids += 1

        print(f"Possible fvids: {possible_fvids - 1}")
        print(f"Generated fvids: {len(fvids)}")

        return fvids
