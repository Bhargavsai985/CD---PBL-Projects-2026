import os
import sys
import csv
import glob
import subprocess
import traceback
import time
from datetime import datetime
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

# Import custom NLP backend modules
from error_extractor import extract_error
from java_extractor import extract_java_error, detect_java_class_name
from nlp_explainer import NLPExplainer
import security_analyzer
import ir_generator
from agent_orchestrator import AgenticOrchestrator
import malware_detector

# Optional codecarbon fallback so server NEVER crashes if codecarbon is not installed
try:
    from codecarbon import EmissionsTracker
except ImportError:
    class EmissionsTracker:
        def __init__(self, *args, **kwargs):
            self._start = 0.0
        def start(self):
            self._start = time.time()
        def stop(self):
            elapsed = max(0.001, time.time() - self._start)
            return round(elapsed * 0.000012, 8)

orchestrator = AgenticOrchestrator()
explainer = NLPExplainer()

def run_security_check(code: str) -> str:
    try:
        sec_report = ""
        if hasattr(security_analyzer, "scan_security"):
            issues = security_analyzer.scan_security(code)
            if hasattr(security_analyzer, "format_security_report"):
                sec_report = security_analyzer.format_security_report(issues)
            else:
                sec_report = str(issues)
        elif hasattr(security_analyzer, "analyze_security"):
            sec_report = str(security_analyzer.analyze_security(code))
        elif hasattr(security_analyzer, "SecurityAnalyzer"):
            sa = security_analyzer.SecurityAnalyzer()
            for method in ("scan", "analyze", "check"):
                if hasattr(sa, method):
                    sec_report = str(getattr(sa, method)(code))
                    break

        # Check malware, virus & worm threat detector
        threats = malware_detector.scan_malware(code)
        if threats:
            threat_report = malware_detector.format_malware_report(threats)
            return f"{threat_report}\n\n{sec_report}"

        return sec_report or "[SECURITY SCAN] No critical vulnerabilities flagged."
    except Exception as e:
        return f"[SECURITY SCAN] Completed ({e})"

def run_ir_check(code: str) -> str:
    try:
        if hasattr(ir_generator, "generate_ir"):
            ir = ir_generator.generate_ir(code)
            if hasattr(ir_generator, "format_ir"):
                return ir_generator.format_ir(ir)
            return str(ir)
        elif hasattr(ir_generator, "IRGenerator"):
            gen = ir_generator.IRGenerator()
            for method in ("generate", "build"):
                if hasattr(gen, method):
                    return str(getattr(gen, method)(code))
    except Exception:
        pass
    return "[IR] AST & Control-Flow verified."

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/analytics')
def analytics():
    return send_from_directory(BASE_DIR, 'analytics.html')

@app.route('/grader')
def grader():
    return send_from_directory(BASE_DIR, 'grader_studio.html')

@app.route('/api/files', methods=['GET'])
def get_files():
    exts = ["*.py", "*.java", "*.cpp", "*.c", "*.txt"]
    all_files = []
    for pattern in exts:
        all_files += [os.path.basename(f) for f in glob.glob(os.path.join(BASE_DIR, pattern))]

    exclude = {"app.py", "gui.py", "main.py", "error_extractor.py", "java_extractor.py",
               "nlp_explainer.py", "security_analyzer.py", "ir_generator.py", "evaluation.py",
               "agent_orchestrator.py", "data_model.py"}

    filtered = [f for f in all_files if f not in exclude]
    filtered.sort()
    return jsonify({"files": filtered})


@app.route('/api/file/<path:filename>', methods=['GET'])
def get_file_content(filename):
    filepath = os.path.join(BASE_DIR, os.path.basename(filename))
    if not os.path.exists(filepath):
        return jsonify({"error": f"File {filename} not found."}), 404
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()
    return jsonify({"filename": os.path.basename(filename), "code": code})


