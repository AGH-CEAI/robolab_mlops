# robolab_mlops

Collection of all services used in Robotics Laboratory (mainly for the [Aegis robot](https://github.com/AGH-CEAI/aegis_ros)).

## List of services with their default ports

* [containers_registry](http://localhost:5000)
* [portainer](http://localhost:8999)
* [ppa_packages](http://localhost:80/debian)

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
