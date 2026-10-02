# Lien LeetCode : https://leetcode.com/problems/two-sum/description/

# Two Sums (Hashing / Complement)

def twoSum(nums: list[int], target: int) -> list[int]:
    dico = {}

    for i, num in enumerate(nums):
        complement = target - num

        if complement in dico:
            return [i, dico[complement]]
        dico[num] = i
