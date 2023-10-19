def nameOutput(LastName, FirstName, MiddleInitial):
    return LastName + ", " + FirstName + " " + MiddleInitial

FirstName = input("Please enter a first name: ")
MiddleInitial = input("Please enter a middle initial: ")
LastName = input("Please enter a last name: ")

print(nameOutput(LastName,FirstName,MiddleInitial))
