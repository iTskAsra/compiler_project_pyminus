from anytree import Node, RenderTree
import scanner
import re

parsed_tree = Node("Program")
token = []
parsed_tree_address = "parse-tree.txt"
syntax_errors_address = "syntax-errors.txt"
syntax_errors = []
error_raised = False
current_line = 1
token_popped = True
errors_raised = False
eop = False

valid_first = re.compile(r'if|else|continue|break|return|while|def')

class parse_table:
    parse_dictionary = {
        'Program' : {
            ';' : 'EMPTY',
            'break' : ['Statements'],
            'continue' : '',
            'ID' : '',
            '=' : '',
            '[' : '',
            ']' : '',
            '(' : '',
            ')' : '',
            ',' : '',
            'global' : '',
            'return' : '',
            'def' : '',
            ':' : '',
            'if' : '',
            'else' : '',
            'while' : '',
            '==' : '',
            '<' : '',
            '+' : '',
            '-' : '',
            '*' : '',
            '**' : '',
            'NUM' : '',
            'dollar_sign' : ''
        },

        'Statements': {
            ';': '',
            'break': '',
            'continue': '',
            'ID': '',
            '=': '',
            '[': '',
            ']': '',
            '(': '',
            ')': '',
            ',': '',
            'global': '',
            'return': '',
            'def': '',
            ':': '',
            'if': '',
            'else': 'EPSILON',
            'while': '',
            '==': '',
            '<': '',
            '+': '',
            '-': '',
            '*': '',
            '**': '',
            'NUM': '',
            'dollar_sign': ''
        },

        'Simple_stmt': {
            ';': 'SYNCH',
            'break': '',
            'continue': '',
            'ID': '',
            '=': '',
            '[': '',
            ']': '',
            '(': '',
            ')': '',
            ',': '',
            'global': '',
            'return': '',
            'def': '',
            ':': '',
            'if': '',
            'else': '',
            'while': '',
            '==': '',
            '<': '',
            '+': '',
            '-': '',
            '*': '',
            '**': '',
            'NUM': '',
            'dollar_sign': ''
        },

        'Statement': {
            ';': '',
            'break': '',
            'continue': '',
            'ID': '',
            '=': '',
            '[': '',
            ']': '',
            '(': '',
            ')': '',
            ',': '',
            'global': '',
            'return': '',
            'def': '',
            ':': '',
            'if': '',
            'else': '',
            'while': '',
            '==': '',
            '<': '',
            '+': '',
            '-': '',
            '*': '',
            '**': '',
            'NUM': '',
            'dollar_sign': ''
        },

        'Compound_stmt': {
            ';': '',
            'break': '',
            'continue': '',
            'ID': '',
            '=': '',
            '[': '',
            ']': '',
            '(': '',
            ')': '',
            ',': '',
            'global': '',
            'return': '',
            'def': '',
            ':': '',
            'if': '',
            'else': '',
            'while': '',
            '==': '',
            '<': '',
            '+': '',
            '-': '',
            '*': '',
            '**': '',
            'NUM': '',
            'dollar_sign': ''
        },

        'Assignment_Call': {
            ';': '',
            'break': '',
            'continue': '',
            'ID': '',
            '=': '',
            '[': '',
            ']': '',
            '(': '',
            ')': '',
            ',': '',
            'global': '',
            'return': '',
            'def': '',
            ':': '',
            'if': '',
            'else': '',
            'while': '',
            '==': '',
            '<': '',
            '+': '',
            '-': '',
            '*': '',
            '**': '',
            'NUM': '',
            'dollar_sign': ''
        },

        'B': {
            ';': '',
            'break': '',
            'continue': '',
            'ID': '',
            '=': '',
            '[': '',
            ']': '',
            '(': '',
            ')': '',
            ',': '',
            'global': '',
            'return': '',
            'def': '',
            ':': '',
            'if': '',
            'else': '',
            'while': '',
            '==': '',
            '<': '',
            '+': '',
            '-': '',
            '*': '',
            '**': '',
            'NUM': '',
            'dollar_sign': ''
        },

        'C': {
            ';': '',
            'break': '',
            'continue': '',
            'ID': '',
            '=': '',
            '[': '',
            ']': '',
            '(': '',
            ')': '',
            ',': '',
            'global': '',
            'return': '',
            'def': '',
            ':': '',
            'if': '',
            'else': '',
            'while': '',
            '==': '',
            '<': '',
            '+': '',
            '-': '',
            '*': '',
            '**': '',
            'NUM': '',
            'dollar_sign': ''
        },

        'List_Rest': {
            ';': '',
            'break': '',
            'continue': '',
            'ID': '',
            '=': '',
            '[': '',
            ']': '',
            '(': '',
            ')': '',
            ',': '',
            'global': '',
            'return': '',
            'def': '',
            ':': '',
            'if': '',
            'else': '',
            'while': '',
            '==': '',
            '<': '',
            '+': '',
            '-': '',
            '*': '',
            '**': '',
            'NUM': '',
            'dollar_sign': ''
        },

        'Return_stmt': {
            ';': '',
            'break': '',
            'continue': '',
            'ID': '',
            '=': '',
            '[': '',
            ']': '',
            '(': '',
            ')': '',
            ',': '',
            'global': '',
            'return': '',
            'def': '',
            ':': '',
            'if': '',
            'else': '',
            'while': '',
            '==': '',
            '<': '',
            '+': '',
            '-': '',
            '*': '',
            '**': '',
            'NUM': '',
            'dollar_sign': ''
        },

        'Return_Value': {
            ';': '',
            'break': '',
            'continue': '',
            'ID': '',
            '=': '',
            '[': '',
            ']': '',
            '(': '',
            ')': '',
            ',': '',
            'global': '',
            'return': '',
            'def': '',
            ':': '',
            'if': '',
            'else': '',
            'while': '',
            '==': '',
            '<': '',
            '+': '',
            '-': '',
            '*': '',
            '**': '',
            'NUM': '',
            'dollar_sign': ''
        },

        'Global_stmt': {
            ';': '',
            'break': '',
            'continue': '',
            'ID': '',
            '=': '',
            '[': '',
            ']': '',
            '(': '',
            ')': '',
            ',': '',
            'global': '',
            'return': '',
            'def': '',
            ':': '',
            'if': '',
            'else': '',
            'while': '',
            '==': '',
            '<': '',
            '+': '',
            '-': '',
            '*': '',
            '**': '',
            'NUM': '',
            'dollar_sign': ''
        },

        'Function_def': {
            ';': '',
            'break': '',
            'continue': '',
            'ID': '',
            '=': '',
            '[': '',
            ']': '',
            '(': '',
            ')': '',
            ',': '',
            'global': '',
            'return': '',
            'def': '',
            ':': '',
            'if': '',
            'else': '',
            'while': '',
            '==': '',
            '<': '',
            '+': '',
            '-': '',
            '*': '',
            '**': '',
            'NUM': '',
            'dollar_sign': ''
        },

        'Params': {
            ';': '',
            'break': '',
            'continue': '',
            'ID': '',
            '=': '',
            '[': '',
            ']': '',
            '(': '',
            ')': '',
            ',': '',
            'global': '',
            'return': '',
            'def': '',
            ':': '',
            'if': '',
            'else': '',
            'while': '',
            '==': '',
            '<': '',
            '+': '',
            '-': '',
            '*': '',
            '**': '',
            'NUM': '',
            'dollar_sign': ''
        },

        'Params_Prime': {
            ';': '',
            'break': '',
            'continue': '',
            'ID': '',
            '=': '',
            '[': '',
            ']': '',
            '(': '',
            ')': '',
            ',': '',
            'global': '',
            'return': '',
            'def': '',
            ':': '',
            'if': '',
            'else': '',
            'while': '',
            '==': '',
            '<': '',
            '+': '',
            '-': '',
            '*': '',
            '**': '',
            'NUM': '',
            'dollar_sign': ''
        },

        'If_stmt': {
            ';': '',
            'break': '',
            'continue': '',
            'ID': '',
            '=': '',
            '[': '',
            ']': '',
            '(': '',
            ')': '',
            ',': '',
            'global': '',
            'return': '',
            'def': '',
            ':': '',
            'if': '',
            'else': '',
            'while': '',
            '==': '',
            '<': '',
            '+': '',
            '-': '',
            '*': '',
            '**': '',
            'NUM': '',
            'dollar_sign': ''
        },

        'Else_block': {
            ';': '',
            'break': '',
            'continue': '',
            'ID': '',
            '=': '',
            '[': '',
            ']': '',
            '(': '',
            ')': '',
            ',': '',
            'global': '',
            'return': '',
            'def': '',
            ':': '',
            'if': '',
            'else': '',
            'while': '',
            '==': '',
            '<': '',
            '+': '',
            '-': '',
            '*': '',
            '**': '',
            'NUM': '',
            'dollar_sign': ''
        },
        'Iteration_stmt': {
            ';': '',
            'break': '',
            'continue': '',
            'ID': '',
            '=': '',
            '[': '',
            ']': '',
            '(': '',
            ')': '',
            ',': '',
            'global': '',
            'return': '',
            'def': '',
            ':': '',
            'if': '',
            'else': '',
            'while': '',
            '==': '',
            '<': '',
            '+': '',
            '-': '',
            '*': '',
            '**': '',
            'NUM': '',
            'dollar_sign': ''
        },
        'Relational_Expression': {
            ';': '',
            'break': '',
            'continue': '',
            'ID': '',
            '=': '',
            '[': '',
            ']': '',
            '(': '',
            ')': '',
            ',': '',
            'global': '',
            'return': '',
            'def': '',
            ':': '',
            'if': '',
            'else': '',
            'while': '',
            '==': '',
            '<': '',
            '+': '',
            '-': '',
            '*': '',
            '**': '',
            'NUM': '',
            'dollar_sign': ''
        },
        'Relop': {
            ';': '',
            'break': '',
            'continue': '',
            'ID': '',
            '=': '',
            '[': '',
            ']': '',
            '(': '',
            ')': '',
            ',': '',
            'global': '',
            'return': '',
            'def': '',
            ':': '',
            'if': '',
            'else': '',
            'while': '',
            '==': '',
            '<': '',
            '+': '',
            '-': '',
            '*': '',
            '**': '',
            'NUM': '',
            'dollar_sign': ''
        },
        'Expression': {
            ';': '',
            'break': '',
            'continue': '',
            'ID': '',
            '=': '',
            '[': '',
            ']': '',
            '(': '',
            ')': '',
            ',': '',
            'global': '',
            'return': '',
            'def': '',
            ':': '',
            'if': '',
            'else': '',
            'while': '',
            '==': '',
            '<': '',
            '+': '',
            '-': '',
            '*': '',
            '**': '',
            'NUM': '',
            'dollar_sign': ''
        },
        'Expression_Prime': {
            ';': '',
            'break': '',
            'continue': '',
            'ID': '',
            '=': '',
            '[': '',
            ']': '',
            '(': '',
            ')': '',
            ',': '',
            'global': '',
            'return': '',
            'def': '',
            ':': '',
            'if': '',
            'else': '',
            'while': '',
            '==': '',
            '<': '',
            '+': '',
            '-': '',
            '*': '',
            '**': '',
            'NUM': '',
            'dollar_sign': ''
        },
        'Term': {
            ';': '',
            'break': '',
            'continue': '',
            'ID': '',
            '=': '',
            '[': '',
            ']': '',
            '(': '',
            ')': '',
            ',': '',
            'global': '',
            'return': '',
            'def': '',
            ':': '',
            'if': '',
            'else': '',
            'while': '',
            '==': '',
            '<': '',
            '+': '',
            '-': '',
            '*': '',
            '**': '',
            'NUM': '',
            'dollar_sign': ''
        },
        'Term_Prime': {
            ';': '',
            'break': '',
            'continue': '',
            'ID': '',
            '=': '',
            '[': '',
            ']': '',
            '(': '',
            ')': '',
            ',': '',
            'global': '',
            'return': '',
            'def': '',
            ':': '',
            'if': '',
            'else': '',
            'while': '',
            '==': '',
            '<': '',
            '+': '',
            '-': '',
            '*': '',
            '**': '',
            'NUM': '',
            'dollar_sign': ''
        },
        'Factor': {
            ';': '',
            'break': '',
            'continue': '',
            'ID': '',
            '=': '',
            '[': '',
            ']': '',
            '(': '',
            ')': '',
            ',': '',
            'global': '',
            'return': '',
            'def': '',
            ':': '',
            'if': '',
            'else': '',
            'while': '',
            '==': '',
            '<': '',
            '+': '',
            '-': '',
            '*': '',
            '**': '',
            'NUM': '',
            'dollar_sign': ''
        },
        'Power': {
            ';': '',
            'break': '',
            'continue': '',
            'ID': '',
            '=': '',
            '[': '',
            ']': '',
            '(': '',
            ')': '',
            ',': '',
            'global': '',
            'return': '',
            'def': '',
            ':': '',
            'if': '',
            'else': '',
            'while': '',
            '==': '',
            '<': '',
            '+': '',
            '-': '',
            '*': '',
            '**': '',
            'NUM': '',
            'dollar_sign': ''
        },
        'Primary': {
            ';': '',
            'break': '',
            'continue': '',
            'ID': '',
            '=': '',
            '[': '',
            ']': '',
            '(': '',
            ')': '',
            ',': '',
            'global': '',
            'return': '',
            'def': '',
            ':': '',
            'if': '',
            'else': '',
            'while': '',
            '==': '',
            '<': '',
            '+': '',
            '-': '',
            '*': '',
            '**': '',
            'NUM': '',
            'dollar_sign': ''
        },
        'Arguments': {
            ';': '',
            'break': '',
            'continue': '',
            'ID': '',
            '=': '',
            '[': '',
            ']': '',
            '(': '',
            ')': '',
            ',': '',
            'global': '',
            'return': '',
            'def': '',
            ':': '',
            'if': '',
            'else': '',
            'while': '',
            '==': '',
            '<': '',
            '+': '',
            '-': '',
            '*': '',
            '**': '',
            'NUM': '',
            'dollar_sign': ''
        },
        'Arguments_Prime': {
            ';': '',
            'break': '',
            'continue': '',
            'ID': '',
            '=': '',
            '[': '',
            ']': '',
            '(': '',
            ')': '',
            ',': '',
            'global': '',
            'return': '',
            'def': '',
            ':': '',
            'if': '',
            'else': '',
            'while': '',
            '==': '',
            '<': '',
            '+': '',
            '-': '',
            '*': '',
            '**': '',
            'NUM': '',
            'dollar_sign': ''
        },
        'Atom': {
            ';': '',
            'break': '',
            'continue': '',
            'ID': '',
            '=': '',
            '[': '',
            ']': '',
            '(': '',
            ')': '',
            ',': '',
            'global': '',
            'return': '',
            'def': '',
            ':': '',
            'if': '',
            'else': '',
            'while': '',
            '==': '',
            '<': '',
            '+': '',
            '-': '',
            '*': '',
            '**': '',
            'NUM': '',
            'dollar_sign': ''
        },
    }
    def parse(self, nt, t):
        pass