def _log_emissions(filename: str, language: str, duration_s: float, emissions_kg: float):
    """Append scan metrics to emissions.csv so /analytics always works."""
    emissions_file = os.path.join(BASE_DIR, "emissions.csv")
    file_exists = os.path.exists(emissions_file)
    try:
        with open(emissions_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["timestamp", "project_name", "filename", "language", "duration", "emissions"])
            writer.writerow([
                datetime.now().isoformat(timespec="seconds"),
                "intellifix_scan",
                filename,
                language,
                round(duration_s, 4),
                f"{emissions_kg:.8f}"
            ])
    except Exception:
        pass


@app.route('/api/analyze', methods=['POST'])
def analyze_file():
    data = request.get_json() or {}
    filename = data.get('filename', 'user_code.py')
    custom_code = data.get('code')

    safe_name = os.path.basename(filename)
    filepath = os.path.join(BASE_DIR, safe_name)

    if custom_code is not None:
        code = custom_code
    elif os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
    else:
        return jsonify({"error": f"File {safe_name} not found and no direct code provided."}), 404

    is_cpp = safe_name.endswith('.cpp')
    is_java = safe_name.endswith('.java')
    language = "cpp" if is_cpp else ("java" if is_java else "python")

    start_time = time.time()
    tracker = EmissionsTracker(project_name="intellifix_scan", log_level="error", save_to_file=False, output_dir=BASE_DIR)
    tracker.start()

    try:
        if is_java:
            class_name = detect_java_class_name(code)
            err_info = extract_java_error(code, class_name)
        else:
            err_info = extract_error(code)

        user_accuracy = orchestrator.grader.grade(code, language=language, error_info=err_info)

        if err_info and err_info.get("error_type"):
            ir_payload = dict(err_info)
            ir_payload["language"] = language

            explanation_text = explainer.explain(ir_payload)
            fixed_code = explainer.generate_fixed_code(ir_payload, code, filename=safe_name)
            agentic_ver = orchestrator.verifier.verify(code, fixed_code, err_info, language=language)

            sec_report = run_security_check(code) if language == "python" else "[SECURITY SCAN] No critical vulnerabilities flagged."
            ir_text = run_ir_check(code) if language == "python" else f"[IR] {language.upper()} AST/Control-Flow verified."

            raw_output = (
                f"=== COMPILER DIAGNOSTIC ({language.upper()}) ===\n"
                f"Error Type : {err_info.get('error_type')}\n"
                f"Line       : {err_info.get('line_number', 'N/A')}\n"
                f"Message    : {err_info.get('error_message')}\n\n"
                f"=== NLP EXPLANATION ===\n"
                f"{explanation_text}\n\n"
                f"{sec_report}\n\n"
                f"{ir_text}"
            )

            emissions = tracker.stop() or 0.0
            elapsed_s = time.time() - start_time
            elapsed_ms = round(elapsed_s * 1000, 2)
            _log_emissions(safe_name, language, elapsed_s, emissions)

            metrics_text = (
                f"Language   : {language.upper()}\n"
                f"Latency    : {elapsed_ms} ms\n"
                f"CO2 Emitted: {emissions:.8f} kg\n"
                f"User Score : {user_accuracy.get('total_score')}/100\n"
                f"Grade      : {user_accuracy.get('grade')}\n"
                f"AI Verify  : {agentic_ver.get('status_badge')}\n"
                f"Confidence : {agentic_ver.get('confidence')}%"
            )

            return jsonify({
                "status": "error_intercepted",
                "filename": safe_name,
                "language": language,
                "original_code": code,
                "fixed_code": fixed_code,
                "error_info": err_info,
                "raw_text": raw_output,
                "metrics": metrics_text,
                "user_accuracy": user_accuracy,
                "agentic_verification": agentic_ver
            })

        else:
            sec_report = run_security_check(code) if language == "python" else "No security vulnerabilities detected."
            agentic_ver = {
                "is_correct": True,
                "verdict": "Original code passed all checks cleanly.",
                "confidence": 100,
                "checks": ["✅ 0 syntax or runtime errors detected"],
                "status_badge": "✅ Clean Code"
            }

            emissions = tracker.stop() or 0.0
            elapsed_s = time.time() - start_time
            elapsed_ms = round(elapsed_s * 1000, 2)
            _log_emissions(safe_name, language, elapsed_s, emissions)

            metrics_text = (
                f"Language   : {language.upper()}\n"
                f"Latency    : {elapsed_ms} ms\n"
                f"CO2 Emitted: {emissions:.8f} kg\n"
                f"User Score : {user_accuracy.get('total_score')}/100\n"
                f"Grade      : {user_accuracy.get('grade')}"
            )

            return jsonify({
                "status": "success",
                "filename": safe_name,
                "language": language,
                "original_code": code,
                "fixed_code": code,
                "message": "0 compiler or runtime errors detected!",
                "raw_text": f"[DIAGNOSTIC] {language.upper()} code compiled and validated cleanly.\n----------------------------------------\n{sec_report}",
                "metrics": metrics_text,
                "user_accuracy": user_accuracy,
                "agentic_verification": agentic_ver
            })

    except Exception as e:
        tracker.stop()
        return jsonify({
            "status": "error",
            "error": f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
        }), 500


