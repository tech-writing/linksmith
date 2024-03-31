(development)=
(development-sandbox)=
(sandbox)=

# Development Sandbox


## Setup
Those commands will get you started with a sandboxed development environment.
After invoking `poe check`, and observing the software tests succeed, you
should be ready to start hacking.

```shell
git clone https://github.com/tech-writing/linksmith
cd linksmith
python3 -m venv .venv
source .venv/bin/activate
pip install --editable=.[develop,docs,test]
poe check
```


## Software tests

For running the software tests after setup, invoke `poe check`.
Optionally, activate the virtualenv, if you are coming back to
development using a fresh terminal session.

```shell
source .venv/bin/activate
poe check
```


## Documentation

In order to build the documentation, invoke `poe docs-html`.
```shell
poe docs-html
```

In order to _continuously_ rebuild the documentation, while editing it,
invoke `poe docs-autobuild`.
```shell
poe docs-autobuild
```


## Releasing

```shell
# Install a few more prerequisites.
pip install --editable=.[release]

# Designate a new version.
git tag v0.1.0
git push --tags

# Build package, and publish to PyPI.
poe release
```
