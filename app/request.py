# app/request.py

# Import necessary modules
from app._internal import _wsgi_decoding_dance

class Request:
    """
    A basic class to handle HTTP requests.
    You can expand this with more functionality as per your needs.
    """
    
    def __init__(self, method, url, headers=None, body=None):
        self.method = method
        self.url = url
        self.headers = headers or {}
        self.body = body
    
    def get_header(self, name):
        """Return the value of a specific header."""
        return self.headers.get(name)
    
    def get_body(self):
        """Return the body of the request."""
        return self.body

    def process(self):
        """
        Process the request (dummy method for illustration).
        You can implement additional logic here.
        """
        print(f"Processing {self.method} request for {self.url}")
        # Example use of the imported internal function
        _wsgi_decoding_dance(self.body)

    def __str__(self):
        """Return a string representation of the request."""
        return f"{self.method} {self.url} with headers {self.headers}"

# A sample method to illustrate usage of the class
def example_request():
    req = Request(method="GET", url="https://example.com", headers={"User-Agent": "MyApp"}, body="Hello, World!")
    req.process()
    print(req)

# Uncomment the following line if you want to test the example request
# example_request()

