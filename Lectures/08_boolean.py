x = 16
y = 7


# Check: x > y
is_x_greater_than_y = x > y
print(is_x_greater_than_y)

# Comparison

# Equality
print(x == y)

# Inequality
print(x > y)
print(x >= y)
print(x < y)
print(x <= y)
print(x != y)

# Boolean Operations
condition_1 = x > y
condition_2 = x < y

print(f"condition_1 is {condition_1}")
print(f"condition_2 is {condition_2}")

new_condition = condition_1 and condition_2
print(f"new_condition is {new_condition}")


new_condition = condition_1 or condition_2
print(f"new_condition is {new_condition}")

cond3 = not condition_1
print(f"condition3 = {cond3}")

whatIs = None
print(whatIs == True)
print(whatIs == False)

if whatIs:
	print("a")
else:
	print("b")
