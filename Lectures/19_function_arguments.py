def greeting(username):
	print(f"Hello {username}")
	print("Nice to see you here")

def deny(username):
	print(f"Sorry {username}")
	print("Your login is unwelcome")


boss = "prayuth"

print("Login System")
login = input("Enter your name: ")

if login == boss:
	greeting(login)
else:
	deny(login)
