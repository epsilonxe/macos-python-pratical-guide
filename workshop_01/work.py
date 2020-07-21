import math

print("Circumference Calculator")
r = float(input("Enter the radius:"))


area = math.pi * (r**2)
cir = 2 * math.pi * r

print(f"Area is {area:.3f} cm^2")
print(f"Circumference is {cir:.3f} cm")