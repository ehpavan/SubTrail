#!/usr/bin/env python3
# I switched this to python3 just to be safe. Some people still keep it as just python, which can be messy depending on system.

import requests
import argparse
import pyfiglet
import random
import json      # not really using it much,
import socket

def draw_banner():
    text = "Subdomain Finder"   
    sub = "- SecurityTrails API -" 
    author = "Pavan"   # :)

    try:
        art = pyfiglet.figlet_format(text, font="slant")
        print(art)
    except Exception as art_err:
        print("[!] Couldn’t generate ASCII art:", art_err)
        print(text)

    print(sub)
    print("-" * 36)
    print("Written by:", author)
    print("-" * 36, "\n")


# quick DNS check to make sure the subdomain actually resolves
def dns_check(name, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.gethostbyname(name)
        return True
    except Exception as e:
        return False


def grab_subdomains(domain, key, out_file):
    base_url = f"https://api.securitytrails.com/v1/domain/{domain}/subdomains"
    params = {"children_only": "true"}  

    headers = {
        "accept": "application/json",
        "apikey": key
    }

    print(f"[+] Querying SecurityTrails for {domain}...")

    try:
        r = requests.get(base_url, headers=headers, params=params)
        r.raise_for_status()   # throws an error if we got a bad HTTP response

        payload = r.json()

        if "subdomains" not in payload:
            print("[-] Hmmm... no 'subdomains' in response.")
            print("    Maybe API key quota exhausted? Or domain has none.")
            print("    Raw msg:", payload.get("message", "<nothing returned>"))
            return

        # Collecting subdomains that actually resolve
        alive = []
        for sub in payload["subdomains"]:
            fqdn = sub + "." + domain
            if dns_check(fqdn):   # Only add if it's alive
                alive.append(fqdn)

        
        if not alive:
            print("[-] No resolvable subdomains found. Might want to retry later.")
            return

        try:
            f = open(out_file, "w")
            for line in alive:
                f.write(line + "\n")
            f.close()
        except Exception as fe:
            print("[!] Error writing results:", fe)
            return

        print(f"[+] Finished! Found {len(alive)} working subdomains.")
        print(f"[i] Results saved to: {out_file}")

    except requests.exceptions.HTTPError as http_err:
        print("HTTP problem:", http_err)
        print("Tip: Check your API key or if the domain is spelled right.")
    except Exception as err:
        print("Unexpected error happened:", err)


if __name__ == "__main__":
    draw_banner()

    parser = argparse.ArgumentParser(
        description="Find subdomains using the SecurityTrails API."
    )

    parser.add_argument("-d", "--domain", help="Target domain (e.g. example.com)", required=True)
    parser.add_argument("-k", "--api-key", help="SecurityTrails API key", required=True)

    prelim_args, leftovers = parser.parse_known_args()
    file_safe = prelim_args.domain.replace(".", "_")

    rand_num = random.randint(0, 9999)

    rand_str = str(rand_num).zfill(4)
    default_file = f"{file_safe}-{rand_str}.txt"

    parser.add_argument("-o", "--output", help="Output file path", default=default_file)

    args = parser.parse_args()

    grab_subdomains(args.domain, args.api_key, args.output)