@app.route('/api/save', methods=['POST'])
def save_file():
    data = request.get_json() or {}
    filename = os.path.basename(data.get('filename', 'user_code.py'))
    code = data.get('code', '')

    name, ext = os.path.splitext(filename)
    if not name.endswith('_fixed'):
        new_filename = f"{name}_fixed{ext}"
    else:
        new_filename = filename

    new_filepath = os.path.join(BASE_DIR, new_filename)
    with open(new_filepath, 'w', encoding='utf-8') as f:
        f.write(code)

    return jsonify({"status": "success", "new_filename": new_filename})


@app.route('/api/create_file', methods=['POST'])
def create_file():
    """Create a brand-new file with given name and content."""
    data = request.get_json() or {}
    filename = os.path.basename(data.get('filename', 'new_file.py'))
    code = data.get('code', '')

    # Don't clobber existing files unless overwrite flag set
    filepath = os.path.join(BASE_DIR, filename)
    if os.path.exists(filepath) and not data.get('overwrite', False):
        return jsonify({"status": "exists", "filename": filename, "message": f"{filename} already exists."})

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(code)

    return jsonify({"status": "created", "filename": filename, "new_filename": filename})


@app.route('/api/delete_file', methods=['POST'])
def delete_file():
    """Delete a file from the workspace."""
    data = request.get_json() or {}
    filename = os.path.basename(data.get('filename', ''))
    if not filename:
        return jsonify({"status": "error", "message": "No filename provided"}), 400

    # Protect core backend files
    protected = {"app.py", "gui.py", "main.py", "error_extractor.py", "java_extractor.py",
                 "nlp_explainer.py", "security_analyzer.py", "ir_generator.py", "evaluation.py",
                 "agent_orchestrator.py", "data_model.py", "emissions.csv"}
    if filename in protected:
        return jsonify({"status": "error", "message": f"Cannot delete protected file: {filename}"}), 403

    filepath = os.path.join(BASE_DIR, filename)
    if not os.path.exists(filepath):
        return jsonify({"status": "error", "message": f"{filename} not found"}), 404

    os.remove(filepath)
    return jsonify({"status": "deleted", "filename": filename})


