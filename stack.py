class Stack:
    def __init__(self, starting_index: int):
        self.filled_cells = 0
        self.stack = []
        self.scope = 0
        self.starting_index = starting_index

    def push(self, element):
        self.stack.append(element)

    def pop(self):
        return self.stack.pop()

    def is_empty(self):
        return not bool(len(self.stack))

    def size(self):
        return len(self.stack)

    def peek(self, index):
        length = self.size() - 1
        if index <= length:
            return self.stack[length - index]  # peek(2) -> return stack [top - 2]

    def clear(self):
        self.stack.clear()

    def new_scope(self):
        self.scope = self.scope + 1

    def get_scope(self):
        return self.scope

    def get_first_empty_cell(self) -> int:
        empty_cell = self.starting_index + 4 * self.filled_cells
        self.filled_cells += 1
        return empty_cell


# test
if __name__ == '__main__':
    stack = Stack()
    stack.push(3)
    stack.push(6)
    stack.push(12)
    # 3, 6, 12
    # stack.clear()
    # stack.newScope()
    print(stack.size())
