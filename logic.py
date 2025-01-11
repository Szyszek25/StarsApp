# logic.py

from typing import List, Optional

class Star:
    def __init__(self, name: str, distance: float, spectral_type: str):
        self.name = name
        self.distance = distance
        self.spectral_type = spectral_type

    def __str__(self):
        return f"{self.name} | {self.distance:.2f} ly | {self.spectral_type}"

def merge_sort(stars_list: List[Star]) -> List[Star]:
    if len(stars_list) <= 1:
        return stars_list
    mid = len(stars_list) // 2
    left_half = merge_sort(stars_list[:mid])
    right_half = merge_sort(stars_list[mid:])
    return merge(left_half, right_half)

def merge(left: List[Star], right: List[Star]) -> List[Star]:
    merged = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if left[i].distance <= right[j].distance:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

def binary_search_by_name(stars_list: List[Star], target_name: str) -> Optional[int]:
    # Kopia i sortowanie po nazwie (rosnąco)
    sorted_by_name = sorted(stars_list, key=lambda s: s.name.lower())
    left, right = 0, len(sorted_by_name) - 1
    target_name_lower = target_name.lower()

    while left <= right:
        mid = (left + right) // 2
        mid_name = sorted_by_name[mid].name.lower()
        if mid_name == target_name_lower:
            return mid
        elif mid_name < target_name_lower:
            left = mid + 1
        else:
            right = mid - 1
    return None
