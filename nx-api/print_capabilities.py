from ncclient import manager

conn = manager.connect(
        host='192.168.0.70', 
        port=22, 
        username='student', 
        password='Admin1234!', 
        hostkey_verify=False, 
        device_params={'name': 'nexus'}, 
        look_for_keys=False
        )

for value in conn.server_capabilities:
    print(value)

conn.close_session()