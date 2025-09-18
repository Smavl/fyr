import argparse
# import flask
import basic_http

class ServerOptions:
    def __init__(self, echo=False, verbose=False):
        self.echo = echo
        self.verbose = verbose


def print_banner():
    banner="""
   ▄████████ ▄██   ▄      ▄████████ 
  ███    ███ ███   ██▄   ███    ███ 
  ███    █▀  ███▄▄▄███   ███    ███ 
 ▄███▄▄▄     ▀▀▀▀▀▀███  ▄███▄▄▄▄██▀ 
▀▀███▀▀▀     ▄██   ███ ▀▀███▀▀▀▀▀   
  ███        ███   ███ ▀███████████ 
  ███        ███   ███   ███    ███ 
  ███         ▀█████▀    ███    ███ 
                         ███    ███
        """
    print(banner)

def main():

    print("launching HTTPServer")

    port = int(args.port) if args.port else 8888
    bind = str(args.bind) if args.bind else 'localhost'
    server_options = ServerOptions(echo=args.echo,verbose=args.verbose)
    basic_http.run(host=bind, port=port, options=server_options)




if __name__ == "__main__":
    p = argparse.ArgumentParser(description="PLACEHOLDER DESCRIPTION")
    p.add_argument("-b","--bind", help="Binding address")
    p.add_argument("-p","--port", help="Port for HTTP (Default: 8888)")
    p.add_argument("-v", "--verbose", action="store_true",
                        help="Enable verbose output")
    p.add_argument("-e","--echo", help="Enable echoing back the result", action="store_true")

    args = p.parse_args()

    print_banner()

    if args.verbose:
        print(f"Verbose mode is on.")

    main()
