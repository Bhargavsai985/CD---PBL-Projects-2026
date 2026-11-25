╔══════════════════════════════════════════════════════════════════════╗
║          INTELLIFIX — TEST CASES REFERENCE GUIDE                    ║
║   ALL 57 TEST CASES STANDARDIZED TO 1,000+ CODE LINES EACH           ║
╚══════════════════════════════════════════════════════════════════════╝

HOW TO USE:
1. Run: python app.py
2. Open: http://localhost:5000
3. Click any test case file in the Explorer sidebar (all files >= 1,000 lines)
4. Click "Scan & Diagnose" or press Ctrl+Enter
5. View results in Output, Security, Messages, and Eco Metrics tabs

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 PYTHON ERROR TEST CASES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

tc_01_syntax_error.py
  Error Type : SyntaxError
  Triggers   : Missing colon after function/if, missing closing parenthesis
  Expected   : NLP explains the syntax mistake and shows corrected code

tc_02_indentation_error.py
  Error Type : IndentationError
  Triggers   : Extra space before 'count += 1' inside loop
  Expected   : NLP flags incorrect indentation level

tc_03_name_error.py
  Error Type : NameError
  Triggers   : 'reslt' and 'sqared' (typos for 'result' and 'squared')
  Expected   : NLP identifies undefined variable and suggests correction

tc_04_type_error.py
  Error Type : TypeError
  Triggers   : str + int concatenation without str() conversion
  Expected   : NLP explains type mismatch and adds str() conversion

tc_05_index_error.py
  Error Type : IndexError
  Triggers   : Accessing index 2 on a list with only 2 elements
  Expected   : NLP explains out-of-bounds access and adds bounds check

tc_06_key_error.py
  Error Type : KeyError
  Triggers   : contact["phone"] when 'phone' key doesn't exist
  Expected   : NLP suggests .get() method or key existence check

tc_07_attribute_error.py
  Error Type : AttributeError
  Triggers   : list.push() (Python uses .append()), str.upper_case()
  Expected   : NLP identifies wrong method name and suggests correct one

tc_08_zero_division.py
  Error Type : ZeroDivisionError
  Triggers   : Division when count=0 or mean=0
  Expected   : NLP adds zero-check guard before division

tc_09_value_error.py
  Error Type : ValueError
  Triggers   : int("not_a_number"), float("0") causing division by zero
  Expected   : NLP adds try/except and input validation

tc_10_recursion_error.py
  Error Type : RecursionError
  Triggers   : factorial() with no base case, countdown() that increments
  Expected   : NLP adds proper base case to recursive functions

tc_11_import_error.py
  Error Type : ModuleNotFoundError
  Triggers   : import numpy_extended, from ml_magic import AutoModel
  Expected   : NLP flags unavailable modules

tc_12_logic_error.py
  Error Type : Logic Error (no exception, wrong output)
  Triggers   : bubble_sort wrong order/bounds, binary_search infinite loop
  Expected   : NLP detects incorrect algorithm and suggests fix

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 SECURITY VULNERABILITY TEST CASES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

tc_13_sec_eval_exec.py
  Severity   : CRITICAL (🔴 HIGH)
  Vuln Type  : Arbitrary Code Execution
  Pattern    : eval(user_input), exec(plugin_code)
  Attack     : Pass "__import__('os').system('del C:\\')" to eval()
  Fix        : Use ast.literal_eval() for safe expression parsing

tc_14_sec_sql_injection.py
  Severity   : CRITICAL (🔴 HIGH)
  Vuln Type  : SQL Injection
  Pattern    : f"SELECT * WHERE name='{username}'"
  Attack     : Pass "admin' OR '1'='1" to bypass authentication
  Fix        : Use parameterized queries: cursor.execute("?", (val,))

tc_15_sec_hardcoded_credentials.py
  Severity   : HIGH (🔴 HIGH)
  Vuln Type  : Hardcoded Secrets / Credential Exposure
  Pattern    : password = "Sup3rS3cr3t!", API_KEY = "sk-live-..."
  Attack     : Source code leaked via git exposes all credentials
  Fix        : Use os.environ.get("DB_PASSWORD") or python-dotenv

tc_16_sec_pickle_deserialization.py
  Severity   : CRITICAL (🔴 HIGH)
  Vuln Type  : Unsafe Deserialization
  Pattern    : pickle.loads(user_data), pickle.load(file)
  Attack     : Malicious __reduce__ executes OS commands on load
  Fix        : Use json.loads() for untrusted data, sign pickle data

