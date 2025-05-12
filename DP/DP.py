import random
import time
import psutil
import os

def generate_random_cnf_clause(num_vars, clause_len):
    return [random.choice([i + 1, -(i + 1)]) for i in random.sample(range(num_vars), clause_len)]

def generate_input_file(filename, num_lines=100, num_vars=5, max_clause_len=3, max_clauses=5):
    with open(filename, 'w') as f:
        for _ in range(num_lines):
            num_clauses = random.randint(1, max_clauses)
            cnf = [generate_random_cnf_clause(num_vars, random.randint(1, max_clause_len)) for _ in range(num_clauses)]
            f.write(str(cnf) + '\n')

def is_satisfiable_dpll(cnf, assignment={}):
    cnf = [clause for clause in cnf if not any(
        lit in assignment and assignment[abs(lit)] == (lit > 0) for lit in clause)]
    if not cnf:
        return True
    if any(len(clause) == 0 for clause in cnf):
        return False
    for clause in cnf:
        for lit in clause:
            var = abs(lit)
            if var not in assignment:
                break
        else:
            continue
        break
    for value in [True, False]:
        new_assignment = assignment.copy()
        new_assignment[var] = value
        if is_satisfiable_dpll(cnf, new_assignment):
            return True
    return False

def process_input_file(input_file, output_file):
    process = psutil.Process(os.getpid())
    start_time = time.time()
    peak_memory = 0

    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for i, line in enumerate(f_in, 1):
            try:
                cnf = eval(line.strip())
                result = is_satisfiable_dpll(cnf)
                f_out.write(f"Line {i}: {'SATISFIABLE' if result else 'UNSATISFIABLE'}\n")
            except Exception as e:
                f_out.write(f"Line {i}: ERROR - {str(e)}\n")
            # Update peak memory
            mem = process.memory_info().rss / (1024 * 1024)  # in MB
            peak_memory = max(peak_memory, mem)

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Log runtime and memory usage
    with open("stats.txt", 'w') as f_stats:
        f_stats.write(f"Execution Time: {elapsed_time:.4f} seconds\n")
        f_stats.write(f"Peak Memory Usage: {peak_memory:.2f} MB\n")

if __name__ == '__main__':
    instances = int(input(f"Insert how many instances you wish to solve: "))
    generate_input_file('input.txt', instances)
    process_input_file('input.txt', 'output.txt')
    print(f"Done!")