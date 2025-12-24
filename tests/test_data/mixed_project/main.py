"""Main module that uses functions from utils."""

from utils import calculate_sum, calculate_product, Calculator


def main():
    """Main function demonstrating usage of utility functions."""
    # Use the functions from utils
    result1 = calculate_sum(10, 20)
    print(f"Sum: {result1}")

    result2 = calculate_product(5, 6)
    print(f"Product: {result2}")

    # Use the Calculator class
    calc = Calculator()
    calc.add(15, 25)
    calc.multiply(3, 7)

    print("Calculation history:")
    for entry in calc.history:
        print(f"  {entry}")


def process_data(data):
    """Process a list of numbers using utils functions.

    Args:
        data: List of numbers

    Returns:
        Dictionary with sum and product
    """
    total = 0
    product = 1

    for i in range(len(data)):
        total = calculate_sum(total, data[i])
        product = calculate_product(product, data[i])

    return {"sum": total, "product": product}


if __name__ == "__main__":
    main()
