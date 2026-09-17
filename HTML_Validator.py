#!/bin/python3


def validate_html(html):
    '''
    This function performs a limited version of html validation by checking whether every opening tag has a corresponding closing tag.
    '''
    try:
        tags = _extract_tags(html)
    except ValueError:
        return False

    stack = []
    for tag in tags:
        if tag.startswith('</'):
            # closing tag
            if len(stack) == 0:
                return False
            if stack.pop() != _name_of(tag):
                return False
        elif tag.endswith('/>'):
            # self-closing tag: nothing to remember
            continue
        else:
            # opening tag
            stack.append(_name_of(tag))

    return len(stack) == 0


def _extract_tags(html):
    '''
    This is a helper function for `validate_html`.
    By convention in Python, helper functions that are not meant to be used directly by the user are prefixed with an underscore.

    This function returns a list of all the html tags contained in the input string,
    stripping out all text not contained within angle brackets.
    '''
    tags = []
    i = 0
    n = len(html)
    while i < n:
        if html[i] == '<':
            j = html.find('>', i)
            if j == -1:
                raise ValueError('found < without matching >')
            raw = html[i:j + 1]
            tags.append(_strip_attributes(raw))
            i = j + 1
        else:
            i += 1
    return tags


def _strip_attributes(tag):
    '''
    Given a raw tag like '<a href="x">', return '<a>'.
    Handles closing tags and self-closing tags too.
    '''
    inner = tag[1:-1].strip()
    if inner.startswith('/'):
        name = inner[1:].strip().split()[0] if inner[1:].strip() else ''
        return '</' + name + '>'
    if inner.endswith('/'):
        name = inner[:-1].strip().split()[0] if inner[:-1].strip() else ''
        return '<' + name + '/>'
    name = inner.split()[0] if inner else ''
    return '<' + name + '>'


def _name_of(tag):
    '''
    Extract the tag name from a normalized tag string.
    '<a>' -> 'a', '</a>' -> 'a', '<br/>' -> 'br'
    '''
    inner = tag[1:-1].strip().strip('/').strip()
    if not inner:
        return ''
    return inner.split()[0].lower()


def balanced_parens(text):
    '''
    Checks whether every opening parenthesis has a corresponding closing parenthesis of a matching type.
    '''
    stack = []
    for char in text:
        if char in '([{':
            stack.append(char)
        elif char in ')]}':
            if len(stack) == 0:
                return False
            if (stack[-1] == '(' and char == ')') or \
               (stack[-1] == '[' and char == ']') or \
               (stack[-1] == '{' and char == '}'):
                stack.pop()
            else:
                return False
    return len(stack) == 0
