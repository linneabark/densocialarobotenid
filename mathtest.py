
def subtraction(first_term, second_term):
    return first_term - second_term


def addition(first_term, second_term):
    return first_term + second_term


def multiplication(first_term, second_term):
    return first_term * second_term

def division(first_term, second_term):
    return first_term / second_term


def find_numbers(str_input):
    temporary = list()
    i = 0
    temporary2 = []
    while i < len(str_input):
        if str_input[i].isdigit():
          temporary2.append(str_input[i])
        elif temporary2:
          temporary.append("".join(temporary2))
          temporary2 = []
        i = i + 1
        if i == len(str_input) and temporary2:
            temporary.append("".join(temporary2))
    print(temporary)
    return temporary


def start_mathtest():
    while True:
        str_input = input("Enter string: ")
        print(str_input)

        temp = list()
        temp.extend(find_numbers(str_input))

        if len(temp) < 2:
            print("Too few numbers")
            continue
        if len(temp) > 2:
            print("Only do two terms")
            continue

        first_term = int(temp[0])
        second_term = int(temp[1])

        operator_count = 0
        operator_input = str_input.lower()
        operators = {
            'PLUS': ["plus", "addera", "lägg till"],
            'MINUS': ["minus"],
            'MULTIPLICATION': ["multiplicerat", "gånger"],
            'DIVISION' : ["delat med", "delat på", "dividerat med", "dividerat på"]
        }

        actual_operator = None
        for operator, synonyms in operators.items():
            count = 0
            for synonym in synonyms:
                count += operator_input.count(synonym)
            if count > 0:
                actual_operator = operator
            operator_count += count

        if operator_count > 1:
            print('Too many operators')
            continue
        elif operator_count < 1:
            print('No operator found')
            continue

        if actual_operator == 'MINUS':
            print(subtraction(first_term, second_term))
        elif actual_operator == 'PLUS':
            print(addition(first_term, second_term))
        elif actual_operator == 'MULTIPLICATION':
            print(multiplication(first_term, second_term))
        elif actual_operator == 'DIVISION':
            print(division(first_term, second_term))
        else:
            print("Dunno WHAT u want!")

        break

print("mathtest __name__" + __name__)

if __name__ == '__main__':
    start_mathtest()
