import random
import time
import psutil
import os

INPUT_FILE = "input.txt"
OUTPUT_FILE = "output.txt"
STATS_FILE = "stats.txt"
MAX_VARS = 10
MAX_CLAUSES_PER_LINE = 5
MAX_LITS_PER_CLAUSE = 3

def generate_clause(num_vars):
    num_lits = random.randint(1, MAX_LITS_PER_CLAUSE)
    clause = random.sample(range(1, num_vars + 1), num_lits)
    clause = [lit if random.random() > 0.5 else -lit for lit in clause]
    return clause

def generate_input_file(num_lines):
    with open(INPUT_FILE, "w") as f:
        for _ in range(num_lines):
            num_clauses = random.randint(1, MAX_CLAUSES_PER_LINE)
            line = []
            for _ in range(num_clauses):
                clause = generate_clause(MAX_VARS)
                line.append(" ".join(map(str, clause)) + " 0")
            f.write(" | ".join(line) + "\n")

def parse_line_to_clauses(line):
    clause_strs = line.strip().split(" | ")
    return [list(map(int, clause.strip().split()[:-1])) for clause in clause_strs]

def is_clause_satisfied(clause, assignment):
    return any((lit > 0 and assignment.get(abs(lit), None) == True) or
               (lit < 0 and assignment.get(abs(lit), None) == False)
               for lit in clause)

def unit_propagate(clauses, assignment):
    changed = True
    while changed:
        changed = False
        for clause in clauses:
            unassigned = [lit for lit in clause if abs(lit) not in assignment]
            if len(unassigned) == 1:
                forced_lit = unassigned[0]
                assignment[abs(forced_lit)] = forced_lit > 0
                changed = True
    return assignment

def solve_cdcl(clauses, assignment={}, depth=0):
    assignment = unit_propagate(clauses, dict(assignment))

    if all(is_clause_satisfied(clause, assignment) for clause in clauses):
        return True, assignment

    if any(all(abs(lit) in assignment and not is_clause_satisfied([lit], assignment) for lit in clause)
           for clause in clauses):
        return False, None

    unassigned_vars = [i for i in range(1, MAX_VARS + 1) if i not in assignment]
    if not unassigned_vars:
        return False, None

    var = unassigned_vars[0]
    for value in [True, False]:
        new_assignment = dict(assignment)
        new_assignment[var] = value
        sat, result = solve_cdcl(clauses, new_assignment, depth + 1)
        if sat:
            return True, result

    return False, None

def measure_memory():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)  # MB

def process_input_file():
    with open(INPUT_FILE, "r") as infile, \
         open(OUTPUT_FILE, "w") as out_sat, \
         open(STATS_FILE, "w") as out_stats:

        total_start = time.time()
        start_mem = measure_memory()
        
        for line_num, line in enumerate(infile, start=1):
            clauses = parse_line_to_clauses(line)
            start_time = time.time()
            sat, _ = solve_cdcl(clauses)
            end_time = time.time()
            line_runtime = end_time - start_time

            out_sat.write(f"Line {line_num}: {'SAT' if sat else 'UNSAT'} in {line_runtime:.4f} sec\n")

        end_mem = measure_memory()
        total_end = time.time()
        total_runtime = total_end - total_start

        out_stats.write(f"Total Time: {total_runtime:.4f} seconds\n")
        out_stats.write(f"RAM Usage: {end_mem:.2f} MB\n")

def main():
    instances = int(input(f"Insert how many instances you wish to solve: "))
    generate_input_file(instances)
    process_input_file()
    print(f"Done!")

if __name__ == "__main__":
    main()
