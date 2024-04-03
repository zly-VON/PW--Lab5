import sys, ssl
import socket, warnings
import os, hashlib
from urllib.parse import urlparse
from bs4 import BeautifulSoup

CACHE_DIRECTORY = 'http_cache'

def search_term(term):
    response = make_request(f"https://www.google.com/search?q={term}")
    soup = BeautifulSoup(response, "html.parser")
    search_results = soup.find_all("a")
    count = 0

    for result in search_results:
        if count >= 10:
            break
        link = result.get("href")
        if link.startswith("/url?q="):
            link = link.split("/url?q=")[1].split("&")[0]
            if term in result.text.lower():
                count += 1
                print(f"Result {count}: {result.text}")
                print(f"Link: {link}" + "\n")

def print_url_response(url):
    response = make_request(url)
    soup = BeautifulSoup(response, 'html.parser')

    print("\nURL Content:")
    print("=" * 20)
    for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'a', 'ul', 'img']):
        if tag.name.startswith('h'):
            print("\n" + tag.get_text().strip() + "\n")
        elif tag.name == 'ul':
            for li in tag.find_all('li'):
                print(li.get_text().strip())
        elif tag.name == 'a' and tag.get('href') and (tag.get('href').startswith('http://') or tag.get('href').startswith('https://')):
            print(tag.get_text().strip())
            print("Link:", tag.get('href'))
        elif tag.name == 'p':
            print(tag.get_text().strip())
        elif tag.name == 'img' and tag.get('src'):
            print("Image:", tag.get('src'))

warnings.filterwarnings("ignore", category=DeprecationWarning)

def make_request(url):
    cache_key = hashlib.md5(url.encode()).hexdigest()
    cache_file = os.path.join(CACHE_DIRECTORY, cache_key)

    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            print("Retrieved from cache\n")
            return f.read()

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

        with open(cache_file, 'w') as f:
            f.write(response.decode('utf-8', errors='ignore'))

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
        if len(sys.argv) < 3:
            print("Missing arguments. Use -h for help.")
        else:
            term = sys.argv[2]
            search_term(term)
    else:
        print("Invalid arguments. Use -h for help.")

if __name__ == "__main__":
    main()