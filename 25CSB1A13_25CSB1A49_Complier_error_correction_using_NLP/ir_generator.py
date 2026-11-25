# ir_generator.py — Enhanced v2.0
import ast
import json
import re


class IRGenerator:
    """
    Generates a rich Intermediate Representation (IR) JSON
    from raw Python source code + a CompilerError object.

    IR fields:
      error_type, error_message, error_category, line_number,
      ast_node, parent_node, variables_used, error_variable,
      indentation_level, surrounding_lines, function_context,
      traceback
    """

    def __init__(self, code: str, error_obj):
        self.code  = code
        self.error = error_obj
        self.lines = code.split("\n")

    # ── AST parent attachment ─────────────────────────────────────────
    def attach_parents(self, tree):
        for parent in ast.walk(tree):
            for child in ast.iter_child_nodes(parent):
                child.parent = parent

    # ── AST node info at error line ───────────────────────────────────
    def get_ast_info(self):
        try:
            tree = ast.parse(self.code)
            self.attach_parents(tree)
            for node in ast.walk(tree):
                if hasattr(node, "lineno") and node.lineno == self.error.line_number:
                    node_name   = type(node).__name__
                    parent_name = (type(node.parent).__name__
                                   if hasattr(node, "parent") else None)
                    return node_name, parent_name
        except Exception:
            pass
        return None, None

    # ── All variable names in code ────────────────────────────────────
    def get_variables(self):
        variables = set()
        try:
            tree = ast.parse(self.code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Name):
                    variables.add(node.id)
        except Exception:
            pass
        return sorted(variables)

    # ── Extract the specific variable causing the error ───────────────
    def extract_error_variable(self):
        msg = self.error.message or ""
        # NameError: name 'x' is not defined
        m = re.search(r"name '(.+?)' is not defined", msg)
        if m:
            return m.group(1)
        # KeyError: 'some_key'
        m = re.search(r"KeyError: '(.+?)'", msg)
        if m:
            return m.group(1)
        # AttributeError: 'NoneType' object has no attribute 'x'
        m = re.search(r"has no attribute '(.+?)'", msg)
        if m:
            return m.group(1)
        # Generic: anything in single quotes
        m = re.search(r"'(.+?)'", msg)
        if m:
            return m.group(1)
        return None

    # ── Indentation depth of error line ──────────────────────────────
    def get_indentation_level(self):
        try:
            line = self.lines[self.error.line_number - 1]
            return len(line) - len(line.lstrip())
        except Exception:
            return None

    # ── Surrounding 3 lines around error ─────────────────────────────
    def get_surrounding_lines(self):
        try:
            ln  = self.error.line_number
            start = max(0, ln - 2)
            end   = min(len(self.lines), ln + 2)
            return {
                str(i + 1): self.lines[i]
                for i in range(start, end)
            }
        except Exception:
            return {}

    # ── Which function/class contains the error line ──────────────────
    def get_function_context(self):
        try:
            tree = ast.parse(self.code)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    if hasattr(node, 'end_lineno'):
                        if node.lineno <= self.error.line_number <= node.end_lineno:
                            kind = "class" if isinstance(node, ast.ClassDef) else "function"
                            return f"{kind} '{node.name}' (lines {node.lineno}–{node.end_lineno})"
        except Exception:
            pass
        return "module level"

    # ── Classify error into broad category ───────────────────────────
    def classify_category(self):
        syntax_errors   = {"SyntaxError", "IndentationError", "TabError"}
        runtime_errors  = {"NameError", "TypeError", "ValueError", "ZeroDivisionError",
                           "IndexError", "KeyError", "AttributeError", "RuntimeError"}
        import_errors   = {"ImportError", "ModuleNotFoundError"}
        io_errors       = {"FileNotFoundError", "PermissionError", "IOError", "OSError"}
        memory_errors   = {"MemoryError", "RecursionError", "OverflowError"}

        et = self.error.error_type or ""
        if et in syntax_errors:   return "Syntax Error"
        if et in runtime_errors:  return "Runtime Error"
        if et in import_errors:   return "Import Error"
        if et in io_errors:       return "I/O Error"
        if et in memory_errors:   return "Memory / Resource Error"
        return "Unknown Error"

    # ── Main: build full IR dict ──────────────────────────────────────
    def generate_ir(self) -> str:
        ast_node, parent_node = self.get_ast_info()

        ir = {
            "error_type":        self.error.error_type,
            "error_message":     self.error.message,
            "error_category":    self.classify_category(),
            "line_number":       self.error.line_number,
            "ast_node":          ast_node,
            "parent_node":       parent_node,
            "variables_used":    self.get_variables(),
            "error_variable":    self.extract_error_variable(),
            "indentation_level": self.get_indentation_level(),
            "surrounding_lines": self.get_surrounding_lines(),
            "function_context":  self.get_function_context(),
            "traceback":         self.error.traceback_info,
        }

        return json.dumps(ir, indent=4)
