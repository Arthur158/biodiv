liste = [[1, 2, 3], [4,5,6], [7,8,9]]
print(liste)
liste2 = [[liste[-i][::-1]] for i in range(1,4)]
print(liste2)