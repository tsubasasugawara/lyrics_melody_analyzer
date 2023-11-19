class Rate:
    def __init__(self, denominator: int, numerator: int, section_name: str) -> None:
        """木の類似度や単語の一致率を格納するデータ構造

        Args:
            denominator (int): 分母
            numerator (int): 分子
            section_name (str): 楽曲名とセクション。<楽曲名>_[A,S]
        """

        self.denominator = denominator
        self.numerator = numerator
        self.section_name = section_name

    def print(self):
        print(f"{self.section_name}\n分母：{self.denominator}\n分子：{self.numerator}")
