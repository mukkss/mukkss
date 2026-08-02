#!/usr/bin/env python3
import os
import subprocess
import sys

def run_script(script, *args):
    cmd = [sys.executable, f"scripts/{script}"] + list(args)
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

def main():
    # Make sure we're in the project root
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root)
    
    # Check for GitHub Token
    if not os.environ.get("MY_TOKEN"):
        sys.exit("MY_TOKEN is not set. Cannot fetch data.")
        
    print("=== Fetching Profile Data ===")
    run_script("fetch_data.py")
    
    print("\n=== Generating Stats Assets ===")
    run_script("generate_stats.py")
    run_script("generate_streak.py")
    run_script("generate_languages.py")
    run_script("generate_calendar.py")
    
    print("\n=== Generating Headings ===")
    headings = ["about", "stack", "projects", "stats", "about this page"]
    for word in headings:
        out_path = f"assets/headings/hd-{word.replace(' ', '-')}.svg"
        run_script("generate_heading.py", word, out_path)
        
    print("\nAll assets generated successfully!")

if __name__ == "__main__":
    main()
