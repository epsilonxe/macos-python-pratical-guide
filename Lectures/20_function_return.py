def absolute(x):
	
	if x >= 0:
		abs_x = x
	else:
		abs_x = -x
	
	return abs_x


print("Finding absolute value")
input_number = float(input("Enter a number: "))

abs_val = absolute(input_number)

print(f"Absolute value of {input_number} is {abs_val}")

