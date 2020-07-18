boss = "prayuth"


print("The Military Authentication")
username = input("Enter your name: ")

if username == boss:
	print(f"Hello {username}")
	print("Welcome to the system")
else:
	print(f"You are {username}")
	print("Denied Login")
