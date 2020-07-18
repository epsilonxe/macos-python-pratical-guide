my_list = [34.0, 43.5, 100.3, 45.6, 3.16, 0.28, 45.45, 3.2, 66.4]

line = 20 * "-"

print(f"This will show members of {my_list}")

for k in range(0, 4):
	print(f"Member number {k} is {my_list[k]}")

print(line)

for k in range(1, 8, 2):
	print(f"Member number {k} is {my_list[k]}")

print(line)

print("Here is Python-Exclusive")

for k in my_list:
	print(k)

print(line)

# Example of usage
# Finding Summation
sum = 0
for k in my_list:
	sum = sum + k
print(f"Summation of members in {my_list} is {sum}")