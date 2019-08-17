import csv
import os
import re
import telnetlib

import docker
from flask import Flask
from flask_restful import Resource, Api


def get_status(host, port=5555):
    '''
    login to openvpn host
    write 'status' to telnet console
    get all connected clients
    return count of connected clients
    '''
    telnet = telnetlib.Telnet()
    telnet.open(host, port)
    telnet.write(b'status\r\n')

    pattern = 'Common Name(.*?)ROUTING TABLE'
    try:
        status = telnet.read_until(b'END')
        clean = 'Common Name' + re.findall(pattern, str(status))[0]
        clean_string = bytes(clean, 'utf-8').decode('unicode_escape')
        infos = csv.DictReader(clean_string.splitlines())
    except:
        return 0

    telnet.close()
    return len(list(infos))


class ContainerClients(Resource):
    # https://flask-restful.readthedocs.io
    def get(self):
        # check all containers on the host
        result = []
        for container in client.containers.list():
            image = client.images.get(container.attrs['Image']).tags[0]
            if image == check_image:
                networks = container.attrs['NetworkSettings']['Networks']
                filtered = {k: v for k, v in networks.items() if k.count('statusgrabber') == 1}
                try:
                    network = list(filtered.keys())[0]
                    IP = filtered[network]['IPAddress']
                    result.append({"connected clients": get_status(IP), "container": container.name})
                except IndexError:
                    print("VPN {} keinem Status netzwerk zugeordnet".format(container.name))
        return result


check_image = os.getenv('check_image', 'vpn:latest')
client = docker.from_env()
app = Flask(__name__)
api = Api(app)

api.add_resource(ContainerClients, '/')

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
