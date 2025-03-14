a_man = "gay"

# for i in range(20):
    
            
#     if i < 3:
#         pass
#     if i < 5:
#         pass
#     if i < 10:
#         pass

#     if i==6:
#         print("skip====")
#         continue
#     elif i==3:  
#         print(i, "is the best")
#     else:
#         print(i)
#     print("=======")
#     if i==8:
#         break

def factorial(n:int)->int:
    if n==1:
        return 1
    return n*factorial(n-1) 

print(factorial(5))

def factorial_better(n:int)->int:
    i=2
    res = 1
    while i<=n:
        res=res*i
        i=i+1
    return res

print(factorial_better(1))



def fibonnaci(x):
    if x==0:
        return 1    
    if x==1:
        return 1
    
    return fibonnaci(x-1)+fibonnaci(x-2)

print(fibonnaci(40))

# 2^x