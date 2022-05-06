import re

# regular expression compilations:
white_space_rexp = re.compile(r'\n|\t|\f|\r|\v|\s')
symbol_rexp = re.compile(r';|:|,|\[|]|\(|\)|\+|-|\*|=|<')
alphabet_rexp = re.compile(r'[A-Za-z]')
num_rexp = re.compile(r'[0-9]')
valid_inputs = re.compile(r"[A-Za-z]|[0-9]|;|:|,|\[|\]|\(|\)|\+|-|\*|/|=|<|#|\n|\r|\t|\v|\f|\s")
keywords = re.compile(r'if|else|continue|break|return|while|def')

# scanner variables
tokens_address = "tokens.txt"
lex_errors_address = "lexical_errors.txt"
symbol_table_address = "symbol_table.txt"
input_address = "input.txt"
current_line = 1
input_stream_pointer = 0
new_token = []
input_stream = ""
terminate_flag = False
eof_flag = False
unseen_token = False
error_raised = False
emergency_flag = False
return_eop_next_time = False
lexical_errors = []
tokens = []
symbol_table_elements = [
    "break", "continue", "def", "else", "if", "return", "while"
]


def update_symbol_table(element):
    for i in range(len(symbol_table_elements)):
        if element == symbol_table_elements[i]:
            return 1

    symbol_table_elements.append(element)
    return 0


def update_tokens(line, token, ttype):
    global unseen_token, new_token, current_line
    tokens.append([line, token, ttype])
    unseen_token = True
    new_token = [current_line, token, ttype]


def update_errors(line, error, error_description):
    lexical_errors.append([line, error, error_description])


def save_symbol_table(address):
    with open(address, 'w') as f:
        for i in range(len(symbol_table_elements)):
            f.write(f"{i + 1}.\t{symbol_table_elements[i]}\n")


def save_errors(address):
    if error_raised:
        with open(address, 'w') as f:
            cline = 1
            lines_first_token = True
            no_line_written_yet = True
            for error in lexical_errors:
                if not error:
                    continue
                line_number = error[0]
                error_itself = error[1]
                error_description = error[2]
                while line_number != cline:
                    cline += 1
                    lines_first_token = True
                if lines_first_token:
                    lines_first_token = False
                    if cline != 1 and (not no_line_written_yet):
                        f.write("\n")
                    f.write(f"{cline}.\t")
                f.write(f"({error_itself}, {error_description}) ")
                no_line_written_yet = False


def save_tokens(address):
    with open(tokens_address, 'w') as f:
        current_line = 1
        lines_first_token = True
        no_line_written_yet = True
        for token in tokens:
            if not token:
                continue
            line_number = token[0]
            token_name = token[1]
            token_type = token[2]
            while line_number != current_line:
                current_line += 1
                lines_first_token = True
            if lines_first_token:
                lines_first_token = False
                if current_line != 1 and (not no_line_written_yet):
                    f.write("\n")
                f.write(f"{current_line}.\t")
            f.write(f"({token_type}, {token_name}) ")
            no_line_written_yet = False


def initiate_lexical_errors_file(address):
    with open(address, 'w') as f:
        f.write("There is no lexical error.")


def get_input_stream_from_input(address):
    global input_stream
    with open(address, 'rb') as f:
        input_stream = (f.read(50000)).decode()
    input_stream += '\n'


def check_white_space(char):
    if char == "\n":
        global current_line
        current_line += 1
    return re.match(white_space_rexp, char)


def start_state():
    global error_raised, input_stream_pointer, new_token, eof_flag, unseen_token
    if input_stream_pointer >= len(input_stream):
        eof_flag = True
        unseen_token = True
        return
    while input_stream_pointer in range(len(input_stream)):
        if check_white_space(input_stream[input_stream_pointer]):
            input_stream_pointer += 1
            if not input_stream_pointer in range(len(input_stream)):
                eof_flag = True
                return
            continue
        if re.match(symbol_rexp, input_stream[input_stream_pointer]):
            symbol_state()
            break
        elif re.match(num_rexp, input_stream[input_stream_pointer]):
            num_state()
            break
        elif re.match(alphabet_rexp, input_stream[input_stream_pointer]):
            keyword_or_id_state()
            break
        elif input_stream[input_stream_pointer] == "/" or input_stream[input_stream_pointer] == "#":
            comment_state()
            break
        else:
            update_errors(current_line, input_stream[input_stream_pointer], "Invalid input")
            input_stream_pointer += 1
            error_raised = True
            break


def symbol_state():
    global input_stream_pointer, error_raised, eof_flag, unseen_token, emergency_flag
    if not (input_stream_pointer + 1 in range(len(input_stream))):
        update_tokens(current_line, input_stream[input_stream_pointer], "SYMBOL")
        input_stream_pointer += 1
        #emergency_flag = True
        eof_flag = True
        return
    if not re.match(valid_inputs, input_stream[input_stream_pointer + 1]):
        if input_stream[input_stream_pointer] == "=" or input_stream[input_stream_pointer] == "*":
            update_errors(current_line, input_stream[input_stream_pointer] + input_stream[input_stream_pointer + 1],
                          "Invalid "
                          "input")
            input_stream_pointer += 2
            error_raised = True
            return
    if input_stream[input_stream_pointer] == "=":
        if input_stream[input_stream_pointer + 1]:
            if input_stream[input_stream_pointer + 1] == "=":
                update_tokens(current_line, "==", "SYMBOL")
                input_stream_pointer += 2
                return
        update_tokens(current_line, "=", "SYMBOL")
        input_stream_pointer += 1
        return
    elif input_stream[input_stream_pointer] == "*":
        if input_stream[input_stream_pointer + 1]:
            if input_stream[input_stream_pointer + 1] == "*":
                update_tokens(current_line, "**", "SYMBOL")
                input_stream_pointer += 2
                return
            elif input_stream[input_stream_pointer + 1] == '/':
                update_errors(current_line, "*/", "Unmatched comment")
                error_raised = True
                input_stream_pointer += 2
                return
        update_tokens(current_line, "*", "SYMBOL")
        input_stream_pointer += 1
        return
    elif input_stream[input_stream_pointer] == "*" and input_stream[input_stream_pointer + 1] == "/":
        update_errors(current_line, "*/", "Unmatched comment")
        error_raised = True
        input_stream_pointer += 2
        return
    else:
        update_tokens(current_line, input_stream[input_stream_pointer], "SYMBOL")
        input_stream_pointer += 1
        return


