from pathlib import Path
import subprocess
import sys
import os
from subprocess import TimeoutExpired
from enum import Enum
from time import perf_counter

class c(Enum):

    __use_colors__ = False

    g  = "\033[0m\033[1;92m"
    r  = "\033[0m\033[1;91m"
    d  = "\033[0m\033[1;49;90m"
    y  = "\033[0m\033[1;93m"
    c  = "\033[0m\033[1;96m"
    cu  = "\033[0m\033[4;96m"

    w  = "\033[0m"

    def __str__(self):
        return self.value if c.__use_colors__ else ""
    def enable_colors():
        c.__use_colors__ = True


def get_difference_disp(ans: str,out: str) -> (str, str):
    lines_ans = ans.split("\n")
    lines_out = out.split("\n")

    f_ans=""; f_out = ""
    len_min = min(len(lines_ans),len(lines_out))
    for i in range(0,len_min):
        col = c.g if lines_ans[i] == lines_out[i] else c.r
        f_ans+=str(col)+lines_ans[i]+"\n"
        f_out+=str(col)+lines_out[i]+"\n"
    f_ans+=str(c.y)+"\n".join(lines_ans[len_min:])+str(c.w)
    f_out+=str(c.y)+"\n".join(lines_out[len_min:])+str(c.w)
    return f_ans,f_out
        
def parse_params(argv: list):
    argc = len(argv)
    file: str = ""
    samples_directory: str = ""
    unit_tests = set()
    option_map = {"-t": "--test", "-c": "--color", "-f": "--file", "-d": "--directory"}
    for i, arg in enumerate(argv): 
        if arg in option_map.keys(): argv[i] = option_map[arg]
    if "--test" in argv:
        i = argv.index("--test")+1
        while i < argc and str.isnumeric(argv[i]):
            unit_tests.add(int(argv[i]))
            i+=1
    if "--color" in argv: 
        c.enable_colors()
    if "--file" in argv:
        i = argv.index("--file")
        if i+1 == argc: 
            print(f"{c.r}error: --file option requires a file path{c.w}")
            exit(1)
        file = Path(argv[i+1])
    if "--directory" in argv:
        i = argv.index("--directory")
        if i+1 == argc:
            print(f"{c.r}error: --folder option requires a folder path{c.w}")
        samples_directory = Path(argv[i+1])
    if not(file and samples_directory):
        print("missing arguments, no url or file found")
        print("format : python3 main.py [-f <solution file>] [-t <unit_tests_to_run...>] [<options...>]")
        exit(1)
    return file, samples_directory, unit_tests

def run_test(solution_path: str, test_input: str, test_answer: str):
    t = perf_counter()
    p = subprocess.run([sys.executable, solution_path],
                    input=test_input, encoding="utf-8", capture_output=True, timeout=10.)
    t = perf_counter()-t

    out = p.stdout.strip()
    # strip all lines
    out = "\n".join([line.strip() for line in out.split("\n")])

    print("Sample input:\n", test_input, sep="")
    if p.returncode != 0:
        print(f"{c.r}Error while running solution:{c.w}\n{p.stderr}\n")
        print(f"output:\n{out}")
        return

    if out != test_answer:
        print(f"{c.r}Wrong answer!{c.w}")
        f_ans,f_out = get_difference_disp(test_answer,out)
        print("Expected:", len(test_answer),"\n\"", f_ans, sep="", end="\"\n\n")
        print("Got:", len(out),"\n\"", f_out, sep="", end="\"\n")
    else:
        print(f"{c.g}Good answer!{c.w}")
        print(f"Answer:\n{c.g}{out}{c.w}")
    print(f"{c.d}took {round(t,3)}s{c.w}\n")

def main():
    solution_path, samples_directory, unit_tests = parse_params(sys.argv)

    print(f"argv: {c.c}{' '.join(sys.argv)}{c.w}")

    if not Path.exists(solution_path):
        print(f"{c.r}error: file {solution_path} does not exist !{c.w}")
        exit(1)
    print(f"running solution: {c.c}{solution_path}{c.w}")    
    
    if not Path.exists(samples_directory):
        print(f"{c.r}error: folder {solution_path} does not exist !{c.w}")
        exit(1)
    print(f"reading samples from: {c.c}{samples_directory}{c.w}")
    
    available_samples = set()
    for file in os.listdir(samples_directory):
        if "output" in file: continue
        available_samples.add(int(file.replace("input","").replace(".txt","")))
    samples_to_run = sorted(list(unit_tests.intersection(available_samples) if unit_tests else available_samples))
    print(f"unit test to run: {c.c}{' '.join(map(str,samples_to_run))}{c.w}\n")

    for i in samples_to_run:
        print(f"{c.cu}Test case {i}{c.w}")
        with open(f"{samples_directory}/input{i}.txt", "r") as problem_input:
            test_input = problem_input.read()
        with open(f"{samples_directory}/output{i}.txt", "r") as problem_input:
            test_answer = problem_input.read()
        try:
            run_test(solution_path, test_input, test_answer)
        except TimeoutExpired:
            print(f"{c.r}subprocess timeout{c.w}\n")         

if __name__ == "__main__":
    print(f" _____ _           _             _                     _\n|_   _| |         | |           | |                   | |\n  | | | |__   __ _| | ___  ___  | |     ___   __ _  __| | ___ _ __\n  | | | '_ \ / _` | |/ _ \/ __| | |    / _ \ / _` |/ _` |/ _ \ '__|\n  | | | | | | (_| | |  __/\__ \ | |___| (_) | (_| | (_| |  __/ |\n  \_/ |_| |_|\__,_|_|\___||___/ \_____/\___/ \__,_|\__,_|\___|_|\n{64*'='}")
    main()