"""
第3.1.2.4节 5轮CipherFour算法的差分密钥恢复攻击

本程序基于给定的第3.1.2.4节参考程序修改，保留原攻击流程。
本次攻击使用的差分为: (0x0,0x0,0x0,0x1)-4轮->(0x0,0x0,0x1,0x0)
攻击步骤:
    (1) 从plaintext.txt和ciphertext.txt读取一一对应的明密文.
    (2) 选择输入差分为0001的明文对及其密文对.
    (3) 只保留密文差分为0010, 0020或0050的密文对.
    (4) 遍历k5,2的16种可能, 部分解密最后一轮的第三个S盒.
    (5) 统计满足S盒输入差分为0001的密钥猜测.

注:
    (1) 输入文件plaintext.txt为所有明文, ciphertext.txt为所有密文且明密文按照顺序对应(固定密钥下)
    (2) 输入文件中的数据可以用逗号, 空格或换行分隔. 每个数可以写成0000或0x0000的形式.
"""

import os


S = [9, 8, 0, 1, 14, 11, 12, 13, 3, 2, 5, 7, 15, 10, 6, 4]
S_reverse = [2, 3, 9, 8, 15, 10, 14, 11, 1, 0, 13, 5, 6, 7, 4, 12]

INPUT_DIFFERENCE = 0x0001
# 此处是单个活跃S盒的输入差分，不是完整16比特的四轮输出差分0010。
OUTPUT_DIFFERENCE = 0x0001
ALLOWED_DIFFERENCES = [0x1, 0x2, 0x5]

# plaintext.txt和ciphertext.txt使用的6个轮密钥k0, k1, ..., k5.
ROUND_KEYS = [0x0123, 0x4567, 0x89AB, 0xCDEF, 0xFEDC, 0xBA98]
CORRECT_KEY = (ROUND_KEYS[5] >> 4) & 0xF

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
PLAINTEXT_FILE = os.path.join(FILE_PATH, "plaintext.txt")
CIPHERTEXT_FILE = os.path.join(FILE_PATH, "ciphertext.txt")


def read_data(filename):
    """从文件中读取16比特十六进制数据."""
    with open(filename, "r", encoding="utf-8") as file:
        data = file.read().replace(",", " ").split()
    return [int(value, 16) for value in data]


def get_ciphertext_pairs():
    """读取明密文并获得输入差分为0001的密文对."""
    plaintext = read_data(PLAINTEXT_FILE)
    ciphertext = read_data(CIPHERTEXT_FILE)

    codebook = {}
    for i in range(len(plaintext)):
        codebook[plaintext[i]] = ciphertext[i]

    ciphertext_pairs = []
    for plainText1 in plaintext:
        plainText2 = plainText1 ^ INPUT_DIFFERENCE
        if plainText2 in codebook:
            cipherText1 = codebook[plainText1]
            cipherText2 = codebook[plainText2]
            ciphertext_pairs.append((cipherText1, cipherText2))

    return plaintext, ciphertext_pairs


def data_select(ciphertext_pairs):
    """根据密文差分进行去噪."""
    selected_pairs = []

    for cipherText1, cipherText2 in ciphertext_pairs:
        difference = cipherText1 ^ cipherText2

        # 第一个、第二个、第四个半字节差分为0，第三个为1、2或5
        if difference & 0xFF0F == 0:
            if (difference >> 4) & 0xF in ALLOWED_DIFFERENCES:
                selected_pairs.append((cipherText1, cipherText2))

    return selected_pairs


def CountKey(selected_pairs):
    """统计16种k5,2猜测满足差分方程的次数."""
    counters = [0 for _ in range(16)]

    for cipherText1, cipherText2 in selected_pairs:
        nibble1 = (cipherText1 >> 4) & 0xF
        nibble2 = (cipherText2 >> 4) & 0xF

        for key in range(16):
            input1 = S_reverse[nibble1 ^ key]
            input2 = S_reverse[nibble2 ^ key]

            if input1 ^ input2 == OUTPUT_DIFFERENCE:
                counters[key] += 1

    return counters


if __name__ == "__main__":
    print("本题使用的轮密钥:", ["0x%04X" % key for key in ROUND_KEYS])
    print("本次攻击的正确密钥k5,2（仅用于核对）:", "0x%X" % CORRECT_KEY)
    print()
    plaintext, ciphertext_pairs = get_ciphertext_pairs()
    selected_pairs = data_select(ciphertext_pairs)
    counters = CountKey(selected_pairs)

    # 先按计数从大到小排列, 计数相同时按密钥值从小到大排列.
    key_order = sorted(range(16), key=lambda key: (-counters[key], key))
    candidate_keys = key_order[:2]

    print("明文数量:", len(plaintext))
    print("输入差分为0001的密文对数:", len(ciphertext_pairs))
    print("去噪后保留的密文对数:", len(selected_pairs))
    print()
    print("密钥猜测 | 计数")
    print("-" * 19)

    for key in key_order:
        print("     %X   | %d" % (key, counters[key]))

    print("-" * 19)
    print("候选密钥:", [hex(key) for key in candidate_keys])
