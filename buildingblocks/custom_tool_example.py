class CustomCalculatorTool:
    """
    A simple custom tool for agents: a basic calculator.
    Methods: add, subtract, multiply, divide.
    """
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b


if __name__ == "__main__":
    tool = CustomCalculatorTool()
    print("Add: 2 + 3 =", tool.add(2, 3))
    print("Subtract: 5 - 2 =", tool.subtract(5, 2))
    print("Multiply: 4 * 3 =", tool.multiply(4, 3))
    print("Divide: 10 / 2 =", tool.divide(10, 2))
