# Lien LeetCode : https://leetcode.com/problems/find-pivot-index/

### Find Pivot Index (Prefix - Suffix)

def pivotIndex(nums: list[int]) -> int:
    left_sum =0
    rigth_sum =sum(nums)

    for i in range(len(nums)):

        rigth_sum -= nums[i]

        if left_sum == rigth_sum:
            return i
        
        left_sum += nums[i]
    
    return -1
