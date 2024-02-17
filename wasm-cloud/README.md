# WASMCloud

wasmCloud helps you build and run globally distributed applications on any cloud and any edge.

Our goal is to make developers more productive by allowing them to write only the code that matters.

## Install the WashCLI

```bash
brew install wasmcloud/wasmcloud/wash
```

## Start WASH

```bash
wash up
```

## Open WASM cloud UI

- From different terminal

```bash
wash ui
```

- Explore the UI

```bash
open http://localhost:3030/
```

## Create the first WASMCloud app

- Create a new python application

```bash
wash new actor hello --template-name hello-world-python
```

- Check the new application directory

```bash
cd hello
```

- Review the files
- - app.py: Where the business logic is implemented
- - wasmcloud.toml: Actor metadata and capability permissions
- - wadm.yaml: A declarative manifest for running the full application

## Build the WASM application

- Install python components cli

```bash
pip install componentize-py
```

- Build using wash

```bash
wash build
```

## Deploy the applicaion

- Deploy using the wash command

```bash
wash app deploy wadm.yaml
```

- Check the UI

```bash
wash ui
```

- Find the actor you just deployed

```bash
open http://localhost:3030/
```
