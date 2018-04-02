"""
Test email addresses against a database of known third party data breaches.

References:
* https://haveibeenpwned.com/FAQs
"""
import click
import requests

BASE_URL = "https://haveibeenpwned.com/api/v2/breachedaccount/"

@click.command()
@click.option('--input_file', default='test.txt')
def do_audit(input_file):
    results = {}
    with open(input_file, 'r') as address_file:
        for address in address_file:
            address = address.strip()
            url = '{}{}'.format(BASE_URL, address)
            resp = requests.get(url)
            if resp.ok:
                num_breaches = len(resp.json())
                results[address] = num_breaches
            else:
                status_code = resp.status_code
                if status_code == 404:
                    results[address] = 'Not included in breach DB'
                else:
                    results[address] = 'API response code: {}'.format(resp.status_code)
    print(results)

if __name__ == '__main__':
    do_audit()
