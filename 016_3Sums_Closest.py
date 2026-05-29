class Solution:
    def threeSumClosest(self, nums: list[int], target: int) -> int:
        ##排列
        nums.sort()
        closest_sum = float("inf")
        for i in range(len(nums)-2):
            left = i+1
            right = len(nums) - 1
            
            while left < right:
                tmp_sum = nums[i] + nums[left] + nums[right]
                tmp_diff = abs(tmp_sum - target)
                if tmp_diff <= abs(closest_sum - target):
                        closest_sum = tmp_sum
                if tmp_diff == 0:
                    return target
                elif tmp_sum > target:
                    right -= 1
                elif tmp_sum < target:
                    left += 1
        
        return closest_sum

test = Solution()
print(test.threeSumClosest([-1,2,1,-4], 1))