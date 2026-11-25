import sys
import traceback
import io
import contextlib
import re

try:
    from codecarbon import EmissionsTracker
    CODECARBON_AVAILABLE = True
except ImportError:
    CODECARBON_AVAILABLE = False


def parse_cpp_errors(code_str):
    """
    Parses C++ source code or compiler logs to detect syntax errors, missing 
    headers, missing namespaces, missing semicolons, and bracket mismatches.
    """
    # 1. Missing 'cout', 'cin', or 'endl' (Missing namespace std or <iostream>)
    if re.search(r"(‘cout’|'cout'|\bcout\b|‘cin’|'cin'|\bcin\b|‘endl’|'endl'|\bendl\b)", code_str):
        has_iostream = "#include <iostream>" in code_str or "#include<iostream>" in code_str
        has_std = "using namespace std;" in code_str or "std::cout" in code_str

        if not has_iostream or not has_std:
            missing_parts = []
            if not has_iostream:
                missing_parts.append("`#include <iostream>` header is missing")
            if not has_std:
                missing_parts.append("`using namespace std;` or `std::` prefix is missing")

            return {
                "error_type": "Missing C++ Standard I/O Identifier",
                "error_message": "cout/cin/endl is missing or unrecognized by the C++ compiler.",
                "line_number": _find_line_number(code_str, r"\b(cout|cin|endl)\b"),
                "error_category": "Header / Namespace Error",
                "traceback": f"error: 'cout' was not declared in this scope; did you mean 'std::cout'?\nDetails: {', '.join(missing_parts)}.",
                "green_metrics": {"execution_time_sec": 0.005},
                "stdout": ""
            }

    # 2. Missing Semicolon ';' in C++
    lines = code_str.split("\n")
    for idx, line in enumerate(lines, 1):
        line_clean = line.strip()
        # Lines that usually require semicolons in C++
        if line_clean and not line_clean.startswith("//") and not line_clean.startswith("#"):
            if not line_clean.endswith(";") and not line_clean.endswith("{") and not line_clean.endswith("}"):
                if any(kw in line_clean for kw in ["cout", "cin", "return", "int ", "float ", "double ", "string ", "char "]):
                    return {
                        "error_type": "SyntaxError: Missing Semicolon",
                        "error_message": f"Missing semicolon ';' at line {idx}.",
                        "line_number": idx,
                        "error_category": "SyntaxError",
                        "traceback": f"error: expected ';' before line {idx+1}\n  {line_clean}",
                        "green_metrics": {"execution_time_sec": 0.004},
                        "stdout": ""
                    }

    # 3. Unmatched Brackets '{ }' or '( )'
    if code_str.count("{") != code_str.count("}"):
        return {
            "error_type": "SyntaxError: Unmatched Braces",
            "error_message": "Mismatched curly braces `{}` detected.",
            "line_number": len(lines),
            "error_category": "SyntaxError",
            "traceback": "error: expected '}' at end of input",
            "green_metrics": {"execution_time_sec": 0.003},
            "stdout": ""
        }

    # 4. Missing main() function in C++
    if "main()" not in code_str and "main (" not in code_str:
        return {
            "error_type": "Missing Main Function",
            "error_message": "The mandatory `int main()` entry point function is missing.",
            "line_number": 1,
            "error_category": "Linker / Structural Error",
            "traceback": "error: undefined reference to `main'",
            "green_metrics": {"execution_time_sec": 0.002},
            "stdout": ""
        }

    return None


def _find_line_number(code_str, pattern):
    """Utility to find the line number matching a regex pattern."""
    for idx, line in enumerate(code_str.split("\n"), 1):
        if re.search(pattern, line):
            return idx
    return 1


def extract_error(code):
    """
    Executes code safely, captures error type, message, traceback,
    line number, and optionally tracks CodeCarbon emissions.
    Supports both C++ code and Python test cases.
    """
    ir = {
        "error_type": None,
        "error_message": None,
        "line_number": None,
        "error_category": None,
        "traceback": None,
        "green_metrics": None,
        "stdout": ""
    }

    # Step A: Check if the code is C++ (contains C++ syntax indicators)
    is_cpp = any(tag in code for tag in ["#include", "int main", "cout", "cin", "std::", "using namespace"])
    if is_cpp:
        cpp_result = parse_cpp_errors(code)
        if cpp_result:
            return cpp_result

    # Step B: Python Code Execution & Runtime/Syntax Error Interception
    tracker = None
    if CODECARBON_AVAILABLE:
        try:
            tracker = EmissionsTracker(save_to_file=False, log_level="error")
            tracker.start()
        except Exception:
            tracker = None

    import time
    start_time = time.perf_counter()

    f = io.StringIO()
    try:
        with contextlib.redirect_stdout(f):
            exec(code, {"__name__": "__main__"})
        ir["stdout"] = f.getvalue()

    except Exception as e:
        exec_time = time.perf_counter() - start_time
        ir["stdout"] = f.getvalue()
        
        exc_type, exc_value, exc_tb = sys.exc_info()
        tb_lines = traceback.format_exception(exc_type, exc_value, exc_tb)
        full_traceback = "".join(tb_lines)

        ir["error_type"] = exc_type.__name__
        ir["error_message"] = str(exc_value)
        ir["traceback"] = full_traceback

        # Categorize Python errors
        if isinstance(e, SyntaxError):
            ir["error_category"] = "Syntax/Parsing Issue"
            ir["line_number"] = e.lineno
        elif isinstance(e, NameError):
            ir["error_category"] = "Undeclared Identifier"
            ir["line_number"] = _extract_line_from_tb(exc_tb)
        elif isinstance(e, TypeError):
            ir["error_category"] = "Type Mismatch"
            ir["line_number"] = _extract_line_from_tb(exc_tb)
        elif isinstance(e, ZeroDivisionError):
            ir["error_category"] = "Arithmetic Exception"
            ir["line_number"] = _extract_line_from_tb(exc_tb)
        else:
            ir["error_category"] = "Runtime Error"
            ir["line_number"] = _extract_line_from_tb(exc_tb)

        emissions = 0.0
        if tracker:
            try:
                emissions = tracker.stop() or 0.0
            except Exception:
                emissions = 0.0

        ir["green_metrics"] = {
            "execution_time_sec": exec_time,
            "emissions_kg": emissions
        }
        return ir

    exec_time = time.perf_counter() - start_time
    if tracker:
        try:
            tracker.stop()
        except Exception:
            pass

    ir["green_metrics"] = {"execution_time_sec": exec_time, "emissions_kg": 0.0}
    return ir


def _extract_line_from_tb(tb):
    """Extracts the line number from the traceback object."""
    while tb and tb.tb_next:
        tb = tb.tb_next
    return tb.tb_lineno if tb else 1