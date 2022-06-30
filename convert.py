import os.path
import sys
from typing import TypedDict, Optional, Dict

import yaml


class Build(TypedDict):
    context: str


class Service(TypedDict):
    image: Optional[str]
    build: Optional[Build]


class ComposeYml(TypedDict):
    services: Dict[str, Service]


def convert(context_name: str, compose: ComposeYml, local: bool) -> ComposeYml:
    for name, service in compose["services"].items():
        if not service.get("build"):
            continue
        image_tag = f"{context_name}_{name}:latest"
        if "image" not in service:
            service["image"] = image_tag
        if local:
            service["image"] = f"localhost:5000/{image_tag}"
    return compose


def main():
    argc = len(sys.argv)
    if argc < 2:
        print("yaml filename is required")
        return sys.exit(1)
    if argc < 3:
        print("mode (remote|local) is required")
        return sys.exit(1)
    _, filename, mode, *_ = sys.argv

    if mode not in ("remote", "local"):
        print(f"mode must be one of `remote` or `local`: {mode} given")
    try:
        with open(filename) as f:
            compose: ComposeYml = yaml.safe_load(f)
    except Exception as e:
        print(f"failed loading compose yaml: {e}")
        return sys.exit(1)

    abspath = os.path.abspath(filename)
    dirname = os.path.basename(os.path.dirname(abspath))
    compose = convert(dirname, compose, mode == "local")
    with open(filename, 'w') as f:
        yaml.dump(compose, f)


if __name__ == "__main__":
    main()
