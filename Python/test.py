import math

x1 = float(input("Enter the first x value: "))
y1 = float(input("Enter the first Y value: "))
x2 = float(input("Enter the second x value: "))
y2 = float(input("Enter the second y value: "))

a = x2 - x1
b = y2 - y1

c = (a * a) + (b * b)

c = math.sqrt(c)

print("The distance between the two points is " + str(c))
