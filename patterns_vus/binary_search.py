# Lien LeetCode : https://leetcode.com/problems/binary-search/description/

### Binary Search

def binary_search(nums: list[int], target: int) -> int:
    left = 0
    rigth = len(nums) - 1

    while left <= rigth:
        mid = (left + rigth) // 2

        if nums[mid] == target:
            return mid
        
        if nums[mid] < target:
            left = mid + 1
        else:
            rigth = mid - 1
    return -1
