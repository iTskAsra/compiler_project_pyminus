# Created by:
# 1. Kasra Amani: 98101171
# 2. Sara Zahedi: 98170849
import scanner
import parser

#scanner.initiate_lexical_errors_file(scanner.lex_errors_address)
scanner.get_input_stream_from_input(scanner.input_address)


if scanner.error_raised:
    pass
    #scanner.save_errors(scanner.lex_errors_address)

#scanner.save_symbol_table(scanner.symbol_table_address)

parser.initiate_parsing()
#parser.save_syntax_errors(parser.syntax_errors_address)
#parser.save_parsed_tree(parser.parsed_tree_address)
#parser.truncate_utf8_chars(parser.parsed_tree_address)
#scanner.save_tokens(scanner.tokens_address)