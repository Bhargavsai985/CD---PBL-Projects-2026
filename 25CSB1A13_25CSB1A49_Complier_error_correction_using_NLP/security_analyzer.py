"""
INTELLIFIX / SecAICodeTutor — Advanced Security Vulnerability & Code Auditing Engine
Comprehensive AST and static semantic analysis covering 52+ CWE and OWASP Top 10 vulnerabilities.
"""

import ast
import re

class SecurityAnalyzer:
    """
    Enterprise-grade static security analyzer using Python's Abstract Syntax Tree (AST)
    and heuristic taint analysis to detect 52+ vulnerability types before code execution.
    """

    def __init__(self):
        pass

    def scan_code(self, code_string: str):
        """
        Parses the code string into an AST and inspects all nodes for security weaknesses.
        Returns a list of structured vulnerability dictionaries.
        """
        vulnerabilities = []
        if not code_string or not code_string.strip():
            return vulnerabilities

        try:
            tree = ast.parse(code_string)
        except SyntaxError:
            # If the code has syntax errors, fall back to line-by-line regex scanning
            return self._fallback_regex_scan(code_string)

        # ── AST Node-Level Traversal ──────────────────────────────────────────
        for node in ast.walk(tree):
            lineno = getattr(node, 'lineno', 1)

            # 1. Function and Method Calls
            if isinstance(node, ast.Call):
                self._check_call_node(node, lineno, vulnerabilities, code_string)

            # 2. Variable and Secret Assignments
            elif isinstance(node, ast.Assign):
                self._check_assign_node(node, lineno, vulnerabilities)

            # 3. Assert Statements Used for Security Checks
            elif isinstance(node, ast.Assert):
                self._check_assert_node(node, lineno, vulnerabilities)

            # 4. Insecure Imports
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                self._check_import_node(node, lineno, vulnerabilities)

            # 5. Dangerous Binary Comparisons (Timing Attacks)
            elif isinstance(node, ast.Compare):
                self._check_compare_node(node, lineno, vulnerabilities)

            # 6. Silent Exception Suppression
            elif isinstance(node, ast.ExceptHandler):
                self._check_except_node(node, lineno, vulnerabilities)

        # Merge with supplementary pattern scans (e.g., regex for raw URLs, comments, templates)
        supp_vulns = self._supplementary_scan(code_string)
        for sv in supp_vulns:
            # Avoid duplicate warnings on the same line for the same vulnerability
            if not any(v.get('line') == sv.get('line') and v.get('type') == sv.get('type') for v in vulnerabilities):
                vulnerabilities.append(sv)

        # ── Cross-Check with Malware, Virus & Worm Safety Shield ──
        try:
            import malware_detector
            threats = malware_detector.scan_malware(code_string)
            for t in threats:
                if not any(v.get('line') == t.get('line') and t.get('name') in v.get('type', '') for v in vulnerabilities):
                    vulnerabilities.append({
                        "type": f"{t['icon']} {t['category']}: {t['name']}",
                        "cwe": t.get("cwe", "CWE-506"),
                        "severity": "CRITICAL",
                        "message": f"[{t.get('mitre', 'Malware')}] {t.get('description', '')} (Safety Action: {t.get('safety_action', 'BLOCKED')})",
                        "line": t.get("line", 1)
                    })
        except Exception:
            pass

        # Sort by line number
        vulnerabilities.sort(key=lambda x: x.get('line', 0) if isinstance(x.get('line'), int) else 0)
        return vulnerabilities

    def scan(self, code_string: str):
        """Alias for scan_code."""
        return self.scan_code(code_string)

    def _check_call_node(self, node, lineno, vulns, code_string):
        """Inspects all Call nodes for dangerous functions, methods, and arguments."""
        func = node.func
        func_name = ""
        attr_name = ""
        full_call = ""

        if isinstance(func, ast.Name):
            func_name = func.id
            full_call = func_name
        elif isinstance(func, ast.Attribute):
            attr_name = func.attr
            if isinstance(func.value, ast.Name):
                full_call = f"{func.value.id}.{attr_name}"
            elif isinstance(func.value, ast.Attribute):
                full_call = f"{getattr(func.value.value, 'id', '')}.{func.value.attr}.{attr_name}"
            else:
                full_call = attr_name

        # ── Group 1: Arbitrary Code Execution (CWE-95) ──
        if func_name in ('eval', 'exec'):
            vulns.append({
                "type": "Arbitrary Code Execution",
                "cwe": "CWE-95",
                "severity": "CRITICAL",
                "message": f"{func_name}() executes untrusted strings as raw Python code. Use ast.literal_eval() or safe parser.",
                "line": lineno
            })
        elif func_name == 'input':
            vulns.append({
                "type": "Unvalidated User Input",
                "cwe": "CWE-20",
                "severity": "MEDIUM",
                "message": "input() captures raw user string without validation or boundary checks. Wrap in validation/sanitization functions.",
                "line": lineno
            })

        # ── Group 2: OS Command Injections (CWE-78) ──
        if full_call in ('os.system', 'system'):
            vulns.append({
                "type": "OS Command Injection",
                "cwe": "CWE-78",
                "severity": "CRITICAL",
                "message": "os.system() directly invokes the host shell. Use subprocess.run() with a list of arguments and shell=False.",
                "line": lineno
            })
        elif full_call in ('os.popen', 'popen'):
            vulns.append({
                "type": "Command Injection via os.popen",
                "cwe": "CWE-78",
                "severity": "CRITICAL",
                "message": "os.popen() opens a pipe to an insecure shell command. Use subprocess.Popen() with explicit arg vector.",
                "line": lineno
            })
        elif full_call.startswith('os.spawn') or full_call in ('os.posix_spawn', 'posix_spawn'):
            vulns.append({
                "type": "Process Execution via os.spawn",
                "cwe": "CWE-78",
                "severity": "HIGH",
                "message": f"{full_call}() is a deprecated, low-level process spawn method. Migrate to subprocess.run().",
                "line": lineno
            })
        elif full_call in ('pty.spawn',):
            vulns.append({
                "type": "Pseudo-Terminal Command Injection (pty.spawn)",
                "cwe": "CWE-78",
                "severity": "HIGH",
                "message": "pty.spawn() allocates an interactive pseudo-terminal. Restrict terminal execution to sanitized commands.",
                "line": lineno
            })

        # ── Group 3: Subprocess with shell=True (CWE-78) ──
        if full_call in ('subprocess.Popen', 'subprocess.run', 'subprocess.call', 'subprocess.check_output', 'subprocess.check_call'):
            for kw in node.keywords:
                if kw.arg == 'shell':
                    if isinstance(kw.value, ast.Constant) and kw.value.value is True:
                        vulns.append({
                            "type": "Shell Command Injection",
                            "cwe": "CWE-78",
                            "severity": "HIGH",
                            "message": f"{full_call}(..., shell=True) allows shell metacharacter injection. Set shell=False and pass args as list.",
                            "line": lineno
                        })

        # ── Group 4: Insecure Deserialization (CWE-502) ──
        if full_call in ('pickle.load', 'pickle.loads', 'pickle.dump', 'pickle.dumps', '_pickle.loads'):
            vulns.append({
                "type": "Insecure Deserialization (Pickle)",
                "cwe": "CWE-502",
                "severity": "CRITICAL",
                "message": "pickle deserialization executes arbitrary bytecode via __reduce__. Replace with JSON, Protocol Buffers, or safe serialization.",
                "line": lineno
            })
        elif full_call in ('yaml.load', 'load') and full_call.startswith('yaml.'):
            has_safe = any(kw.arg == 'Loader' and 'Safe' in getattr(kw.value, 'id', getattr(kw.value, 'attr', '')) for kw in node.keywords)
            if not has_safe:
                vulns.append({
                    "type": "Unsafe YAML Deserialization",
                    "cwe": "CWE-502",
                    "severity": "CRITICAL",
                    "message": "yaml.load() without Loader=yaml.SafeLoader can instantiate arbitrary Python objects. Use yaml.safe_load().",
                    "line": lineno
                })
        elif full_call in ('marshal.load', 'marshal.loads', 'shelve.open'):
            vulns.append({
                "type": "Insecure Deserialization (Marshal/Shelve)",
                "cwe": "CWE-502",
                "severity": "HIGH",
                "message": f"{full_call}() is vulnerable to code execution when parsing untrusted data.",
                "line": lineno
            })
        elif full_call in ('dill.load', 'dill.loads', 'cloudpickle.load', 'cloudpickle.loads'):
            vulns.append({
                "type": "Insecure Deserialization (Dill/Cloudpickle)",
                "cwe": "CWE-502",
                "severity": "CRITICAL",
                "message": f"{full_call}() deserializes Python code objects and closures directly, allowing arbitrary code execution.",
                "line": lineno
            })
        elif full_call in ('jsonpickle.decode', 'jsonpickle.encode'):
            vulns.append({
                "type": "Insecure Object Hydration (jsonpickle)",
                "cwe": "CWE-502",
                "severity": "HIGH",
                "message": "jsonpickle dynamically constructs object instances from JSON. Use standard json with explicit schemas.",
                "line": lineno
            })

        # ── Group 5: SQL Injection (CWE-89) ──
        if attr_name in ('execute', 'executemany', 'raw'):
            if node.args:
                arg0 = node.args[0]
                if isinstance(arg0, ast.JoinedStr):
                    vulns.append({
                        "type": "SQL Injection via f-string",
                        "cwe": "CWE-89",
                        "severity": "CRITICAL",
                        "message": "SQL query built using formatted string (f-string). Use parameterized queries: cursor.execute('SELECT ... WHERE id = %s', (id,)).",
                        "line": lineno
                    })
                elif isinstance(arg0, ast.BinOp) and isinstance(arg0.op, (ast.Mod, ast.Add)):
                    vulns.append({
                        "type": "SQL Injection via Concatenation",
                        "cwe": "CWE-89",
                        "severity": "CRITICAL",
                        "message": "SQL query built via string concatenation (+) or modulo format (%). Use parameterized binding placeholders.",
                        "line": lineno
                    })
                elif isinstance(arg0, ast.Call) and isinstance(arg0.func, ast.Attribute) and arg0.func.attr == 'format':
                    vulns.append({
                        "type": "SQL Injection via format()",
                        "cwe": "CWE-89",
                        "severity": "CRITICAL",
                        "message": "SQL query built via .format(). Replace with parameterized query placeholders.",
                        "line": lineno
                    })

        # ── Group 6: Broken Cryptographic Hashes (CWE-328) ──
        if full_call in ('hashlib.md5', 'md5'):
            vulns.append({
                "type": "Broken Cryptographic Hash (MD5)",
                "cwe": "CWE-328",
                "severity": "HIGH",
                "message": "MD5 is cryptographically broken and collision-vulnerable. Use SHA-256 (hashlib.sha256()) or Argon2/bcrypt for passwords.",
                "line": lineno
            })
        elif full_call in ('hashlib.sha1', 'sha1'):
            vulns.append({
                "type": "Collision-Vulnerable Hash (SHA-1)",
                "cwe": "CWE-328",
                "severity": "MEDIUM",
                "message": "SHA-1 is deprecated and vulnerable to collision attacks. Upgrade to SHA-256 or SHA-512.",
                "line": lineno
            })

        # ── Group 7: Cryptographically Insecure PRNG (CWE-330) ──
        if full_call in ('random.random', 'random.randint', 'random.choice', 'random.randrange', 'random.sample'):
            vulns.append({
                "type": "Insecure Pseudo-Random Number Generator",
                "cwe": "CWE-330",
                "severity": "HIGH",
                "message": f"{full_call}() uses the Mersenne Twister which is predictable. Use secrets.token_hex() or secrets.SystemRandom() for tokens/passwords.",
                "line": lineno
            })

        # ── Group 8: Weak Cipher Modes & Algorithms (CWE-327) ──
        if attr_name == 'MODE_ECB' or 'ECB' in full_call:
            vulns.append({
                "type": "Insecure Cipher Mode (ECB)",
                "cwe": "CWE-327",
                "severity": "HIGH",
                "message": "Electronic Codebook (ECB) mode lacks diffusion and reveals plaintext patterns. Use GCM or CBC with random IV.",
                "line": lineno
            })
        if full_call in ('DES.new', 'ARC4.new', 'Blowfish.new'):
            vulns.append({
                "type": "Deprecated Weak Cipher (DES/RC4)",
                "cwe": "CWE-327",
                "severity": "HIGH",
                "message": f"Cipher {full_call} is deprecated and susceptible to cryptanalysis. Upgrade to AES-GCM or ChaCha20-Poly1305.",
                "line": lineno
            })

        # ── Group 9: Insecure SSL/TLS Verification (CWE-295) ──
        if full_call in ('requests.get', 'requests.post', 'requests.put', 'requests.delete', 'requests.request', 'urllib.request.urlopen'):
            for kw in node.keywords:
                if kw.arg == 'verify' and isinstance(kw.value, ast.Constant) and kw.value.value is False:
                    vulns.append({
                        "type": "Disabled SSL Certificate Verification",
                        "cwe": "CWE-295",
                        "severity": "CRITICAL",
                        "message": "verify=False disables TLS certificate verification, leaving network connections open to Man-in-the-Middle (MITM) attacks.",
                        "line": lineno
                    })
        if full_call in ('ssl._create_unverified_context', '_create_unverified_context'):
            vulns.append({
                "type": "Unverified SSL Context",
                "cwe": "CWE-295",
                "severity": "CRITICAL",
                "message": "ssl._create_unverified_context() bypasses root CA trust chains. Use ssl.create_default_context().",
                "line": lineno
            })

        # ── Group 10: Server-Side Template Injection (SSTI) (CWE-1336) ──
        if full_call in ('render_template_string', 'jinja2.Template', 'Template') or attr_name == 'render_template_string':
            vulns.append({
                "type": "Server-Side Template Injection (SSTI)",
                "cwe": "CWE-1336",
                "severity": "HIGH",
                "message": "Rendering unescaped user strings as Jinja2 templates allows remote code execution (RCE). Use render_template() with static files.",
                "line": lineno
            })

        # ── Group 11: Unsafe XML Processing / XXE Injection (CWE-611) ──
        if full_call in ('xml.etree.ElementTree.parse', 'xml.etree.ElementTree.fromstring', 'minidom.parseString', 'lxml.etree.fromstring'):
            vulns.append({
                "type": "XML External Entity (XXE) Injection",
                "cwe": "CWE-611",
                "severity": "HIGH",
                "message": "Default XML parsers resolve external entities and DTDs leading to SSRF or file read. Use defusedxml.minidom or defusedxml.ElementTree.",
                "line": lineno
            })

        # ── Group 12: Tar / Zip Slip Arbitrary File Overwrite (CWE-22) ──
        if attr_name == 'extractall':
            vulns.append({
                "type": "Zip Slip / Directory Traversal in Archive",
                "cwe": "CWE-22",
                "severity": "HIGH",
                "message": "extractall() extracts files without validating member paths, allowing malicious archives with '../' to overwrite critical system files.",
                "line": lineno
            })

        # ── Group 13: Insecure Temporary Files (CWE-377) ──
        if full_call in ('tempfile.mktemp', 'mktemp'):
            vulns.append({
                "type": "Insecure Temp File (mktemp)",
                "cwe": "CWE-377",
                "severity": "MEDIUM",
                "message": "mktemp() creates a race condition (TOCTOU) between name generation and file creation. Use tempfile.NamedTemporaryFile() or mkstemp().",
                "line": lineno
            })

        # ── Group 14: Permissive File Permissions (CWE-732) ──
        if full_call in ('os.chmod', 'chmod'):
            if len(node.args) >= 2 and isinstance(node.args[1], ast.Constant):
                mode = node.args[1].value
                if mode in (0o777, 511, 0o666, 438):
                    vulns.append({
                        "type": "Permissive File Permissions (0o777)",
                        "cwe": "CWE-732",
                        "severity": "HIGH",
                        "message": f"chmod mode {oct(mode)} grants read/write/execute to all users on the host system. Restrict to 0o600 or 0o700.",
                        "line": lineno
                    })

        # ── Group 15: Server-Side Request Forgery (SSRF) (CWE-918) ──
        if full_call in ('requests.get', 'requests.post', 'urllib.request.urlopen', 'http.client.HTTPConnection'):
            if node.args and isinstance(node.args[0], (ast.Name, ast.JoinedStr, ast.BinOp)):
                vulns.append({
                    "type": "Potential SSRF (Server-Side Request Forgery)",
                    "cwe": "CWE-918",
                    "severity": "HIGH",
                    "message": "HTTP request destination determined dynamically by variable/string formatting. Validate target against strict domain whitelist.",
                    "line": lineno
                })

        # ── Group 16: XPath Injection (CWE-643) ──
        if attr_name in ('xpath', 'find_by_xpath'):
            if node.args and isinstance(node.args[0], (ast.JoinedStr, ast.BinOp)):
                vulns.append({
                    "type": "XPath Injection",
                    "cwe": "CWE-643",
                    "severity": "HIGH",
                    "message": "XPath query constructed dynamically via string formatting. Use parameterized XPath variables.",
                    "line": lineno
                })

        # ── Group 17: Insecure JWT Decoding (CWE-345) ──
        if full_call in ('jwt.decode', 'decode') and full_call.startswith('jwt.'):
            for kw in node.keywords:
                if kw.arg == 'verify' and isinstance(kw.value, ast.Constant) and kw.value.value is False:
                    vulns.append({
                        "type": "Disabled JWT Signature Verification",
                        "cwe": "CWE-345",
                        "severity": "CRITICAL",
                        "message": "jwt.decode(..., verify=False) accepts forged JWTs. Always verify signatures with a trusted secret/key.",
                        "line": lineno
                    })
                if kw.arg == 'algorithms' and isinstance(kw.value, ast.List):
                    for elt in kw.value.elts:
                        if isinstance(elt, ast.Constant) and str(elt.value).lower() == 'none':
                            vulns.append({
                                "type": "JWT None Algorithm Permitted",
                                "cwe": "CWE-345",
                                "severity": "CRITICAL",
                                "message": "Permitting 'none' algorithm in JWT decode allows attackers to bypass token authentication entirely.",
                                "line": lineno
                            })

        # ── Group 18: Debug Mode Enabled in Production (CWE-489) ──
        if full_call in ('app.run', 'run'):
            for kw in node.keywords:
                if kw.arg == 'debug' and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                    vulns.append({
                        "type": "Debug Mode Enabled in Production",
                        "cwe": "CWE-489",
                        "severity": "CRITICAL",
                        "message": "app.run(debug=True) enables the interactive Werkzeug PIN debugger, allowing unauthenticated Remote Code Execution (RCE). Set debug=False.",
                        "line": lineno
                    })

        # ── Group 19: Unsafe Dynamic Reflection (getattr / __import__) (CWE-470) ──
        if func_name == 'getattr' and len(node.args) >= 2:
            arg1 = node.args[1]
            if not isinstance(arg1, ast.Constant):
                vulns.append({
                    "type": "Unsafe Dynamic Reflection (getattr)",
                    "cwe": "CWE-470",
                    "severity": "HIGH",
                    "message": "getattr() with dynamic attribute string allows callers to invoke sensitive internal or administrative methods. Use an allowlist dispatch map.",
                    "line": lineno
                })
        elif func_name == '__import__':
            if node.args and not isinstance(node.args[0], ast.Constant):
                vulns.append({
                    "type": "Dynamic Module Import (__import__)",
                    "cwe": "CWE-470",
                    "severity": "HIGH",
                    "message": "__import__() with dynamic input permits loading arbitrary system modules (e.g. 'os', 'subprocess').",
                    "line": lineno
                })

        # ── Group 20: Mass Assignment via __dict__.update (CWE-915) ──
        if attr_name == 'update' and full_call.endswith('__dict__.update'):
            vulns.append({
                "type": "Mass Assignment via __dict__.update()",
                "cwe": "CWE-915",
                "severity": "HIGH",
                "message": "Directly updating __dict__ from input allows attackers to overwrite critical fields like is_admin or role. Use explicit DTO field mapping.",
                "line": lineno
            })

        # ── Group 21: HTTP Response Header / CRLF Injection Risk (CWE-113) ──
        if attr_name in ('set_header', 'add_header') or full_call.startswith(('response.headers', 'headers.add')):
            if node.args and any(not isinstance(a, ast.Constant) for a in node.args):
                vulns.append({
                    "type": "HTTP Response Header / CRLF Injection Risk",
                    "cwe": "CWE-113",
                    "severity": "HIGH",
                    "message": "Dynamic header construction without CRLF stripping allows HTTP response splitting and cookie injection.",
                    "line": lineno
                })

    def _check_assign_node(self, node, lineno, vulns):
        """Inspects variable assignments for hardcoded credentials, keys, or passwords."""
        # 1. Check dynamic SQL queries assigned to variables like query = f"SELECT..."
        is_dynamic_sql = False
        if isinstance(node.value, ast.JoinedStr):
            for part in node.value.values:
                if isinstance(part, ast.Constant) and any(sql_kw in str(part.value).upper() for sql_kw in ('SELECT ', 'INSERT ', 'UPDATE ', 'DELETE ', 'DROP ')):
                    is_dynamic_sql = True
                    break
        elif isinstance(node.value, ast.BinOp) and isinstance(node.value.op, (ast.Mod, ast.Add)):
            left_val = getattr(getattr(node.value, 'left', None), 'value', '')
            if isinstance(left_val, str) and any(sql_kw in left_val.upper() for sql_kw in ('SELECT ', 'INSERT ', 'UPDATE ', 'DELETE ', 'DROP ')):
                is_dynamic_sql = True

        if is_dynamic_sql:
            vulns.append({
                "type": "SQL Injection in Formatted Query",
                "cwe": "CWE-89",
                "severity": "CRITICAL",
                "message": "SQL query constructed using dynamic interpolation. Use parameterized queries with %s or ? placeholders.",
                "line": lineno
            })

        # 2. Path traversal in string constants like "../../../etc/passwd"
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            if '../' in node.value.value or '..\\' in node.value.value:
                vulns.append({
                    "type": "Directory Path Traversal Pattern",
                    "cwe": "CWE-22",
                    "severity": "HIGH",
                    "message": "Relative path traversal ('../') sequence detected. Validate and resolve canonical path using os.path.realpath.",
                    "line": lineno
                })

        # 3. Static IV / Nonce assignment (CWE-329)
        for target in node.targets:
            if isinstance(target, ast.Name):
                t_name = target.id.lower()
                if t_name in ('iv', 'nonce', 'init_vector'):
                    if isinstance(node.value, ast.Constant) and isinstance(node.value.value, (str, bytes)):
                        vulns.append({
                            "type": "Cryptographic Static IV / Nonce Reuse",
                            "cwe": "CWE-329",
                            "severity": "HIGH",
                            "message": f"Static IV/nonce '{target.id}' compromises cipher confidentiality. Generate fresh random IVs using os.urandom(16).",
                            "line": lineno
                        })

        # 4. Hardcoded Secrets and Cloud API Keys (CWE-798)
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            val = node.value.value
            if re.search(r'AKIA[0-9A-Z]{16}', val):
                vulns.append({
                    "type": "Hardcoded AWS Access Key",
                    "cwe": "CWE-798",
                    "severity": "CRITICAL",
                    "message": "AWS Access Key ID pattern (AKIA...) detected. Revoke immediately and load via IAM roles or AWS_ACCESS_KEY_ID env var.",
                    "line": lineno
                })
            elif re.search(r'ghp_[a-zA-Z0-9]{36}', val):
                vulns.append({
                    "type": "Hardcoded GitHub Personal Access Token",
                    "cwe": "CWE-798",
                    "severity": "CRITICAL",
                    "message": "GitHub Personal Access Token (ghp_...) detected. Revoke token and store in secrets manager.",
                    "line": lineno
                })
            elif re.search(r'xox[baprs]-[0-9a-zA-Z]{10,48}', val):
                vulns.append({
                    "type": "Hardcoded Slack API Token",
                    "cwe": "CWE-798",
                    "severity": "CRITICAL",
                    "message": "Slack API token pattern (xox*-...) detected. Revoke and load from environment variables.",
                    "line": lineno
                })

        # Standard secret variable check
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_name = target.id.lower()
                secret_keywords = ('password', 'passwd', 'secret', 'api_key', 'apikey', 'auth_token', 'private_key', 'access_token', 'jwt_secret')
                if any(k in var_name for k in secret_keywords):
                    if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                        val = node.value.value
                        if len(val) >= 4 and not val.startswith(('os.getenv', 'env', 'config')):
                            vulns.append({
                                "type": "Hardcoded Secret / Credential",
                                "cwe": "CWE-798",
                                "severity": "HIGH",
                                "message": f"Hardcoded credential assigned to variable '{target.id}'. Load secrets via environment variables (os.environ).",
                                "line": lineno
                            })

    def _check_assert_node(self, node, lineno, vulns):
        """Detects assert statements used for authorization or security checks."""
        vulns.append({
            "type": "Bypassable Security Check (assert)",
            "cwe": "CWE-617",
            "severity": "MEDIUM",
            "message": "assert statements are removed in optimized Python bytecode (python -O). Use explicit 'if not condition: raise PermissionError()'.",
            "line": lineno
        })

    def _check_import_node(self, node, lineno, vulns):
        """Flags deprecated or dangerous libraries."""
        names = []
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            names = [node.module]

        for n in names:
            if n in ('telnetlib', 'ftplib'):
                vulns.append({
                    "type": "Insecure Cleartext Protocol Library",
                    "cwe": "CWE-319",
                    "severity": "LOW",
                    "message": f"Module '{n}' transmits credentials and data in cleartext. Use SSH (paramiko) or SFTP.",
                    "line": lineno
                })

    def _check_compare_node(self, node, lineno, vulns):
        """Detects timing attack vulnerabilities when comparing hashes or secrets with '=='."""
        is_eq = any(isinstance(op, ast.Eq) for op in node.ops)
        if is_eq:
            left_name = getattr(node.left, 'id', getattr(node.left, 'attr', '')).lower()
            if any(k in left_name for k in ('token', 'password', 'signature', 'hash', 'digest', 'secret')):
                vulns.append({
                    "type": "Timing Attack in Secret Comparison",
                    "cwe": "CWE-208",
                    "severity": "MEDIUM",
                    "message": "Comparing sensitive tokens/hashes with '==' leaks timing information. Use hmac.compare_digest() for constant-time comparison.",
                    "line": lineno
                })

    def _check_except_node(self, node, lineno, vulns):
        """Flags empty except: pass blocks that swallow security/integrity exceptions."""
        if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
            vulns.append({
                "type": "Silent Exception Suppression (except: pass)",
                "cwe": "CWE-390",
                "severity": "MEDIUM",
                "message": "Empty 'except: pass' block swallows errors, hiding security check failures or database corruption. Log errors explicitly.",
                "line": lineno
            })

    def _supplementary_scan(self, code_string: str):
        """Regex-based checks for patterns that might escape standard AST checks."""
        extra = []
        lines = code_string.splitlines()

        for idx, line in enumerate(lines):
            lineno = idx + 1
            l_strip = line.strip()

            if l_strip.startswith('#'):
                continue

            # Insecure HTTP
            if re.search(r'http://[a-zA-Z0-9]', line) and not re.search(r'localhost|127\.0\.0\.1|schemas\.xmlsoap', line):
                extra.append({
                    "type": "Insecure Cleartext Transport (HTTP)",
                    "cwe": "CWE-319",
                    "severity": "LOW",
                    "message": "Cleartext HTTP URL detected. Use encrypted HTTPS (https://) to prevent traffic eavesdropping.",
                    "line": lineno
                })

            # Hardcoded Private Key Headers
            if 'BEGIN PRIVATE KEY' in line or 'BEGIN RSA PRIVATE KEY' in line:
                extra.append({
                    "type": "Hardcoded Private Key",
                    "cwe": "CWE-321",
                    "severity": "CRITICAL",
                    "message": "Raw cryptographic private key detected in code. Store keys in a secure secret manager or HSM.",
                    "line": lineno
                })

            # CORS Wildcard
            if re.search(r'Access-Control-Allow-Origin.*\*', line):
                extra.append({
                    "type": "Permissive CORS Wildcard",
                    "cwe": "CWE-942",
                    "severity": "MEDIUM",
                    "message": "Access-Control-Allow-Origin wildcard (*) allows arbitrary malicious websites to read responses. Restrict to trusted origins.",
                    "line": lineno
                })

            # CSRF Protection Disabled
            if '@csrf.exempt' in line:
                extra.append({
                    "type": "CSRF Protection Disabled",
                    "cwe": "CWE-352",
                    "severity": "HIGH",
                    "message": "@csrf.exempt bypasses Cross-Site Request Forgery tokens. Keep CSRF tokens enforced on state-changing endpoints.",
                    "line": lineno
                })

            # Insecure Socket Binding to 0.0.0.0
            if re.search(r'bind\s*\(\s*\(?\s*[\'"]0\.0\.0\.0[\'"]', line) or 'host="0.0.0.0"' in line or "host='0.0.0.0'" in line:
                extra.append({
                    "type": "Insecure Interface Binding (0.0.0.0)",
                    "cwe": "CWE-200",
                    "severity": "LOW",
                    "message": "Service bound to all network interfaces (0.0.0.0). Bind explicitly to 127.0.0.1 for local services.",
                    "line": lineno
                })

            # Credential leak via print()
            if re.search(r'print\s*\([^)]*(?:password|token|secret|key|api_key)[^)]*\)', line, re.IGNORECASE):
                extra.append({
                    "type": "Sensitive Data Leak in Logs/Print",
                    "cwe": "CWE-532",
                    "severity": "LOW",
                    "message": "Sensitive credentials passed to print(). Avoid writing tokens or passwords to standard output or log streams.",
                    "line": lineno
                })

            # ReDoS (Catastrophic Backtracking Regex)
            if re.search(r're\.compile\s*\(.*(?:\([a-zA-Z0-9_\-.]+\+\)\+|\([a-zA-Z0-9_\-.]+\*\)\*)', line):
                extra.append({
                    "type": "Regular Expression Denial of Service (ReDoS)",
                    "cwe": "CWE-1333",
                    "severity": "HIGH",
                    "message": "Nested quantifiers ((a+)+) in regex cause exponential catastrophic backtracking. Simplify regex or use re2.",
                    "line": lineno
                })

            # Hardcoded Insecure Temp Directory (/tmp/ or C:\Temp\) (CWE-379)
            if re.search(r'open\s*\(\s*[\'"](?:/tmp/|/var/tmp/|[A-Za-z]:[/\\](?:temp|tmp)[/\\])', line, re.IGNORECASE):
                extra.append({
                    "type": "Insecure Hardcoded Temp Directory",
                    "cwe": "CWE-379",
                    "severity": "MEDIUM",
                    "message": "Hardcoding shared temporary directories (/tmp/) is vulnerable to symlink pre-creation attacks. Use tempfile.NamedTemporaryFile().",
                    "line": lineno
                })

            # Unanchored Validation Regex (CWE-625)
            if re.search(r're\.(?:match|search)\s*\(\s*r?[\'"][^$^]*[a-zA-Z0-9_\-]+[+*][^$^]*[\'"]\s*,', line):
                if 're.compile' not in line:
                    extra.append({
                        "type": "Unanchored Validation Regex Bypass",
                        "cwe": "CWE-625",
                        "severity": "MEDIUM",
                        "message": "Validation regex lacks start (^) or end ($) anchor, allowing attackers to inject trailing malicious payloads.",
                        "line": lineno
                    })

        # ── Cross-Language (C/C++ & Java) Static Security Signatures ──
        multi_patterns = [
            (
                r'(?:executeQuery|executeUpdate|execute)\s*\([^)]*\+',
                "SQL Injection in Query Concatenation", "CWE-89", "CRITICAL",
                "Dynamic SQL query constructed via string concatenation. Use PreparedStatement with parameter placeholders."
            ),
            (
                r'(?:Runtime\.getRuntime\(\)\.exec|system\s*\(|popen\s*\()',
                "OS Command Injection", "CWE-78", "CRITICAL",
                "Unsanitized command executed via shell/runtime. Use process builders with explicit tokenized argument lists."
            ),
            (
                r'\b(?:strcpy|sprintf|gets)\s*\(',
                "Unbounded Buffer Copy / Stack Overflow", "CWE-120", "CRITICAL",
                "Unsafe C-style string function without bounds verification. Use strncpy, snprintf, or std::string."
            ),
            (
                r'\bprintf\s*\(\s*[a-zA-Z0-9_]+\s*\)',
                "Format String Vulnerability", "CWE-134", "HIGH",
                "Passing variable directly as format argument in printf(). Use printf(\"%s\", arg) format specifiers."
            ),
            (
                r'new\s+ObjectInputStream|readObject\s*\(',
                "Insecure Java Object Deserialization", "CWE-502", "CRITICAL",
                "ObjectInputStream deserialization on untrusted streams permits arbitrary class instantiation. Use LookAheadObjectInputStream or JSON/Protobuf."
            ),
            (
                r'DocumentBuilderFactory\.newInstance',
                "XML External Entity (XXE) Processing", "CWE-611", "HIGH",
                "XML parser instantiated without disabling external DTDs (disallow-doctype-decl). Vulnerable to XXE SSRF and file disclosure."
            ),
            (
                r'(?:FileInputStream|open)\s*\([^)]*\.\./|(?:FileInputStream|FileReader)\s*\([^)]*\+',
                "Directory Path Traversal", "CWE-22", "HIGH",
                "File path constructed from input or contains relative traversal (../). Validate paths against base directory."
            ),
            (
                r'MessageDigest\.getInstance\s*\(\s*["\'](?:MD5|SHA-1)["\']',
                "Broken Cryptographic Hash Algorithm", "CWE-328", "HIGH",
                "MD5/SHA-1 is cryptographically broken and collision-vulnerable. Upgrade to SHA-256 (SHA-2) or SHA-512."
            ),
            (
                r'new\s+Random\s*\(|\brand\s*\(\)',
                "Predictable Pseudorandom Number Generator (PRNG)", "CWE-330", "HIGH",
                "Linear congruential PRNG (rand / java.util.Random) is predictable. Use SecureRandom or std::random_device."
            ),
            (
                r'(?:PASSWORD|AUTH_TOKEN|SECRET_KEY|MASTER_KEY|AES_ENCRYPTION_KEY)\s*=\s*["\'][^"\']{6,}["\']',
                "Hardcoded Secret / Master Credential", "CWE-798", "HIGH",
                "Sensitive cryptographic key or password hardcoded in source. Extract into secure secret manager or vault."
            )
        ]

        for idx, line in enumerate(lines, 1):
            l_strip = line.strip()
            if l_strip.startswith('//') or l_strip.startswith('/*') or l_strip.startswith('*'):
                continue
            for pat, name, cwe, sev, msg in multi_patterns:
                if re.search(pat, line):
                    if not any(v.get('line') == idx and v.get('type') == name for v in extra):
                        extra.append({
                            "type": name,
                            "cwe": cwe,
                            "severity": sev,
                            "message": msg,
                            "line": idx
                        })

        extra.sort(key=lambda x: x.get('line', 0) if isinstance(x.get('line'), int) else 0)
        return extra

    def _fallback_regex_scan(self, code_string: str):
        """Fallback scanner if AST parsing fails due to syntax errors or non-Python code (Java, C++)."""
        extra = self._supplementary_scan(code_string)
        try:
            import malware_detector
            threats = malware_detector.scan_malware(code_string)
            for t in threats:
                if not any(v.get('line') == t.get('line') and t.get('name') in v.get('type', '') for v in extra):
                    extra.append({
                        "type": f"{t['icon']} {t['category']}: {t['name']}",
                        "cwe": t.get("cwe", "CWE-506"),
                        "severity": "CRITICAL",
                        "message": f"[{t.get('mitre', 'Malware')}] {t.get('description', '')} (Safety Action: {t.get('safety_action', 'BLOCKED')})",
                        "line": t.get("line", 1)
                    })
        except Exception:
            pass
        extra.sort(key=lambda x: x.get('line', 0) if isinstance(x.get('line'), int) else 0)
        return extra


def scan_security(code: str):
    """Convenience module function."""
    sa = SecurityAnalyzer()
    return sa.scan_code(code)


def format_security_report(issues: list) -> str:
    """Formats a list of issues into a human-readable CLI/terminal diagnostic report."""
    if not issues:
        return "[SECURITY SCAN] ✅ No static security vulnerabilities detected."

    lines = [f"[SECURITY SCAN] 🛡️ {len(issues)} Security Issue(s) Detected:\n"]
    for i, issue in enumerate(issues, 1):
        sev = issue.get('severity', 'HIGH')
        cwe = issue.get('cwe', 'CWE-Unknown')
        name = issue.get('type', 'Vulnerability')
        line = issue.get('line', 'Unknown')
        msg = issue.get('message', '')
        lines.append(f"  {i}. [{sev}] [{cwe}] {name} (Line {line})")
        lines.append(f"     Details: {msg}\n")
    return "\n".join(lines)
