# Lien LeetCode : https://leetcode.com/problems/maximum-average-subarray-i/

### Maximum Avergage Subarray I

def findMaxAverage(nums: list[int], k: int) -> float:
    actual_window_sum = sum(nums[:k])
    max_sum = actual_window_sum

    for i in range(k, len(nums)):
        actual_window_sum -= nums[i - k]
        actual_window_sum += nums[i]

        max_sum = max(max_sum, actual_window_sum)
    
    return max_sum / k
