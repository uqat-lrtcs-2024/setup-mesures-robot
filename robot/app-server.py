from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import urlparse
import subprocess

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        query_params = urlparse.parse_qs(parsed_path.query)

        script_name = "./gotoGoal3"
        args = query_params.get("args", [])

        cmd = [script_name] + args

        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()
            if process.returncode != 0:
                raise Exception(error)

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(output)
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write("Error running command: %s" % str(e))

def run(server_class=HTTPServer, handler_class=MyHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print "Starting HTTP server on port %d..." % port
    httpd.serve_forever()

if __name__ == '__main__':
    run()
