
arr = [1,2,3,4,5]

for i in range(1,len(arr)):
    arr_ = [arr[0]]
    for j in range(1,len(arr)):
        if i != j:
            arr_.append(arr[j])

    print(arr_)


    
