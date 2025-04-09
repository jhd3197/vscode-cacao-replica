def hello_world():
    """A simple hello world function"""
    print("Hello, World!")

class ExampleClass:
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        return f"Hello, {self.name}!"

if __name__ == "__main__":
    hello_world()
    example = ExampleClass("Cacao")
    print(example.greet())