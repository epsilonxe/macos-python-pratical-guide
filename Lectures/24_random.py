import random

# random number from closed interval [0,1]
x = random.random()
print(f"x = {x}")

# Include boundary
y = random.randint(50, 100)
print(f"y = {y}")

# Exclude boundary
y = random.randrange(0, 10)
print(f"y = {y}")

z = random.uniform(1, 100)
print(f"z = {z}")