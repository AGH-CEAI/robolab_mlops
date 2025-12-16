# robolab_mlops

Collection of all services used in Robotics Laboratory (mainly for the [Aegis robot](https://github.com/AGH-CEAI/aegis_ros)).

## List of services with their default ports

* ClearML - [clearml](http://localhost:8080)
* Containers registry - [containers_registry](http://localhost:5000)
* Portainer - [portainer](http://localhost:8999)
* PPA repository - [ppa_packages](http://localhost:80/debian)

**Before first run, be sure to read the whole README!**

## Start all services

```bash
# In the main directory
docker compose up -d
```

## Shutdown all services

```bash
# In the main directory
docker compose down
```

---

### Private Packages Repo (PPA)

You can find instructions for setting up a private repository [here](./ppa_packages/README.md).

**Adding private repo**
```bash
echo "deb [trusted=yes] http://192.168.0.100/debian ./" | tee -a /etc/apt/sources.list > /dev/null
```
### Containers registry

You can find instructions for using the self-hosted container registry [here](./containers_registry/README.md).

#### Building & pushing a particular release tag
```bash
export REGISTRY_HOSTNAME=geonosis:5000
export AEGIS_ROS_VERSION=<TAG>
export AEGIS_CONTAINER_VERSION=<TAG>

# if the building is happening on the same machine as PPA server, add argument:
# --add-host $(hostname):$(hostname -I | awk '{print $1}')
podman build . -t ceai/aegis_dev:${AEGIS_CONTAINER_VERSION} --build-arg AEGIS_ROS_TAG=${AEGIS_ROS_VERSION}
podman tag ceai/aegis_dev:${AEGIS_CONTAINER_VERSION} ${REGISTRY_HOSTNAME}/ceai/aegis:${AEGIS_CONTAINER_VERSION}
podman image inspect --format='{{json .Config.Labels}}' ${REGISTRY_HOSTNAME}/ceai/aegis:${AEGIS_CONTAINER_VERSION}

podman push ${REGISTRY_HOSTNAME}/ceai/aegis:${AEGIS_CONTAINER_VERSION}
```

#### Pulling & entering a particular release tag
```bash
export REGISTRY_HOSTNAME=geonosis:5000
export AEGIS_CONTAINER_VERSION=<TAG>

podman pull ${REGISTRY_HOSTNAME}/ceai/aegis:${AEGIS_CONTAINER_VERSION}
podman image inspect --format='{{json .Config.Labels}}' ${REGISTRY_HOSTNAME}/ceai/aegis:${AEGIS_CONTAINER_VERSION}

toolbox create --image ${REGISTRY_HOSTNAME}/ceai/aegis:${AEGIS_CONTAINER_VERSION}
toolbox enter aegis-${AEGIS_CONTAINER_VERSION}
```
