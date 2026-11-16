from typing import List, Any
import random


def sample_n(arr: List[Any], n: int) -> List[Any]:
    """Random sample of up to n items. Uses all items if n >= len(arr)."""
    n = min(n, len(arr))
    return random.sample(arr, n)


def apply_ordered_groups(ids: List[str], groups: List[List[str]]) -> List[str]:
    """If any track of a group is in ids, the whole group goes in, back to back and in
    order, where the first one appeared. Keeps len(ids) by dropping tracks from the end."""
    size = len(ids)
    ids = list(ids)
    grouped = {t for g in groups for t in g}
    for group in groups:
        hits = [i for i, t in enumerate(ids) if t in group]
        if not hits:
            continue
        ids = [t for t in ids if t not in group]
        ids[hits[0]:hits[0]] = group
    while len(ids) > size:
        # drop the last track that isn't part of a rule
        ids.pop(max(i for i, t in enumerate(ids) if t not in grouped))
    return ids
