import random
import time
import sys
sys.setrecursionlimit(100000)
#class to define node
class Node:
    #constructor to intialize node
    def __init__(self,data):
        self.next =None
        self.data = data
        self.prev = None 
    #print the node data    
    def __repr__(self):
        return self.data

#class to define linked list      
class LinkedList:
    #constructor to intialize linked list
    def __init__(self):
        self.head =None
        
    #to print the linked list -- time complexity o(n)
    def __repr__(self):
        node = self.head
        nodes = []
        while node is not None:
            nodes.append(str(node.data))
            node = node.next
        nodes.append('None')
        return " -> ".join(nodes)
    
    #to iterate linked list 
    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next
            
    # method to insert elements into the linked list to the head -- time complexity o(1)
    def add_first(self,data):
        node = Node(data)
        if self.head is None:
            self.head = node 
        else:
            self.head.prev = node
            node.next = self.head
            #node.prev = None        #optional
            self.head = node
    
    #method to insert element to the descending order linked list 
    #-- worst case time complexity o(n)
    def add_to_dsc(self, value):
        new_node = Node(value)
        cur = self.head
        #if the node has to added at head
        if cur.data <= value:
            cur.prev = new_node
            new_node.next = cur 
            self.head = new_node
        else:
            while cur:
                if cur.next is None:
                    new_node.prev = cur
                    cur.next = new_node
                    break
                elif cur.data <= value:
                    p = cur.prev 
                    
                    new_node.next= cur
                    cur.prev = new_node
                    
                    p.next = new_node
                    new_node.prev = p 
                    break
                cur=cur.next
    
    #method to insert element to the ascending order linked list
    #-- worst case time complexity o(n)
    def add_to_asc(self,value):
        new_node = Node(value)
        cur = self.head
        #if the node has to added at head
        if cur.data >= value:
            cur.prev = new_node
            new_node.next = cur 
            self.head = new_node
        else: 
            while cur:
                if cur.next is None:
                    new_node.prev = cur
                    cur.next = new_node
                    break
                elif cur.data >= value:
                    p = cur.prev 
                    
                    new_node.next= cur
                    cur.prev = new_node
                    
                    p.next = new_node
                    new_node.prev = p 
                    break
                cur=cur.next
        
    #deletes the element from the linked list for a given position -- 
    #worst case pos is last time complexity O(n)
    def delete_ele(self,pos):
        counter = 1
        cur = self.head
        if pos == 1:
            cur.prev = None
            self.head = cur
        else:
            while counter!=pos:
                cur = cur.next
                counter+=1
            pre = cur.prev
            nex = cur.next 
            pre.next = cur.next 
            nex.prev = cur.prev 
            
# merge sort for doubly linked list --> referenced from geeks for geeks 
'''this method implements merge sort 
ie recusively divides the linked list into  two parts 
by recieving the mid node and then merging the two
individual sorted linked list -- time complexity n log(n)'''    
def merge_sort_linked_list(head, increasing_order=True):
    if head is None or head.next is None:
        return head
    
    mid = get_middle(head)
    mid_next = mid.next
    mid_next.prev = None
    mid.next = None
    
    left = merge_sort_linked_list(head, increasing_order)
    right = merge_sort_linked_list(mid_next, increasing_order)
    
    return merge(left, right, increasing_order)
    
#this method returns the middle node
#-- time complexity O(n)
def get_middle(head):
    slow = head
    fast = head
    
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    
    return slow

#this method merges two individual sorted linked list
def merge(left, right, increasing_order):
    result = None
    
    if left is None:
        return right
    if right is None:
        return left
    
    if increasing_order:
        if left.data <= right.data:
            result = left
            result.next = merge(left.next, right, increasing_order)
        else:
            result = right
            result.next = merge(left, right.next, increasing_order)
    else:
        if left.data >= right.data:
            result = left
            result.next = merge(left.next, right, increasing_order)
        else:
            result = right
            result.next = merge(left, right.next, increasing_order)
    
    result.next.prev = result
    return result
    
#start of the assignment code 
        
no_terms = int(input('enter no of terms:'))
end_range = int(input('enter the end range:'))

#caputre start time ---> reference stack over flow
start_time = time.perf_counter()

llist=LinkedList()
count = 0
#random integer generation and adding it to linked list -- time complexity O(n)
for i in range(0,no_terms):
    ele = random.randint(1,end_range)
    if ele > 50 and count <= 5:
        count+=1       
    llist.add_first(ele)

print('input linked list:\n',llist)
print('no of elements greater than 50',count)

if count < 5:
    final_linked_list=LinkedList()
    #sort the linked list in descending order
    #time complexity -- O(n log(n))
    final_linked_list.head = merge_sort_linked_list(llist.head, False)
    print('linked list after sort:')
    print(final_linked_list)
    #delete the second element --time complexity O(1)
    final_linked_list.delete_ele(2)
    print('after delete:')
    print(final_linked_list)
    #adding 10 to linked list --time complexity O(1)
    final_linked_list.add_to_dsc(10)
    print('final linked list')
    print(final_linked_list)

else:
    final_linked_list=LinkedList()
    #sort the linked list in ascending order
    #time complexity -- O(n log(n))
    final_linked_list.head = merge_sort_linked_list(llist.head, True)
    print('linked list after sort:')
    print(final_linked_list)
    #deleting the fifth element --time complexity O(1)
    final_linked_list.delete_ele(5)
    print('after delete:')
    print(final_linked_list)
    #adding 10 to sorted array --time complexity O(1)
    final_linked_list.add_to_asc(10)
    print('final linked list')
    print(final_linked_list)
end_time = time.perf_counter()
elapsed_time_microseconds = (end_time - start_time) * 1e6
space_complexity = sys.getsizeof(final_linked_list) 
print(f"Space complexity of linked list: {space_complexity} bytes")
print(f"Elapsed time: {elapsed_time_microseconds:.2f} microseconds")