first_term = 0
second_term = 0

str_input = input("Enter string: ")
print(str_input)


def subtraction(first_term, second_term):
    return first_term - second_term


def addition(first_term, second_term):
    return first_term + second_term


def multiplication(first_term, second_term):
    return first_term * second_term


def find_numbers(str_input):
    temporary = list()
    i = 0
    while i < len(str_input):
        if str_input[i].isdigit() and str_input[i+1].isdigit():
            temporary.append(str_input[i] + str_input[i+1])
        elif str_input[i].isdigit():
            temporary.append(str_input[i])
        i = i + 1
    print(temporary)
    return temporary


temp = list()
temp.extend(find_numbers(str_input))

first_term = int(temp[0])
second_term = int(temp[1])
print(first_term)
print(second_term)


operator = str_input.lower()
if operator.find("minus") != -1:
    print(subtraction(first_term, second_term))
elif operator.find("pluss") != -1:
    print(addition(first_term, second_term))
elif operator.find("multiplicerat") != -1:
    print(multiplication(first_term, second_term))
else:
    print("Dunno WHAT u want!")
