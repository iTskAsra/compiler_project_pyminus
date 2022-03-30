# Created by:
# 1. Kasra Amani: 98101171
# 2. Sara Zahedi: 98170849
import scanner

scanner.initiate_lexical_errors_file(scanner.lex_errors_address)
scanner.get_input_stream_from_input(scanner.input_address)
tokens = []
while True:
    if scanner.eof_flag:
        break
    token = scanner.get_next_token()
    tokens.append(token)


if scanner.error_raised:
    scanner.save_errors(scanner.lex_errors_address)

scanner.save_tokens(scanner.tokens_address)
scanner.save_symbol_table(scanner.symbol_table_address)