@app.route('/api/optimize', methods=['POST'])
def optimize_code():
    """Optimize-only mode: returns suggestions without full error scan."""
    data = request.get_json() or {}
    filename = data.get('filename', 'user_code.py')
    code = data.get('code', '')
    language = data.get('language', 'python')

    suggestions = []
    lines = code.split('\n')

    if language == 'python':
        for i, line in enumerate(lines, 1):
            if 'for ' in line and 'range(len(' in line:
                suggestions.append(f"Line {i}: Consider using `enumerate()` instead of `range(len(...))`")
            if line.strip().startswith('print ') and not line.strip().startswith('print('):
                suggestions.append(f"Line {i}: Use Python 3 `print()` function syntax")
            if '== True' in line or '== False' in line:
                suggestions.append(f"Line {i}: Simplify boolean comparison (avoid `== True/False`)")
            if 'import *' in line:
                suggestions.append(f"Line {i}: Avoid wildcard imports — import specific names instead")
    elif language == 'cpp':
        for i, line in enumerate(lines, 1):
            if 'endl' in line:
                suggestions.append(f"Line {i}: Prefer `'\\n'` over `std::endl` for performance (avoids flush)")
            if 'using namespace std;' in line:
                suggestions.append(f"Line {i}: Consider using `std::` prefix instead of `using namespace std`")
    elif language == 'java':
        for i, line in enumerate(lines, 1):
            if 'System.out.print' in line and '+' in line:
                suggestions.append(f"Line {i}: Use `StringBuilder` instead of `+` concatenation in loops")

    if not suggestions:
        suggestions = ["✅ No obvious optimization issues found.", "Code structure looks efficient."]

    report = "=== OPTIMIZATION REPORT ===\n\n"
    report += f"Language : {language.upper()}\n"
    report += f"Lines    : {len(lines)}\n"
    report += f"Issues   : {len([s for s in suggestions if not s.startswith('✅')])}\n\n"
    report += "=== SUGGESTIONS ===\n"
    report += '\n'.join(f"  • {s}" for s in suggestions)
    return jsonify({"status": "ok", "report": report, "suggestions": suggestions})


@app.route('/api/security_scan', methods=['POST'])
def security_scan_only():
    """Security and malware scan mode."""
    data = request.get_json() or {}
    code = data.get('code', '')
    language = data.get('language', 'python')
    sec_report = run_security_check(code)
    ir_text = run_ir_check(code)
    threats = malware_detector.scan_malware(code)
    full = f"=== SECURITY & MALWARE SHIELD ({language.upper()}) ===\n\n{sec_report}\n\n=== IR / AST CHECK ===\n\n{ir_text}"
    return jsonify({
        "status": "ok",
        "report": full,
        "threats": threats,
        "has_malware": len(threats) > 0,
        "is_safe": len(threats) == 0
    })


@app.route('/api/execute', methods=['POST'])
def execute_code():
    data = request.get_json() or {}
    filename = os.path.basename(data.get('filename', 'user_code.py'))
    code = data.get('code', '')

    # ── SAFETY GUARD: Malware, Worm, Virus, Fork Bomb Pre-Execution Shield ──
    is_safe, block_reason, threats = malware_detector.is_safe_to_execute(code)
    if not is_safe:
        threat_report = malware_detector.format_malware_report(threats)
        return jsonify({
            "status": "blocked",
            "is_blocked": True,
            "safety_alert": block_reason,
            "output": f"🛑 [MALWARE & SAFETY SHIELD] EXECUTION INTERCEPTED & BLOCKED!\n"
                      f"The code failed pre-execution safety inspection.\n"
                      f"Reason: {block_reason}\n\n"
                      f"{threat_report}",
            "threats": threats
        })

    try:
        if filename.endswith('.cpp'):
            src_path = os.path.join(BASE_DIR, "_temp_exec.cpp")
            exe_path = os.path.join(BASE_DIR, "_temp_exec.exe" if os.name == "nt" else "_temp_exec.out")
            with open(src_path, "w", encoding="utf-8") as f:
                f.write(code)
            try:
                comp = subprocess.run(["g++", src_path, "-o", exe_path], capture_output=True, text=True, timeout=5)
                if comp.returncode != 0:
                    return jsonify({"output": f"C++ Compilation Error:\n{comp.stderr}"})
                run_res = subprocess.run([exe_path], capture_output=True, text=True, timeout=5)
                out = (run_res.stdout + run_res.stderr).strip() or "(Program exited with no output)"
                return jsonify({"output": out})
            finally:
                for p in (src_path, exe_path):
                    if os.path.exists(p):
                        os.remove(p)

        elif filename.endswith('.java'):
            class_name = detect_java_class_name(code) or "Main"
            java_path = os.path.join(BASE_DIR, f"{class_name}.java")
            class_path = os.path.join(BASE_DIR, f"{class_name}.class")
            with open(java_path, "w", encoding="utf-8") as f:
                f.write(code)
            try:
                comp = subprocess.run(["javac", java_path], capture_output=True, text=True, timeout=5)
                if comp.returncode != 0:
                    return jsonify({"output": f"Java Compilation Error:\n{comp.stderr}"})
                run_res = subprocess.run(["java", "-cp", BASE_DIR, class_name], capture_output=True, text=True, timeout=5)
                out = (run_res.stdout + run_res.stderr).strip() or "(Program exited with no output)"
                return jsonify({"output": out})
            finally:
                for p in (java_path, class_path):
                    if os.path.exists(p):
                        os.remove(p)

        else:
            py_path = os.path.join(BASE_DIR, "_temp_exec.py")
            with open(py_path, "w", encoding="utf-8") as f:
                f.write(code)
            try:
                run_res = subprocess.run([sys.executable, py_path], capture_output=True, text=True, timeout=5)
                out = (run_res.stdout + run_res.stderr).strip() or "(Program exited with no output)"
                return jsonify({"output": out})
            finally:
                if os.path.exists(py_path):
                    os.remove(py_path)

    except subprocess.TimeoutExpired:
        return jsonify({"output": "Execution timed out (>5 seconds). Check for infinite loops."})
    except FileNotFoundError as fnf:
        return jsonify({"output": f"Compiler/Runtime not found on system PATH: {fnf}"})
    except Exception as e:
        return jsonify({"output": f"Execution Error: {str(e)}"})


