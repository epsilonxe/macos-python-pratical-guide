import random

my_number = random.randint(1, 100)
isCorrect = False

# print(my_number)

print("Try to guess my number (0 - 100)")

while not isCorrect:
	x = input("Guess my number: ")
	if x.isdigit():
		x = int(x)
		if x == my_number:
			print(f"Yes, my number is {my_number}")
			isCorrect = True
		else:
			print("No, it's not")
			if x > my_number:
				print("It is too high")
			else:
				print("It is too low")
				print("Try it again")
	else:
		if x == "give_up":
			isCorrect = True
			print(f"Sorry loser, the correct number is {my_number}")
		else:
			pass
		
print("Thanks for playing")
