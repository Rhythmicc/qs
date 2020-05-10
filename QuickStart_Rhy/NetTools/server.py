def network_ip_address():
    from socket import gethostbyname
    from socket import gethostname
    return gethostbyname(gethostname())


def make_temp_file(length=8):
    from os import environ
    from random import randint
    s = ''
    for c in range(0, length):
        s += chr(randint(97, 122))
    # s = environ['TMPDIR']+'\\'+s+'.tmp' #Linux
    s = environ['TEMP'] + '\\' + s + '.tmp'
    return s


def pem2file(pemstr):
    fp = make_temp_file()
    pemlines = ''
    pemdata = pemstr.strip().split('\n')
    for s in pemdata:
        if '-----' in s:
            p = s.find('-')
            pemlines += s[p:] + '\n'
            continue
        pemlines += s.replace(' ', '') + '\n'
    with open(fp, 'w') as f:
        f.write(pemlines)
    return fp


def delete_file(fpath):
    from os import remove as remove_file
    remove_file(fpath)


class HttpServers:
    from http.server import HTTPServer
    from http.server import SimpleHTTPRequestHandler
    from http.server import CGIHTTPRequestHandler
    from ssl import wrap_socket as ssl_wrap_socket
    import qrcode_terminal
    import signal
    # PEM: http://www.cert-depot.com/

    local_keyfile = private_pem = """-----BEGIN RSA PRIVATE KEY-----
    MIICWwIBAAKBgQCebbtX+NVLy1vpcCQTKM5eSmaCpzoqtoAkRoE6KAnowWX2REja
    uGXsrFJVwGz6zCC2+0wgD4AUzxkI3I5Di/xhd5huJ5Ffgs9a5EbhqxoAoNWhTpov
    hSlkiy6s4wJcUQAsrkKIhnbhxDl7+lC1OCk1ZVHfUOkcQO/LUKRbIjlO7QIDAQAB
    AoGAR+clj9evdqblIB11QfzTLJg3zjR3gcsyfURCglKJrMmZrRtwtVPbbn8HH0Qm
    Me1TK7kB48slJkyX4B25s45lDGCYo5cMAt2GFe5ghrng7TkeCr/s8OKiMUBgrK/o
    AS2jnMHCf681tt7+vcqnoITepy7ksHl+NEs8IRw7uqOhJUECQQDMOwgUhQb7UvQy
    uaQl29w5n1nc1SpaYKVSTjKE/q+F5KD3rONzvSttQXMGc1JKj6T3DNUBuPITCvUV
    3MNudjsjAkEAxpaC/vI7zcclqCHIp3deJ35nr4jVqU/ONdSpC5/Tt1/CeZYLprcu
    YYYtgI5iIcxpnjpN8JgEFysZfz96PPS2rwJAFL+CiKMjHHFHAcg+VuJJM0lvFbJK
    RThAU2ZCV6SQLGgXulHEIcP8H3Ngvi0FFTIWrkqNcUlavniEgZ4V9KjqRQJAbJ3D
    9jd9ODa1RPl9awMhz04W3e5kll9c9Rpkf0Qio0hP8Pp9UukcCCFAX/EAgWXxWqaf
    HHm4uwdKwctxS0e5ZwJAdQa5t0XiRzCXa044tkdho0lsom9JoWvoTGxPSyK+cVeO
    WzWyqxlLdFeuzgbTchZGd9OeWZmXFsfWnfRlpWKMqA==
    -----END RSA PRIVATE KEY-----"""

    local_certfile = public_pem = """-----BEGIN CERTIFICATE-----
    MIIDCjCCAnOgAwIBAgIJAPHaaD4ypyZAMA0GCSqGSIb3DQEBBQUAMIGcMRowGAYD
    VQQDDBFQeXRob24gU1NMIFNlcnZlcjELMAkGA1UEBhMCUHkxEjAQBgNVBAgMCWxv
    Y2FsaG9zdDESMBAGA1UEBwwJbG9jYWxob3N0MRIwEAYDVQQKDAlsb2NhbGhvc3Qx
    EjAQBgNVBAsMCWxvY2FsaG9zdDEhMB8GCSqGSIb3DQEJARYScm9vdEBsb2NhbGhv
    c3Qub3JnMCAXDTE1MDcyMzAyMDEzNVoYDzIxMTUwNjI5MDIwMTM1WjCBnDEaMBgG
    A1UEAwwRUHl0aG9uIFNTTCBTZXJ2ZXIxCzAJBgNVBAYTAlB5MRIwEAYDVQQIDAls
    b2NhbGhvc3QxEjAQBgNVBAcMCWxvY2FsaG9zdDESMBAGA1UECgwJbG9jYWxob3N0
    MRIwEAYDVQQLDAlsb2NhbGhvc3QxITAfBgkqhkiG9w0BCQEWEnJvb3RAbG9jYWxo
    b3N0Lm9yZzCBnzANBgkqhkiG9w0BAQEFAAOBjQAwgYkCgYEAnm27V/jVS8tb6XAk
    EyjOXkpmgqc6KraAJEaBOigJ6MFl9kRI2rhl7KxSVcBs+swgtvtMIA+AFM8ZCNyO
    Q4v8YXeYbieRX4LPWuRG4asaAKDVoU6aL4UpZIsurOMCXFEALK5CiIZ24cQ5e/pQ
    tTgpNWVR31DpHEDvy1CkWyI5Tu0CAwEAAaNQME4wHQYDVR0OBBYEFCVBtdE7QlUk
    jfNyTUlPqR/j1ElFMB8GA1UdIwQYMBaAFCVBtdE7QlUkjfNyTUlPqR/j1ElFMAwG
    A1UdEwQFMAMBAf8wDQYJKoZIhvcNAQEFBQADgYEAFMxmuEWwvk8b+dpVEhbVQHta
    ii2vyfa4fW74pBKnTcZRsvoDdyqjV91JeM1G3tVAsi+JLQ/udfv70WG04NwrDoQ4
    mAoYy8KVFpq2nTQ/fPXhqFPOnkWFH3xak4i07zOACXdozcb85gAonQJBv3fnOz7B
    hJzPSTxc/V03FjzqizA=
    -----END CERTIFICATE-----"""

    keep_server_running = True

    def __init__(self, ip='localhost', port=8000, ssl_port=1443, use_ssl=False, use_cgi=False, pem_cert_file='',
                 pem_key_file=''):
        self.web_address = ip
        self.web_port = port
        self.ssl_port = ssl_port
        self.use_ssl = use_ssl
        self.use_cgi = use_cgi
        self.cert_file_path = pem_cert_file
        self.key_file_path = pem_key_file
        self.httpd = None

    class CGIRequestHandler(CGIHTTPRequestHandler):
        from QuickStart_Rhy.ThreadTools import ThreadFunctionWrapper
        job_q = []

        def do_GET(self):
            t = self.ThreadFunctionWrapper(HttpServers.CGIHTTPRequestHandler.do_GET, self)
            self.job_q.append(t)
            t.run()

        def do_POST(self):
            t = self.ThreadFunctionWrapper(HttpServers.CGIHTTPRequestHandler.do_POST, self)
            self.job_q.append(t)
            t.run()

        def do_HEAD(self):
            t = self.ThreadFunctionWrapper(HttpServers.CGIHTTPRequestHandler.do_HEAD, self)
            self.job_q.append(t)
            t.run()

        def wait(self):
            for t in self.job_q:
                t.join()

    class SimpleRequestHandler(SimpleHTTPRequestHandler):
        from QuickStart_Rhy.ThreadTools import ThreadFunctionWrapper
        job_q = []

        def do_GET(self):
            t = self.ThreadFunctionWrapper(HttpServers.SimpleHTTPRequestHandler.do_GET, self)
            self.job_q.append(t)
            t.run()

        def do_POST(self):
            t = self.ThreadFunctionWrapper(HttpServers.SimpleHTTPRequestHandler.do_POST, self)
            self.job_q.append(t)
            t.run()

        def do_HEAD(self):
            t = self.ThreadFunctionWrapper(HttpServers.SimpleHTTPRequestHandler.do_HEAD, self)
            self.job_q.append(t)
            t.run()

        def wait(self):
            for t in self.job_q:
                t.join()

    def start(self):
        if self.use_cgi:
            ReqHandler = self.CGIRequestHandler
        else:
            ReqHandler = self.SimpleRequestHandler
        HttpServers.signal.signal(HttpServers.signal.SIGINT, self.shutdown)
        if self.use_ssl:
            self.httpd = self.HTTPServer((self.web_address, self.ssl_port), ReqHandler)
            if not len(self.key_file_path):
                self.key_file_path = pem2file(HttpServers.local_keyfile)
            if not len(self.cert_file_path):
                self.cert_file_path = pem2file(HttpServers.local_certfile)
            self.httpd.socket = HttpServers.ssl_wrap_socket(self.httpd.socket, server_side=True,
                                                            keyfile=self.key_file_path, certfile=self.cert_file_path)
            delete_file(self.key_file_path)
            delete_file(self.cert_file_path)
            print('HTTPS Server: Started on', self.web_address, 'Port', self.ssl_port)
            HttpServers.qrcode_terminal.draw('http://' + self.web_address + ':' + str(self.ssl_port))
        else:
            self.httpd = self.HTTPServer((self.web_address, self.web_port), ReqHandler)
            print('HTTP Server: Started on', self.web_address, 'Port', self.web_port)
            HttpServers.qrcode_terminal.draw('http://' + self.web_address + ':' + str(self.web_port))
        while self.keep_server_running:
            self.httpd.handle_request()

    def shutdown(self, a, b):
        self.httpd.server_close()
        print('HTTP Server: Closed.')
        exit(0)
