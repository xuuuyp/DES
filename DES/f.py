import table


def char2unicode_ascii(in_text):
    """将字符串转化为unicode码，即整数"""
    out_put = []
    for i in range(len(in_text)):
        out_put.append(ord(in_text[i]))
    return out_put


def unicode2bit(in_text):
    """将16位unicode码转化为bit"""
    out_bit = []
    for i in range(len(in_text) * 16):
        out_bit.append((in_text[int(i / 16)] >> (i % 16)) & 1)
    return out_bit


def ascii2bit(in_char):
    """将8位ASCII码转为bit"""
    out_bit = []
    for i in range(len(in_char) * 8):
        out_bit.append((in_char[int(i / 8)] >> (i % 8)) & 1)  # 等同于一次左移一bit
    return out_bit


def bit2unicode(in_bit):
    """将bit转为ascii 码"""
    out_put = []
    temp = 0
    for i in range(len(in_bit)):
        temp = temp | (in_bit[i] << (i % 16))
        if i % 16 == 15:
            out_put.append(temp)
            temp = 0
    return out_put


def bit2ascii(in_bit):
    """将bit转化为ascii"""
    out_put = []
    temp = 0
    for i in range(len(in_bit)):
        temp = temp | (in_bit[i] << (i % 8))
        if i % 8 == 7:
            out_put.append(temp)
            temp = 0
    return out_put


def unicode_ascii2char(in_byte):
    """将unicode,ascii码转为字符"""
    out_text = ""
    for i in range(len(in_byte)):
        out_text = out_text + chr(in_byte[i])
    return out_text


def create_keys(in_keys):
    """生成每一轮的key"""
    b = []
    ascii_key = char2unicode_ascii(in_keys)
    bit_key = ascii2bit(ascii_key)
    for i in range(8):
        a = bit_key[i * 7:i * 7 + 7]
        b.append(a.count(1) % 2)
    for i in range(8):
        bit_key.insert((i + 1) * 7 + i, b[i])


    key = []
    # ascii_key = char2unicode_ascii(in_keys)
    # bit_key = ascii2bit(ascii_key)
    # print(bit_key)

    key0 = [0 for i in range(56)]
    key1 = [0 for i in range(48)]
    # PC1变换（64bit->56bit）
    for i in range(56):
        key0[i] = bit_key[table.yasuo1_table[i] - 1]

    # 确定每轮移位次数
    for i in range(16):
        # 1，2，9，16循环左移一次
        if (i == 0 or i == 1 or i == 8 or i == 15):
            move = 1
        else:
            move = 2

        # 移位操作
        for j in range(move):
            # 每8bit左移一次
            for k in range(8):
                temp = key0[k * 7]
                for m in range(7 * k, 7 * k + 6):
                    key0[m] = key0[m + 1]
                key0[k * 7 + 6] = temp
            temp = key0[0]
            #每28bit左移一次
            for k in range(27):
                key0[k] = key0[k + 1]
            key0[27] = temp
            temp = key0[28]
            for k in range(28, 55):
                key0[k] = key0[k + 1]
            key0[55] = temp

        # PC2变换（56bit->48bit）
        for k in range(48):
            key1[k] = key0[table.yasuo2_table[k] - 1]
        key.extend(key1)
    return key


def des(text, key, type):
    if type == 0:  # 加密
        a = 0
        b = 15
        c = 1
        # d = 15
    else:
        a = 15
        b = 0
        c = -1
        # d = 0
    key = create_keys(key)

    finalTextOfBit = [0 for i in range(64)]
    finalTextOfUnicode = [0 for i in range(4)]

    tempText = [0 for i in range(64)]  # IP逆置换之前结果
    extendR = [0 for i in range(48)]  # 右边明文E扩展结果
    unicodeText = char2unicode_ascii(text)
    if type == 0: #加密
        bitText = ascii2bit(unicodeText)
    else:
        bitText = ascii2bit(unicodeText)

    initTrans = [0 for i in range(64)]  # 初始化，用于存放IP置换后的结果,64

    # 初始IP置换
    for i in range(64):
        initTrans[i] = bitText[table.IP_table[i] - 1]

    # 分为左右两部分
    L = [initTrans[i] for i in range(32)]
    R = [initTrans[i] for i in range(32, 64)]

    # 16轮
    for i in range(a, b, c):
        tempR = R  # 放最初的右明文

        # E扩展置换（32bit->48bit)
        for j in range(48):
            extendR[j] = R[table.extend_table[j] - 1]

        # 本轮key值
        keyi = [key[j] for j in range(i * 48, i * 48 + 48)]

        # 与key值进行异或
        XORResult = [0 for j in range(48)]
        for j in range(48):
            XORResult[j] = keyi[j] ^ extendR[j]

        # S盒替换
        SResult = [0 for k in range(32)]
        for k in range(8):
            row = XORResult[k * 6] * 2 + XORResult[k * 6 + 5]
            column = XORResult[k * 6 + 1] * 8 + XORResult[k * 6 + 2] * 4 + XORResult[k * 6 + 3] * 2 + XORResult[
                k * 6 + 4]
            temp = table.S[k][row * 16 + column]
            for m in range(4):
                SResult[k * 4 + m] = (temp >> m) & 1

        # P盒置换
        PResult = [0 for k in range(32)]
        for k in range(32):
            PResult[k] = SResult[table.P_table[k] - 1]

        # 与L部分异或
        XORWithL = [0 for k in range(32)]
        for k in range(32):
            XORWithL[k] = L[k] ^ PResult[k]
        # L_i = R_(i-1)
        L = tempR
        R = XORWithL
    if type == 0:
        i = i+1
    else:
        i = i-1
    tempR = R  # 放最初的右明文

    # E扩展置换（32bit->48bit)
    for j in range(48):
        extendR[j] = R[table.extend_table[j] - 1]

    # 本轮key值
    keyi = [key[j] for j in range(i * 48, i * 48 + 48)]

    # 与key值进行异或
    XORResult = [0 for j in range(48)]
    for j in range(48):
        XORResult[j] = keyi[j] ^ extendR[j]

    # S盒替换
    SResult = [0 for k in range(32)]
    for k in range(8):
        row = XORResult[k * 6] * 2 + XORResult[k * 6 + 5]
        column = XORResult[k * 6 + 1] * 8 + XORResult[k * 6 + 2] * 4 + XORResult[k * 6 + 3] * 2 + XORResult[
            k * 6 + 4]
        temp = table.S[k][row * 16 + column]
        for m in range(4):
            SResult[k * 4 + m] = (temp >> m) & 1

    # P盒置换
    PResult = [0 for k in range(32)]
    for k in range(32):
        PResult[k] = SResult[table.P_table[k] - 1]

    # 与L部分异或
    XORWithL = [0 for k in range(32)]
    for k in range(32):
        XORWithL[k] = L[k] ^ PResult[k]
    R = tempR
    L = XORWithL

    tempText = L
    tempText.extend(R)

    # IP逆置换
    for k in range(64):
        finalTextOfBit[k] = tempText[table._IP_table[k] - 1]
    if type == 0: #加密
        finalTextOfUnicode = bit2ascii(finalTextOfBit)
    else:
        finalTextOfUnicode = bit2ascii(finalTextOfBit)
    finalTextOfChar = unicode_ascii2char(finalTextOfUnicode)
    return finalTextOfChar


