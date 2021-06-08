def conflict(state, nextX):
    """
        nextX 表示下一个皇后的水平位置（X 坐标，既列）
        nextY 表示下一个皇后的垂直位置（y 坐标，即行）
        检查下一个皇后与当前皇后的X坐标相同或在同一条对角线上，将发生冲突，返回True
        如果下一个皇后和当前皇后的水平距离为0（在同一列）或与他们的垂直距离想等（位于一条对角线上），就冲突
    """
    netxY = len(state)
    for i in range(netxY):
        if abs(state[i] - nextX) in (0, netxY - i):
            return True
    return False


def queens(num, state):
    if len(state) == num - 1:
        for pos in range(num):
            if not conflict(state, pos):
                yield (pos, )
    else:
        for pos in range(num):
            if not conflict(state, pos):
                for result in queens(num, state + (pos, )):
                    yield (pos, ) + result


print(list(queens(8, ())))
