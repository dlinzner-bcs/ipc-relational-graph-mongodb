# iPC relational graph

Package to organize relational graphs in the iPC projects.

## development setup

### setup a `venv`

Create and activate a `venv`:

```sh
python3 -m venv venv
source venv/bin/activate
```

### install dependencies

Install package dependencies:

```sh
pip install -r requirements.txt
```

Install packages used for styling and development:

```sh
pip install -r dev_requirements.txt
```

Install the package in editable mode:

```sh
pip install -e .
```

### run db and cos using `docker-compose`

To spawn the services just run:

```sh
docker-compose -f docker/docker-compose.yml up -d
```

To tear them down run:

```sh
docker-compose -f docker/docker-compose.yml down
```

**NOTE:** the data in the containers are not persisted on a physical volume. In order to store data volumes should be configured an mounted.