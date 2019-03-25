from sys import exit


def main():
    # Variables
    first_term = 0
    second_term = 0

    # Input string
    str = input("Enter string: ")

    # Find terms
    temp_term = find_numbers(str)
    first_term = int(temp_term[1])
    second_term = int(temp_term[2])

    # Find operator
    operator = find_operator(str)


def find_numbers(str):
    input_str = str
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
                print("No digits in expression")
    return terms


def find_operator(str):
    input_str = str
    i = 0
    while i < len(input_str):
        if input_str[i].i
        i = i + 1
    operator = ""
    return operator


def subtraction(first_term, second_term):
    return first_term - second_term


def addition(first_term, second_term):
    return first_term + second_term


def multiplication(first_term, second_term):
    return first_term * second_term
