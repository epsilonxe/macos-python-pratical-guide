from work_08 import fact

def cosh(x):
	'''
	Output = (sum, u)
	sum is ....
	u is ....
	'''
	sum = 0
	# round = 10
	# for n in range(0, round):
	# 	sum = sum + (x ** (2*n))/fact(2*n)

	i = 0
	u = (x ** (2*i))/fact(2*i)
	error = 10 ** (-15)
	while u > error:
		sum = sum + u
		i = i + 1
		u = (x ** (2*i))/fact(2*i)
	output = (sum, u)
	return output

print(cosh(5)[0])






