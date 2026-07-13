"""
Day 8 test file for CodeSage AI
"""

import subprocess

API_KEY = "12345ABCDE"
PASSWORD = "password123"


def greet(name):
    """Greets the user."""
    print(f"Hello, {name}")


def run_command():
    """Runs a system command."""
    subprocess.run("dir", shell=True)


def calculate():
    """Performs a calculation."""
    result = 10 + 20
    unused_variable = 50
    print(result)


greet("Aishwarya")
run_command()
calculate()