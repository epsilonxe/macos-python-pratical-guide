print("Grade System")
x = float(input("Enter a score: "))

# if x >= 80 and x <= 100:
# if 80 <= x <= 100:
if x >= 80:
	grade = "A"
elif x >= 75:
	grade = "B+"
else:
	grade = "F"

print(f"{x} --> {grade}")