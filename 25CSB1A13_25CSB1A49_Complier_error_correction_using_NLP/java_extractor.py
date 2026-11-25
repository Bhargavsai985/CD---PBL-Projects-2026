# java_extractor.py — Java Compiler Error Extraction Engine
"""
Compiles and captures Java compilation errors using javac.
Returns a structured IR dict identical in shape to error_extractor.py
so the rest of the pipeline (IRGenerator, NLPExplainer, Evaluator) works
unchanged.
"""

import subprocess
import tempfile
import os
import re
import time

# ── Path to javac (auto-detect or fallback to PATH) ───────────────────
_JAVAC_CANDIDATES = [
    r"C:\Program Files\Java\jdk-27.0.1.0.3\bin\javac.exe",
    r"C:\Program Files\Java\latest\bin\javac.exe",
    r"C:\Program Files\Eclipse Adoptium\jdk-21\bin\javac.exe",
    "javac",   # if on PATH
]

def _find_javac() -> str:
    for candidate in _JAVAC_CANDIDATES:
        if os.path.isfile(candidate):
            return candidate
        try:
            subprocess.run([candidate, "-version"],
                           capture_output=True, timeout=5)
            return candidate
        except Exception:
            pass
    return None

JAVAC_PATH = _find_javac()


# ── Common Java runtime error patterns ───────────────────────────────
_RUNTIME_PATTERNS = [
    (r"cannot find symbol",                        "SymbolError",        "Cannot find symbol — variable or method not declared."),
    (r"reached end of file while parsing",         "SyntaxError",        "Missing closing brace '}'. Check all braces are matched."),
    (r"';' expected",                              "SyntaxError",        "Missing semicolon ';' at end of statement."),
    (r"illegal start of expression",               "SyntaxError",        "Illegal start of expression — unexpected token found."),
    (r"class .+ is public.*must be declared",      "ClassNameError",     "Public class name must match the filename exactly."),
    (r"incompatible types",                        "TypeError",          "Incompatible types — cannot assign or convert between types."),
    (r"variable .+ might not have been initialized","UninitializedError","Variable used before it was initialized."),
    (r"method .+ cannot be applied",               "MethodError",        "Method called with wrong number or type of arguments."),
    (r"operator .+ cannot be applied",             "OperatorError",      "Operator used on incompatible types."),
    (r"array required, but",                       "ArrayError",         "Array indexing attempted on a non-array variable."),
    (r"ArrayIndexOutOfBoundsException",            "IndexError",         "Array index out of bounds at runtime."),
    (r"NullPointerException",                      "NullError",          "Null pointer dereference — object is null."),
    (r"StackOverflowError",                        "RecursionError",     "Stack overflow — infinite recursion detected."),
    (r"ClassCastException",                        "CastError",          "Invalid class cast — incompatible object types."),
    (r"NumberFormatException",                     "ValueError",         "Invalid number format — cannot parse string as number."),
    (r"ArithmeticException.*/ by zero",            "ZeroDivisionError",  "Division by zero."),
    (r"duplicate class",                           "DuplicateError",     "Duplicate class name — class already defined."),
    (r"unchecked or unsafe operations",            "UncheckedWarning",   "Unchecked operations detected — use generics properly."),
    (r"package .+ does not exist",                 "ImportError",        "Package does not exist — check import statement."),
    (r"exception .+ is never thrown",              "ExceptionError",     "Declared exception is never thrown in the method body."),
]


