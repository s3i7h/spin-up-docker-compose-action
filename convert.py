import os.path
import sys
from typing import TypedDict, Optional, Dict, List

import yaml


class Build(TypedDict):
    context: str


class Service(TypedDict):
    image: Optional[str]
    build: Optional[Build]


class ComposeYml(TypedDict):
    services: Dict[str, Service]


def convert(context_name: str, compose: ComposeYml) -> ComposeYml:
    for name, service in compose["services"].items():
        if not service.get("build"):
            continue
        image_tag = f"{context_name}_{name}:latest"
        service["image"] = f"localhost:5000/{image_tag}"
    return compose


def main():
    if len(sys.argv) < 2:
        print("yaml filename is required")
        return sys.exit(1)
    _, filename, *_ = sys.argv
    try:
        with open(filename) as f:
            compose: ComposeYml = yaml.safe_load(f)
    except Exception as e:
        print(f"failed loading compose yaml: {e}")
        return sys.exit(1)

    abspath = os.path.abspath(filename)
    dirname = os.path.basename(os.path.dirname(abspath))
    compose = convert(dirname, compose)
    with open(filename, 'w') as f:
        yaml.dump(compose, f)


if __name__ == "__main__":
    main()
