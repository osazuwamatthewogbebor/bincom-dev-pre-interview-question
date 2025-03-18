import random


def binary_decimal_generator():
    binary = ""
    for i in range(4):
        binary += random.choice("01")

    decimal = int(binary, 2)

    print(f"Binary number generated: {binary}")
    print(f"Decimal number: {decimal}")


binary_decimal_generator()
