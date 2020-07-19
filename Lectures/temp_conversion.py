def tempConvert(temp, mode):

	if mode == "c->f":
		output_temp = (temp / 5) * 9 + 32
	elif mode == "f->c":
		output_temp = ((temp - 32) / 9) *5
	else:
		output_temp = None

	return output_temp


print("Temperature Converter")
t = float(input("Enter a temperature: "))
m = input("Conversion mode: ")
output = tempConvert(t, m)
print(f"Output is {output}")

# if __name__ == "__main__":
# 	print("Temperature Converter")
# 	t = float(input("Enter a temperature: "))
# 	m = input("Conversion mode: ")
# 	output = tempConvert(t, m)
# 	print(f"Output is {output}")