def get_token_line():
    return token[0]


def get_token():
    return token[1]


def get_new_token():
    global token
    token = scanner.get_next_token()


def get_token_type():
    return token[2]


def save_parsed_tree(address):
    with open(address, 'w', encoding="utf-8") as f:
        for pre, fill, node in RenderTree(parsed_tree):
            f.write("%s%s\n" % (pre, node.name))


def initialize_errors_file(address):
    with open(address, 'w') as f:
        f.write("There is no syntax error.")


def update_syntax_errors(line, terminal, error_description):
    global errors_raised
    errors_raised = True
    syntax_errors.append([line, terminal, error_description])


def save_syntax_errors(address):
    with open(address, 'w') as f:
        for error in syntax_errors:
            if error[1] == 'Unexpected EOF':
                f.write(f'#{error[0]} : syntax error, Unexpected EOF\n')
            else:
                f.write(f"#{error[0]} : syntax error, {error[2]} {error[1]}\n")


class FirstAndFollowSets:
    first_and_follow_sets = [
        ('Program', ['break', 'continue', 'ID', 'return', 'global', 'def', 'if', 'while', 'EPSILON'],
         ['$']),

        ('Statements', ['break', 'continue', 'ID', 'return', 'global', 'def', 'if', 'while', 'EPSILON'],
         ['$', ';', 'else']),

        ('Statement', ['break', 'continue', 'ID', 'return', 'global', 'def', 'if', 'while'],
         [';']),

        ('Simple_stmt	', ['break', 'continue', 'ID', 'return', 'global'],
         [';']),

        ('Compound_stmt', ['def', 'if', 'while'],
         [';']),

        ('Assignment_Call', ['ID'],
         [';']),

        ('B', ['(', '[', '='],
         [';']),

        ('C', ['ID', '[', 'NUM'],
         [';']),

        ('List_Rest', [',', 'EPSILON'],
         [']']),

        ('Return_stmt', ['return'],
         [';']),

        ('Return_Value', ['ID', 'NUM', 'EPSILON'],
         [';']),

        ('Global_stmt', ['global'],
         [';']),

        ('Function_def', ['def'],
         [';']),

        ('Params', ['ID', 'EPSILON'],
         [')']),

        ('Params_Prime', [',', 'EPSILON'],
         [')']),

        ('If_stmt', ['if'],
         [";"]),

        ('Else_block', ['else', 'EPSILON'],
         [";"]),

        ('Iteration_stmt', ['while'],
         [";"]),

        ('Relational_Expression', ['ID', 'NUM'],
         [")", ':']),

        ('Relop', ['==', '<'],
         ['ID', 'NUM']),

        ('Expression', ['ID', 'NUM'],
         [";", "]", ")", ",", ":", "==", "<"]),

        ('Expression_Prime', ['+', '-', 'EPSILON'],
         [";", "]", ")", ",", ":", "==", "<"]),

        ('Term', ['ID', 'NUM'],
         [";", "]", ")", ",", ":", "==", "<"], "+", "-"),

        ('Term_Prime', ['*', 'EPSILON'],
         [";", "]", ")", ",", ":", "==", "<"], "+", "-"),

        ('Factor', ['ID', 'NUM'],
         [";", "]", ")", ",", ":", "==", "<", "+", "-", "*"]),

        ('Power', ['(', '[', '**', 'EPSILON'],
         [";", "]", ")", ",", ":", "==", "<", "+", "-", "*"]),

        ('Primary', ['(', '[', 'EPSILON'],
         [";", "]", ")", ",", ":", "==", "<", "+", "-", "*"]),


        ('Arguments', ['ID', 'NUM', 'EPSILON'],
         [")"]),

        ('Arguments_Prime', [',', 'EPSILON'],
         [")"]),

        ('Atom', ['ID', 'NUM'],
         [";", "[", "]", "(", ")", ",", ":", "==", "<", "+", "-", "*", "**"]),
    ]

    def is_token_in_firsts(self, non_terminal, terminal):
        result = False
        for pair in self.first_and_follow_sets:
            if pair[0] == non_terminal:
                for first in pair[1]:
                    if first == terminal:
                        result = True

        if terminal == non_terminal:
            result = True
        return result

    def is_token_in_follows(self, non_terminal, terminal):
        for pair in self.first_and_follow_sets:
            if pair[0] == non_terminal:
                for follow in pair[2]:
                    if follow == terminal:
                        return True

        return False

    def get_a_first(self, non_terminal):
        for pair in self.first_and_follow_sets:
            if pair[0] == non_terminal:
                return pair[1][0]


