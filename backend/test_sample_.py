import subprocess


password = "admin123"


def execute_command(command):
    subprocess.call(command, shell=True)


def calculate():
    x = 10
    y = 20
    z = x + y
    unused = 100
    print(z)


execute_command("dir")
calculate()