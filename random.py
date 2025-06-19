def is_perfect_number(num):
    # Start with sum of divisors as 0
    sum_of_divisors = 0
    
    # Find divisors of num (we don't include num itself)
    for i in range(1, num):
        if num % i == 0:  # If i divides num, it's a divisor
            sum_of_divisors += i  # Add it to sum
    
    # If the sum of divisors is equal to the number, it's perfect
    if sum_of_divisors == num:
        return True
    else:
        return False

# Ask the user for input
num = int(input("Enter a number: "))

# Check if the number is perfect
if is_perfect_number(num):
    print(f"{num} is a Perfect Number")
else:
    print(f"{num} is not a Perfect Number")
