Coloring New Languages
======================

Print to HTML maps Sublime Text 2's language scopes to Pygments tokens. This document aims to explain what that means, how it works, and how you can improve incorrect/missing colorings yourself.

## What is a scope? ##

Sublime Text 2 names the tags given to each character, scopes. For instance, Python's ```import``` statement has the scope ```keyword.control.import.python```. Characters can have a bunch of scopes at once, so the order that we map scopes to tokens does matter.

## What is a token? ##

Pygments uses a bunch of tokens to map out the different types of code, and how to format them. Pygments tokens are things like ```Name.Builtin```, ```Comment.Multiline```, ```String```. The full list of Pygments tokens are in pygments/token.py, defined in STANDARD_TYPES.

# Mapping Scopes to Tokens #

Now, how do we map these Sublime scopes to Pygments tokens? There's a workflow that I use, that seems to work fairly well:

1. Enable ```debug``` in PrintToHTML's user settings. This allows you to see the scopes for every character of text PrintToHTML parses. (I also like to disable ```auto_print_in_browser```)
2. Select a short amount of text, containing just the line(s) with the part of code you're looking to color.
3. I like to copy the console output to a new buffer, to make it easier to search and look through.
4. Find an appropriate character in the output stream.
5. Look through the scopes applied to that character. Choose the scope you think fits best for coloring this code.
6. Map it to a scope that fits.
7. Test, check with default color theme and with perldoc.
