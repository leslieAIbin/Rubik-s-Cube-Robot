import kociemba

# 红色 0 蓝白 1 白色 2 橙色 3 绿色 4  黄色 5
#              |************|
#              |*U1**U2**U3*|
#              |************|
#              |*U4**U5**U6*|
#              |************|
#              |*U7**U8**U9*|
#              |************|
#  ************|************|************|************
#  *L1**L2**L3*|*F1**F2**F3*|*R1**R2**R3*|*B1**B2**B3*
#  ************|************|************|************
#  *L4**L5**L6*|*F4**F5**F6*|*R4**R5**R6*|*B4**B5**B6*
#  ************|************|************|************
#  *L7**L8**L9*|*F7**F8**F9*|*R7**R8**R9*|*B7**B8**B9*
#  ************|************|************|************
#              |************|
#              |*D1**D2**D3*|
#              |************|
#              |*D4**D5**D6*|
#              |************|
#              |*D7**D8**D9*|
#              |************|
# 按照U R F D L B的顺序形成色块位置顺序 0-53


# cube_list = [0, 0, 4, 0, 4, 2, 5, 4, 1,
#              2, 3, 3, 3, 2, 0, 0, 2, 5,
#              1, 3, 3, 5, 0, 1, 3, 2, 2,
#              2, 1, 4, 5, 1, 4, 0, 4, 1,
#              2, 1, 3, 4, 5, 3, 4, 1, 4,
#              5, 2, 1, 5, 3, 0, 0, 5, 5]


cube_list_origin = [0, 0, 4, 0, 4, 2, 5, 4, 1,
                    2, 3, 3, 3, 2, 0, 0, 2, 5,
                    1, 3, 3, 5, 0, 1, 3, 2, 2,
                    2, 1, 4, 5, 1, 4, 0, 4, 1,
                    2, 1, 3, 4, 5, 3, 4, 1, 4,
                    5, 2, 1, 5, 3, 0, 0, 5, 5]

# 12个棱块对应的色块
edge = [[1, 46], [3, 37], [5, 10], [7, 19],
        [12, 23], [14, 48], [16, 32], [21, 41],
        [25, 28], [30, 43], [39, 50], [34, 52]]

# 8个角块对应的色块
horn = [[0, 36, 47], [2, 11, 45], [6, 18, 38], [8, 20, 9],
        [15, 26, 29], [33, 42, 53], [35, 17, 51], [44, 24, 27]]

center = [4, 13, 22, 31, 40, 49]


# 红色和橙色容易误判，这里对出错后的橙色位置进行判断
# 假定只有红橙色有错，其他颜色正常
def edge_assert(cube_list):
    # 根据棱块位置列出所有棱块色块颜色

    # 存储红色和橙色色块
    edge_orange = {}
    edge_red = {}
    for i in range(len(edge)):
        edge_c = [cube_list[edge[i][0]], cube_list[edge[i][1]]]
        for j in range(2):
            if j == 0:
                temp = edge_c[1]
            else:
                temp = edge_c[0]

            if edge_c[j] == 0:
                if temp in edge_red:
                    edge_red[temp].append(edge[i][j])
                else:
                    edge_red.update({temp: [edge[i][j]]})
            elif edge_c[j] == 3:
                if temp in edge_orange:
                    edge_orange[temp].append(edge[i][j])
                else:
                    edge_orange.update({temp: [edge[i][j]]})

    other_color = [1, 2, 4, 5]

    for i in other_color:
        if i in edge_orange and len(edge_orange[i]) == 1:
            edge_orange.pop(i)
        if i in edge_red and len(edge_red[i]) == 1:
            edge_red.pop(i)

    edge_orange_v = list(edge_orange.values())
    edge_red_v = list(edge_red.values())
    # print(edge_orange_v)
    # print(edge_red_v)
    return [edge_orange_v, edge_red_v]


