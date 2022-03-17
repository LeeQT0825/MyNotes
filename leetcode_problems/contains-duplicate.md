# 题目：contains-duplicate
&emsp;给定一个整数数组，判断是否存在重复元素。
如果存在一值在数组中出现至少两次，函数返回 true 。如果数组中每个元素都不相同，则返回 false 。
## 示例1
```
输入: [1,2,3,1]
输出: true
```
## 示例2
```
输入: [1,1,1,3,3,4,3,2,4,2]
输出: true
```
------
# 解题思路
## 方法一：排序
&emsp;在对数字从小到大排序之后，数组的重复元素一定出现在相邻位置中。因此，我们可以扫描已排序的数组，每次判断相邻的两个元素是否相等，如果相等则说明存在重复的元素。

### 代码
```cpp
class Solution {
public:
    bool containsDuplicate(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        int n = nums.size();
        for (int i = 0; i < n - 1; i++) {
            if (nums[i] == nums[i + 1]) {
                return true;
            }
        }
        return false;
    }
};
```

### 复杂度分析
- 时间复杂度：**O(NlogN)**，其中 ***N*** 为数组的长度。需要对数组进行排序。
- 空间复杂度：**O(logN)**，其中 ***N*** 为数组的长度。注意我们在这里应当考虑递归调用栈的深度。
  
## 方法二：哈希表
&emsp;对于数组中每个元素，我们将它插入到哈希表中。如果插入一个元素时发现该元素已经存在于哈希表中，则说明存在重复的元素。

### 代码
```cpp
class Solution {
public:
    bool containsDuplicate(vector<int>& nums) {
        unordered_set<int> s;
        for (int x: nums) {
            if (s.find(x) != s.end()) {
                return true;
            }
            s.insert(x);
        }
        return false;
    }
};
```

### 复杂度分析
- 时间复杂度：**O(N)**，其中 ***N*** 为数组的长度。
- 空间复杂度：**O(N)**，其中 ***N*** 为数组的长度。