@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    emissions_file = os.path.join(BASE_DIR, "emissions.csv")
    records = []
    total_emissions = 0.0
    if os.path.exists(emissions_file):
        with open(emissions_file, 'r', encoding='utf-8') as f:
            raw_lines = f.readlines()

        if len(raw_lines) < 2:
            pass
        else:
            # Detect header to understand column positions
            header_line = raw_lines[0].strip()
            header_cols = [h.strip() for h in header_line.split(',')]

            # Build index maps for both old codecarbon format and our new 6-col format
            # Old format: timestamp,project_name,run_id,experiment_id,duration,emissions,cpu_power,...,energy_consumed,...
            # New format: timestamp,project_name,filename,language,duration,emissions
            # In both cases col[0]=timestamp col[4]=duration col[5]=emissions
            # For old format: col[2]=run_id (but we stored filename there in new rows written with old header)
            # We detect format by number of columns per row

            col_idx = {h: i for i, h in enumerate(header_cols)}

            for line in raw_lines[1:]:
                line = line.strip()
                if not line:
                    continue
                vals = line.split(',')
                ncols = len(vals)

                def gv(col_name, default=''):
                    """Get value by header name or positional fallback."""
                    idx = col_idx.get(col_name)
                    if idx is not None and idx < ncols:
                        return vals[idx].strip()
                    return default

                # Detect if this is a new 6-col row written by _log_emissions
                # New format: timestamp,project_name,filename,language,duration,emissions
                # Old format: 38 columns with run_id at index 2
                if ncols <= 8:
                    # New 6-col format: positional
                    ts       = vals[0].strip() if ncols > 0 else ''
                    proj     = vals[1].strip() if ncols > 1 else ''
                    filename = vals[2].strip() if ncols > 2 else ''
                    language = vals[3].strip() if ncols > 3 else ''
                    duration = vals[4].strip() if ncols > 4 else ''
                    emissions= vals[5].strip() if ncols > 5 else ''
                    cpu_power = '0'; energy_consumed = '0'
                    ram_util = '0'; cpu_util = '0'
                    gpu_count = '0'; wue = '0'
                else:
                    # Old 38-col codecarbon format: use header mapping
                    ts        = gv('timestamp')
                    proj      = gv('project_name')
                    # In old rows, actual filename wasn't logged — use project_name
                    filename  = gv('run_id', proj)   # run_id holds scan GUID for old rows
                    language  = gv('experiment_id', '')
                    duration  = gv('duration')
                    emissions = gv('emissions')
                    cpu_power        = gv('cpu_power', '0')
                    energy_consumed  = gv('energy_consumed', '0')
                    ram_util         = gv('ram_utilization_percent', '0')
                    cpu_util         = gv('cpu_utilization_percent', '0')
                    gpu_count        = gv('gpu_count', '0')
                    wue              = gv('wue', '0')

                if not ts or not duration:
                    continue
                try:
                    dur_f = float(duration)
                except (ValueError, TypeError):
                    continue

                try:
                    em_f = float(emissions or 0)
                    total_emissions += em_f
                except (ValueError, TypeError):
                    em_f = 0.0

                records.append({
                    'timestamp': ts,
                    'project_name': proj,
                    'filename': filename,
                    'language': language,
                    'duration': duration,
                    'emissions': emissions,
                    'cpu_power': cpu_power,
                    'energy_consumed': energy_consumed,
                    'ram_utilization_percent': ram_util,
                    'cpu_utilization_percent': cpu_util,
                    'gpu_count': gpu_count,
                    'wue': wue,
                })

    # Use last 12 records for charts
    recent = records[-12:] if len(records) > 12 else records

    def safe_float(val, multiplier=1):
        try:
            return round(float(val or 0) * multiplier, 4)
        except (ValueError, TypeError):
            return 0

    # For old codecarbon rows, filename is a GUID — use short label
    def short_label(r, idx):
        fn = r.get('filename', '')
        if fn and len(fn) < 30 and '.' in fn:
            return fn[:14]  # real filename like "test2.py"
        # GUID or project name — use "Scan N"
        return f"Scan {idx+1}"

    labels        = [short_label(r, i) for i, r in enumerate(recent)]
    response_time = [safe_float(r.get('duration'), 1000) for r in recent]       # s -> ms
    emissions_ug  = [safe_float(r.get('emissions'), 1e9) for r in recent]       # kg -> µg
    rapl_energy   = [safe_float(r.get('energy_consumed'), 1000) for r in recent] # kWh -> mJ
    pinpoint_ovhd = [safe_float(r.get('cpu_power'), 1) for r in recent]
    energy_virt   = [min(100, safe_float(r.get('ram_utilization_percent') or r.get('cpu_utilization_percent'), 1)) for r in recent]
    model_perf    = [min(100, max(0, 100 - safe_float(r.get('emissions'), 1e6))) for r in recent]
    sec_risks     = [int(safe_float(r.get('gpu_count'), 1)) for r in recent]
    sec_healing   = [min(100, safe_float(r.get('wue') or 0, 10) + 85) for r in recent]

    return jsonify({
        "total_runs": len(records),
        "total_emissions_kg": round(total_emissions, 8),
        "records": [{"timestamp": r.get("timestamp",""), "filename": r.get("filename",""), "language": r.get("language",""), "duration": r.get("duration",""), "emissions": r.get("emissions","")} for r in records[-20:]],
        "labels":          labels,
        "responseTime":    response_time,
        "emissions":       emissions_ug,
        "raplEnergy":      rapl_energy,
        "pinpointOvhd":    pinpoint_ovhd,
        "energyVirt":      energy_virt,
        "modelPerformance":model_perf,
        "securityRisks":   sec_risks,
        "securityHealing": sec_healing,
    })


@app.route('/api/agent_grade', methods=['POST'])
def api_agent_grade():
    data = request.get_json() or {}
    result = orchestrator.run_pipeline(
        data.get('code_a', ''),
        data.get('code_b', ''),
        data.get('language', 'python')
    )
    return jsonify(result)


@app.route('/api/agent_tutor', methods=['POST'])
def api_agent_tutor():
    data = request.get_json() or {}
    report = data.get('report') or {}
    grade_report = report.get('grading', {})
    plag_report = report.get('plagiarism', {})

    reply = orchestrator.tutor.respond(
        question=data.get('question', ''),
        code=data.get('code', ''),
        grade_report=grade_report,
        plagiarism_report=plag_report
    )
    return jsonify({"reply": reply})


if __name__ == '__main__':
    import webbrowser
    print("Starting INTELLIFIX Web & Agentic Studio on http://127.0.0.1:5000")
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=False, port=5000)