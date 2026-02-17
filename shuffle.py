from typing import List, Any
import random


def sample_n(arr: List[Any], n: int) -> List[Any]:
    """Random sample of up to n items. Uses all items if n >= len(arr)."""
    n = min(n, len(arr))
    return random.sample(arr, n)
