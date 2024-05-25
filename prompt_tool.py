from prompt_toolkit.lexers import Lexer
from prompt_toolkit.styles.named_colors import NAMED_COLORS
from prompt_toolkit.completion import NestedCompleter

class RainbowLexer(Lexer):
    def lex_document(self, document):
        colors = list(sorted(NAMED_COLORS.keys(), key=NAMED_COLORS.get))

        def get_line(lineno):
            return [
                (colors[i % len(colors)], c)
                for i, c in enumerate(document.lines[lineno])
            ]

        return get_line

completer = NestedCompleter.from_nested_dict({
    'hello': None,
    'exit': None,
    'close': None,
    'add': None,
    'change': None,
    'edit': None,
    'phone': None,
    'show': None,
    'all': None,
    'birthdays': None,
    'show-birthday': None,
    'add-birthday': None,
    'add-note': None,
    'find-tag': None,
    'sort-notes': None
})