import re

def extract_number_in_string(string: str):
    """
    文字列から数字のみを抽出します
    """
    return int("".join(re.findall(r'\d+', string)))
