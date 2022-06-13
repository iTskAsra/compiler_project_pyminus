from anytree import Node, RenderTree
import scanner
import re
import os
from parsetable import parse_table
from code_generator import CodeGenerator

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
code_generator = CodeGenerator()
output_address = 'output.txt'

valid_first = re.compile(r'if|else|continue|break|return|while|def')


def write_code_to_file(address):
    with open(address, 'w') as f:
        for tac in code_generator.program_block:
            f.write(f'{tac.opno}\t({tac.operation}, {tac.lhs}, {tac.rhs}, {tac.target})')


def truncate_utf8_chars(filename, count=1, ignore_newlines=False):
    """
    Truncates last `count` characters of a text file encoded in UTF-8.
    :param filename: The path to the text file to read
    :param count: Number of UTF-8 characters to remove from the end of the file
    :param ignore_newlines: Set to true, if the newline character at the end of the file should be ignored
    """
    with open(filename, 'rb+') as f:
        last_char = None

        size = os.fstat(f.fileno()).st_size

        offset = 1
        chars = 0
        while offset <= size:
            f.seek(-offset, os.SEEK_END)
            b = ord(f.read(1))

            if ignore_newlines:
                if b == 0x0D or b == 0x0A:
                    offset += 1
                    continue

            if b & 0b10000000 == 0 or b & 0b11000000 == 0b11000000:
                # This is the first byte of a UTF8 character
                chars += 1
                if chars == count:
                    # When `count` number of characters have been found, move current position back
                    # with one byte (to include the byte just checked) and truncate the file
                    f.seek(-1, os.SEEK_CUR)
                    f.truncate()
                    return
            offset += 1


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
    initialize_errors_file(address)
    if syntax_errors:
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
        # print(f'new token is: {get_token()}: {get_token_type()}')
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
    if token_popped:
        get_new_token()
        print(f'new token is: {get_token()}: {get_token_type()}')
        token_popped = False

    if element == 'EPSILON':
        return Node('epsilon')

    if element[1] == 'AS':
        pass
        code_generator.call_routine(element[0])
        print(f'generated code for {element[0]}')
        return

    diagram_node = Node(f'{element[0]}')

    if element[1] == 'T':
        if element[0] in [get_token(), get_token_type()]:
            print(f'parsed {get_token()}')
            if get_token() == '$':
                eop = True
                diagram_node.name = '$'
                token_popped = True
                return diagram_node

            diagram_node.name = f'({get_token_type()}, {get_token()})'
            token_popped = True
            return diagram_node
        else:
            if get_token() == '$':
                update_syntax_errors(get_token_line(), element[0], 'missing')
                eop = True
                return Node('$')
            else:
                update_syntax_errors(get_token_line(), element[0], 'missing')
                if element[0] == '$':
                    print(get_token())
                return None

    if get_token_type() in ['NUM', 'ID']:
        parser_result = parse_table.parse(element[0], get_token_type())
    else:
        parser_result = parse_table.parse(element[0], get_token())

    children = []
    if parser_result == 'EPSILON':
        new_node = parse_diagram(parser_result)
        children.append(new_node)
        diagram_node.children = children
        return diagram_node

    if parser_result == 'SYNCH':
        update_syntax_errors(get_token_line(), element[0], 'missing')
        return None

    if not parser_result:
        if get_token() == '$':
            update_syntax_errors(get_token_line(), 'Unexpected EOF', '')
            eop = True
            return None
        if get_token_type() in ['ID', 'NUM']:
            update_syntax_errors(get_token_line(), get_token_type(), 'illegal')
        else:
            update_syntax_errors(get_token_line(), get_token(), 'illegal')
        token_popped = True
        return parse_diagram(element)

    if parser_result == 'SYNCH':
        update_syntax_errors(get_token_line(), element[0], 'missing')
        return None

    for parsable in parser_result:
        new_node = parse_diagram(parsable)
        if new_node is not None:
            children.append(new_node)
    diagram_node.children = children
    return diagram_node
