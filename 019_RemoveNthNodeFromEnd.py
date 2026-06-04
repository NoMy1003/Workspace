# Definition for singly-linked list.
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        tmp = head
        if tmp == None:
            return tmp
        count = 1
        while(tmp.next != None):
            count += 1
            tmp = tmp.next
        result = head
        for i in range(count - n - 1):
            result = result.next
        if count - n > 0:
            result.next = result.next.next
        else:
            head = head.next
            
        return head

test = Solution()
head = ListNode(1)
head.next = ListNode(2)
head.next.next = ListNode(3)
head.next.next.next = ListNode(4)
head.next.next.next.next = ListNode(5)
#print(test.removeNthFromEnd(head, 2).val)
tmp = test
count = 1
while(tmp.next != None):
    count += 1
    tmp = tmp.next
for i in range(count):
    head = head.next
    print(head.val)