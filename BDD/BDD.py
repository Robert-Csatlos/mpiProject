import time
import psutil
from dd.autoref import BDD
import random
import string
import os

INPUT_FILE = "input.txt"
OUTPUT_FILE = "output.txt"
LOG_FILE = "stats.txt"

NUM_VARS = 5  # number of boolean variables per expression


def generate_random_expr(vars):
    """Generate a random boolean expression from a list of variables."""
    ops = ['&', '|', '^']
    expr = ""
    for _ in range(random.randint(1, 3)):
        var1 = random.choice(vars)
        var2 = random.choice(vars)
        op = random.choice(ops)
        expr += f"({var1} {op} {var2})"
        if random.random() < 0.5:
            expr += " | "
    return expr.strip(" |")


def generate_input_file(num_lines):
    """Generate a BDD-based solver input text file."""
    vars = [random.choice(string.ascii_lowercase) for _ in range(NUM_VARS)]
    with open(INPUT_FILE, "w") as f:
        for _ in range(num_lines):
            expr = generate_random_expr(vars)
            f.write(expr + "\n")


def is_satisfiable(expr, bdd, vars):
    """Check if a boolean expression is satisfiable using BDD."""
    try:
        # Parse the expression into BDD
        compiled = bdd.add_expr(expr)
        return not bdd.is_zero(compiled)
    except Exception as e:
        return False


def solve_bdd_file():
    """Read input file, evaluate satisfiability, and write output."""
    bdd = BDD()
    vars = set()

    with open(INPUT_FILE, "r") as fin:
        lines = fin.readlines()
        for line in lines:
            vars.update(filter(str.isalpha, line))

    # Declare variables in BDD
    for var in vars:
        bdd.declare(var)

    with open(INPUT_FILE, "r") as fin, open(OUTPUT_FILE, "w") as fout:
        for line in fin:
            expr = line.strip()
            result = is_satisfiable(expr, bdd, vars)
            fout.write(f"{expr} => {'SAT' if result else 'UNSAT'}\n")


def log_performance(start_time, start_mem):
    """Log runtime and RAM consumption."""
    end_time = time.time()
    end_mem = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024  # MB
    duration = end_time - start_time
    ram_used = end_mem

    with open(LOG_FILE, "w") as f:
        f.write(f"Runtime: {duration:.4f} seconds\n")
        f.write(f"RAM Used: {ram_used:.2f} MB\n")


def main():
    instances = int(input(f"Insert how many instances you wish to solve: "))
    start_time = time.time()
    start_mem = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
    generate_input_file(instances)
    solve_bdd_file()
    log_performance(start_time, start_mem)


if __name__ == "__main__":
    main()
