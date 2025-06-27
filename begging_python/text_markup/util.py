"""
    文本快生成器
    收集空行前的所有行并将它们返回
    空行忽略，文件最后返回空行，表示文件结束
"""


def lines(file):
    for line in file:
        yield line
    yield '\n'


def blocks(file):
    block = []
    for line in lines(file):
        if line.strip():
            block.append(line)
        elif block:
            yield ''.join(block).strip()
            block = []