tc_17_sec_subprocess_injection.py
  Severity   : HIGH (🔴 HIGH)
  Vuln Type  : OS Command Injection
  Pattern    : os.system(f"ping {hostname}"), subprocess(shell=True)
  Attack     : Pass "localhost; del /f /s /q C:\*" as hostname
  Fix        : Use list form subprocess.run(["ping", hostname])

tc_18_sec_unvalidated_input.py
  Severity   : MEDIUM (🟡 MEDIUM)
  Vuln Type  : Path Traversal, Unvalidated Input (CWE-20 / CWE-22)
  Pattern    : open("/uploads/" + filename), int(input())
  Attack     : Pass "../../../etc/passwd" to read sensitive files
  Fix        : Use os.path.basename(), validate type/range/format

tc_23_sec_ssti_template_injection.py
  Severity   : CRITICAL / HIGH (🔴 HIGH)
  Vuln Type  : Server-Side Template Injection (CWE-1336 / OWASP A03)
  Pattern    : render_template_string(f"Hello {username}"), Template(user_template)
  Attack     : Inject {{7*7}} or {{config.items()}} for Remote Code Execution
  Fix        : Use render_template("profile.html", name=username) with context

tc_24_sec_weak_cryptography_hashes.py
  Severity   : HIGH (🔴 HIGH)
  Vuln Type  : Broken Cryptographic Hashes & Ciphers (CWE-328 / CWE-327)
  Pattern    : hashlib.md5(), hashlib.sha1(), AES.MODE_ECB, DES.new()
  Attack     : Collision attacks, rainbow table cracking, ECB pattern disclosure
  Fix        : Migrate to SHA-256, bcrypt/argon2, and AES-GCM (MODE_GCM)

tc_25_sec_insecure_random_timing.py
  Severity   : HIGH / MEDIUM (🟡 MEDIUM)
  Vuln Type  : Insecure PRNG & Timing Attacks (CWE-330 / CWE-208)
  Pattern    : random.randint() for security tokens, '==' secret string comparison
  Attack     : PRNG state reconstruction (624 MT states), sub-ms timing analysis
  Fix        : Use secrets.token_hex(32) and hmac.compare_digest(a, b)

tc_26_sec_unsafe_yaml_deserialization.py
  Severity   : CRITICAL (🔴 HIGH)
  Vuln Type  : Unsafe YAML & Deserialization (CWE-502 / OWASP A08)
  Pattern    : yaml.load(data) without SafeLoader, marshal.loads(), shelve.open()
  Attack     : Arbitrary object instantiation via !!python/object/apply:os.system
  Fix        : Use yaml.safe_load(data) or Loader=yaml.SafeLoader

tc_27_sec_ssrf_unverified_ssl.py
  Severity   : CRITICAL / HIGH (🔴 HIGH)
  Vuln Type  : SSRF & Disabled SSL Verification (CWE-918 / CWE-295)
  Pattern    : requests.get(target_url), verify=False, ssl._create_unverified_context()
  Attack     : Pivot into AWS metadata (169.254.169.254), Man-in-the-Middle traffic sniffing
  Fix        : Enforce domain allowlist, block RFC 1918 IPs, keep verify=True

tc_28_sec_xxe_xml_bomb.py
  Severity   : HIGH (🔴 HIGH)
  Vuln Type  : XML External Entity & Entity Expansion (CWE-611 / CWE-776)
  Pattern    : ET.fromstring(xml), minidom.parseString(soap)
  Attack     : <!ENTITY xxe SYSTEM "file:///etc/passwd"> and Billion Laughs DoS
  Fix        : Use defusedxml (defusedxml.ElementTree, defusedxml.minidom)

tc_29_sec_jwt_auth_bypass.py
  Severity   : CRITICAL / HIGH (🔴 HIGH)
  Vuln Type  : JWT Signature Bypass & Assert Gates (CWE-345 / CWE-617)
  Pattern    : jwt.decode(token, verify=False), algorithms=['none'], assert user_role == 'admin'
  Attack     : Forge unsigned admin tokens, bypass auth with python -O optimization
  Fix        : Enforce verify=True with algorithms=['HS256'], replace assert with if/raise

