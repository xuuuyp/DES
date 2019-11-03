import f

optionType = input("加密输入0，解密输入其他")
text = input("文本")
length = len(text)

Result = ""
if optionType == '0':
    # 若输入文本的长度不是4的整数倍，即不是64字节的整数倍，用空格补全（此处为了加密中文，用的是unicode编码，
    # 即用16字节表示一个字符）
    text = text + (8 - length % 8) * " "
    length = len(text)
    key = input("输入7位密钥")

    while (len(key) != 7):
        print("7位！")
        key = input("输入7位密钥")

    for i in range(int(length / 8)):
        #一次读入64个字节
        tempText = [text[j] for j in range(i * 8, i * 8 + 8)]
        Result = Result + f.des(tempText, key, int(optionType))
    print("加密后" + Result)

if optionType != '0':
    length = len(text)
    key = input("输入7位密钥")
    while (len(key) != 7):
        print("7位！")
        key = input("输入7位密钥")
    for i in range(int(length / 8)):
        tempText = [text[j] for j in range(i * 8, i * 8 + 8)]
        Result = Result + f.des(tempText, key, int(optionType))
    print("解密后" + Result)
