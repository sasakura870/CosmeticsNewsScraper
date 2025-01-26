from urllib.parse import urlparse

def extract_path_between(url: str, start: str, end: str)  -> list:
    """
    URLから指定された2つのパス間のパスを抽出します
    """
    parsed_url = urlparse(url)
    path_segments = parsed_url.path.split('/')
    try:
        start_index = path_segments.index(start)
        end_index = path_segments.index(end)
        return path_segments[start_index+1:end_index]
    except ValueError:
        return []
