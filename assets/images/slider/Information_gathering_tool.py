#project 2: movidu technology
import sys
import requests
import socket
import json
import dns.resolver  # for DNS lookup
import whois  # for whois lookup

def fetch_headers(url):
    """Fetch and print HTTP headers of the given URL."""
    try:
        req = requests.get(url)
        print(f"\nHTTP Headers for {url}:\n")
        for header, value in req.headers.items():
            print(f"{header}: {value}")
        return req
    except requests.exceptions.RequestException as e:
        print(f"Error fetching headers: {e}")
        sys.exit(1)

def resolve_ip(domain):
    """Resolve the IP address of the domain."""
    try:
        ip_address = socket.gethostbyname(domain)
        print(f"\nThe IP address of {domain} is: {ip_address}\n")
        return ip_address
    except socket.error as e:
        print(f"Error resolving IP address: {e}")
        sys.exit(1)

def fetch_geo_info(ip_address):
    """Fetch geolocation information using the IP address."""
    try:
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        geo_info = response.json()
        print(f"Location: {geo_info.get('loc', 'N/A')}")
        print(f"Region: {geo_info.get('region', 'N/A')}")
        print(f"City: {geo_info.get('city', 'N/A')}")
        print(f"Country: {geo_info.get('country', 'N/A')}")
        print(f"Organization: {geo_info.get('org', 'N/A')}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching geolocation information: {e}")

def fetch_dns_records(domain):
    """Fetch DNS records (A, MX, NS) for the domain."""
    try:
        print(f"\nDNS records for {domain}:\n")
        
        # A records
        a_records = dns.resolver.resolve(domain, 'A')
        print("A Records (IP Addresses):")
        for ipval in a_records:
            print(f"IP: {ipval.to_text()}")
        
        # MX records (Mail exchange)
        mx_records = dns.resolver.resolve(domain, 'MX')
        print("\nMX Records (Mail Servers):")
        for mx in mx_records:
            print(f"Host: {mx.exchange}, Preference: {mx.preference}")

        # NS records (Name servers)
        ns_records = dns.resolver.resolve(domain, 'NS')
        print("\nNS Records (Name Servers):")
        for ns in ns_records:
            print(f"Name Server: {ns.to_text()}")
    except Exception as e:
        print(f"Error fetching DNS records: {e}")

def fetch_whois_info(domain):
    """Fetch Whois information for the domain."""
    try:
        whois_info = whois.whois(domain)
        print(f"\nWhois information for {domain}:\n")
        print(f"Domain Name: {whois_info.domain_name}")
        print(f"Registrar: {whois_info.registrar}")
        print(f"Creation Date: {whois_info.creation_date}")
        print(f"Expiration Date: {whois_info.expiration_date}")
        print(f"Name Servers: {whois_info.name_servers}")
    except Exception as e:
        print(f"Error fetching Whois information: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: " + sys.argv[0] + " <domain>")
        sys.exit(1)

    domain = sys.argv[1]
    
    # Support both http and https
    if not domain.startswith("http"):
        domain_url = "https://" + domain
    else:
        domain_url = domain

    # Fetch HTTP headers
    fetch_headers(domain_url)
    
    # Resolve IP and fetch geolocation
    ip_address = resolve_ip(domain)
    fetch_geo_info(ip_address)
    
    # Fetch DNS records
    fetch_dns_records(domain)
    
    # Fetch Whois information
    fetch_whois_info(domain)

if __name__ == "__main__":
    main()
