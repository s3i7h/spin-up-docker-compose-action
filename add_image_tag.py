import os.path
import sys
from typing import TypedDict, Optional

import json


class Target(TypedDict):
    tags: Optional[list[str]]


class BuildManifest(TypedDict):
    target: dict[str, Target]


def add_tag(context_name: str, manifest: BuildManifest) -> BuildManifest:
    for name, target in manifest["target"].items():
        image_tag = f"{context_name}_{name}:latest"
        target["tags"] = target.get("tags", []) + [image_tag]
    return manifest


def main():
    if len(sys.argv) < 2:
        print("yaml filename is required")
        return sys.exit(1)
    _, filename, *_ = sys.argv
    try:
        with open(filename) as f:
            manifest: BuildManifest = json.load(f)
    except Exception as e:
        print(f"failed loading build manifest: {e}")
        return sys.exit(1)

    abspath = os.path.abspath(filename)
    dirname = os.path.basename(os.path.dirname(abspath))
    manifest = add_tag(dirname, manifest)
    with open(filename, 'w') as f:
        json.dump(manifest, f)


if __name__ == "__main__":
    main()
