from http.server import HTTPServer, BaseHTTPRequestHandler
from http import HTTPMethod
from urllib.parse import urlparse, parse_qs
import base64



# routes = {
#     'GET' :{},
#     'POST': {}
# }
routes = {
    HTTPMethod.GET  : {},
    HTTPMethod.POST : {}
    # HTTPMethod.PUT : {}
}


def route(path,method=HTTPMethod.GET):
    def decorator(func):
        routes[method][path] = func
        return func
    return decorator


class BasicRequestHandler(BaseHTTPRequestHandler):

    # overwrite to 
    def __init__(self, request, client_address, server):  
        super().__init__(request, client_address, server)  
        self.decoded_content = None

    options = None

    def do_GET(self):  self.handle_request(HTTPMethod.GET)
    def do_POST(self): self.handle_request(HTTPMethod.POST)

    # overwrite default log message in stdout
    def log_message(self,format, *args):
        super().log_message(format,*args)
        details = []
        details.append(f"[*] Method: {self.command}")
        details.append(f"[*] Path: {self.path}")
        details.append(f"[*] Headers:")
        for header, value in self.headers.items():
            details.append(f"  {header}: {value}")
        if hasattr(self, 'decoded_content') and self.decoded_content:
            details.append(f"[*] Content:\n{self.decoded_content}")
    

        print("\n".join(details))



    def handle_request(self, method):
        parsed_path = urlparse(self.path).path

        handler = routes[method].get(parsed_path)

        if handler:
            result = handler(self)
            self.send_response(200)
            self.end_headers()
            if result and self.options.echo:
                self.wfile.write(str(result).encode())
        else:
            self.send_response(404)
            self.end_headers()



@route('/bd')
def b64_decode_request(request):
    parsed_params = urlparse(request.path) 
    params = parse_qs(parsed_params.query)

    res = "Successful\n"
        
    if 'd' in params:
        encoded_data = params['d'][0]
        try:
            decoded = base64.b64decode(encoded_data).decode('utf-8')
            d_string = f"{decoded}"
            request.decoded_content = d_string
            return d_string
        except Exception as e:
            print(f"Decode error: {e}")
            return f"error:{e}"

    return res


def run(host='localhost', port=8888, options=None):

    BasicRequestHandler.options = options
    HTTPServer((host,port), BasicRequestHandler).serve_forever()
