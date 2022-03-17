[TOC]
# 题目：maximum-subarray
&emsp;给定一个整数数组 nums ，找到一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。
## 示例1
```
输入：nums = [-2,1,-3,4,-1,2,1,-5,4]
输出：6
解释：连续子数组 [4,-1,2,1] 的和最大，为 6 。
```
## 示例2
```
输入：nums = [-1]
输出：-1
```
------
# 解题思路
## 方法一：动态规划
&emsp;假设 $\textit{nums}$ 数组的长度是 $n$，下标从 $0$ 到 $n−1$。
我们用 $f(i)$ 代表以第 $i$ 个数结尾的「连续子数组的最大和」，那么很显然我们要求的答案就是：

$$
\max_{0 \leq i \leq n-1} \{ f(i) \}
$$

&emsp;因此我们只需要求出每个位置的 $f(i)$，然后返回 $f$ 数组中的最大值即可。那么我们如何求 $f(i)$ 呢？我们可以考虑 $\textit{nums}[i]$ 单独成为一段还是加入 $f(i−1)$ 对应的那一段，这取决于 $\textit{nums}[i]$ 和 $f(i-1) +nums[i]$ 的大小，我们希望获得一个比较大的，于是可以写出这样的动态规划转移方程：

$$
f(i) = \max \{ f(i-1) + \textit{nums}[i], \textit{nums}[i] \}
$$

&emsp;不难给出一个时间复杂度 $O(n)$、空间复杂度 $O(n)$ 的实现，即用一个 $f$ 数组来保存 $f(i)$ 的值，用一个循环求出所有 $f(i)$。考虑到 $f(i)$ 只和 $f(i−1)$ 相关，于是我们可以只用一个变量 $\textit{pre}$ 来维护对于当前 $f(i)$ 的 $f(i−1)$ 的值是多少，从而让空间复杂度降低到 $O(1)$，这有点类似**滚动数组**的思想。

### 代码
```cpp
class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        int pre = 0, maxAns = nums[0];
        for (const auto &x: nums) {
            pre = max(pre + x, x);
            maxAns = max(maxAns, pre);  //更新最大和考虑只有一个元素数组的情况
        }
        return maxAns;
    }
};
```
### 复杂度分析
- 时间复杂度：$O(n)$，其中 $n$ 为 $\textit{nums}$ 数组的长度。我们只需要遍历一遍数组即可求得答案。
- 空间复杂度：$O(1)$。我们只需要常数空间存放若干变量。
### 注意：
1. 数组不是类，但也是容器，也有迭代器。不同的是数组不可以用调用方法的方式调用迭代器。
```cpp
#include <iterator>
int arr[SIZE];
arr.begin();    //错
auto begin(arr);    //正确
```
2. $\textit{size\_t}$ 是一种机器相关的 $\textit{unsigned}$ 类型。  

## 方法二：分治
&emsp;这个分治方法类似于 ***线段树求解最长公共上升子序列问题*** 的 ***pushUp*** 操作。 （推荐阅读线段树区间合并法解决多次询问的 ***区间最长连续上升序列问题*** 和 ***区间最大子段和问题***）

&emsp;我们定义一个操作 $get(a, l, r)$ 表示查询 $a$ 序列 $[l,r]$ 区间内的最大子段和，那么最终我们要求的答案就是 $get(nums, 0, nums.size() - 1)$。如何分治实现这个操作呢？对于一个区间 $[l,r]$，我们取 $m = \lfloor \frac{l + r}{2}​
⌋$，对区间 $[l,m]$ 和 $[m+1,r]$ 分治求解。当递归逐层深入直到区间长度缩小为 $1$ 的时候，递归 *开始回升* 。这个时候我们考虑如何通过 $[l,m]$ 区间的信息和 $[m+1,r]$ 区间的信息合并成区间 $[l,r]$ 的信息。最**关键的两个问题是：**
- **我们要维护区间的哪些信息呢？**
- **我们如何合并这些信息呢？**

