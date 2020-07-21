def greeting(username, lastname="Hello"):
	print(f"Hello {username} {lastname}")
	print("Nice to see you here")

def deny(username):
	print(f"Sorry {username}")
	print("Your login is unwelcome")


boss = "prayuth"

print("Login System")
login = input("Enter your name: ")

if login == boss:
	greeting(boss, "Tum")
else:
	deny(login)
