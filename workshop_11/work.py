import matplotlib.pyplot as plt


def nextDay(S, I, R, beta, delta, gamma):
	next_S = stayPositive(S - beta * I * S + gamma * R)
	next_I = stayPositive(I + beta * I * S - delta * I)
	next_R = stayPositive(R + delta * I - gamma * R)
	next_SIR = (next_S, next_I, next_R)
	return next_SIR

def stayPositive(number):
	if number >= 0:
		output = number
	else:
		output = 0
	return output

def printline():
	print("-" * 45)



print("Disease Spreading Model")

# Human Input paremeters
# printline()
# S_0 = float(input("Enter a number of S(0): "))
# I_0 = float(input("Enter a number of I(0): "))
# R_0 = float(input("Enter a number of R(0): "))
# printline()
# beta = float(input("Enter a number of beta: "))
# delta = float(input("Enter a number of delta: "))
# gamma = float(input("Enter a number of gamma: "))
# printline()
# days = int(input("Enter number of days: "))


# Test
S_0 = 60
I_0 = 0.1
R_0 = 0
beta =  0.0045
delta = 0.0001
gamma = 0.005
days = 120

# States Calculation

S = [S_0]
I = [I_0]
R = [R_0]
T = [0]

for t in range(1, days + 1):
	latest_S = S[-1]
	latest_I = I[-1]
	latest_R = R[-1]
	next_SIR = nextDay(latest_S, latest_I, latest_R, beta, delta, gamma)
	S.append(next_SIR[0])
	I.append(next_SIR[1])
	R.append(next_SIR[2]) 
	T.append(t)


# Show results

print("Here is the result")
# print(f"S = {S}")
# print(f"I = {I}")
# print(f"R = {R}")

print("Here is some visualization")
# plot infected people
# plt.plot(T, I)
# plt.show()

# plot SIR
plt.plot(T, S, label='Susceptible')  
plt.plot(T, I, label='Infected')  
plt.plot(T, R, label='Recovered')
plt.xlabel('Days')
plt.ylabel('Million')
plt.title("Disease Spread Model")
plt.legend()
plt.show()