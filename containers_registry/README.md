# Containers registry

This service allows to self-host container registry for Podman/Docker.

Based on [this](https://infotechys.com/host-your-own-podman-registry/) tutorial.


## Prepare the host
```bash
export REGISTRY_PATH=/var/lib/registry
sudo mkdir -p $REGISTRY_PATH
```

## Run the service
```bash
podman-compose up -d
# or
docker compose up -d
```

## Setup the clients
The easiest way is to provide the registry address manually:
```bash
sudo vim /etc/containers/registries.conf
```

Assuming that `HOSTNAME` is your host IP address:
```
[[registry]]
location = "HOSTNAME:5000"
insecure = true
```

> [!WARNING]
> This configuration is NOT SAFE. Consider setting up proper SSL certificates before running on your machine.

Restart the contenerization engine:
```bash
sudo systemctl restart podman
# or
sudo systemctl restart docker
```

## Use it

### Push
```bash
podman images
podman tag localhost/example:latest HOSTNAME:5000/example:latest
podman push HOSTNAME:5000/example:latest
```

### Pull
```bash
podman pull HOSTNAME:5000/example:latest
podman images
```

---
[Back to main README](../README.md)
