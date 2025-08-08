from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import time
import requests

PORT = 3389  # Açmak istediğiniz port numarası
CHECK_URL = "https://improved-potato-q79r79g6x54q29pg5-3389.app.github.dev/"  # Kontrol edilecek site
CHECK_INTERVAL = 600  # 10 dakika (saniye cinsinden)

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')  # DÜZELTİLDİ: sende_header -> send_header
        self.end_headers()
        self.wfile.write(b"Server is running! Port: " + str(PORT).encode())

def run_server():
    server = HTTPServer(('', PORT), SimpleHandler)
    print(f"Server started on port {PORT}")
    server.serve_forever()

def check_website():
    while True:
        try:
            response = requests.get(CHECK_URL)
            status = "UP" if response.status_code == 200 else "DOWN"
            print(f"[{time.ctime()}] Website status: {status} | Code: {response.status_code}")
        except Exception as e:
            print(f"[{time.ctime()}] Check failed: {str(e)}")
        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    # Sunucuyu thread'de başlat
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Site kontrolünü başlat
    print(f"Monitoring {CHECK_URL} every {CHECK_INTERVAL//60} minutes...")
    check_website()