# in this compiler, the prediction sets are not used but the class is implemented anyway.
class PredictSets:
    prediction_sets = [
        ('Program', []),
        ('Statements', []),
        ('Statements', []),
        ('Simple_stmt', []),
        ('Compound_stmt', []),
        ('Assignment_Call', []),
        ('B', []),
        ('C', []),
        ('List_Rest', []),
        ('Return_stmt', []),
        ('Return_Value', []),
        ('Global_stmt	', []),
        ('Function_def', []),
        ('Params', []),
        ('Params_Prime', []),
        ('If_stmt', []),
        ('Else_block', []),
        ('Iteration_stmt', []),
        ('Relational_Expression', []),
        ('Relop', []),
        ('Expression', []),
        ('Expression_Prime', []),
        ('Term', []),
        ('Term_Prime', []),
        ('Factor', []),
        ('Power', []),
        ('Primary', []),
        ('Arguments', []),
        ('Arguments_Prime', []),
        ('Atom', [])
    ]

    def is_token_in_predicts(self, non_terminal, terminal):
        for pair in self.prediction_sets:
            if pair[0] == non_terminal:
                for prediction in pair[1]:
                    if prediction == terminal:
                        return True

        return False


class TransitionDiagrams:
    diagram_tuples = [
        ('Program', [('Statements', 'NT'), ('$', 'T')]),

        ('Statements', [('Statement', 'NT'), (';', 'NT'), ('Statements', 'NT'),
                        ('EPSILON', 'T')]),

        ('Statement', [('Compound_stmt', 'NT'),
                       ('Simple_stmt', 'NT')]),

        ('Simple_stmt', [('Assignment_Call', 'NT'),
                         ('Return_stmt', 'NT'),
                         ('Global_stmt', 'NT'),
                         ('break', 'T'),
                         ('continue', 'T')]),

        ('Compound_stmt', [('Function_def', 'NT'),
                           ('If_stmt', 'NT'),
                           ('Iteration_stmt', 'NT')]),

        ('Assignment_Call', [('ID', 'T'), ('B', 'NT')]),

        ('B', [('=', 'T'), ('C', 'NT'),
               ('[', 'T'), ('Expression', 'NT'), (']', 'T'),
               ('(', 'T'), ('Arguments', 'NT'), (')', 'T')]),

        ('C', [('Expression', 'NT'),
               ('[', 'T'), ('Expression', 'NT'), ('List_Rest', 'NT'), (']', 'T')]),

        ('List_Rest', [(',', 'T'), ('Expression', 'NT'), ('List_Rest', 'NT'),
                       ('EPSILON', 'T')]),

        ('Return_stmt', [('return', 'T'), ('Return_Value', 'NT')]),

        ('Return_Value', [('Expression', 'NT'),
                          ('EPSILON', 'T')]),

        ('Global_stmt', [('global', 'T'), ('ID', 'T')]),


        ('Function_def', [('def', 'T'), ('ID', 'T'), ('(', 'T'), ('Params', 'NT'), (')', 'T'), (':', 'T'), ('Statements', 'NT')]),

        ('Params', [('ID', 'T'), ('Params_Prime', 'NT'),
                    ('EPSILON', 'T'),]),

        ('Params_Prime', [(',', 'T'), ('ID', 'T'), ('Params_Prime', 'NT'),
                          ('EPSILON', 'T')]),

        #If_stmt -> if Relational_Expression : Statements Else_block
        ('If_stmt', [('if', 'T'), ('Relational_Expression', 'NT'), (':', 'T'), ('Statements', 'NT'), ('Else_block', 'NT')]),

        #Else_block -> else : Statements
        ('Else_block ', [('else', 'T'), (':', 'T'), ('Statements', 'NT'),
                         ('EPSILON', 'T')]),

        #Iteration_stmt -> while ( Relational_Expression ) Statements
        ('Iteration_stmt', [('while', 'T'), ('(', 'T'), ('Relational_Expression', 'NT'), (')', 'T'), ('Statements', 'NT')]),

        #Relational_Expression -> Expression Relop Expression
        ('Relational_Expression', [('Expression', 'NT'), ('Relop', 'NT'), ('Expression', 'NT')]),

        ('Relop', [('==', 'T'), ('<', 'T')]),

        #Expression -> Term Expression_Prime
        ('Expression', [('Term', 'NT'), ('Expression_Prime', 'NT')]),

        #Expression_Prime -> + Term Expression_Prime | Expression_Prime -> - Term Expression_Prime |eps
        ('Expression_Prime', [('+', 'T'), ('Term', 'NT'), ('Expression_Prime', 'NT'),
                              ('Term', 'NT'), ('Expression_Prime', 'NT'),
                              ('EPSILON', 'T')]),

        #Term -> Factor Term_Prime | Term_Prime -> * Factor Term_Prime | esp
        ('Term', [('Factor', 'NT'), ('Term_Prime', 'NT'),
                  ('*', 'T'), ('Factor', 'NT'), ('Term_Prime', 'NT'),
                  ('EPSILON', 'T')]),

        #Factor -> Atom Power
        ('Factor', [('Atom', 'T'), ('Power', 'NT')]),

        #Power -> ** Factor | Power -> Primary
        ('Power', [('**', 'T'), ('Factor', 'NT'),
                   ('Primary', 'NT')]),

        #Primary -> [ Expression ] Primary | Primary -> ( Arguments ) Primary | eps
        ('Primary', [('[', 'T'), ('Expression', 'NT'), (']', 'T'), ('Primary', 'NT'),
                     ('(', 'T'), ('Arguments', 'NT'), (')', 'T'), ('Primary', 'NT'),
                     ('EPSILON', 'T')]),

        #Arguments -> Expression Arguments_Prime | eps
        ('Arguments', [('Expression', 'NT'), ('Arguments_Prime', 'NT'),
                       ('EPSILON', 'T')]),

        #Arguments_Prime -> , Expression Arguments_Prime
        ('Arguments_Prime', [(',', 'T'), ('Expression', 'NT'), ('Arguments_Prime', 'NT'),
                             ('EPSILON', 'T')]),

        ('Atom', [('ID', 'T'), ('NUM', 'T')])
    ]


