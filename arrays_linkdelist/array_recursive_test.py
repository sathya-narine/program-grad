import random
import time
import sys

'''this method implements merge sort 
ie recusively divides the array into  two parts 
by dividing at mid of array and then merging the two
individual sorted array. reference from --->Programiz
time complexity O(n log(n))'''
def merge(left_half, right_half, reverse):
    result = []
    i = j = 0
    while i < len(left_half) and j < len(right_half):
        if reverse:
            if left_half[i] > right_half[j]:    
                result.append(left_half[i])
                i += 1
            else:                               
                result.append(right_half[j])
                j += 1
        else:
            if left_half[i] < right_half[j]:    
                result.append(left_half[i])
                i += 1
            else:                               
                result.append(right_half[j])
                j += 1
    result.extend(left_half[i:])                
    result.extend(right_half[j:])                
    return result

def merge_sort(lst, reverse=False):
    if len(lst) <= 1:                            
        return lst
 
    mid = len(lst) // 2
    left_half = lst[:mid]                        
    right_half = lst[mid:]                       
 
    left_half = merge_sort(left_half, reverse)   
    right_half = merge_sort(right_half, reverse) 
 
    return merge(left_half, right_half, reverse)

def main():
    #begin of the program
    #no_terms = int(input('enter no of terms:'))
    no_terms = 1000
    end_range = int(input('enter the end range:'))
    print('value of n:',no_terms)
    #capture the start time for over all execution
    start_time = time.perf_counter()
    #initialise the empty list
    init_list = []
    count=0
    #generation of random numbers and appending to list -- Time complexity O(n)
    for i in range(0,no_terms):
        ele=random.randint(1,end_range)
        init_list.append(ele)
        if ele > 50:
            count+=1
    
    #print('initial array:')   
    #print(init_list)
    #print('no of elements greater than 50:',count)        
    final_list=[]   
        
    if count > 5:
        #sort the array in ascending order
        #time complexity O(n log(n))
        
        init_list = merge_sort(init_list)
        #print('after sort:')
        #print(init_list)
        #deleting the fifth element --time complexity O(1)
        del(init_list[4])
        #print('after delete')
        #print(init_list)
        #inserting 10 to sorted array
        #worst case time complexity O(n)
        for i in range(0,len(init_list)):
            if init_list[i] >= 10 :
                #print(i)
                final_list=init_list[:i]+[10]+init_list[i:]
                break
    else:
        #sorting the array in descending order
        ##time complexity O(n log(n))
        init_list = merge_sort(init_list,reverse=True)
        #print('after sort:')
        #print(init_list)
        #deleting the second element --time complexity O(1)
        del(init_list[1])
        #print('after delete')
        #print(init_list)
        #inserting 10 to sorted array -- worst case O(n)
        for i in range(len(init_list)-1,-1,-1):
            if init_list[i] >= 10:
                final_list=init_list[:i+1] + [10] + init_list[i+1:]
                break
    #printig the final array    
    #print('final array:',final_list)
    #capture the execution time
    end_time = time.perf_counter()
    #execution_time = end_time - start_time
    elapsed_time_microseconds = (end_time - start_time) * 1e6

    # Print the elapsed time in microseconds
    space_complexity = sys.getsizeof(final_list)
    #print(f"Space complexity of my_list: {space_complexity} bytes")
    print(f"Elapsed time: {elapsed_time_microseconds:.2f} microseconds")
    #print(" Execution time : --- %s seconds ---" % (execution_time.microseconds))
    return elapsed_time_microseconds
    
if __name__ == '__main__':
    r = int(input('enter the vlaue for r:'))
    ex_time=[]
    for i in range(r):
        run_time = main()
        ex_time.append(run_time)
    avg_time=sum(ex_time)/len(ex_time)
    print('-------------------')
    print(f"Average time: {avg_time:.2f} microseconds")
