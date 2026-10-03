"""
验证实验指导书给出的六个密钥字是否生成lab2/code中的明密文文件.

CipherFour结构:
    前四轮: 异或轮密钥、过S盒、拉线置换.
    第五轮: 异或K5、过S盒，不做拉线置换.
    最后: 异或白化密钥K6.

逐个加密明文文件中的数据，并与同一位置的密文比较. 只有全部匹配，
才能确认文件与这组六个密钥及上述轮结构相符.
"""

from pathlib import Path


S = [9, 8, 0, 1, 14, 11, 12, 13, 3, 2, 5, 7, 15, 10, 6, 4]
P = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]

# 实验指导书给出的K1,...,K6.
ROUND_KEYS = [0x0123, 0x4567, 0x89AB, 0xCDEF, 0xFEDC, 0xBA99]
STATE_SIZE = 1 << 16

TASK_DIRECTORY = Path(__file__).resolve().parent
DATA_DIRECTORY = TASK_DIRECTORY.parent / "code"
PLAINTEXT_FILE = DATA_DIRECTORY / "plaintext.txt"
CIPHERTEXT_FILE = DATA_DIRECTORY / "ciphertext.txt"


def read_data(filename):
    """读取以空格、逗号或换行分隔的16比特十六进制数据."""
    data = filename.read_text(encoding="utf-8").replace(",", " ").split()
    values = [int(value, 16) for value in data]

    if any(value < 0 or value >= STATE_SIZE for value in values):
        raise ValueError("输入文件中包含超出16比特范围的数据: %s" % filename)

    return values


def S_box(value):
    """对16比特状态的四个半字节分别使用S盒."""
    output = 0

    for shift in (12, 8, 4, 0):
        output |= S[(value >> shift) & 0xF] << shift

    return output


def P_box(value):
    """对16比特状态进行实验定义的P置换."""
    input_bits = format(value, "016b")
    output_bits = "".join(input_bits[index] for index in P)
    return int(output_bits, 2)


def build_SP_table():
    """预先计算全部16比特状态经过S盒与P置换的结果."""
    return [P_box(S_box(value)) for value in range(STATE_SIZE)]


def cipherFourEnc(plain_text, keys, SP_table):
    """按四轮SP加第五轮无P及末尾白化的结构加密."""
    state = plain_text

    for round_index in range(4):
        state = SP_table[state ^ keys[round_index]]

    state = S_box(state ^ keys[4])
    return state ^ keys[5]


def main():
    """加密文件中的明文并报告与文件密文的逐项比较结果."""
    plaintext = read_data(PLAINTEXT_FILE)
    ciphertext = read_data(CIPHERTEXT_FILE)

    if len(plaintext) != len(ciphertext):
        raise ValueError("明文和密文数量不一致.")
    if len(set(plaintext)) != len(plaintext):
        raise ValueError("明文文件中存在重复值，不能按顺序验证一一对应关系.")

    SP_table = build_SP_table()
    mismatches = []

    for index, (plain_text, expected_cipher_text) in enumerate(
        zip(plaintext, ciphertext)
    ):
        actual_cipher_text = cipherFourEnc(plain_text, ROUND_KEYS, SP_table)
        if actual_cipher_text != expected_cipher_text:
            mismatches.append(
                (index, plain_text, expected_cipher_text, actual_cipher_text)
            )

    print("验证密钥组:", ["0x%04X" % key for key in ROUND_KEYS])
    print("明文数量: %d" % len(plaintext))
    print("密文不匹配数: %d" % len(mismatches))

    if not mismatches:
        print("验证通过：文件中所有明密文均与该密钥组及轮结构一致.")
        return

    print("验证未通过：以下为前%d个不匹配项:" % min(10, len(mismatches)))
    print("序号 | 明文 | 文件密文 | 按指导书密钥计算的密文")
    for index, plain_text, expected, actual in mismatches[:10]:
        print(
            "%4d | 0x%04X | 0x%04X | 0x%04X"
            % (index, plain_text, expected, actual)
        )


if __name__ == "__main__":
    main()
