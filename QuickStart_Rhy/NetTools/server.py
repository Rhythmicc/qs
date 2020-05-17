from socketserver import ThreadingMixIn
from http.server import SimpleHTTPRequestHandler
from http.server import HTTPServer


class HttpServers:
    import qrcode_terminal
    import signal

    def __init__(self, ip='localhost', port=8000, url=''):
        self.web_address = ip
        self.web_port = port
        self.httpd = None
        self.bind_url = url

    class Server(ThreadingMixIn, HTTPServer):
        pass

    def start(self):
        HttpServers.signal.signal(HttpServers.signal.SIGINT, self.shutdown)
        self.httpd = HttpServers.Server((self.web_address, self.web_port), SimpleHTTPRequestHandler)
        if not self.bind_url:
            self.bind_url = 'http://' + self.web_address + ':' + str(self.web_port)
        print(self.bind_url)
        HttpServers.qrcode_terminal.draw(self.bind_url)
        try:
            self.httpd.serve_forever()
        except KeyboardInterrupt:
            self.shutdown(0, 0)

    def shutdown(self, a, b):
        self.httpd.server_close()
        print('HTTP Server: Closed.')
        exit(0)
