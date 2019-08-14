#!/usr/bin/env python
import argparse
from yant import Server

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("basedir", type=str, help="path to directory containing notes")
    parser.add_argument("--port", "-p", type=int, default=8000, help="port listen on (default 8000)")

    args = parser.parse_args()

    s = Server(args.basedir)
    s.start(port=args.port)

if __name__ == "__main__":
    main()
    
