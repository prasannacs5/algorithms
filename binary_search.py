import sys

def main():
    # binary search needs a sorted list
    # for small lists sequentials search is better off
    list1 = [12,23,34,45,56,67,78,89,90]
    print(binary_search(list1,24))

def binary_search(list1, target):
    
    if len(list1) == 0:
        return False
    else:
        median = len(list1)//2
        if list1[median] == target:
            return True;
        if target > list1[median]:
            list2 = list1[median+1:]
            return binary_search(list2, target)
        else:
            list2 = list1[0:median]
            return binary_search(list2, target)

if __name__ == '__main__':
    main()
