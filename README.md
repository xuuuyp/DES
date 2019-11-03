# DES
DES加解密python实现<br>
firstdes.py中代码来自https://blog.csdn.net/u013005150/article/details/25804787<br>
运行DES.py，输入0进行加密，其他任何非0字符进行解密<br>
然后输入7位密钥（firstdes.py中为8位，输入7位是因为每7比特加一个奇偶校验码）<br>
加解密中的修改有，firstdes.py中进行16轮交叉互换循环后最后再进行一次交叉互换，在一定程度上浪费资源<br>
经修改后进行15轮交叉互换循环后最后再进行一次无交叉互换的过程<br>
自此，此代码更加符合DES设计的理念
