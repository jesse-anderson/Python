"""Write a function to find the longest common prefix string amongst an array of strings.

If there is no common prefix, return an empty string "".

 

Example 1:

Input: strs = ["flower","flow","flight"]
Output: "fl"
Example 2:

Input: strs = ["dog","racecar","car"]
Output: ""
Explanation: There is no common prefix among the input strings.
 

Constraints:

1 <= strs.length <= 200
0 <= strs[i].length <= 200
strs[i] consists of only lowercase English letters."""

class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:

        prefix = strs[0]

        for s in strs[1:]:
            i = 0
            while i < len(prefix) and i < len(s) and prefix[i] == s[i]:
                i+=1
            prefix = prefix[:i]
            if not prefix:
                break
            
        return  prefix