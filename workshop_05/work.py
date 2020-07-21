x = float(input("Enter x-coordinate: "))
y = float(input("Enter y-coordinate: "))

z = (x ** 2) + (y ** 2)

if z > 25:
	print(f"The point ({x},{y}) is out of the circle")
elif z == 25:
	print(f"The point ({x},{y}) is on the circle")
else:
	print(f"The point ({x},{y}) is inside of the circle")





