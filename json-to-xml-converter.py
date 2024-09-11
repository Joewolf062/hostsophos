#ip Google to Sophos host conversion tool
#this tool is not a Sophos product, it is not supported by Sophos 

import json
import requests
import xml.etree.ElementTree as ET
from xml.dom import minidom
import ipaddress

def fetch_json_data(url):
    response = requests.get(url)
    return response.json()

def cidr_to_netmask(cidr):
    return str(ipaddress.IPv4Network(f'0.0.0.0/{cidr}').netmask)

def create_xml_element(prefix):
    iphost = ET.Element('IPHost')
    iphost.set('transactionid', '')

    name = ET.SubElement(iphost, 'Name')
    name.text = f"{prefix['service']} {prefix['ipv4Prefix']}"

    description = ET.SubElement(iphost, 'Description')
    description.text = f"{prefix['service']} {prefix['scope']}"

    ip_family = ET.SubElement(iphost, 'IPFamily')
    ip_family.text = 'IPv4'

    host_type = ET.SubElement(iphost, 'HostType')
    host_type.text = 'Network'

    ip_address = ET.SubElement(iphost, 'IPAddress')
    ip_address.text = prefix['ipv4Prefix'].split('/')[0]

    subnet = ET.SubElement(iphost, 'Subnet')
    subnet.text = cidr_to_netmask(prefix['ipv4Prefix'].split('/')[1])

    return iphost

def main():
    url = 'https://www.gstatic.com/ipranges/cloud.json'
    data = fetch_json_data(url)

    root = ET.Element('IPHosts')

    for prefix in data['prefixes']:
        if 'ipv4Prefix' in prefix:
            root.append(create_xml_element(prefix))

    xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
    
    with open('ip_ranges.xml', 'w') as f:
        f.write(xml_str)

    print("XML file 'ip_ranges.xml' has been created successfully.")

if __name__ == "__main__":
    main()
