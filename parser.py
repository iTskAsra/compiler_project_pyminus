from anytree import Node, RenderTree
import scanner
import re
from parsetable import parse_table

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
    global token_popped, parsed_tree
    scanner.initiate_lexical_errors_file(scanner.lex_errors_address)
    scanner.get_input_stream_from_input(scanner.input_address)
    children = []
    if token_popped:
        get_new_token()
        print(f'new token is: {get_token()}: {get_token_type()}')
        token_popped = False

    if get_token_type() in ['NUM', 'ID']:
        parser_result = parse_table.parse('Program', get_token_type())
    else:
        parser_result = parse_table.parse('Program', get_token())

    if not parser_result:
        token_popped = True
        initiate_parsing()
        return
    for edge in parser_result:
        if edge is not None:
            new_node = parse_diagram(edge)
            if new_node is not None:
                children.append(new_node)
    parsed_tree.children = children


def parse_diagram(element):
    global eop, token_popped
    if eop:
        return None
    print(f'parsing: {element}')
    print(f'parse tree is {parsed_tree}')
    if token_popped:
        get_new_token()
        print(f'new token is: {get_token()}: {get_token_type()}')
        token_popped = False

    diagram_node = Node(f'{element[0]}')

    if element == 'EPSILON':
        return Node('epsilon')

    if element[1] == 'T':
        if element[0] in [get_token(), get_token_type()]:
            print(f'parsed {get_token()}')
            if get_token() == '$':
                diagram_node.name = '$'
                token_popped = True
                return diagram_node

            diagram_node.name = f'({get_token_type()}, {get_token()})'
            token_popped = True
            return diagram_node
        else:
            if get_token() == '$':
                update_syntax_errors(get_token_line(), 'Unexpected EOF', '')
                eop = True
                return None
            else:
                update_syntax_errors(get_token_line(), element[0], 'missing')
                return None

    if get_token_type() in ['NUMBER','ID']:
        parser_result = parse_table.parse(element[0],get_token_type())
    else:
        parser_result = parse_table.parse(element[0], get_token())

    children = []
    if parser_result == 'EPSILON':
        new_node = parse_diagram(parser_result)
        children.append(new_node)
        diagram_node.children = children
        return diagram_node

    if not parser_result:
        token_popped = True
        return parse_diagram(element)

    if parser_result == 'SYNCH':
        return None
        pass

    for parsable in parser_result:
        new_node = parse_diagram(parsable)
        if new_node is not None:
            children.append(new_node)
    diagram_node.children = children
    return diagram_node







initialize_errors_file(syntax_errors_address)
initiate_parsing()

save_parsed_tree(parsed_tree_address)

if errors_raised:
    save_syntax_errors(syntax_errors_address)