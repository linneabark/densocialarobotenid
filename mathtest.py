from sys import exit

# Variables
first_term = 0
second_term = 0

# Input string
str_input = input("Enter string: ")
print(str_input)


def subtraction(first_term, second_term):
    return first_term - second_term


def addition(first_term, second_term):
    return first_term + second_term


def multiplication(first_term, second_term):
    return first_term * second_term


def find_numbers(str_input):
    input_str = str_input
    terms = []
    i = 0
    while i < len(input_str):
        temporary = []
        if input_str[i].isdigit() and input_str[i + 1].isdigit():
            temporary.append(input_str[i] + input_str[i + 2])
        elif input_str[i].isdigit():
            temporary.append(input_str[i])

        i = i + 1
        if i == len(input_str) - 1:
            if len(temporary) < 3:
                terms[1] = temporary[1]
                terms[2] = temporary[2]
            else:
                exit("No digits in expression")
    return terms


# Find terms
temp_term = find_numbers(str_input)
first_term = int(temp_term[1])
second_term = int(temp_term[2])

# Find operator
operator = str_input.lower()
if operator.find("minus") != -1:
    print(subtraction(first_term, second_term))
elif operator.find("pluss") != -1:
    print(addition(first_term, second_term))
elif operator.find("multiplicerat") != -1:
    print(multiplication(first_term, second_term))
else:
    exit("Dunno WHAT u want!")
