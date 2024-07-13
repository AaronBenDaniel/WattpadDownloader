#All of this was written with chatgpt 3.5 as a proof-of-concept
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import urlopen, Request
from urllib.parse import urlparse

# HTTPRequestHandler class
class RequestHandler(BaseHTTPRequestHandler):

    # GET method
    def do_GET(self):
        # Parse the request path to extract the URL to fetch
        parsed_url = urlparse(self.path)
        
        # Combine the path and query part to form the complete URL
        if parsed_url.query:
            url_to_fetch = parsed_url.path + '?' + parsed_url.query
        else:
            url_to_fetch = parsed_url.path
        
        # Fetch content from the requested URL
        try:
            req = Request(url_to_fetch[1:], headers={'User-Agent': 'Mozilla/5.0'})
            response = urlopen(req)
            content = response.read()
            
            # Send CORS headers
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')  # Allow requests from any origin
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'X-Requested-With')
            self.end_headers()
            
            # Send the content fetched from the URL
            self.wfile.write(content)
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Error fetching URL: " + str(e).encode())

        return

# Define the HTTP server parameters
host = '0.0.0.0'
port = 5043

# Create an HTTP server
server = HTTPServer((host, port), RequestHandler)

# Run the server
server.serve_forever()