对于一个区间 [l,r][l,r]，我们可以维护四个量：
- $\textit{lSum}$ 表示 $[l,r]$ 内以 $l$ 为左端点的最大子段和
- $\textit{rSum}$ 表示 $[l,r]$ 内以 $r$ 为右端点的最大子段和
- $\textit{mSum}$ 表示 $[l,r]$ 内的最大子段和
- $\textit{iSum}$ 表示 $[l,r]$ 的区间和

&emsp;以下简称 $[l,m]$ 为 $[l,r]$ 的「左子区间」，$[m+1,r]$ 为 $[l,r]$ 的 *右子区间* 。我们考虑如何维护这些量呢（如何通过左右子区间的信息合并得到 $[l,r]$ 的信息）？对于长度为 $1$ 的区间 $[i,i]$，四个量的值都和 $\textit{nums}[i]$ 相等。对于长度大于 $1$ 的区间：
- 首先最好维护的是 $\textit{iSum}$，区间 $[l,r]$ 的 $\textit{iSum}$ 就等于 *左子区间* 的 $\textit{iSum}$ 加上 *右子区间* 的 $\textit{iSum}$。
- 对于 $[l,r]$ 的 $\textit{lSum}$，存在两种可能，它要么等于 *左子区间* 的 $\textit{lSum}$，要么等于 *左子区间* 的 $\textit{iSum}$ 加上 *右子区间* 的 $\textit{lSum}$，二者取大。
对于 $[l,r]$ 的 $\textit{rSum}$，同理，它要么等于 *右子区间* 的 $\textit{rSum}$，要么等于 *右子区间* 的 $\textit{iSum}$ 加上 *左子区间* 的 $\textit{rSum}$，二者取大。
当计算好上面的三个量之后，就很好计算 $[l,r]$ 的 $\textit{mSum}$ 了。我们可以考虑 $[l,r]$ 的 $\textit{mSum}$ 对应的区间是否跨越 mm——它可能不跨越 $m$，也就是说 $[l,r]$ 的 $\textit{mSum}$ 可能是 *左子区间* 的 $\textit{mSum}$ 和  *右子区间* 的 $\textit{mSum}$ 中的一个；它也可能跨越 $m$，可能是 *左子区间* 的 $\textit{rSum}$ 和 *右子区间* 的 $\textit{lSum}$ 求和。三者取大。
这样问题就得到了解决。

### 代码
```cpp
class Solution {
public:
    struct Status{
        int lsum,rsum,msum,isum;
    };

    Status PushUp(Status sta1,Status sta2){
        int lsum=max(sta1.lsum,sta1.isum+sta2.lsum);
        int rsum=max(sta2.rsum,sta1.rsum+sta2.isum);
        int msum_t=max(sta1.msum,sta2.msum);
        int msum=max(msum_t,sta1.rsum+sta2.lsum);
        int isum=sta1.isum+sta2.isum;
        return (Status) {lsum,rsum,msum,isum};
    }

    Status get(vector<int>& a,int l,int r){
        if(l==r){
            return (Status) {a[l],a[l],a[l],a[l]};
        }
        int m=(l+r)>>1;
        Status sta1=get(a,l,m);
        Status sta2=get(a,m+1,r);

        Status sta=PushUp(sta1,sta2);
        return sta;
        
    }

    int maxSubArray(vector<int>& nums) {
        Status sta =get(nums,0,size(nums)-1);
        return sta.msum;
    }
};
```
### 复杂度分析
&emsp;假设序列 $a$ 的长度为 $n$。
- 时间复杂度：假设我们把递归的过程看作是一颗二叉树的先序遍历，那么这颗二叉树的深度的渐进上界为 $O(logn)$，这里的总时间相当于遍历这颗二叉树的所有节点，故总时间的渐进上界是 $O(\sum_{i=1}^{\log n} 2^{i-1})=O(n)$，故渐进时间复杂度为 $O(n)$。
- 空间复杂度：$O(N)$，其中 $N$ 为数组的长度。
### 注意：
- 分治+递归：递归回升要维护的区间信息，即合并的过程要逐步可推。
- 只有每一个元素都对结果会产生影响的时候才会用到分治思想。