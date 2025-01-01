from datetime import datetime

class App:
    def __init__(self):
        self.name = "My Python Application"
        self.version = "1.0.0"

    def run(self):
        print(f"Starting {self.name} v{self.version}")
        print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.greet_user()

    def greet_user(self):
        name = input("Please enter your name: ")
        print(f"Hello, {name}! Welcome to {self.name}")

if __name__ == "__main__":
    app = App()
    app.run()