def num_state():
    global input_stream_pointer, error_raised
    num = ""
    num += (input_stream[input_stream_pointer])
    input_stream_pointer += 1
    while True:
        if input_stream_pointer == len(input_stream):
            update_tokens(current_line, num, "NUM")
            return
        if re.match(num_rexp, input_stream[input_stream_pointer]):
            num += (input_stream[input_stream_pointer])
            input_stream_pointer += 1
            continue
        elif input_stream[input_stream_pointer] == '.':
            num += '.'
            input_stream_pointer += 1
            continue
        elif re.match(alphabet_rexp, input_stream[input_stream_pointer]) or not re.match(valid_inputs, input_stream[input_stream_pointer]):
            update_errors(current_line, num + input_stream[input_stream_pointer], "Invalid number")
            error_raised = True
            input_stream_pointer += 1
            return
        elif re.match(valid_inputs, input_stream[input_stream_pointer]):
            if check_white_space(input_stream[input_stream_pointer]):
                input_stream_pointer += 1
            update_tokens(current_line, num, "NUM")
            return
        else:
            update_tokens(current_line, num, "NUM")
            update_errors(current_line, input_stream[input_stream_pointer], "Invalid input")
            error_raised = True
            input_stream_pointer += 1
            return


def keyword_or_id_state():
    global input_stream_pointer, error_raised
    keyword_or_id = ""
    keyword_or_id += input_stream[input_stream_pointer]
    input_stream_pointer += 1
    while True:
        if re.match(alphabet_rexp, input_stream[input_stream_pointer]) or re.match(num_rexp,
                                                                                   input_stream[input_stream_pointer]):
            keyword_or_id += input_stream[input_stream_pointer]
            input_stream_pointer += 1
            continue
        elif re.match(symbol_rexp, input_stream[input_stream_pointer]) or re.match(white_space_rexp,
                                                                                   input_stream[input_stream_pointer]):
            if re.match(keywords, keyword_or_id):
                update_tokens(current_line, keyword_or_id, "KEYWORD")
            else:
                update_tokens(current_line, keyword_or_id, "ID")
            update_symbol_table(keyword_or_id)
            if re.match(white_space_rexp, input_stream[input_stream_pointer]):
                check_white_space(input_stream[input_stream_pointer])
                input_stream_pointer += 1
            return
        elif re.match(valid_inputs, input_stream[input_stream_pointer]):
            if re.match(keywords, keyword_or_id):
                update_tokens(current_line, keyword_or_id, "KEYWORD")
            else:
                update_tokens(current_line, keyword_or_id, "ID")
            update_symbol_table(keyword_or_id)
            return
        else:
            update_errors(current_line, keyword_or_id + input_stream[input_stream_pointer], "Invalid input")
            error_raised = True
            input_stream_pointer += 1
            return


def comment_state():
    global input_stream_pointer, error_raised, eof_flag
    comment = ""
    if not re.match(valid_inputs, input_stream[input_stream_pointer + 1]):
        update_errors(current_line, input_stream[input_stream_pointer] + input_stream[input_stream_pointer + 1], "Invalid input")
        input_stream_pointer += 2
        error_raised = True
        return
    if input_stream[input_stream_pointer] == "#":
        input_stream_pointer += 1
        while True:
            if (input_stream[input_stream_pointer] == "\n") or (not input_stream_pointer in range(len(input_stream))):
                check_white_space(input_stream[input_stream_pointer])
                input_stream_pointer += 1
                return
            else:
                comment += input_stream[input_stream_pointer]
                input_stream_pointer += 1
                continue
    else:
        input_stream_pointer += 1
        if input_stream[input_stream_pointer] == "*":
            input_stream_pointer += 1
            comment_beginning_line = current_line
            while True:
                if input_stream_pointer in range(len(input_stream)):
                    if input_stream[input_stream_pointer] == "*":
                        if input_stream_pointer + 1 in range(len(input_stream)):
                            if input_stream[input_stream_pointer + 1] == "/":
                                input_stream_pointer += 2
                                return
                            else:
                                comment += "*"
                                input_stream_pointer += 1
                        else:
                            update_errors(comment_beginning_line, f"/*{comment[0:8]}...", "Unclosed comment")
                            error_raised = True
                            eof_flag = True
                            return
                    else:
                        comment += input_stream[input_stream_pointer]
                        check_white_space(input_stream[input_stream_pointer])
                        input_stream_pointer += 1

                else:
                    update_errors(comment_beginning_line, f"/*{comment[0:8]}...", "Unclosed comment")
                    error_raised = True
                    eof_flag = True
                    return
        else:
            update_errors(current_line, "/", "Invalid input")
            error_raised = True
            return


def get_next_token():
    global unseen_token, new_token, eof_flag, terminate_flag, current_line, emergency_flag, return_eop_next_time

    while not unseen_token:
        start_state()
    unseen_token = False
    if eof_flag:
        emergency_flag = True
        eof_flag = False
        temp = new_token
        return_eop_next_time = True
        return [current_line, "$", "EOP"]


    return new_token
