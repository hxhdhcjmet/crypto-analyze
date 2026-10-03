"""补充实验指导要求的去噪测试；直接复用修改后的参考程序。

运行：python3 task4_denoising_test.py
先测试指定的六个轮密钥，再换五组密钥测试，按有序明文对计数。
没有增加辅助差分攻击或截断差分攻击。
"""

import random

from task4_key_recovery import S, INPUT_DIFFERENCE, ROUND_KEYS, data_select, CountKey

P = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
STATE_SIZE = 2 ** 16
SEED = 20261001


def S_box(value):
    output = 0
    for shift in [12, 8, 4, 0]:
        output |= S[(value >> shift) & 0xF] << shift
    return output


def P_box(value):
    input_bits = bin(value)[2:].zfill(16)
    return int(''.join(input_bits[P[i]] for i in range(16)), 2)


def build_tables():
    S_table = [S_box(x) for x in range(STATE_SIZE)]
    SP_table = [P_box(value) for value in S_table]
    return S_table, SP_table


def cipherFourEnc(plainText, keys, S_table, SP_table):
    """五轮加密：前四轮有P置换，第五轮无P置换，共六个密钥字。"""
    state = plainText
    for i in range(4):
        state = SP_table[state ^ keys[i]]
    return S_table[state ^ keys[4]] ^ keys[5]


def generate_key_sets():
    rng = random.Random(SEED)
    key_sets = [tuple(ROUND_KEYS)]
    while len(key_sets) < 6:
        keys = tuple(rng.randrange(STATE_SIZE) for _ in range(6))
        if keys not in key_sets:
            key_sets.append(keys)
    return key_sets


def run_experiment():
    S_table, SP_table = build_tables()
    results = []
    for keys in generate_key_sets():
        ciphertext = [cipherFourEnc(x, keys, S_table, SP_table)
                      for x in range(STATE_SIZE)]
        pairs = [(ciphertext[x], ciphertext[x ^ INPUT_DIFFERENCE])
                 for x in range(STATE_SIZE)]

        # 去噪完全复用第3.1.2.4节修改后的参考程序。
        selected_pairs = data_select(pairs)

        # 仿真密钥已知，用真实目标半字节的评分核对正确对数。
        # 筛选保证其他三个半字节差分为0，因此该评分恰好是正确对数。
        # 这个核对值仅评估去噪效果，不用于明密文文件的攻击排序。
        true_key = (keys[5] >> 4) & 0xF
        correct_count = CountKey(selected_pairs)[true_key]
        kept_count = len(selected_pairs)
        purity = correct_count / kept_count if kept_count else 0.0
        results.append((keys, kept_count, correct_count, purity))
    return results


if __name__ == '__main__':
    print('输入差分: 0x0001，四轮目标输出差分: 0x0010')
    print('五轮算法最后一轮无P置换，六个16比特轮密钥')
    print('随机种子:', SEED)
    print('组别 | 轮密钥组 | 去噪保留对数 | 正确对数 | 正确对占比')
    print('-' * 100)
    results = run_experiment()
    for index, (keys, kept, correct, purity) in enumerate(results):
        key_text = '[' + ', '.join('0x%04X' % key for key in keys) + ']'
        print('%d | %s | %d | %d | %.10f' %
              (index, key_text, kept, correct, purity))
    print('每组初始有序明文对数:', STATE_SIZE)
    print('各组正确对占比的平均值: %.10f' %
          (sum(row[3] for row in results) / len(results)))
    print('合并六组后的正确对占比: %.10f' %
          (sum(row[2] for row in results) / sum(row[1] for row in results)))
