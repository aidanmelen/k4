from collections import defaultdict
from typing import List, Dict

import re


def chunk_dict(d: Dict[str, str], chunk_size=6):
    """
    Splits a dictionary into a list of sub-dictionaries, with each sub-dictionary containing at most chunk_size key-value pairs.

    Args:
        d (Dict[str, str]): The input dictionary to be chunked.
        chunk_size (int, optional): The maximum number of key-value pairs in each sub-dictionary. Defaults to 6.

    Returns:
        List[Dict[str, str]]: A list of sub-dictionaries, each containing at most chunk_size key-value pairs.

    Example:
        >>> d = {'a': '1', 'b': '2', 'c': '3', 'd': '4', 'e': '5', 'f': '6', 'g': '7', 'h': '8', 'i': '9', 'j': '10'}
        >>> chunk_dict(d, chunk_size=3)
        [{'a': '1', 'b': '2', 'c': '3'}, {'d': '4', 'e': '5', 'f': '6'}, {'g': '7', 'h': '8', 'i': '9'}, {'j': '10'}]
    """
    chunks = []
    chunk = {}
    for k, v in d.items():
        if len(chunk) == chunk_size:
            chunks.append(chunk)
            chunk = {}
        chunk[k] = v
    if chunk:
        chunks.append(chunk)
    return chunks


def get_top_prefixes(names: List[str], max_keys: int = 10) -> Dict[str, int]:
    """
    Given a list of names, returns a dictionary of the most common prefixes and their counts.

    Args:
        names (List[str]): A list of topic names.
        max_keys (int, optional): The maximum number of top prefixes to return. Defaults to 10.

    Returns:
        Dict[str, int]: A dictionary of the most common topic prefixes and their counts.

    Example:
        >>> names = ["topic1", "_topic1", "topic2.v1", "topic2.v2", "topic3-example", "topic3-test", "Topic3"]
        >>> get_top_prefixes(names)
        {'topic3': 3, 'topic1': 2, 'topic2': 2}
    """
    pattern = r"^[._-]?([a-zA-Z0-9]+)"

    namespace_to_counts = defaultdict(int)

    for name in names:
        match = re.match(pattern, name, re.IGNORECASE)
        if match:
            namespace_to_counts[match.group(1).lower()] += 1
    
    top_prefix_to_counts = {k:v for k, v in sorted(namespace_to_counts.items(), key=lambda item: item[1], reverse=True)[:max_keys]}

    return top_prefix_to_counts

def shorten(text: str, width: int, placeholder: str = '...') -> str:
    """
    Shortens the given text to the specified width by replacing the characters
    beyond the specified width with the specified placeholder string.

    Args:
        text: The text to be shortened.
        width: The maximum width of the shortened text.
        placeholder: The string to be used as a placeholder for the truncated text.

    Returns:
        The shortened text as a string.

    """
    if len(text) < width:
        return text

    shortened_text = text[:int(width) - len(placeholder)]
    return shortened_text + placeholder

