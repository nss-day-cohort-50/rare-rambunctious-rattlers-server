import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from User import create_user, get_all_users, get_single_user, user_login
from Post import get_all_posts, get_single_post

class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        if "?" in resource:

            param = resource.split("?")[1]  # example: http://localhost:8088/animals?status=Treatment
            resource = resource.split("?")[0]  
            pair = param.split("=")  
            key = pair[0]  
            value = pair[1]  

            return ( resource, key, value )

        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /entrys
            except ValueError:
                pass  # Request had trailing slash: /entrys/

            return (resource, id)


    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        """Handles GET requests to the server
        """
        # Set the response code to 'Ok'
        self._set_headers(200)
        response = {} #default response

        # Parse the URL and capture the tuple that is returned
        parsed = self.parse_url(self.path)

        # Response from parse_url() is a tuple with 2
        # items in it, which means the request was for
        # `/entrys` or `/entrys/2`

        if len(parsed) == 2:
            ( resource, id ) = parsed

            if resource == "users":
                if id is not None:
                    response = f"{get_single_user(id)}"
                else:
                    response = f"{get_all_users()}"
            elif resource == "posts":
                if id is not None:
                    response = f"{get_single_post(id)}"
                else:
                    response = f"{get_all_posts()}"

        elif len(parsed) == 3:
            ( resource, key, value ) = parsed

            if key == "q" and resource == 'entries':
                response = get_entries_by_search_term(value)


        self.wfile.write(response.encode())

    def do_POST(self):
            self._set_headers(201)
            content_len = int(self.headers.get('content-length', 0))
            post_body = self.rfile.read(content_len)

    #         # Convert JSON string to a Python dictionary
            post_body = json.loads(post_body)

            # Parse the URL
            (resource, id) = self.parse_url(self.path)

            # Initialize new entry
            res = None

            # Add a new entry to the list. Don't worry about
            # the orange squiggle, you'll define the create_entry
            # function next.
            if resource == "login":
                res = user_login(post_body)
            # Encode the new entry and send in response
            self.wfile.write(res.encode())

# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
