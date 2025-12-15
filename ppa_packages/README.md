# Private Packages Repo (PPA)

This module enables storing private *.deb packages used for automated container built.

More [here](https://linuxconfig.org/easy-way-to-create-a-debian-package-and-local-package-repository).

## Preparing packages

**Copy packages:**

Copy all `*.deb` packages into the `./packages` directory.

**Generate package list:**

* After moving all packages to the `./packages` directory, you need to generate the **package list**.
* On a Debian-based system (e.g., Ubuntu), run the following command inside the `./packages` directory.
    * There is **no need** to run this inside the container.
```bash
dpkg-scanpackages . | gzip -c9  > Packages.gz
```
or
```bash
sudo sh -c 'dpkg-scanpackages . /dev/null | gzip -9c > Packages.gz'
```

* Done! The PPA server is now ready to serve packages.

## Running Server

**Docker Compose**:
```bash
docker compose up -d
```
You can check the PPA in your webbrowser: `http://HOST/debian/`.

### Adding new packages

Follow `Preparing packages` step and the list of packages will automatically update.

---
[Back to main README](../README.md)
