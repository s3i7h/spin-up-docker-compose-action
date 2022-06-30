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


def add_image_tag(context_name: str, compose: ComposeYml) -> ComposeYml:
    for name, service in compose["services"].items():
        if not service.get("build"):
            continue
        image_tag = f"{context_name}_{name}:latest"
        if "image" not in service:
            service["image"] = image_tag
    return compose


def replace_image_tag_to_local(context_name: str, compose: ComposeYml) -> ComposeYml:
    for name, service in compose["services"].items():
        if not service.get("build"):
            continue
        image_tag = f"{context_name}_{name}:latest"
        service["image"] = f"localhost:5000/{image_tag}"
    return compose


def main():
    argc = len(sys.argv)
    if argc < 2:
        print("command name is required")
        return sys.exit(1)
    if argc < 3:
        print("yaml filename is required")
        return sys.exit(1)
    _, command, filename, *_ = sys.argv

    commands = dict(
        add_image_tag=add_image_tag,
        localhost=replace_image_tag_to_local
    )

    if command not in commands:
        print(f"command must be one of ({', '.join(commands)}): {command}")
        return sys.exit(1)


    try:
        with open(filename) as f:
            compose: ComposeYml = yaml.safe_load(f)
    except Exception as e:
        print(f"failed loading compose yaml: {e}")
        return sys.exit(1)

    abspath = os.path.abspath(filename)
    dirname = os.path.basename(os.path.dirname(abspath))
    compose = commands[command](dirname, compose)
    with open(filename, 'w') as f:
        yaml.dump(compose, f)


if __name__ == "__main__":
    main()