def _parse_javac_output(stderr: str, source_file: str) -> dict:
    """
    Parse javac stderr output into structured IR dict.

    javac error format:
      FileName.java:LINE: error: MESSAGE
              OFFENDING_CODE
              ^
    """
    fname = os.path.basename(source_file)
    errors = []

    # Match each error block
    pattern = re.compile(
        rf'{re.escape(fname)}:(\d+):\s*(error|warning):\s*(.+)', re.IGNORECASE
    )
    for match in pattern.finditer(stderr):
        line_no  = int(match.group(1))
        severity = match.group(2).lower()
        message  = match.group(3).strip()
        errors.append((line_no, severity, message))

    if not errors:
        # Try generic line extraction
        generic = re.search(r':(\d+):\s*(?:error|warning):\s*(.+)', stderr)
        if generic:
            errors.append((int(generic.group(1)), "error", generic.group(2).strip()))

    if not errors:
        return None   # No parseable error

    # Take the first (most critical) error
    line_no, severity, raw_message = errors[0]

    # Match to known error type
    error_type    = "JavaCompileError"
    error_message = raw_message
    for pattern_str, etype, friendly_msg in _RUNTIME_PATTERNS:
        if re.search(pattern_str, raw_message, re.IGNORECASE):
            error_type    = etype
            error_message = friendly_msg + f" (Detail: {raw_message})"
            break

    return {
        "error_type":    error_type,
        "error_message": error_message,
        "line_number":   line_no,
        "traceback":     stderr.strip(),
        "error_category":"Compile Error",
        "stdout":        "",
        "all_errors":    errors,       # all errors found
        "language":      "java",
        "green_metrics": None,
    }


def extract_java_error(code: str, class_name: str = "Main") -> dict:
    """
    Write Java code to a temp file, compile with javac, capture errors.

    Args:
        code:       Raw Java source code string.
        class_name: The public class name in the code (default 'Main').
                    The file must be named <class_name>.java for javac.

    Returns:
        IR dict (same shape as error_extractor.extract_error).
    """
    ir = {
        "error_type":    None,
        "error_message": None,
        "line_number":   None,
        "traceback":     None,
        "error_category":None,
        "stdout":        "",
        "language":      "java",
        "green_metrics": None,
    }

    if not JAVAC_PATH:
        ir["error_type"]    = "EnvironmentError"
        ir["error_message"] = (
            "javac not found. Install JDK from https://www.oracle.com/java/technologies/downloads/ "
            "and ensure javac is in PATH."
        )
        ir["traceback"] = "javac executable not found on this system."
        return ir

    # ── Write to named temp file ──────────────────────────────────────
    tmp_dir  = tempfile.mkdtemp()
    src_file = os.path.join(tmp_dir, f"{class_name}.java")

    try:
        with open(src_file, "w", encoding="utf-8") as f:
            f.write(code)

        start = time.perf_counter()

        # ── Compile ───────────────────────────────────────────────────
        result = subprocess.run(
            [JAVAC_PATH, src_file],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=tmp_dir
        )

        duration = time.perf_counter() - start

        ir["green_metrics"] = {
            "execution_time_sec": duration,
            "emissions_kg":       0,
            "energy_consumed_kwh":0,
        }

        if result.returncode == 0:
            # Compiled successfully — no errors
            ir["stdout"] = result.stdout or "Compiled successfully with no errors."
            return ir

        # ── Parse errors ──────────────────────────────────────────────
        stderr = result.stderr or result.stdout or ""
        parsed = _parse_javac_output(stderr, src_file)

        if parsed:
            ir.update(parsed)
        else:
            ir["error_type"]    = "JavaCompileError"
            ir["error_message"] = stderr.strip()[:500]
            ir["traceback"]     = stderr.strip()

        return ir

    except subprocess.TimeoutExpired:
        ir["error_type"]    = "TimeoutError"
        ir["error_message"] = "Compilation timed out after 30 seconds."
        ir["traceback"]     = "subprocess.TimeoutExpired"
        return ir

    except Exception as e:
        ir["error_type"]    = "InternalError"
        ir["error_message"] = str(e)
        ir["traceback"]     = str(e)
        return ir

    finally:
        # ── Cleanup temp files ────────────────────────────────────────
        try:
            for f in os.listdir(tmp_dir):
                os.remove(os.path.join(tmp_dir, f))
            os.rmdir(tmp_dir)
        except Exception:
            pass


def detect_java_class_name(code: str) -> str:
    """
    Extract the public class name from Java source code.
    Falls back to 'Main' if not found.
    """
    match = re.search(r'\bpublic\s+class\s+(\w+)', code)
    if match:
        return match.group(1)
    # Try any class declaration
    match = re.search(r'\bclass\s+(\w+)', code)
    if match:
        return match.group(1)
    return "Main"
