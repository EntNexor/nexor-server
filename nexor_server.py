from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.request
import urllib.error

API_KEY = "AIzaSyDMh8N08gKPadug_hx0Na8d3-lxTDDuguI"
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

class ProxyHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        if self.path == '/chat':
            try:
                content_length = int(self.headers['Content-Length'])
                body = self.rfile.read(content_length)
                data = json.loads(body)

                # Enviar a Gemini con la key oculta
                req = urllib.request.Request(
                    URL + "?key=" + API_KEY,
                    data=json.dumps(data).encode('utf-8'),
                    headers={'Content-Type': 'application/json'},
                    method='POST'
                )

                with urllib.request.urlopen(req) as response:
                    resp_body = response.read()

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(resp_body)

            except urllib.error.HTTPError as e:
                self.send_response(e.code)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(e.read())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # Silenciar logs

print("🚀 Servidor Nexor iniciado en http://localhost:8000")
print("📡 Proxy a Gemini activo - API Key protegida")
print("⛔ No cierres esta ventana mientras uses el chat")
print("")

server = HTTPServer(('localhost', 8000), ProxyHandler)
server.serve_forever()