import concurrent.futures
import requests

def scan_subdomain(url):
    try:
        get_url =requests.get(url, timeout=5)
        # Set a timeout of 5 seconds
        if 400 <= get_url.status_code < 500:
            print(f"Error: Client error response [-] {url} {get_url}")
            # return f'{url}'
        else:
            print(f'[+] {url} {get_url}')
            return f'{url}'
    except requests.ConnectionError:
        pass

def domain_scanner(domain_name, sub_domnames):
    output = []  # Create an empty list to store the print outputs
    print('-----------Scanner Started-----------')
    print('----URL after scanning subdomains----')

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(scan_subdomain, f"https://{subdomain}.{domain_name}") for subdomain in sub_domnames]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                output.append(result)
                print(result)
    # output.append('\n')
    print('----Scanning Finished----')
    print('-----Scanner Stopped-----')
    return output



def dir_scanner(domain_name, dir_domnames):
    output = []  # Create an empty list to store the print outputs
    print('-----------Scanner Started-----------')
    print('----URL after scanning dir----')
    if "https://" in domain_name:
        domain = domain_name.split('https://')[1]
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(scan_subdomain, f"https://{domain}/{subdomain}.") for subdomain in
                       dir_domnames]
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    output.append(result)
                    print(result)

    elif "http://" in domain_name:
        domain = domain_name.split('http://')[1]
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(scan_subdomain, f"http://{domain}/{subdomain}.") for subdomain in
                       dir_domnames]
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    output.append(result)
                    print(result)
    else:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(scan_subdomain, f"https://{domain_name}/{subdomain}.") for subdomain in
                       dir_domnames]
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    output.append(result)
                    print(result)


    # output.append('\n')
    print('----Scanning Finished----')
    print('-----Scanner Stopped-----')
    return output

