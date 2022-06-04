
class Stack:
    def __init__(self):
        self.stack = []
        self.scope = 0

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
            return self.stack[length - index] #peek(2) -> return stack [top - 2]

    def clear(self):
        self.stack.clear()

    def new_scope(self):
        self.scope = self.scope + 1

    def get_scope(self):
        return self.scope


#test
if __name__ == '__main__':
    stack = Stack()
    stack.push(3)
    stack.push(6)
    stack.push(12)
    #3, 6, 12
    # stack.clear()
    # stack.newScope()
    print(stack.getScope())