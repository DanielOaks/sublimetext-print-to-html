Sublime Text 3 Print to HTML
============================

A Sublime Text 3 plugin to print files as HTML with color syntax highlighting and line numbers, and open them in your browser for printing.

Colorization and HTML conversion is currently performed by [Pygments][0], which supports a range of [languages and syntaxes][3].

## Installation

 * Install [Package Manager][2].
 * Use `Cmd+Shift+P` or `Ctrl+Shift+P` then `Package Control: Install Package`.
 * Look for `Print to HTML` and install it.

If you prefer to install manually, install git, then:

    git clone https://github.com/joelpt/sublimetext-print-to-html "<Sublime Text 3 Packages folder>/Print to HTML"

## Usage

 * For best results, save your file with an appropriate extension beforehand.
 * To print the current file, use one of the following methods:
   * use `Shift+Alt+P` to print current file as HTML via your browser, or
   * from File menu, use `Print as HTML to Browser` or `Print as HTML to New Buffer`.
   * press `Ctrl+Shift+P` or `Cmd+Shift+P` then type `print`.
 * Edit settings in `Preferences->Package Settings->Print in HTML` to customize output formatting and behavior. Options such as monochrome, line numbering, and browser behavior can be modified.


Coloring New Languages
----------------------

Print to HTML maps Sublime Text 2's language scopes to Pygments tokens. This document aims to explain what that means, how it works, and how you can improve incorrect/missing colorings yourself.

## What is a scope? ##

Sublime Text 2 names the tags given to each character, scopes. For instance, Python's ```import``` statement has the scope ```keyword.control.import.python```. Characters can have a bunch of scopes at once, so the order that we map scopes to tokens does matter.

## What is a token? ##

Pygments uses a bunch of tokens to map out the different types of code, and how to format them. Pygments tokens are things like ```Name.Builtin```, ```Comment.Multiline```, ```String```. The full list of Pygments tokens are in pygments/token.py, defined in STANDARD_TYPES.

# Mapping Scopes to Tokens #

Now, how do we map these Sublime scopes to Pygments tokens? There's a workflow that I use, that seems to work fairly well:

1. Install the ```ScopeHunter``` package. Run the *Toggle Instant Scoper* command. Whenever you click on the string you want to highlight, it'll pop up the scope(s) that the text is in down the bottom.
2. Look through the scopes applied to that character. Choose the scope you think fits best for coloring this code.
3. Map it to a scope that fits. Do this by modifying the ```Mappings``` settings document
4. Test, it's good to check with default color theme and with perldoc.

Note: If possible, it's good to try and apply the scoping information to one of the language-independant scopes, rather than a language-specific one. As an example, a class name might be under something like ```class.name.python``` as well as ```class.name```, and in that case it would be better to scope the more generic ```class.name```.

This is so that we can do the least amount of work possible to try and scope everything – as well as the upside that quite a bit of new languages are already scoped decently!


Credits
-------

This code is available on [Github][1]. Pull requests are welcome.

Created by [Joel Thornton][4], extended by [Daniel Oaks][5].

Uses the [Pygments][0] library (included) for code-to-HTML conversion.


 [0]: http://pygments.org/
 [1]: https://github.com/joelpt/sublimetext-print-to-html
 [2]: http://wbond.net/sublime_packages/package_control
 [3]: http://pygments.org/languages/
 [4]: mailto:sublime@joelpt.net
 [5]: mailto:daniel@danieloaks.net
