# BuildPacks

A buildpack is something you’ve probably used without knowing it, as they’re currently being used in many cloud platforms. A buildpack’s job is to gather everything your app needs to build and run, and it often does this job quickly and quietly.

That said, while buildpacks are often a behind-the-scenes detail, they are at the heart of transforming your source code into a runnable app image.

## Install BuildPacks

- Install BuildPacks pack cli

```bash
MAC:
brew install buildpacks/tap/pack

Linux:
sudo add-apt-repository ppa:cncf-buildpacks/pack-cli
sudo apt-get update
sudo apt-get install pack-cli
```

## Build Python Image

- Check Suggested Images

```bash
pack build sample-python-app --path python-app
```

- Build using a builder

```bash
pack build sample-python-app --path python-app --builder paketobuildpacks/builder-jammy-base
```

- run the image

```bash
docker run --rm -p 8080:8080 sample-python-app
```

## Build Go Image

```bash
pack build sample-go-app --path go-app
```

- Build using a builder

```bash
pack build sample-go-app --path go-app --builder paketobuildpacks/builder-jammy-base
```

- run the image

```bash
docker run --rm -p 8080:8080 sample-go-app
```
