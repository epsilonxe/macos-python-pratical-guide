# Division Calculator

print("Division Calculator")

x = input("Enter the value of x: ")
y = input("Enter the value of y: ")

x = float(x)
y = float(y)
z = x / y
print(f"z = {x} / {y} = {z:.5f}")

# try:
# 	x = float(x)
# 	y = float(y)
# 	z = x / y
# 	print(f"z = {x} / {y} = {z:.5f}")

# except ValueError:
# 	print("Data Mis-matched")

# except ZeroDivisionError:
# 	print(" y must be non-zero")