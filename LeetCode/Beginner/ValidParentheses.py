"""Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:

Open brackets must be closed by the same type of brackets.
Open brackets must be closed in the correct order.
Every close bracket has a corresponding open bracket of the same type.
 

Example 1:

Input: s = "()"
Output: true
Example 2:

Input: s = "()[]{}"
Output: true
Example 3:

Input: s = "(]"
Output: false
 

Constraints:

1 <= s.length <= 104
s consists of parentheses only '()[]{}'."""

class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        bracket_map = {')': '(', '}': '{', ']': '['}
        for char in s:
            if char in bracket_map: #check if closing
                #pop item from stack if not empty
                top_element = stack.pop() if stack else '#'
                #ceck if popped matches current bracket
                if bracket_map[char] != top_element:
                    return False
            else:
                    #if opening bracket push to stack
                    stack.append(char)
            
        #ifr stack is empty, all brackets matched
        return not stack