from typing import List, Any
import random


def fisher_yates_shuffle(arr: List[Any]) -> List[Any]:
    for i in range(len(arr) - 1, 0, -1):
        j = random.randint(0, i)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


def shuffle_n_times(arr: List[int], n: int) -> List[int]:
    for _ in range(n):
        arr = fisher_yates_shuffle(arr)
    return arr
