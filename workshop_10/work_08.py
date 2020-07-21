def fact(n):
	r = 1
	if n == 0:
		return 1

	for i in range(n, 0, -1):
		r = r * i
	return r
	
def fact_recur(n):
	if n == 0:
		return 1
	else: 
		return n * fact_recur(n-1)

def fact_str(n):
	temp = []
	
	for i in range(n, 0, -1):
		#r = r * i
		temp.append(str(i))
	text = "x".join(temp)
	return text

# print("Factorial Calculator")
# n = input("Enter an integer:")

# #r = fact(int(n))
# r = fact_recur(int(n))

# text = fact_str(int(n))

# print(f"{n}! = {text} = {r}")
