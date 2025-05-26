while True:
    print("\nDivision Calculation(Enter 'q to exit)")

    try:
        number1_input = input("Enter the first number: ")
        if number1_input.lower() == 'q':
            print("Exiting calculation")
            break

        number2_input = input("Enter second number: ")
        if number2_input.lower() == 'q':
            print("Exting calculation")
            break

        number1 = float(number1_input)
        number2 = float(number2_input)

        if number2 == 0:
            print("Division by zero is not allowed. Please try agin")

        result = number1 / number2
        print(f"{number1} divided by {number2} equals {result:.2f}")
    
    except ValueError:
        print("Please enter valid numbers. Try again")

    except Exception as e:
        print(f"An unexceptional error occurred: {e}. Try agin")
        