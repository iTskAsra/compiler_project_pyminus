import symbol

from stack import Stack


class CodeGenerator:
    def __init__(self):
        self.symbol_stack = []
        self.stack = Stack()
        self.memory_address = []
        self.memory_temp = []
        self.data_block = Stack(100)
        self.temp_block = Stack(500)
        self.semantic_stack = []
        self.program_block = []

    def get_temp(self) -> int:
        return self.temp_block.get_first_empty_cell()

    def pid(self, token):
        address = self.find_address(token)
        self.stack.push(address)

    def calculation(self):
        sign = 'SUB'
        symbol_element = self.symbol_stack.pop()
        if symbol_element == '+':
            sign = 'ADD'
        elif symbol_element == '*':
            sign = 'MULT'
        temp = self.get_temp()
        self.generate_formatted_code(
            sign, self.semantic_stack[-2], self.semantic_stack[-1], temp)
        num1 = self.stack.pop()
        num2 = self.stack.pop()
        num1_type, num2_type = self.get_type(num1), self.get_type(num2)
        self.semantic_stack.append(temp)

    def generate_formatted_code(self, relop: str, s1, s2, s3):
        self.program_block.append(f'({relop}, {s1}, {s2}, {s3})')

    def insert_formatted_code(self, index: int, relop: str, string1, string2, string3):
        self.program_block[index] = f'({relop}, {string1}, {string2}, {string3})'

    def find_address(self, token):
        return 0  # the token address

    def get_type(self, var):
        pass
