import enum
import imp
from three_address_code import three_addr_code
from stack import Stack


class CodeGenerator:
    def __init__(self):
        self.current_id = None
        self.current_keyword = None
        self.current_number = None
        self.current_function = None
        self.current_symbol = None
        self.symbol_stack = []
        self.stack = Stack()
        self.memory_address = []
        self.memory_temp = []
        self.data_block = Stack(100)
        self.temp_block = Stack(500)
        self.semantic_stack = Stack(3000)
        self.program_block = []
        self.pb_ptr = 0

        self.semantic_routines = {
            'pid' : pid,
            'pnum' : pnum,
            'label' : label
        }

    def call_routine(self, routine, token):
        self.semantic_routines[routine]()

    
    def add_code_to_pb(self, operation, lhs, rhs, target):
        self.program_block.append(three_addr_code(self.pb_ptr, operation, lhs, rhs, target))
        self.pb_ptr += 1

    def find_token_address(self, token):
        token_address = token.address
        return token_address #return token address, not implemented!

    def pid(self):
        address = self.find_address(self.current_id)
        self.stack.push(address)

    def pnum(self):
        self.stack.push(self.current_number)

    def push_to_program_block(self, sign, par1, par2, temp):
        self.program_block.append(f'({sign}, {par1}, {par2}, {temp})')
        self.stack.pop()
        self.stack.pop()
        if temp is not None:
            self.stack.push(temp)

    def add(self):
        t = get_temp()
        num1 = self.stack.peek(0)
        num2 = self.stack.peek(-1)
        t = num1 + num2
        self.push_to_program_block("ADD", num1, num2, t)


    def sub(self):
        t = get_temp()
        num1 = self.stack.peek(0)
        num2 = self.stack.peek(-1)
        t = num1 - num2
        self.push_to_program_block("SUB", num1, num2, t)

    def mult(self):
        t = get_temp()
        num1 = self.stack.peek(0)
        num2 = self.stack.peek(-1)
        t = num1 * num2
        self.push_to_program_block("MULT", num1, num2, t)

    def power(self):
        num1 = self.stack.peek(0) #num2 ^ num1
        num2 = self.stack.peek(-1)
        i = num1
        while i > 0:
            self.stack.push(num2)
            self.stack.push(num2)
            self.mult()

    def assign(self):
        self.push_to_program_block("ASSIGN", self.stack.peek(0), self.stack.peek(-1), None)


    ##########################

    def jp_func(self):
        self.insert_formatted_code(
            self.semantic_stack[-1],
            "JP", len(self.program_block),
            "",
            ""
        )
        self.semantic_stack.pop()

    def save_function(self):
        self.semantic_stack.append(len(self.program_block))
        self.program_block.append("")

    def jpf_func(self):
        self.insert_formatted_code(
            self.semantic_stack[-1],
            "JPF",
            self.semantic_stack[-2],
            len(self.program_block), ""
        )

    def save_jpf_func(self):
        self.insert_formatted_code(
            self.semantic_stack[-1],
            'JPF',
            self.semantic_stack[-2],
            len(self.program_block) + 1,
            ''
        )
        self.semantic_stack.pop()
        self.semantic_stack.pop()
        self.save_function()

    def check_temp_address(self, address):
        return address >= self.temp_block.starting_index

    def check_data_address(self, address):
        return (address >= self.data_block.starting_index) \
               and (address < self.temp_block.starting_index)


