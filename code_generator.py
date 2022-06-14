import imp
from stack import Stack
from three_address_code import ThreeAddressCode
from scanner import symbol_table
from parser import token


class CodeGenerator:
    def __init__(self):
        self.current_id = None
        self.current_keyword = None
        self.current_number = None
        self.current_function = None
        self.current_symbol = None
        self.symbol_stack = []
        self.memory_address = []
        self.memory_temp = []
        self.data_block_starting_point = 5000
        self.temp_block_starting_point = 3000
        self.data_block_offset = 0
        self.temp_block_offset = 0
        self.semantic_stack = []
        self.program_block = []
        self.pb_pointer = 0
        self.array_len = 0

        self.semantic_routines = {
            '#pid': self.pid,
            '#pnum': self.pnum,
            '#label': self.label,
            '#relop_sign': self.relop_sign,
            '#jpf_save': self.jpf_save,
            '#save': self.save,
            '#jp': self.jp,
            '#jpf': self.jpf,
            '#while': self.while_func,
            '#add': self.add,
            '#sub': self.sub,
            '#mult': self.mult,
            '#power': self.power,
            '#assign': self.assign,
            '#relop': self.relop,
            '#func': self.func,
            '#return': self.return_func,
            '#function_end': self.function_end
        }

    def call_routine(self, routine, token=None):
        print(self.semantic_stack)
        self.semantic_routines[routine]()

    def add_code_to_pb(self, operation, lhs, rhs, target):
        self.program_block.append(ThreeAddressCode(self.pb_pointer, operation, lhs, rhs, target))
        self.pb_pointer += 1

    def get_new_variable_address(self):
        address = (self.data_block_offset * 4) + self.data_block_starting_point
        self.data_block_offset += 1
        return address
    
    def pid(self):
        if not self.is_variable_defined(token[1]):
            address = self.get_new_variable_address()
            symbol_table.set_symbol_address(token[1], address)

        address = symbol_table.find_address(token[1])
        self.semantic_stack.append(address)

    def pnum(self):
        self.semantic_stack.append({f'#{token[1]}'})

    def relop_sign(self):
        self.semantic_stack.append(self.current_symbol)  ######################### to check

    def reserve_pb(self):
        self.program_block.append('')

    def label(self):
        line = self.pb_pointer
        self.semantic_stack.append(line)
        self.reserve_pb()

    def save(self):
        line = len(self.program_block)
        self.semantic_stack.append(line)

    def jpf_save(self):
        i = len(self.program_block)
        self.add_code_to_pb("JPF", self.semantic_stack.pop(), i, '')
        self.semantic_stack.pop()
        self.semantic_stack.pop()

    def jp(self):
        i = len(self.program_block)
        self.add_code_to_pb("JP", i, '', '')
        self.semantic_stack.pop()

    def jpf(self):
        i = len(self.program_block)  # ???????compare to jpf_save
        self.add_code_to_pb("JPF", self.semantic_stack.pop(), i, '')
        self.semantic_stack.pop()
        self.semantic_stack.pop()

    def while_func(self):  #####is it true? idk
        i = self.pb_pointer
        self.add_code_to_pb("JPF", self.semantic_stack.pop(), i, '')  # i+1
        self.program_block.insert(i, ThreeAddressCode("JP", self.semantic_stack.pop(), '', ''))
        i += 1
        self.semantic_stack.pop()
        self.semantic_stack.pop()
        self.semantic_stack.pop()

    def add(self):
        num1 = self.semantic_stack.pop()
        num2 = self.semantic_stack.pop()
        if not num1.startwith('#'):
            var1 = symbol_table.find_address(num1)
        else:
            var1 = num1
        if not num2.startwith('#'):
            var2 = symbol_table.find_address(num2)
        else:
            var2 = num2
        t = self.get_temp()
        self.add_code_to_pb("ADD", var1, var2, t)
        self.semantic_stack.append(t)

    def sub(self):
        num1 = self.semantic_stack.pop()
        num2 = self.semantic_stack.pop()
        if not num1.startwith('#'):
            var1 = symbol_table.find_address(num1)
        else:
            var1 = num1
        if not num2.startwith('#'):
            var2 = symbol_table.find_address(num2)
        else:
            var2 = num2
        t = self.get_temp()
        self.add_code_to_pb("SUB", num1, num2, t)
        self.semantic_stack.append(t)

    def mult(self):
        num1 = self.semantic_stack.pop()
        num2 = self.semantic_stack.pop()
        if not num1.startwith('#'):
            var1 = symbol_table.find_address(num1)
        else:
            var1 = num1
        if not num2.startwith('#'):
            var2 = symbol_table.find_address(num2)
        else:
            var2 = num2
        t = self.get_temp()
        self.add_code_to_pb("MULT", num1, num2, t)
        self.semantic_stack.append(t)

    def power(self):
        num1 = self.semantic_stack.pop()  # num2 ^ num1
        num2 = self.semantic_stack.pop()
        temp = num1



    def assign(self):
        if self.is_variable_defined():
            address = symbol_table.find_address(self.current_id)
            self.semantic_stack.append(address)
            self.add_code_to_pb("ASSIGN", self.semantic_stack.pop(), self.semantic_stack.pop(), '')

    def array_element(self):
        self.array_len += 1


    def is_variable_defined(self):
        return symbol_table.symbol_has_address(token[1])

    def relop(self):
        # Relational_Expression⟶Expression Relop Expression #relop
        num1 = self.semantic_stack.pop()
        relop = self.semantic_stack.pop()  # how to find relop????????????????????????????????????????????????
        num2 = self.semantic_stack.pop()
        if relop == '<':
            if num1 < num2:
                r = 1
            else:
                r = 0
            self.add_code_to_pb('LT', num1, num2, r)
        elif relop == '==':
            if num1 == num2:
                r = 1
            else:
                r = 0
            self.add_code_to_pb('EQ', num1, num2, r)

    def return_func(self):
        return_value = self.semantic_stack.pop()

    def func(self):
        pass

    def get_temp(self):
        temp_ptr = self.temp_block_starting_point + (self.temp_block_offset * 4)
        self.temp_block_offset += 1
        return temp_ptr

    def function_end(self):
        pass

    ##########################
