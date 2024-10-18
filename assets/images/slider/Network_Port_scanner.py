import argparse
import nmap

def argument_parser():
    """
    Set up argument parser for the host and port options.
    """
    parser = argparse.ArgumentParser(description="TCP port scanner to scan a list of ports on a given host. "
                                     "It attempts to identify the service running on each port.")
    parser.add_argument("-o", "--host", required=True, help="Host IP address or hostname")
    parser.add_argument("-p", "--ports", required=True, help="Comma-separated list of ports to scan, e.g., '22,80,443'")
    
    return vars(parser.parse_args())

def nmap_scan(host, ports):
    """
    Use nmap to scan the specified ports on the given host.
    Prints out the state (open/closed/filtered) of each port and attempts to identify the service.
    """
    try:
        nm_scan = nmap.PortScanner()
        scan_results = []
        print(f"\n[*] Scanning host: {host} on ports: {ports}\n")

        # Scanning each port in the list
        nm_scan.scan(host, ports)

        # Check if the host is up
        if host not in nm_scan.all_hosts():
            raise KeyError(f"{host} is not responding or Nmap cannot reach it.")
        
        # Loop through the scanned ports and extract information
        for port in nm_scan[host]['tcp']:
            state = nm_scan[host]['tcp'][port]['state']
            service = nm_scan[host]['tcp'][port].get('name', 'Unknown')
            version = nm_scan[host]['tcp'][port].get('version', 'Unknown')
            product = nm_scan[host]['tcp'][port].get('product', 'Unknown')
            
            result = (f"[*] {host} tcp/{port}: {state}\n"
                      f"    Service: {service}\n"
                      f"    Product: {product}\n"
                      f"    Version: {version}\n")
            scan_results.append(result)
        
        return scan_results

    except KeyError as e:
        print(f"Error: {e}. Nmap could not find the key during the scan. Is the host reachable?")
    except nmap.PortScannerError as e:
        print(f"Nmap scanning error: {e}. Ensure Nmap is installed and working.")
    except Exception as e:
        print(f"Error occurred: {e}.")


if __name__ == '__main__':
    try:
        user_args = argument_parser()
        host = user_args["host"]
        ports = user_args["ports"]
        
        # Perform the scan and display results
        scan_results = nmap_scan(host, ports)
        if scan_results:
            for result in scan_results:
                print(result)
    
    except Exception as e:
        print(f"Error: {e}. Please check your inputs and try again.")
