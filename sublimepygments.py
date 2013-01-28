# coding=utf8

import sublime
from pygments.lexer import Lexer
from pygments.token import Error, Text, Other, \
     Comment, Operator, Keyword, Name, String, Number, Generic, Punctuation


scope_names = [
    ## Generics
    ['comment.line', Comment.Single],
    ['comment', Comment],

    ['numeric', Number],
    ['arithmetic', Number],

    ## Language-specific scopes
    # Python
    ['constant.other.placeholder.python', Name.Variable],
    ['string.quoted.double.block.python', String.Doc],

    ['keyword.control.import.python', Keyword.Namespace],
    ['keyword.control.import.from.python', Keyword.Namespace],

    ['support.function.builtin.python', Name.Builtin],
    ['variable.language.python', Name.Builtin.Pseudo],

    ['entity.other.inherited-class.python', Name.Attribute],

    ['storage.type.class.python', Keyword],
    ['storage.type.function.python', Keyword],

    ['keyword.operator.logical.python', Operator.Word],

    # C/C-like
    ['storage.modifier.c', Keyword],
    ['storage.type.c', Keyword.Type],
    ['meta.function-call.c', Name.Attribute],
    ['support.function.C99.c', Name.Attribute],

    # Java
    ['storage.modifier.import.java', Name.Namespace],

    ['storage.modifier.java', Keyword],
    ['storage.type.java', Keyword.Type],

    ['variable.parameter.java', Name.Variable],

    ## Low-priority generics
    ['string.quoted.single.single-line', String.Single],
    ['string', String],

    ['constant', Name.Constant],

    # For the operator output with Pygments' lexer, switch 'keyword' and 'operator'
    ['keyword', Keyword],
    ['operator', Operator],

    ['entity.name.type.class', Name.Class],
    ['entity.name.function', Name.Function],
    ['storage.type', Keyword.Type],

    ['variable.parameter.function', Name.Variable],
]


class SublimeLexer(Lexer):
    """
    For `Sublime Text 2 <http://www.sublimetext.com/2>`_ source code.
    """

    name = 'Sublime'
    aliases = []
    filenames = []
    mimetypes = []

    def get_tokens(self, args, unfiltered=False):
        region, view = args

        tokens = []
        buffer_token = Generic
        buffer_string = u''

        spaces = u' ' * int(view.settings().get('tab_size', 8))

        python_namespace = 0

        settings = sublime.load_settings('Print to HTML.sublime-settings')
        debug = settings.get('debug', False)

        for i in range(region.a, region.b):
            current_string = view.substr(sublime.Region(i, i+1))
            current_scope = view.scope_name(i)

            # turn tabs into spaces per view's setting to ensure proper indentation
            if current_string == u'\t':
                current_string = spaces

            for scope in scope_names:
                if scope[0] in current_scope:
                    current_token = scope[1]
                    break
                elif scope == scope_names[-1]:
                    current_token = Generic

            # Python namespace highlighting
            if python_namespace and (current_string == u'\n'):
                python_namespace = 0
            if (('keyword.control.import.python' in current_scope) or \
                ('keyword.control.import.from.python' in current_scope)) and \
                ((len(buffer_string) == 0) or (buffer_token != current_token)):
                python_namespace += 1
            if (python_namespace == 1) and ('keyword.control.import' not in current_scope) and \
                (current_string not in [u' ', u'\n']):
                current_token = Name.Namespace

            if debug:
                if len(buffer_string) > 50:
                    print_buffer_string = buffer_string[(len(buffer_string) - 50):]
                else:
                    print_buffer_string = buffer_string
                print [python_namespace, current_string, current_token, print_buffer_string]
                print '  ', [current_scope]

            if buffer_token == current_token:
                buffer_string += current_string
            else:
                if len(buffer_string):
                    tokens.append((buffer_token, buffer_string))
                    if debug:
                        print '    ', [buffer_token, buffer_string], '\n'
                buffer_token = current_token
                buffer_string = current_string

        tokens.append((buffer_token, buffer_string))

        return tokens
