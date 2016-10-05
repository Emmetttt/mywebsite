

code_sample = """"""


print(code_sample)

def codify(x):
    code_open = "<ol>\n<li><code>"
    code_close = "<\code><\li>\n<\ol>"
    new_lines = x.replace('\n', '<\code><\li>\n<code><li>')
    new_indent = new_lines.replace('    ', '&nbsp&nbsp&nbsp ')
    new_code = code_open + new_indent + code_close
    return print(new_code)

codify(code_sample)