fafs = FirstAndFollowSets()
td = TransitionDiagrams()


def initiate_parsing():
    scanner.initiate_lexical_errors_file(scanner.lex_errors_address)
    scanner.get_input_stream_from_input(scanner.input_address)
    children = []
    for edge in td.diagram_tuples[0][1][0]:
        if edge is not None:
            new_node = parse_diagram(edge)
            if new_node is not None:
                children.append(new_node)
    parsed_tree.children = children


def parse_diagram(diagram):
    global eop
    if eop:
        return None
    print(f'parsing: {diagram}')
    global token_popped
    if token_popped:
        get_new_token()
        print(f'new token is: {get_token()}: {get_token_type()}')
        token_popped = False
    diagram_node = Node(f'{diagram[0]}')

    if diagram[1] == 'T':
        if diagram[0] == 'EPSILON':
            diagram_node.children = [Node('epsilon')]
            return diagram_node
        if get_token() == diagram[0] or get_token_type() == diagram[0]:
            print(f'parsed {get_token()}')
            if get_token() == '$':
                diagram_node.name = '$'
                token_popped = True
                return diagram_node
            else:
                diagram_node.name = f'({get_token_type()}, {get_token()})'
                token_popped = True
                return diagram_node
        else:
            if get_token() == '$':
                update_syntax_errors(get_token_line(), 'Unexpected EOF', '')
                eop = True
                return None
            else:
                update_syntax_errors(get_token_line(), diagram[0], 'missing')
                return None
    else:

        children = []
        for sequence in td.diagram_tuples:
            if diagram[0] == sequence[0]:

                for route in sequence[1]:
                    if fafs.is_token_in_firsts(route[0][0], get_token()) or fafs.is_token_in_firsts(route[0][0],
                                                                                                    get_token_type()):
                        for edge in route:
                            new_node = parse_diagram(edge)
                            if new_node is not None:
                                children.append(new_node)

                        if children:
                            diagram_node.children = children
                            return diagram_node

                for route in sequence[1]:
                    if fafs.is_token_in_follows(diagram[0], get_token()) or fafs.is_token_in_follows(diagram[0],
                                                                                                     get_token_type()):
                        if fafs.is_token_in_firsts(diagram[0], 'EPSILON'):
                            if route[0][0] == 'EPSILON':
                                diagram_node.children = [Node('epsilon')]
                                return diagram_node

                for route in sequence[1]:
                    if fafs.is_token_in_firsts(route[0][0], 'EPSILON') and (
                            fafs.is_token_in_follows(route[0][0], get_token()) or fafs.is_token_in_follows(route[0][0],
                                                                                                           get_token_type())):
                        for edge in route:
                            new_node = parse_diagram(edge)
                            if new_node is not None:
                                children.append(new_node)
                        diagram_node.children = children
                        return diagram_node

                if fafs.is_token_in_follows(sequence[0], get_token()) or fafs.is_token_in_follows(sequence[0],
                                                                                                  get_token_type()):
                    update_syntax_errors(get_token_line(), sequence[0], 'missing')
                    return None

                else:
                    if get_token_type() == 'ID' or get_token_type() == 'NUM':
                        if get_token_type() == 'SYMBOL':
                            print('\n\n\nhi\n\n\n')
                        update_syntax_errors(get_token_line(), get_token_type(), 'illegal')
                        token_popped = True
                        return parse_diagram(diagram)
                    else:

                        update_syntax_errors(get_token_line(), get_token(), 'illegal')
                        token_popped = True
                        return parse_diagram(diagram)


initialize_errors_file(syntax_errors_address)
initiate_parsing()

save_parsed_tree(parsed_tree_address)

if errors_raised:
    save_syntax_errors(syntax_errors_address)