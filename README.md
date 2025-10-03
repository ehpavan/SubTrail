# SubTrail
this is SubTrail, a tiny Python script that hits the SecurityTrails API, pulls subdomains for whatever domain you point it at, checks which ones actually resolve via DNS (using sockets), and saves only the live ones to a file. No fluff, just useful output you can use.

# Installation

```
git clone https://github.com/ehpavan/SubTrail
cd SubTrail
pip3 install -r requirements.txt
```


# What it does
- Calls SecurityTrails API to get subdomains for a domain.
- Uses Python socket to check DNS resolution — only saves subdomains that actually resolve.
- Uses random to add a 4-digit suffix to the default filename so you don’t accidentally overwrite stuff.
- Prints a simple status + number of live subs found and writes them to a file (one per line).

# Usage
```
python3 SubTrail.py -d example.com -k YOUR_SECURITYTRAILS_API_KEY
```
* Optional output file:
```
python3 subtrail.py -d example.com -k YOUR_KEY -o my-live-subs.txt
```
* Default filename (if you don’t pass -o) looks like:
```
example_com-0421.txt
```
# Example output
```
[+] Querying SecurityTrails for example.com...
[+] Finished! Found 12 working subdomains.
[i] Results saved to: example_com-7294.txt
```
* Inside example_com-7294.txt:
```
www.example.com
api.example.com
dev.example.com
...
```
Only the resolvable ones. Dead subdomains = ignored.

# Why this is handy
* Fast way to get a clean list of live subdomains from SecurityTrails without sifting through dead entries.
* Good for recon, triage, or as input to other tools (port scanners, vulnerability scanners, etc.).
* Minimal, readable code — easy to tweak.

# Note
* Make sure your SecurityTrails API key is valid and has quota. If you get empty results, check the key first.
* DNS check is done with socket.gethostbyname() — it only checks resolution, not HTTP status or open ports. If you want “is the site up?” checks, add httpx, curl, or nmap later.
* The script adds a random suffix (0–9999) to the default filename to avoid overwrites. Use -o to force your own filename.
* Only supports SecurityTrails out of the box. Could be extended to other sources.

# Author
 Pavan
 
### About Me
> Hi, I’m Pavan, a 16-year-old cybersecurity enthusiast from India. I build tools, hunt bugs, and explore web and cloud security.
