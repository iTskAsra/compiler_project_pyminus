from anytree import Node, RenderTree
import scanner
import re
from parsetable.py import parse_table

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


parse_table = parse_table()

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


def parse_diagram(element):
    global eop, token_popped
    if eop:
        return None
    printf(f'parsing: {element}')
    if token_popped:
        get_new_token()
        printf(f'new token is: {get_token()}: {get_token_type()}')
        token_popped = False

    if element == 'EPSILON':
        diagram_node.children = [Node('epsilon')]
        return diagram_node

    diagram_node = Node(f'{element[0]}')

    if element == 'EPSILON':
        diagram_node.children = [Node('epsilon')]
        return diagram_node

    if get_token_type() ['NUM','ID']:
        parser_result = parse_table.parse(element[0],get_token_type())
    else:
        parser_result = parse_table.parse(element[0], get_token())

    if parser_result == 'EPSILON':
        new_node = parse_diagram(parser_result)
        children.append(new_node)
        diagram_node.children = children
        return diagram_node

    if not parser_result:

        pass

    if parser_result == 'SYNCH':

        pass







initialize_errors_file(syntax_errors_address)
initiate_parsing()

save_parsed_tree(parsed_tree_address)

if errors_raised:
    save_syntax_errors(syntax_errors_address)