# pygeoapi MapML integration

This repo holds a prototype implementation of a geospatial server based on
pygeoapi that is able to serve MapML resources.

This work came about during the 
[July 2024 OGC Open Standards Code Sprint](https://developer.ogc.org/sprints/24/).


## Running the demo

Create a suitable pygeoapi config

Start our pygeoapi-backed server:

```shell
export PYGEOAPI_CONFIG=mapml-prototype-config.yml 
export PYGEOAPI_OPENAPI=mapml-prototype-openapi.yml 

poetry run mapml-pygeoapi
```

Install the simple HTML client's dependencies (really only the MapML polyfill lib):

```shell
cd src/simple-html-client
npm install
```

Using another terminal, start the simple HTML client:

```shell
poetry run python -m http.server --directory src/simple-html-client 9000
```


## Generating demo slides

```shell
npx @marp-team/marp-cli@latest demo-slides/code-sprint-demo.md --allow-local-files -o sprint-demo.pdf
```