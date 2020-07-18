my_list = [1, 2, 3, 4, 5]


print(f"This will show members of {my_list}")

k = 0
n = len(my_list)
while k < my_list:
	print(f"Member number {k} is {my_list[k]}")
	k = k + 1


# Example of usage
# Finding Summation
sum = 0
k = 0
n = len(my_list)
while k < n:
	sum = sum + my_list[k]
	k = k + 1

print(f"Summation of members in {my_list} is {sum}")