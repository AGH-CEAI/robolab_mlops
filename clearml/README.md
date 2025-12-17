# ClearML

Deploy instructions can be found in the [official docs](https://clear.ml/docs/latest/docs/deploying_clearml/clearml_server_linux_mac).

## Highlight
Before first run you need to create all catalogs and setup the Elasticsearch params:

```bash
echo "vm.max_map_count=524288" > /tmp/99-clearml.conf
sudo mv /tmp/99-clearml.conf /etc/sysctl.d/99-clearml.conf
sudo sysctl -w vm.max_map_count=524288
sudo service docker restart
```

Please continue the setup procedure for:
* [Web Login Authentication](https://clear.ml/docs/latest/docs/deploying_clearml/clearml_server_config#web-login-authentication)
* [Hashing passwords](https://clear.ml/docs/latest/docs/deploying_clearml/clearml_server_config#using-hashed-passwords)
* [Removing Fileserver Artifacts for Deleted Tasks](https://clear.ml/docs/latest/docs/deploying_clearml/clearml_server_config#removing-fileserver-artifacts-for-deleted-tasks)