def horn_assert(cube_list):
    # 根据角块位置列出所有角块色块颜色

    # 存储红色和橙色色块
    horn_orange = {}
    horn_red = {}
    for i in range(len(horn)):
        horn_c = []
        for j in range(3):
            horn_c.append(cube_list[horn[i][j]])
        for j in range(3):
            horn_temp = horn_c.copy()
            del horn_temp[j]
            horn_temp.sort()
            temp = horn_temp[0] * 10 + horn_temp[1]
            if horn_c[j] == 0:
                if temp in horn_red:
                    horn_red[temp].append(horn[i][j])
                else:
                    horn_red.update({temp: [horn[i][j]]})
            elif horn_c[j] == 3:
                if temp in horn_orange:
                    horn_orange[temp].append(horn[i][j])
                else:
                    horn_orange.update({temp: [horn[i][j]]})
    other_color = [12, 24, 45, 15]

    for i in other_color:
        if i in horn_orange and len(horn_orange[i]) == 1:
            horn_orange.pop(i)
        if i in horn_red and len(horn_red[i]) == 1:
            horn_red.pop(i)

    horn_orange_v = list(horn_orange.values())
    horn_red_v = list(horn_red.values())
    # print(horn_orange_v)
    # print(horn_red_v)
    return [horn_orange_v, horn_red_v]


def correct(orange_v, red_v, cube_list):

    if len(orange_v) == 2:
        for i in range(2):
            for j in range(2):
                if len(red_v) == 1:
                    for k in range(2):
                        cube_list0 = cube_list.copy()
                        cube_list0[orange_v[0][i]] = 0
                        cube_list0[orange_v[1][j]] = 0
                        cube_list0[red_v[0][k]] = 3
                        step = solve_list(cube_list0)
                        if step:
                            return step
                elif len(red_v) == 0:
                    cube_list0 = cube_list.copy()
                    cube_list0[orange_v[0][i]] = 0
                    cube_list0[orange_v[1][j]] = 0
                    step = solve_list(cube_list0)
                    if step:
                        return step
    elif len(orange_v) == 1:
        for i in range(2):
            if len(red_v) == 2:
                for j in range(2):
                    for k in range(2):
                        cube_list0 = cube_list.copy()
                        cube_list0[orange_v[0][i]] = 0
                        cube_list0[red_v[0][j]] = 3
                        cube_list0[red_v[1][k]] = 3
                        step = solve_list(cube_list0)
                        if step:
                            return step
            elif len(red_v) == 1:
                for j in range(2):
                    cube_list0 = cube_list.copy()
                    cube_list0[orange_v[0][i]] = 0
                    cube_list0[red_v[0][j]] = 3
                    step = solve_list(cube_list0)
                    if step:
                        return step
            elif len(red_v) == 0:
                cube_list0 = cube_list.copy()
                cube_list0[orange_v[0][i]] = 0
                step = solve_list(cube_list0)
                if step:
                    return step
    elif len(orange_v) == 0:
        if len(red_v) == 2:
            for j in range(2):
                for k in range(2):
                    cube_list0 = cube_list.copy()
                    cube_list0[red_v[0][j]] = 3
                    cube_list0[red_v[1][k]] = 3
                    step = solve_list(cube_list0)
                    if step:
                        return step
        elif len(red_v) == 1:
            for j in range(2):
                cube_list0 = cube_list.copy()
                cube_list0[red_v[0][j]] = 3
                step = solve_list(cube_list0)
                if step:
                    return step

    return False


def solve_list(cube_l):
    cube_str = ""
    try:
        for i in range(len(cube_l)):
            if cube_l[i] == cube_l[4]:
                cube_str += 'U'
            elif cube_l[i] == cube_l[13]:
                cube_str += 'R'
            elif cube_l[i] == cube_l[22]:
                cube_str += 'F'
            elif cube_l[i] == cube_l[31]:
                cube_str += 'D'
            elif cube_l[i] == cube_l[40]:
                cube_str += 'L'
            elif cube_l[i] == cube_l[49]:
                cube_str += 'B'
            else:
                return None
        cube_step = kociemba.solve(cube_str)
        return cube_step
    except ValueError:
        return None


def cube_assert(cube_list):
    step = solve_list(cube_list)
    if step:
        print("魔方色块正确")
        print(step)
        return step

    if cube_list.count(1) != 9 or cube_list.count(2) != 9 or cube_list.count(4) != 9 or cube_list.count(5) != 9:
        print("其他颜色出错，无法矫正")
        return False

    cube_edge = edge_assert(cube_list)
    cube_horn = horn_assert(cube_list)

    orange_err = cube_edge[0] + cube_horn[0]
    red_err = cube_edge[1] + cube_horn[1]

    if len(orange_err) > 2 or len(red_err) > 2 or (len(orange_err) == 2 and len(red_err) == 2):
        print("棱块角块错误太多，无法矫正")
        return False

    step = correct(orange_err, red_err, cube_list)
    if step:
        print("经过矫正")
        print(step)
        return step
    else:
        print("中心块可能出错")
        return False


if __name__ == "__main__":
    cube_assert(cube_list_origin)



