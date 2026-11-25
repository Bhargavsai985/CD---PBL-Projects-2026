import logging
from app import app, PORT

# Suppress verbose Flask traffic logs to keep terminal clean
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

print("\n" + "="*60)
print("[WEB STUDIO INITIATED]")
print("Click the link below (CTRL+Click) to open the interactive website for deeper modifications!")
print(f"  http://127.0.0.1:{PORT}")
print("="*60 + "\n")

if __name__ == '__main__':
    try:
        app.run(host='127.0.0.1', port=PORT, debug=False, use_reloader=False)
    except Exception as e:
        print(f"Failed to start Website Server: {e}")
