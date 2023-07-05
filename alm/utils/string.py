def contains(str_list: list, text: str) -> bool:
    """文字列が含まれるかを確認する

    Args:
        str_list (list): 文字列のリスト
        text (str): 探したい文字列

    Returns:
        bool: 文字列が含まれるかどうか
    """
    res = False
    for s in str_list:
        res = res or s == text
    return res
