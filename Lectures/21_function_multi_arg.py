def c2f(c):
	print("c2f")
def f2c(f):
	print("f2c")

def tempConvert(temp, mode):
	myfuncs = {'c->f': c2f(temp), 'f->c': f2c(temp)}
	return myfuncs.get(mode, None)
	


print("Temperature Converter")

t = float(input("Enter a temperature: "))
m = input("Conversion mode: ")

output = tempConvert(t, m)

print(f"Output is {output}")