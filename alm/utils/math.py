import math

def comb(n, r) -> int:
    """nCrを求める

    Args:
        n (int): 総数
        r (int): 選ぶ個数

    Returns:
        int: nCrの解
    """
    return math.factorial(n) // (math.factorial(n-r) * math.factorial(r))
