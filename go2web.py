import sys

def print_help():
    print("Usage:")
    print("go2web.py -u <URL>         # make an HTTP request to the specified URL and print the response")
    print("go2web.py -s <search-term> # make an HTTP request to search the term using your favorite search engine and print top 10 results")
    print("go2web.py -h               # show this help")

def main():
    if len(sys.argv) < 2 or sys.argv[1] == '-h':
        print_help()
    elif sys.argv[1] == '-u' and len(sys.argv) == 3:
        url = sys.argv[2]
    elif sys.argv[1] == '-s' and len(sys.argv) == 3:
        term = sys.argv[2]
    else:
        print("Invalid arguments. Use -h for help.")

if __name__ == "__main__":
    main()