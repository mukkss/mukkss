#!/usr/bin/env python3
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import github_graphql

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--login", default=os.environ.get("GH_LOGIN", "mukkss"))
    ap.add_argument("--token", default=os.environ.get("MY_TOKEN"))
    ap.add_argument("--out", default="data/profile.json")
    args = ap.parse_args()
    
    if not args.token:
        sys.exit("MY_TOKEN is not set")
        
    data = github_graphql.get_profile_data(args.login, args.token)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Data fetched and saved to {args.out}")

if __name__ == "__main__":
    main()
