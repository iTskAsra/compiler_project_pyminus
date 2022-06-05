import enum

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
        self.semantic_stack = []
        self.program_block = []

    def get_temp_func(self) -> int:
        return self.temp_block.get_first_empty_cell()

    def pid_func(self):
        address = self.find_address(self.current_id)
        self.stack.push(address)

    def assign_func(self):
        self.generate_formatted_code(
            'ASSIGN', self.semantic_stack[-1], self.semantic_stack[-2], '')
        num1_type = self.get_type(self.semantic_stack.pop())
        num2_type = self.get_type(self.semantic_stack[-1])

    def calculation(self):
        sign = 'SUB'
        symbol_element = self.symbol_stack.pop()
        if symbol_element == '+':
            sign = 'ADD'
        elif symbol_element == '*':
            sign = 'MULT'
        temp = self.get_temp_func()
        self.generate_formatted_code(
            sign,
            self.semantic_stack[-2],
            self.semantic_stack[-1],
            temp
        )
        num1 = self.stack.pop()
        num2 = self.stack.pop()
        num1_type, num2_type = self.get_type(num1), self.get_type(num2)
        self.semantic_stack.append(temp)

    def push_number_dec(self):
        self.semantic_stack.append(self.current_num)

    def push_number(self):
        self.semantic_stack.append(f'#{self.current_number}')

    def generate_formatted_code(self, relop: str,
                                string1, string2, string3):
        self.program_block.append(f'({relop}, {string1}, {string2}, {string3})')

    def insert_formatted_code(self, index: int, relop: str,
                              string1, string2, string3):
        self.program_block[index] = \
            f'({relop}, {string1}, {string2}, {string3})'

    def find_address(self, token):
        return 0  # the token address

    def get_type(self, var):
        pass

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


