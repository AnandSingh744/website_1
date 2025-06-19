def is_prime(n):
    """
    Function to check if a number is prime.
    Returns 1 if the number is prime, else returns 0.
    """
    if n <= 1:
        return 0  # Numbers <= 1 are not prime
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return 0  # Number is not prime
    return 1  # Number is prime

def main():
    # Input from the user
    num = int(input("Enter a number to check if it is prime: "))
    
    # Check if the number is prime
    if is_prime(num):
        print(f"{num} is a prime number.")
    else:
        print(f"{num} is not a prime number.")

# Call the main function
if __name__ == "__main__":
    main()
