def test(a,b):
    
    result = 1
    
    if b > 0 : 
        n = b
    else: 
        n = b*(-1)
    
    for i in range(n):
        if b>0:
            result*=a
        else:
            result/=a
            
    return result

# print(test(5,2))

def power(a,b):

    if a == 0:
        #to gain time
        return 0
    if b==0:
        return 1
    if b >0:
        if (b%2==0): 
            #this will reduce time by 2 when number are even and it just calculate the power of one part and then multiply 
            if b==2:
                return a*a
            else:
                return power(power(a,b//2),2)
        else:
            #the main case when the number is odd
            return a * power(a, b- 1)
    elif not b > 0:
        #this is for negatives exposents
        return 1./float(power(a,-b))

print(power(5,3))

