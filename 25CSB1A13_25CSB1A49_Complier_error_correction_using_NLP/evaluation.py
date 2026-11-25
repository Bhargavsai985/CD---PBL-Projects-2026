"""
evaluation.py — Enhanced Evaluator v2.0

Scoring metrics:
  1. Format Score     — checks for Mistake / Reason / Fix keywords
  2. Keyword Score    — checks for error-type-specific technical keywords
  3. Similarity Score — word-level Jaccard overlap with expected output
  4. Length Penalty   — penalises very short (too vague) responses
  5. Final Score      — weighted combination of all above
"""

import re


class Evaluator:

    # Technical keywords expected per error type
    ERROR_KEYWORDS = {
        "NameError":        ["undefined", "variable", "not defined", "declared", "scope"],
        "TypeError":        ["type", "incompatible", "conversion", "integer", "string", "operand"],
        "ZeroDivisionError":["zero", "division", "denominator", "undefined", "guard"],
        "SyntaxError":      ["syntax", "structure", "colon", "bracket", "indentation", "invalid"],
        "IndexError":       ["index", "range", "bounds", "list", "out of"],
        "KeyError":         ["key", "dictionary", "dict", "missing", "not found"],
        "AttributeError":   ["attribute", "object", "method", "property", "NoneType"],
        "ValueError":       ["value", "conversion", "invalid", "format", "literal"],
        "ImportError":      ["module", "import", "package", "install", "not found"],
        "IndentationError": ["indentation", "indent", "spaces", "tabs", "block"],
        "RecursionError":   ["recursion", "base case", "infinite", "stack", "recursive"],
        "FileNotFoundError":["file", "path", "not found", "directory", "exists"],
        "OverflowError":    ["overflow", "too large", "numeric", "range", "maximum"],
        "MemoryError":      ["memory", "allocation", "exhausted", "RAM", "resources"],
        "StopIteration":    ["iteration", "iterator", "next", "generator", "exhausted"],
    }

    # Weights for final score calculation
    WEIGHTS = {
        "format":     0.30,
        "keyword":    0.25,
        "similarity": 0.35,
        "length":     0.10,
    }

    # ─────────────────────────────────────────────────────────────────

    def evaluate(self, predicted: str, expected: str, error_type: str = "") -> dict:
        """
        Evaluate the quality of a predicted explanation against
        an expected explanation.

        Returns a dict with individual scores and final_score (0.0–1.0).
        """
        predicted = predicted.strip()
        expected  = expected.strip()

        # 1. Format Score
        format_score = self._format_score(predicted)

        # 2. Keyword Score
        keyword_score = self._keyword_score(predicted, error_type)

        # 3. Similarity Score (Jaccard word overlap)
        similarity_score = self._similarity_score(predicted, expected)

        # 4. Length Penalty (ideal: 10–80 words)
        length_score = self._length_score(predicted)

        # 5. Weighted Final Score
        final_score = (
            self.WEIGHTS["format"]     * format_score +
            self.WEIGHTS["keyword"]    * keyword_score +
            self.WEIGHTS["similarity"] * similarity_score +
            self.WEIGHTS["length"]     * length_score
        )

        return {
            "format_score":     round(format_score,     2),
            "keyword_score":    round(keyword_score,    2),
            "similarity_score": round(similarity_score, 2),
            "length_score":     round(length_score,     2),
            "final_score":      round(final_score,      2),
            "grade":            self._grade(final_score),
        }

    # ── Individual Scoring Methods ────────────────────────────────────

    def _format_score(self, text: str) -> float:
        """Check presence of required structural keywords."""
        required = ["Mistake", "Reason", "Fix"]
        found = sum(1 for kw in required if kw.lower() in text.lower())
        return found / len(required)

    def _keyword_score(self, text: str, error_type: str) -> float:
        """Check how many domain-specific keywords are present."""
        keywords = self.ERROR_KEYWORDS.get(error_type, [])
        if not keywords:
            return 0.5  # neutral if error type unknown
        text_lower = text.lower()
        found = sum(1 for kw in keywords if kw in text_lower)
        return min(found / max(len(keywords), 1), 1.0)

    def _similarity_score(self, predicted: str, expected: str) -> float:
        """Jaccard word-level similarity."""
        if not expected:
            return 0.5  # neutral when no expected
        pred_words = set(re.findall(r'\w+', predicted.lower()))
        exp_words  = set(re.findall(r'\w+', expected.lower()))
        # Remove stopwords
        stopwords  = {"the", "a", "an", "is", "it", "in", "of", "to",
                      "and", "or", "be", "by", "for", "on", "at", "as"}
        pred_words -= stopwords
        exp_words  -= stopwords
        if not exp_words:
            return 0.5
        intersection = pred_words & exp_words
        union        = pred_words | exp_words
        return len(intersection) / max(len(union), 1)

    def _length_score(self, text: str) -> float:
        """Penalise too-short or too-long explanations."""
        word_count = len(text.split())
        if word_count < 5:
            return 0.0   # too short — useless
        elif word_count <= 60:
            return 1.0   # ideal range
        elif word_count <= 100:
            return 0.75  # slightly verbose
        else:
            return 0.5   # too long

    def _grade(self, score: float) -> str:
        """Convert numeric score to letter grade."""
        if score >= 0.90: return "A+"
        if score >= 0.80: return "A"
        if score >= 0.70: return "B"
        if score >= 0.60: return "C"
        if score >= 0.50: return "D"
        return "F"

    # ── Batch Evaluation ──────────────────────────────────────────────

    def evaluate_batch(self, pairs: list) -> dict:
        """
        Evaluate a list of (predicted, expected, error_type) tuples.
        Returns aggregate statistics.
        """
        results = []
        for item in pairs:
            predicted  = item.get("predicted", "")
            expected   = item.get("expected",  "")
            error_type = item.get("error_type","")
            results.append(self.evaluate(predicted, expected, error_type))

        if not results:
            return {}

        keys = ["format_score", "keyword_score", "similarity_score",
                "length_score", "final_score"]
        avg = {k: round(sum(r[k] for r in results) / len(results), 2) for k in keys}
        avg["total_evaluated"] = len(results)
        avg["grade"]           = self._grade(avg["final_score"])
        return avg
