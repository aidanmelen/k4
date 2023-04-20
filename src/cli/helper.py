from collections import defaultdict
from typing import List, Dict

import re

def chunk_dict(d: Dict[str, str], chunk_size=6):
    """Split a dictionary into a list of dictionaries, with each sub-dictionary containing at most chunk_size key-value pairs."""
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
        >>> names = ["topic1", "_topic1", "topic2.test", "topic2.example", "topic3.v1"]
        >>> get_top_prefixes(names)
        {'topic1': 2, 'topic2': 2, 'topic3': 1}
    """
    pattern = r"^[._-]?([a-zA-Z0-9]+)"

    namespace_to_counts = defaultdict(int)

    for name in names:
        match = re.match(pattern, name)
        if match:
            namespace_to_counts[match.group(1)] += 1
    
    top_prefix_to_counts = {k:v for k, v in sorted(namespace_to_counts.items(), key=lambda item: item[1], reverse=True)[:max_keys]}

    return top_prefix_to_counts