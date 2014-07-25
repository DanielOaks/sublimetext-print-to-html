# coding=utf8

import sublime
from pygments.lexer import Lexer
from pygments.token import STANDARD_TYPES, Generic, Name, Keyword


token_alias_maps = [
    ['Token.Generic', 'Generic'],
    ['Token.Comment', 'Comment'],
    ['Token.Operator', 'Operator'],
    ['Token.Punctuation', 'Punctuation'],
    ['Token.Literal', 'Literal'],
    ['Token.Name', 'Name'],
    ['Token.Keyword', 'Keyword'],
    ['Token.Other', 'Other'],
    ['Token.Error', 'Error'],
    ['Token.Text', 'Text'],

    ['Literal.Number', 'Number'],
    ['Literal.String', 'String'],
    ['Text.Whitespace', 'Whitespace'],
]


def create_token_mapping_dict():
    """Return a dict with all the string -> token mappings."""
    tokens = {}
    for token in STANDARD_TYPES:
        tokens[str(token)] = token

        current_token = str(token)
        for actual, alias in token_alias_maps:
            if current_token.startswith(actual):
                current_token = alias + current_token[len(actual):]
                tokens[str(current_token)] = token
    return tokens


class SublimeLexer(Lexer):
    """
    For `Sublime Text 3 <http://www.sublimetext.com/3>`_ source code.
    """

    name = 'Sublime'
    aliases = []
    filenames = []
    mimetypes = []
    tokens = {}

    def __init__(self):
        self.tokens = create_token_mapping_dict()
        settings = sublime.load_settings('Print to HTML.sublime-settings')
        if settings.get('debug', False):
            from pprint import pprint
            pprint(self.tokens)

    def get_tokens(self, args, unfiltered=False):
        region, view = args

        tokens = []
        buffer_token = Generic
        buffer_string = u''

        spaces_per_tab = int(view.settings().get('tab_size', 8))

        python_namespace = 0

        settings = sublime.load_settings('Print to HTML.sublime-settings')
        debug = settings.get('debug', False)

        scope_map_settings = sublime.load_settings('Mappings.sublime-settings')
        scope_map = scope_map_settings.get('map', [])

        for i in range(region.a, region.b):
            current_string = view.substr(sublime.Region(i, i + 1))
            current_scope = view.scope_name(i)

            # turn tabs into spaces per view's setting to ensure proper indentation
            if current_string == u'\t':
                line_start = i - view.line(sublime.Region(i, i + 1)).a

                this_line = view.substr(view.line(sublime.Region(i, i + 1)))
                this_line_cut = this_line[:line_start + 1]

                cur_tab_length = 0
                cur_out_string = ''
                for char in this_line_cut:
                    if char == '\t':
                        loop_size = 0
                        while loop_size <= len(cur_out_string):
                            loop_size += spaces_per_tab
                        cur_tab_length = loop_size - len(cur_out_string)
                        cur_out_string += u' ' * cur_tab_length
                    else:
                        cur_out_string += char

                current_string = u' ' * cur_tab_length

            for scope in scope_map:
                if scope[0] in current_scope:
                    current_token = self.tokens[scope[1]]
                    break
                elif scope == scope_map[-1]:
                    current_token = Generic

            # Python namespace highlighting
            if python_namespace and (current_string == u'\n'):
                python_namespace = 0
            if (('keyword.control.import.python' in current_scope) or
                    ('keyword.control.import.from.python' in current_scope)) and \
                    ((len(buffer_string) == 0) or (buffer_token != current_token)):
                python_namespace += 1
            if (python_namespace >= 1) and ('keyword.control.import' not in current_scope) and \
                    (current_string not in [u' ', u'\n']):
                current_token = Keyword.Namespace

            if debug:
                if len(buffer_string) > 50:
                    print_buffer_string = buffer_string[(len(buffer_string) - 50):]
                else:
                    print_buffer_string = buffer_string
                print('db1', [python_namespace, current_string, current_token, print_buffer_string])
                print('db2   ', [current_scope])

            if buffer_token == current_token:
                buffer_string += current_string
            else:
                if len(buffer_string):
                    tokens.append((buffer_token, buffer_string))
                    if debug:
                        print('db3      ', [buffer_token, buffer_string], '\n')
                buffer_token = current_token
                buffer_string = current_string

        tokens.append((buffer_token, buffer_string))

        return tokens
