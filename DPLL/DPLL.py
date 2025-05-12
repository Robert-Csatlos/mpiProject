import time
import psutil
import os
import random

def assign(clauses, literal):
    new_clauses = []
    for clause in clauses:
        if literal in clause:
            continue
        new_clause = [l for l in clause if l != -literal]
        new_clauses.append(new_clause)
    return new_clauses

def dpll(clauses, assignment):
    if not clauses:
        return assignment
    if any(clause == [] for clause in clauses):
        return None

    # Unit clause rule
    for clause in clauses:
        if len(clause) == 1:
            unit = clause[0]
            return dpll(assign(clauses, unit), assignment + [unit])

    # Pure literal rule
    all_literals = [literal for clause in clauses for literal in clause]
    for literal in set(all_literals):
        if -literal not in all_literals:
            return dpll(assign(clauses, literal), assignment + [literal])

    chosen_literal = clauses[0][0]
    result = dpll(assign(clauses, chosen_literal), assignment + [chosen_literal])
    if result is not None:
        return result

    return dpll(assign(clauses, -chosen_literal), assignment + [-chosen_literal])

def read_cnf_file(filename):
    clauses = []
    with open(filename, 'r') as f:
        for line in f:
            if line.strip() == "":
                continue
            literals = list(map(int, line.strip().split()))
            if literals[-1] == 0:
                literals.pop()
            clauses.append(literals)
    return clauses

def write_output_file(filename, result, elapsed_time, memory_mb):
    with open(filename, 'w') as f:
        if result is None:
            f.write("UNSATISFIABLE\n")
        else:
            f.write("SATISFIABLE\n")
            f.write("Assignment: " + ' '.join(map(str, result)) + '\n')
        f.write(f"Time taken: {elapsed_time:.4f} seconds\n")
        f.write(f"Memory used: {memory_mb:.2f} MB\n")

def generate_random_cnf(filename, num_clauses=100, num_vars=10, clause_len_range=(2, 4)):
    with open(filename, 'w') as f:
        for _ in range(num_clauses):
            clause_len = random.randint(*clause_len_range)
            clause = random.sample(range(1, num_vars + 1), clause_len)
            clause = [lit if random.random() > 0.5 else -lit for lit in clause]
            f.write(' '.join(map(str, clause)) + ' 0\n')

if __name__ == "__main__":
    instances = int(input(f"Insert how many instances you wish to solve: "))
    generate_random_cnf("input.txt", num_clauses=instances, num_vars=20)

    process = psutil.Process(os.getpid())
    start_time = time.time()

    clauses = read_cnf_file("input.txt")
    solution = dpll(clauses, [])

    end_time = time.time()
    elapsed = end_time - start_time
    memory_info = process.memory_info().rss / (1024 * 1024)  # in MB

    write_output_file("output.txt", solution, elapsed, memory_info)

    print("Done!")
