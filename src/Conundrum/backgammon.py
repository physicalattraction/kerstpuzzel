def take_from_msg(msg):
    positions = (21, 19, 5, 3, 15, 20)  # black first
    letters = [msg[x - 1] for x in positions]  # -1 to let array start at 1
    print(''.join(letters))

    # positions = (19, 21, 3, 5, 20, 15)  # white first
    # letters = [msg[x - 1] for x in positions]  # -1 to let array start at 1
    # print(''.join(letters))


if __name__ == '__main__':
    p1 = 'abcdef'
    p2 = 'ghijkl'
    p3 = 'mnopqr'
    p4 = 'stuvwy'
    r1 = p1[::-1]
    r2 = p2[::-1]
    r3 = p3[::-1]
    r4 = p4[::-1]

    take_from_msg(p1 + p2 + p3 + p4)  # 1234
    take_from_msg(p1 + p2 + r4 + r3)  # 1243
    take_from_msg(r2 + r1 + p3 + p4)  # 2134
    take_from_msg(r2 + r1 + r4 + r3)  # 2143
    take_from_msg(p3 + p4 + p1 + p2)  # 3412
    take_from_msg(r4 + r3 + p1 + p2)  # 3421
    take_from_msg(p3 + p4 + r2 + r1)  # 4312
    take_from_msg(r4 + r3 + r2 + r1)  # 4321
