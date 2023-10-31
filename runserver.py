from flaskapp import app
import argparse
import sys

def main():
    # argument parser
    parser = argparse.ArgumentParser(
        prog="lux.py"
    )
    parser.add_argument("port",
                        help="the port at which the server should listen")
    args = parser.parse_args()

    # validate port argument
    port = None
    try:
        port = int(args.port)
    except ValueError:
        print("Port must be a number", file=sys.stderr)
        sys.exit(1)
    
    # attempt to run the application
    try: 
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as err:
        print("Something went wrong", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()