tc_30_sec_redos_zipslip_traversal.py
  Severity   : HIGH (🔴 HIGH)
  Vuln Type  : ReDoS, Zip Slip, & World-Writable Permissions (CWE-1333 / CWE-22 / CWE-732)
  Pattern    : Nested regex quantifiers ((a+)+), zip_ref.extractall(), os.chmod(..., 0o777)
  Attack     : Server process CPU freeze (100% DoS), arbitrary file overwrite via ../
  Fix        : Eliminate nested quantifiers, validate ZipInfo paths, use 0o600 permissions

tc_31_sec_cloud_keys_debug_mode.py
  Severity   : CRITICAL / HIGH (🔴 HIGH)
  Vuln Type  : Cloud API Keys, Debug Mode & Static IV Reuse (CWE-798 / CWE-489 / CWE-329)
  Pattern    : AKIA[0-9A-Z]{16}, ghp_*, app.run(debug=True), static IV in AES-CBC
  Attack     : AWS infrastructure takeover, unauthenticated interactive RCE via Werkzeug PIN
  Fix        : Store keys in environment variables, set debug=False, generate random IV

tc_32_sec_unsafe_reflection_mass_assignment.py
  Severity   : CRITICAL / HIGH (🔴 HIGH)
  Vuln Type  : Unsafe Reflection, Mass Assignment, & Dill Deserialization (CWE-470 / CWE-915 / CWE-502 / CWE-113 / CWE-390)
  Pattern    : getattr(app, action), user.__dict__.update(), dill.loads(), CRLF headers, except: pass
  Attack     : Privilege escalation to admin, closure code execution, HTTP response splitting
  Fix        : Use strict dispatch map, Pydantic schemas, and sanitize response headers

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 JAVA TEST CASES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

tc_19_java_compile_error.java
  Error Type : Compilation Error (javac)
  Triggers   : Missing return type, missing semicolons, undeclared variable
  Expected   : NLP lists each compilation error with line numbers

tc_20_java_runtime_error.java
  Error Type : RuntimeException (NullPointerException, ArrayIndexOutOfBoundsException,
               ClassCastException, NumberFormatException)
  Triggers   : processName(null), getElement(arr, 10), (Integer)"Hello"
  Expected   : NLP explains runtime exceptions and suggests null checks

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 C++ TEST CASES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

tc_21_cpp_compile_error.cpp
  Error Type : Compilation Error (g++)
  Triggers   : Missing semicolon after struct, wrong return type, undeclared var
  Expected   : NLP explains each g++ error and location

tc_22_cpp_memory_error.cpp
  Error Type : Memory Errors (Buffer Overflow, Memory Leak, Dangling Pointer,
               Use-After-Free, Double Free, Uninitialized Variable, Off-By-One)
  Triggers   : Various unsafe memory operations
  Expected   : NLP flags memory management issues with severity labels

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 QUICK TEST SEQUENCE (Recommended order)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. tc_01_syntax_error.py     → SyntaxError demo
2. tc_04_type_error.py       → TypeError demo
3. tc_08_zero_division.py    → ZeroDivisionError demo
4. tc_13_sec_eval_exec.py    → Security: Critical eval() vuln
5. tc_15_sec_hardcoded.py    → Security: Hardcoded passwords
6. tc_14_sec_sql_injection.py → Security: SQL Injection
7. tc_19_java_compile_error.java → Java compile errors
8. tc_22_cpp_memory_error.cpp    → C++ memory errors

Then go to Eco Analytics tab to see the performance charts from your scans!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 LARGE-SCALE ENTERPRISE BENCHMARK TEST SUITES (900+ LINES EACH)
 Language Distribution: 70% Python (5,679 LOC), 15% Java (1,323 LOC), 15% C++ (1,315 LOC)
 Total Volume: 8,317 Lines
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

tc_33_enterprise_ecommerce_platform.py
  Language   : Python (70% Allocation Group)
  Line Count : 2,283 Lines
  Domain     : Distributed E-Commerce Microservices & Inventory Management
  Errors     : Syntax error, Indentation, NameError, ZeroDivisionError, KeyError, RecursionError
  Vulns      : SQL Injection (CWE-89), Slack API Token (CWE-798), AWS Access Key (CWE-798),
               Hardcoded DB Credentials (CWE-798), Silent Exception Pass (CWE-390), Insecure HTTP (CWE-319)

