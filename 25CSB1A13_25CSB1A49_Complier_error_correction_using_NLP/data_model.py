# data_model.py — Restored (was deleted from original project)

class CompilerError:
    """
    Data model representing a captured compiler/runtime error.
    Used by IRGenerator and NLPExplainer.
    """
    def __init__(self, error_type, message, line_number, category, traceback_info):
        self.error_type     = error_type       # e.g. "NameError"
        self.message        = message          # e.g. "name 'x' is not defined"
        self.line_number    = line_number      # int line number
        self.category       = category        # e.g. "Runtime" / "Syntax"
        self.traceback_info = traceback_info  # full traceback string

    def __repr__(self):
        return (f"CompilerError(type={self.error_type}, "
                f"line={self.line_number}, msg={self.message!r})")
