# docker-openvpn-status
grabs the number of all connected OpenVPN clients for all containers on the docker host and returns in with a REST API

    docker run -d -v /var/run/docker.sock:/var/run/docker.sock -v /etc/localtime:/etc/localtime:ro --name statusgrabber --restart always docker-openvpn-status