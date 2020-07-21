boss = "prayuth"


print("The Military Authentication")
username = input("Enter your name: ")

if username == boss:
	print(f"Hello {username}")
	print("Welcome to the matrix")
else:
	print(f"You are {username}, and u are a human")
	print("Denied Login")
