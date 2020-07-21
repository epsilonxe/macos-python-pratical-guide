f = open("demofile.txt", "r")

print(f.read())
f.close()

#line by line
print("Read line by line")
f = open("demofile.txt", "r")
print(f.readline())
print(f.readline())
f.close()

#line by line by for
print("read line by line use for iteration")
f = open("demofile.txt", "r")
for x in f:
  print(x)
f.close()

#write to file by append
print("write by append mode")
f = open("demofile2.txt", "a")
f.write("Now the file has more content!")
f.close()

#open and read the file after the appending:
f = open("demofile2.txt", "r")
print(f.read())
f.close()


print("write file by rewrite mode")
f = open("demofile3.txt", "w")
f.write("Woops! I have deleted the content!")
f.close()

#open and read the file after the appending:
f = open("demofile3.txt", "r")
print(f.read())