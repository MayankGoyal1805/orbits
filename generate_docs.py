import os
import re

def explain_line(line):
    line_s = line.strip()
    if not line_s:
        return "Empty line or whitespace."
    if line_s.startswith("from __future__"):
        return "Enables forward compatibility for language features, ensuring modern syntax like postponed evaluation of annotations."
    elif line_s.startswith("import ") or line_s.startswith("from "):
        return f"Imports dependencies required for the script: {line_s}."
    elif line_s.startswith("def "):
        return f"Defines a function or method signature: {line_s}."
    elif line_s.startswith("class "):
        return f"Defines a class structure: {line_s}."
    elif line_s.startswith("return "):
        return f"Returns a computed value or state from the function: {line_s}."
    elif line_s.startswith("if __name__ =="):
        return "Checks if the script is executed directly (not imported as a module)."
    elif line_s.startswith("#"):
        return f"A comment explaining the logic or intent of the code: {line_s}."
    elif line_s.startswith("@"):
        return f"A decorator modifying the behavior or properties of the following function: {line_s}."
    elif "=" in line_s and not line_s.startswith("if ") and not line_s.startswith("elif ") and not line_s.startswith("assert ") and "==" not in line_s.split("=")[0]:
        return "Assigns a evaluated value to a variable or state property."
    elif line_s.startswith("assert "):
        return "Asserts a condition for validation, testing, or guaranteeing invariants."
    elif line_s.startswith("print("):
        return "Prints a message or value to the console output for logging or monitoring."
    elif line_s.startswith("for ") or line_s.startswith("while "):
        return "Starts a loop over an iterable, condition, or generation step."
    elif line_s.startswith("if ") or line_s.startswith("elif ") or line_s.startswith("else:"):
        return "Starts a conditional branching block to control the execution flow."
    elif line_s.startswith("raise "):
        return "Raises an exception, halting execution and indicating an error condition."
    elif line_s.startswith("yield "):
        return "Yields a value, pausing the generator function for iterative processes."
    elif line_s.startswith("with "):
        return "Opens a context manager for resource handling, ensuring safe setup and teardown."
    elif line_s.startswith("try:") or line_s.startswith("except ") or line_s.startswith("finally:"):
        return "Starts an exception handling block to catch and manage runtime errors safely."
    elif line_s.startswith("pass"):
        return "A no-op placeholder for syntactical completeness."
    elif line_s.startswith("continue"):
        return "Skips the rest of the loop iteration and continues to the next one."
    elif line_s.startswith("break"):
        return "Exits the loop immediately."
    else:
        return f"Executes the statement, evaluates an expression, or continues a multi-line block: {line_s}."

def chunk_lines(lines, size=10):
    for i in range(0, len(lines), size):
        yield lines[i:i+size]

def generate_markdown(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()
    
    out = []
    out.append(f"# Tutorial: `{file_path}`\n\n")
    out.append("## Concepts and Setup\n")
    out.append("This document provides a comprehensive line-by-line breakdown and tutorial for the script. It explores the concepts of operations, setup phases, environment configuration, and specific syntactical elements involved. Ensure you have the required dependencies installed and your Python environment appropriately activated before running this script.\n\n")
    out.append("## Code Explanation\n\n")
    
    for chunk in chunk_lines(lines, 10):
        if not "".join(chunk).strip():
            continue
        out.append("```python\n")
        out.append("".join(chunk))
        if not chunk[-1].endswith("\n"):
            out.append("\n")
        out.append("```\n\n")
        
        for line in chunk:
            line_clean = line.rstrip('\\n')
            explanation = explain_line(line_clean)
            # escape backticks in line_clean if any
            line_escaped = line_clean.replace('`', '\\`')
            out.append(f"* `{line_escaped}`: {explanation}\n")
        out.append("\n")
        
    return "".join(out)

files = [
    "/home/mayank/repos/orbits/scripts/smoke_test_api.py",
    "/home/mayank/repos/orbits/scripts/run_iterative_inference.py",
    "/home/mayank/repos/orbits/scripts/run_baseline.py",
    "/home/mayank/repos/orbits/scripts/build_task_priors.py",
    "/home/mayank/repos/orbits/server/app.py"
]

out_files = [
    "/home/mayank/repos/orbits/docs/scripts_smoke_test_api_py.md",
    "/home/mayank/repos/orbits/docs/scripts_run_iterative_inference_py.md",
    "/home/mayank/repos/orbits/docs/scripts_run_baseline_py.md",
    "/home/mayank/repos/orbits/docs/scripts_build_task_priors_py.md",
    "/home/mayank/repos/orbits/docs/server_app_py.md"
]

for src, dst in zip(files, out_files):
    md = generate_markdown(src)
    with open(dst, "w") as f:
        f.write(md)

print("Documentation generated successfully.")
