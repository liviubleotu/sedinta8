from textwrap import indent
import requests
import json
from pprint import pprint
requests.packages.urllib3.disable_warnings()

router_local = {"ip": "192.168.0.47", "port": "443",
          "user": "student", "password": "cisco"}


# set REST API headers
headers = {"Accept": "application/yang-data+json",
           "Content-Type": "application/yang-data+json"}
interface_speed_url = f"https://{router_local['ip']}/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces/interface=GigabitEthernet1/ether-state/negotiated-port-speed/"
interface_duplex_url = f"https://{router_local['ip']}/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces/interface=GigabitEthernet1/ether-state/negotiated-duplex-mode"
interface_status_url = f"https://{router_local['ip']}/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces/interface=GigabitEthernet1/admin-status/"
configure_loopback_url = f"https://{router_local['ip']}/restconf/data/ietf-interfaces:interfaces/interface=Loopback100"
save_config_url = f"https://{router_local['ip']}/restconf/operations/cisco-ia:save-config"
payload_config_loopback = {
    "ietf-interfaces:interface": {
        "name": "Loopback100",
        "description": "Adaugata prin restconf",
        "type": "iana-if-type:softwareLoopback",
        "enabled": True,
        "ietf-ip:ipv4": {
            "address": [
                {
                    "ip": "150.1.1.1",
                    "netmask": "255.255.255.0"
                }
            ]
        }
    }
}

# print(url)
lista_rutere = [router_local]
for router in lista_rutere:
    url = interface_speed_url
    response = requests.get(url, headers=headers, auth=(router['user'], router['password']), verify=False)
    api_data = response.json()
    #print (api_data)
    print (f"Interfata are speed:{api_data['Cisco-IOS-XE-interfaces-oper:negotiated-port-speed']}")
    print("*" * 40)
    url = interface_duplex_url
    response = requests.get(url, headers=headers, auth=(router['user'], router['password']), verify=False)
    api_data = response.json()
    #print (api_data)
    print (f"Interfata are duplex:{api_data['Cisco-IOS-XE-interfaces-oper:negotiated-duplex-mode']}")
    print("*" * 40)
    url = interface_status_url
    response = requests.get(url, headers=headers, auth=(router['user'], router['password']), verify=False)
    api_data = response.json()
    #print (api_data)
    print (f"Interfata are statusul:{api_data['Cisco-IOS-XE-interfaces-oper:admin-status']}")
    print("*" * 40)
    print ("Configurez interfata Loopback:")
    url = configure_loopback_url
    response = requests.put(url, headers=headers, auth=(router['user'], router['password']), verify=False, data=json.dumps(payload_config_loopback))
    if(response.status_code >= 200 and response.status_code <= 299):
        print (f"S-a creat interfata de Loopback, status code {response.status_code}")
        url = save_config_url
        response = requests.post(url, headers=headers, auth=(router['user'], router['password']), verify=False)
        response_save=response.json()
        print (response_save['cisco-ia:output']['result'])
    else:
        print ("Nu s-a putut crea interfata de Loopback. Status Code: {} \nError message: {}".format(response.status_code, response.json()))
    


