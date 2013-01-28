# coding=utf8

import sublime
import sublime_plugin
import desktop
import tempfile
import re
import textwrap

from sublimepygments import SublimeLexer

import pygments
import pygments.formatters
import pygments.lexers

with open('wordwrap.js') as f:
    WORD_WRAP_SCRIPT_BLOCK = '\n'.join(['<script>', f.read(), '</script>'])


class PrintToHtmlCommand(sublime_plugin.TextCommand):
    """Convert current file to HTML and view in browser or ST2 buffer."""

    def run(self, edit, target='browser'):
        settings = sublime.load_settings('Print to HTML.sublime-settings')

        # get the selected text or the full text, based on whether regions are selected
        selections = self.view.sel()

        if text_selected(selections):
            regions = []

            for selection in selections:
                # convert to start/end at start/end of selected line
                region = self.view.line(sublime.Region(selection.a, selection.b))

                # check for previous selection's bounds, add together if they overlap
                if len(regions) > 0 and (regions[-1].b >= region.a):
                    new_region = sublime.Region(regions[-1].a, region.b)
                    regions[-1] = new_region
                else:
                    regions.append(region)

        else:
            region = sublime.Region(0, self.view.size())
            regions = [region]

        # get the buffer's filename
        filename = self.view.file_name()

        # determine output encoding
        encoding = self.view.encoding()
        if encoding == 'Undefined':
            encoding = 'UTF-8'
        elif encoding == 'Western (Windows 1252)':
            encoding = 'windows-1252'

        # turn tabs into spaces per view's setting to ensure proper indentation
        #spaces = ' ' * int(self.view.settings().get('tab_size', 8))
        #for i in range(len(texts)):
        #    texts[i][1] = re.sub(r'\t', spaces, texts[i][1])

        # gather Pygment related option flags from plugin settings
        optlist = ['line_numbering', 'draw_background', 'line_anchors']
        options = dict(map(lambda x: (x, settings.get(x, False)), optlist))

        # style
        style = settings.get('style', 'default')

        # perform the conversion to HTML
        css, texts = convert_to_html(filename, regions, encoding, options, style, self.view)

        # construct onload body attrib for print/close JS within browser
        if target == 'browser':
            onload = ' onload="'
            if settings.get('auto_print_in_browser', False):
                onload += 'window.print();'
                if settings.get('auto_close_in_browser', False):
                    onload += 'window.close();'
            onload += '"'
        else:
            onload = ''

        # force black and white styling if monochrome setting is on
        if settings.get('monochrome', False):
            css += '\n'.join(['',
                '.highlight * { color: black !important; }',
                '.highlight .err { border: 1px solid black !important; }'])

        # set font family
        if settings.get('font_face', None):
            css += '\n.highlight * { font-family: %s; }' % settings.get('font_face')

        # set font size
        if settings.get('font_size', None):
            css += '\n.highlight { font-size: %s; }' % settings.get('font_size')

        # set line height
        if settings.get('line_height', None):
            css += '\n.highlight { line-height: %s; }' % settings.get('line_height')

        # hide Pygments error borders unless requested to show
        if not settings.get('draw_error_borders', False):
            css += '\n.highlight .err { border: none !important }'

        # wrap long lines if requested
        if settings.get('word_wrap', False):
            # default css word wrap
            css += '\n.highlight > pre { word-wrap: break-word; white-space: pre-wrap; }'

            # use JS in browser to indent wrapped lines past edge of line-number column
            texts += [WORD_WRAP_SCRIPT_BLOCK]

            if settings.get('word_wrap_break_anywhere', False):
                # permit browser to wrap anywhere, not just between words
                css += '\n.highlight > pre { word-break: break-all; }'

        # add custom css
        if settings.get('custom_css', None):
            css += '\n' + settings.get('custom_css')

        # prepare html for final output
        html = construct_html_document(encoding, filename, css, texts, onload)

        # show html in browser or new buffer
        if target == 'browser':
            send_to_browser(html)
        elif target == 'sublime':
            send_to_new_buffer(self.view, html)
        else:
            raise Exception('Unsupported arg "target"')


def construct_html_document(encoding, title, css, texts, body_attribs):
    """Populate simple boilerplate HTML with given arguments."""
    body = '\n'.join(texts).decode('utf-8').encode('ascii', 'xmlcharrefreplace')
    output = '\n'.join([
        '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">',
        '<meta charset="%s">' % encoding,
        '<html>',
        '<head>',
        '<title>%s</title>' % title,
        '<style>',
        css,
        '</style>',
        '</head>',
        '<body%s>' % body_attribs,
        body,
        '</body>',
        '</html>'])
    return output


def send_to_browser(html):
    """Create a temp file containing html and open it in the default web browser."""
    tmp_html = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
    tmp_html.write(html)
    tmp_html.close()
    desktop.open(tmp_html.name)


def send_to_new_buffer(view, html):
    """Load html into a new buffer in the same window as view."""
    new_view = view.window().new_file()
    new_edit = new_view.begin_edit()
    new_view.insert(new_edit, 0, html)
    new_view.end_edit(new_edit)


def convert_to_html(filename, regions, encoding, options, style, view):
    """Convert text to HTML form, using filename and syntax as lexer hints."""
    formatter = pygments.formatters.HtmlFormatter(
        encoding=encoding,
        linenos='inline' if options['line_numbering'] else False,
        nobackground=not options['draw_background'],
        lineanchors='line' if options['line_anchors'] else False,
        style=style,
        linenoend=view.rowcol(regions[-1].b)[0] + 1)

    css = formatter.get_style_defs('.highlight')
    texts = []
    for region in regions:
        formatter.linenostart = view.rowcol(region.a)[0] + 1  # line number for each block
        html = pygments.format(SublimeLexer().get_tokens([region, view]), formatter)
        texts.append(html)

    return css, texts


def text_selected(selections):
    """Return whether or not any text is selected"""
    for selection in selections:
        if selection.a != selection.b:
            return True
    return False