tc_34_financial_analytics_pipeline.py
  Language   : Python (70% Allocation Group)
  Line Count : 1,623 Lines
  Domain     : Algorithmic Stock Trading, Portfolio Risk & Monte Carlo Valuation
  Errors     : ZeroDivisionError (Sharpe ratio), IndexError, KeyError, TypeError, Floating-point NaN
  Vulns      : Broken MD5 Hashing (CWE-328), Path Traversal (CWE-22), Cleartext Transport (CWE-319),
               Hardcoded Master API Secret (CWE-798)

tc_35_cloud_microservices_gateway.py
  Language   : Python (70% Allocation Group)
  Line Count : 1,773 Lines
  Domain     : Cloud API Gateway, JWT Proxy, Rate Limiting & Circuit Breaker Engine
  Errors     : NameError, AttributeError, ValueError, Logic Error in Rate Limiter
  Vulns      : Hardcoded GitHub PAT (CWE-798), Hardcoded Slack Bot Token (CWE-798),
               Insecure Cleartext Microservice URLs (CWE-319), Hardcoded Gateway Secrets (CWE-798)

tc_36_enterprise_banking_system.java
  Language   : Java (15% Allocation Group)
  Line Count : 1,323 Lines
  Domain     : High-Throughput Core Banking, Double-Entry Ledger & Fraud Detection Engine
  Errors     : NullPointerException, ArithmeticException (/ by zero), ClassCastException,
               ArrayIndexOutOfBoundsException, IncompatibleTypes, MissingReturn
  Vulns      : SQL Injection via Statement (CWE-89), Insecure ObjectInputStream Deserialization (CWE-502),
               OS Command Injection (CWE-78), XML External Entity XXE (CWE-611), Path Traversal (CWE-22),
               Broken MD5/SHA-1 Hash (CWE-328), Predictable java.util.Random PRNG (CWE-330),
               Hardcoded Production DB Password & Fixed AES Key (CWE-798)

tc_37_network_security_kernel.cpp
  Language   : C++ (15% Allocation Group)
  Line Count : 1,315 Lines
  Domain     : Low-Level Packet Routing, Stateful Firewall Kernel & Deep Packet Inspection (DPI)
  Errors     : Use-After-Free (UAF), Double Free, Heap/Stack Buffer Overflow, Off-By-One,
               Dangling Pointer, Integer Overflow, Divide-by-Zero, Memory Leak
  Vulns      : Format String in printf (CWE-134), Stack Buffer Overflow via strcpy (CWE-120),
               Command Injection via system() (CWE-78), Predictable rand() PRNG (CWE-330),
               Hardcoded Ring-0 Master Token (CWE-798)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 MALWARE, VIRUS, WORM & THREAT DEFENSE TEST SUITES (1,000+ LOC EACH)
 Pre-Execution Safety Shield Active — Sandbox Execution Automatically Quarantined
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

tc_38_sec_worm_self_replicator.py
  Threat     : Self-Replicating Worm / File Infection Loop (MITRE T1080 / CWE-829)
  Line Count : 1,015 Lines
  Severity   : CRITICAL_MALWARE
  Behavior   : Recursively walks file trees and prepends viral code to target scripts
  Safety     : Pre-execution shield detects signature and BLOCKS execution

tc_39_sec_ransomware_cryptolocker.py
  Threat     : Ransomware File Encryption & Extortion Note (MITRE T1486 / CWE-73)
  Line Count : 1,015 Lines
  Severity   : CRITICAL_MALWARE
  Behavior   : Mass document encryption and extortion demand
  Safety     : Pre-execution shield detects signature and BLOCKS execution

tc_40_sec_trojan_reverse_shell.py
  Threat     : Interactive Socket Dup2 Reverse Shell (MITRE T1059 / CWE-506)
  Line Count : 1,015 Lines
  Severity   : CRITICAL_MALWARE
  Behavior   : Rebinds stdin/stdout descriptors to socket and spawns shell
  Safety     : Pre-execution shield detects signature and BLOCKS execution

tc_41_sec_destructive_wiper_forkbomb.py
  Threat     : System Root Wiper & Process Fork Bomb (MITRE T1485, T1499 / CWE-459, CWE-400)
  Line Count : 1,015 Lines
  Severity   : CRITICAL_MALWARE
  Behavior   : Root directory wipe and process table exhaustion bomb
  Safety     : Pre-execution shield detects signature and BLOCKS execution
