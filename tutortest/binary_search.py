import unittest

def binary_search(arr,l,r,x):

    while r >= l:
        mid = l + (r-l) // 2

        if arr[mid] == x:
            return mid
        
        elif arr[mid] > x:
            r = mid - 1

        else:
            l = mid + 1

    return -1

def binary_search_recursive(arr,l,r,x):

    if r >= l:
        mid = l + (r-l) // 2

        if arr[mid] == x:
            return mid

        elif arr[mid] > x:
            return binary_search_recursive(arr,l,mid - 1,x)

        else:
            return binary_search_recursive(arr,mid +1 ,r, x)

    return -1

arr = [2, 3, 4, 10, 40,50]

# result = binary_search(arr,0,len(arr)-1,20)
# print(result)

# result = binary_search_recursive(arr,0,len(arr)-1,20)
# print(result)


class TestFunction(unittest.TestCase):

    def test_return(self):
        self.assertEqual(binary_search_recursive(arr,0,len(arr)-1,10),3)

if __name__ == '__main__':
    unittest.main()

# class TestStringMethods(unittest.TestCase):

#     def test_upper(self):
#         self.assertEqual('foo'.upper(), 'FOO')

#     def test_isupper(self):
#         self.assertTrue('FOO'.isupper())
#         self.assertFalse('Foo'.isupper())

#     def test_split(self):
#         s = 'hello world'
#         self.assertEqual(s.split(), ['hello', 'world'])
#         # check that s.split fails when the separator is not a string
#         with self.assertRaises(TypeError):
#             s.split(2)
