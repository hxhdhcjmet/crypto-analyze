"""
用五组新生成的六密钥组测试第五轮密文差分筛选效果.

复用lab2/code/plaintext.txt中的明文集合；每组新密钥都重新计算对应密文，
不使用现有ciphertext.txt中的固定密钥密文.

去噪条件在最终密文差分上判断. 本程序统计筛选后保留的明文对数，并用
任务一的理论差分概率估计保留对中正确对所占的比例，不逐对解密判定.
"""

import random
from pathlib import Path


S = [9, 8, 0, 1, 14, 11, 12, 13, 3, 2, 5, 7, 15, 10, 6, 4]
P = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]

STATE_SIZE = 1 << 16
INPUT_DIFFERENCE = 0x0001
ACTIVE_NIBBLE_SHIFT = 4
ALLOWED_SBOX_OUTPUT_DIFFERENCES = {0x1, 0x2, 0x5}
THEORETICAL_DIFFERENTIAL_PROBABILITY = 0.0479736328125
NUMBER_OF_KEY_SETS = 5
RANDOM_SEED = 20261003

# 避免生成的五组新密钥中偶然包含指导书示例密钥组.
REFERENCE_KEYS = (0x0123, 0x4567, 0x89AB, 0xCDEF, 0xFEDC, 0xBA98)

TASK_DIRECTORY = Path(__file__).resolve().parent
PLAINTEXT_FILE = TASK_DIRECTORY.parent / "code" / "plaintext.txt"


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
    """预先计算全部16比特状态经过一轮S盒与P置换的结果."""
    return [P_box(S_box(value)) for value in range(STATE_SIZE)]


def generate_key_sets(number_of_sets=NUMBER_OF_KEY_SETS, seed=RANDOM_SEED):
    """生成互不相同、且不同于指导书示例组的六字密钥组."""
    rng = random.Random(seed)
    used_key_sets = {REFERENCE_KEYS}
    key_sets = []

    while len(key_sets) < number_of_sets:
        keys = tuple(rng.randrange(STATE_SIZE) for _ in range(6))
        if keys not in used_key_sets:
            used_key_sets.add(keys)
            key_sets.append(keys)

    return key_sets


def cipherFourEnc(plain_text, keys, SP_table):
    """执行四轮SP、第五轮无P以及末尾白化，返回密文."""
    state = plain_text

    for round_index in range(4):
        state = SP_table[state ^ keys[round_index]]

    state = S_box(state ^ keys[4])
    return state ^ keys[5]


def get_input_difference_pairs(plaintext):
    """构造输入差分为0x0001的有序明文对索引."""
    plaintext_index = {value: index for index, value in enumerate(plaintext)}
    if len(plaintext_index) != len(plaintext):
        raise ValueError("明文文件中存在重复值，无法建立明文索引.")

    pairs = []
    for index, plain_text in enumerate(plaintext):
        paired_plain_text = plain_text ^ INPUT_DIFFERENCE
        if paired_plain_text in plaintext_index:
            pairs.append((index, plaintext_index[paired_plain_text]))

    return pairs


def passes_denoising(cipher_text_1, cipher_text_2):
    """判断密文差分是否属于0x0010、0x0020或0x0050."""
    difference = cipher_text_1 ^ cipher_text_2
    other_nibbles_are_zero = (difference & 0xFF0F) == 0
    active_difference = (difference >> ACTIVE_NIBBLE_SHIFT) & 0xF

    return (
        other_nibbles_are_zero
        and active_difference in ALLOWED_SBOX_OUTPUT_DIFFERENCES
    )


def count_retained_pairs(plaintext, pair_indices, keys, SP_table):
    """统计一组六字密钥下通过密文差分筛选的明文对数."""
    ciphertexts = [
        cipherFourEnc(plain_text, keys, SP_table) for plain_text in plaintext
    ]

    retained_count = 0
    for index_1, index_2 in pair_indices:
        if passes_denoising(ciphertexts[index_1], ciphertexts[index_2]):
            retained_count += 1

    return retained_count


def main():
    """使用五组新密钥执行密文差分筛选并输出保留对数."""
    plaintext = read_data(PLAINTEXT_FILE)
    pair_indices = get_input_difference_pairs(plaintext)
    SP_table = build_SP_table()
    key_sets = generate_key_sets()

    print("输入明文数: %d" % len(plaintext))
    print("输入差分: 0x%04X" % INPUT_DIFFERENCE)
    print("密文筛选差分: 0x0010、0x0020、0x0050")
    print("有序输入差分对数: %d" % len(pair_indices))
    print(
        "理论差分概率p: %.13f，m*p: %.2f"
        % (
            THEORETICAL_DIFFERENTIAL_PROBABILITY,
            len(pair_indices) * THEORETICAL_DIFFERENTIAL_PROBABILITY,
        )
    )
    print("密钥组数: %d" % NUMBER_OF_KEY_SETS)
    print("随机种子: %d" % RANDOM_SEED)
    print()
    print("序号 | 六字密钥组 | 实际保留数 | 理论正确对数m*p | 正确对占比估计")

    results = []
    for index, keys in enumerate(key_sets, start=1):
        retained_count = count_retained_pairs(
            plaintext, pair_indices, keys, SP_table
        )
        results.append(retained_count)
        theoretical_correct_count = (
            len(pair_indices) * THEORETICAL_DIFFERENTIAL_PROBABILITY
        )
        estimated_correct_ratio = (
            theoretical_correct_count / retained_count
            if retained_count
            else 0.0
        )
        key_text = "[" + ", ".join("0x%04X" % key for key in keys) + "]"
        print(
            "%2d | %s | %8d | %14.2f | %.6f (%.2f%%)"
            % (
                index,
                key_text,
                retained_count,
                theoretical_correct_count,
                estimated_correct_ratio,
                100 * estimated_correct_ratio,
            )
        )

    if results:
        print()
        print("五组平均去噪保留对数: %.2f" % (sum(results) / len(results)))


if __name__ == "__main__":
    main()
