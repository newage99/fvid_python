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
        first_symbol_str = str(fvid[0])
        current_variables = []
        are_current_variables_ordered = True

        if first_symbol_str == ')' or first_symbol_str in self.functions_strs:
            return False

        fvid_str = ' '.join([str(f) for f in fvid])
        # for f in fvid:
        #     fvid_str += str(f) + ' '

        if fvid_str.startswith('1 /') or fvid_str.startswith('1 *'):
            return False

        # TODO: Put inside loop
        if '+ + +' in fvid_str or '- - -' in fvid_str or '% %' in fvid_str:
            return False

        # TODO: 07/05/203 Last thought: 1 1 n +. All sumatory must only have one 1, because more than one it's the
        #  same as the number 2.

        fvid_strs = []
        symbol_types = []

        for i in range(len(fvid)):

            if fvid_str == '2 1 +':
                a = 0

            fvid_strs.append(str(fvid[i]))
            symbol_types.append(self.__get_symbol_type(fvid_strs[-1]))

            if symbol_types[-1] == 'v':
                current_variables.append(fvid_strs[-1])

            if i > 0:

                if fvid_strs[-1] == '%' and (symbol_types[-2] == 'f' or fvid_strs[-2] == ')'):
                    # Modulus of just one variable not allowed
                    return False

                if symbol_types[-1] == ')' and (symbol_types[-2] == 'v' or
                                                (last_open_parenthesis_pos > -1 and last_open_parenthesis_pos > i - 3)):
                    return False

                if symbol_types[-1] == 'f' and symbol_types[-2] == '(':
                    return False

                if i == 1 or (i > 2 and fvid_strs[-3] == '('):
                    if fvid_strs[-1] == '+':
                        # Absoluting a number already positive -> n +, (x +)
                        return False
                    elif fvid_strs[-1] == '%':
                        # Cannot perform mod of just one number -> n %, 2 %
                        return False
                    elif fvid_strs[-2] == '2' and fvid_strs[-1] == '/':
                        # math.isqrt(2) equals 1, which we already have -> 2 /
                        return False

                if symbol_types[-1] == 'v':
                    if len(current_variables) > 1 and fvid_strs[-1] < fvid_strs[-2]:
                        are_current_variables_ordered = False
                elif len(current_variables) > 0:
                    fun = getattr(fvid[-1], 'does_parameters_order_affects_result', None)
                    if fun and not fun() and not are_current_variables_ordered:
                        return False
                    current_variables.clear()
                    are_current_variables_ordered = True

            if i > 1:

                if symbol_types[-3] == 'f':
                    if fvid_strs[-1] == '+' and fvid_strs[-2] == '+':
                        # Absoluting an already absoluted number -> n + +, (y n %) + +
                        return False
                    elif fvid_strs[-1] == '-' and fvid_strs[-2] == '-':
                        # Negating an already negated number -> n - -, (n y *) - -
                        return False

                if (i == 2 or (i > 2 and fvid_strs[-4] == '(')) and symbol_types[-3] == 'v':
                    if fvid_strs[-1] == '+':
                        if fvid_strs[-2] == '-':
                            # Absoluting a previously negated number -> n - +, 2 - +
                            return False
                        elif fvid_strs[-2] == '*':
                            # Positive square numbers do not need to be absoluted -> 2 * +, y * +
                            return False
                        elif fvid_strs[-2] == '/':
                            # Positive square rooted numbers do not need to be absoluted -> 2 / +, x / +
                            return False
                        elif fvid_strs[-3] == '1' and fvid_strs[-2] == '1':
                            # 1 + 1 equals 2, which we already have -> 1 1 +
                            return False
                        elif fvid_strs[-3] == '2' and fvid_strs[-2] == '2':
                            # 4 can be achieved shortly with 2 *, se we discard this case
                            return False
                    elif fvid_strs[-1] == '-':
                        if fvid_strs[-2] == '-':
                            # Negating a previously negated number -> 2 - -, n - -
                            return False
                        if fvid_strs[-3] == fvid_strs[-2]:
                            # A number minus itself always gives 0 -> n n -, x x -
                            return False
                        if fvid_strs[-3] == '2' and fvid_strs[-2] == '1':
                            # 2 - 1 equals 1, which we already have
                            return False
                        if fvid_strs[-3] == '1' and fvid_strs[-2] == '2':
                            # -1 can be achieved with 1 -, which is shorter than 1 2 -
                            return False
                    elif fvid_strs[-1] == '/':
                        if fvid_strs[-2] == '*':
                            # Multiply by itself to later square root itself -> n * /, x * /
                            return False
                        elif fvid_strs[-2] == '-':
                            # Square roots of negative numbers are not allowed -> x - /, 2 - /
                            return False
                        elif fvid_strs[-2] == '1':
                            # Division by 1 -> x 1 /, 2 1 /
                            return False
                        elif fvid_strs[-3] == fvid_strs[-2]:
                            # Division by itself equals 1 -> n n /, y y /
                            return False
                        elif fvid_strs[-3] == '1':
                            # 1 divided by any positive number always returns 0 -> 1 x /, 1 2 /
                            return False
                    elif fvid_strs[-1] == '%':
                        if fvid_strs[-2] == '1':
                            # Modulus by 1 always equals 0 -> n 1 %, x 1 %
                            return False
                        elif fvid_strs[-3] == '1' or fvid_strs[-3] == '2':
                            # 1 or 2 mod any number always returns the same number -> 1 n %, 2 x %
                            return False
                        elif fvid_strs[-3] == fvid_strs[-2]:
                            # Modulus of itself always equals 0 -> n n %, y y %
                            return False
                    elif fvid_strs[-1] == '*':
                        if fvid_strs[-3] == fvid_strs[-2]:
                            # n n *, 2 2 *, y y *,... it's the same as n *, 2 *, y *,... and these last ones are shorter
                            return False
                        elif fvid_strs[-3] == '1' or fvid_strs[-2] == '1':
                            # Multiplication by 1 returns the same number -> 1 n *, x 1 *
                            return False
                        elif fvid_strs[-3] == '2' or fvid_strs[-2] == '2':
                            # Multiplication by 2 it's the same as n n +, y y +,..., so we choose these last ones better
                            return False
                        elif fvid_strs[-2] == '-':
                            # Square the negation of any number it's the same as squaring it directly -> n - +, 2 - *
                            return False

            if i > 2:
                if (i == 3 or (i > 3 and fvid_strs[-5] == '(')) and symbol_types[-4] == 'v':
                    if symbol_types[-3] == 'v':
                        if fvid_strs[-1] == '+':
                            if fvid_strs[-2] == '+':
                                # Absoluting a summary already positive -> n n + +, x x + +
                                return False
                            elif fvid_strs[-2] == '/':
                                # Absoluting a division already positive -> n y / +, 2 y / +
                                return False
                            elif fvid_strs[-2] == '%':
                                # Absoluting a modulus already positive -> n y % +, x y % +
                                return False
                            elif fvid_strs[-2] == '*':
                                # Absoluting a multiplication already positive -> n x * +, x y * +
                                return False
                    elif fvid_strs[-1] == '+':
                        if symbol_types[-2] == 'v':
                            if fvid_strs[-3] == '-' and fvid_strs[-4] == fvid_strs[-2]:
                                # Negating a number to later add itself returns 0 -> n - n +, x - x +
                                return False
                        elif fvid_strs[-2] == '/':
                            if fvid_strs[-3] == '/':
                                return False
                            elif fvid_strs[-3] == '*':
                                return False
                        elif fvid_strs[-2] == '*':
                            if fvid_strs[-3] == '*':
                                return False
                            elif fvid_strs[-3] == '/':
                                return False
                        elif fvid_strs[-2] == '-':
                            if fvid_strs[-3] == '/':
                                return False
                            elif fvid_strs[-3] == '*':
                                return False

            if symbol_types[-1] == "(":
                last_open_parenthesis_pos = i
                currently_open_parenthesis += 1
            elif symbol_types[-1] == ")":
                currently_open_parenthesis -= 1
                if currently_open_parenthesis < 0:
                    return False

        if currently_open_parenthesis != 0 or symbol_types[-1] != 'f':
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
        last_symbol_str = str(self.symbols[-1])
        first_symbol = self.symbols[0]

        while not not_modified:
            not_modified = True
            for i in range(0, length):
                str_symbol = str(fvid_copy[i])
                if str_symbol != last_symbol_str:
                    next_symbol = self.__get_next_symbol(fvid_copy[i])
                    fvid_copy[i] = next_symbol
                    for j in range(i - 1, -1, -1):
                        fvid_copy[j] = first_symbol
                    if self.__check_fvid(fvid_copy):
                        return fvid_copy
                    not_modified = False
                    break
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
        current_fvid = first_fvid

        while current_fvid is not None:
            print(' '.join([s.symbol() for s in current_fvid]))
            fvids.append(current_fvid)
            current_fvid = self.get_next_fvid(current_fvid)

        print(f"Generated fvids: {len(fvids)}")

        return fvids


if __name__ == '__main__':
    generator = FvidGenerator(4)
    generator.generate()
