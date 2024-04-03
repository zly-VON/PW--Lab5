import sys, ssl
import socket
from urllib.parse import urlparse

def print_url_response(url):
    return

def make_request(url):

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    parsed_url = urlparse(url)
    host, port, path = parsed_url.netloc, 443, parsed_url.path

    client_socket = ssl.wrap_socket(client_socket)

    try:
        client_socket.settimeout(2)
        client_socket.connect((host, port))

        request = f"GET {url} HTTP/1.1\r\nHost: {host}\r\n\r\n"
        client_socket.send(request.encode())

        response = b""
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                response += data
            except socket.timeout:
                break

        client_socket.close()
        return response.decode('utf-8', errors='ignore')

    except socket.error as e:
        print("Error making request:", e)
        sys.exit(1)

def print_help():
    print("Usage:")
    print("go2web.py -u <URL>         # make an HTTP request to the specified URL and print the response")
    print("go2web.py -s <search-term> # make an HTTP request to search the term using your favorite search engine and print top 10 results")
    print("go2web.py -h               # show this help")

def main():
    if len(sys.argv) < 2 or sys.argv[1] == '-h':
        print_help()
    elif sys.argv[1] == '-u':
        if len(sys.argv) < 3:
            print("Missing arguments. Use -h for help.")
        else:
            url = sys.argv[2]
            print_url_response(url)
    elif sys.argv[1] == '-s':
        term = sys.argv[2]
    else:
        print("Invalid arguments. Use -h for help.")

if __name__ == "__main__":
    main()