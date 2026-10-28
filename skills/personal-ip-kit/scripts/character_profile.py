#!/usr/bin/env python3
"""Initialize and validate local character profiles; never generate or upload art."""
import argparse
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import tempfile

from PIL import Image


def identity(value):
    if not isinstance(value, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value) or len(value) > 64:
        raise ValueError("Character id must be lowercase letters/digits with single hyphens (max 64).")
    return value


def safe_file(root, value):
    if not isinstance(value, str) or not value:
        raise ValueError("Expected a nonempty relative file path.")
    relative = PurePosixPath(value)
    if relative.is_absolute() or ".." in relative.parts or "\\" in value or ":" in value:
        raise ValueError("Path must stay within its root: " + value)
    resolved = (root / value).resolve()
    if not resolved.is_relative_to(root.resolve()) or not resolved.is_file():
        raise ValueError("Missing file or path outside root: " + value)
    return resolved


def image_file(path):
    with Image.open(path) as im:
        im.verify()


def validate(profile_path):
    profile_path = Path(profile_path).resolve()
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    if not isinstance(profile, dict) or type(profile.get("schemaVersion")) is not int or profile["schemaVersion"] != 1:
        raise ValueError("Expected character schemaVersion 1.")
    identity(profile.get("id"))
    if not isinstance(profile.get("name"), str) or not profile["name"].strip():
        raise ValueError("Character name is required.")
    if not isinstance(profile.get("version"), str) or not profile["version"].strip():
        raise ValueError("Character version is required.")
    if profile.get("status") not in {"draft", "working", "approved"}:
        raise ValueError("Status must be draft, working or approved.")
    if profile.get("subjectType") not in {"person", "animal", "plant", "fruit", "object", "other"}:
        raise ValueError("Unknown subjectType.")
    for key in ("fixedTraits", "variableTraits", "designAssumptions"):
        values = profile.get(key)
        if not isinstance(values, list) or any(not isinstance(x, str) or not x.strip() for x in values):
            raise ValueError(key + " must be a list of nonempty strings.")
    refs = profile.get("referenceImages")
    if not isinstance(refs, list) or not refs:
        raise ValueError("At least one identity reference is required.")
    root = profile_path.parent
    for ref in refs:
        image_file(safe_file(root, ref))
    if profile.get("masterReference") is not None:
        image_file(safe_file(root, profile["masterReference"]))
    elif profile["status"] != "draft":
        raise ValueError("Working/approved profiles require masterReference.")
    if profile.get("brandGuide") is not None:
        safe_file(root, profile["brandGuide"])
    assets = profile.get("assets")
    if not isinstance(assets, list):
        raise ValueError("assets must be a list.")
    seen = set()
    for asset in assets:
        if not isinstance(asset, dict):
            raise ValueError("Each asset must be an object.")
        key = identity(asset.get("id"))
        if key in seen:
            raise ValueError("Duplicate asset id: " + key)
        seen.add(key)
        safe_file(root, asset.get("path"))
        if "alpha" in asset and not isinstance(asset["alpha"], bool):
            raise ValueError("Asset alpha must be boolean.")
    return profile


def initialize(character_id, name, references, output):
    identity(character_id)
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Character name is required.")
    if not references:
        raise ValueError("Provide at least one reference image.")
    sources = [Path(p).resolve() for p in references]
    for source in sources:
        image_file(source)
    output = Path(output).absolute()
    if output.exists() or output.is_symlink():
        raise ValueError("Output already exists; use a new character directory.")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".character-", dir=output.parent) as temporary:
        stage = Path(temporary)
        (stage / "reference").mkdir()
        refs = []
        for i, source in enumerate(sources, 1):
            relative = f"reference/original-{i:02d}{source.suffix.lower()}"
            shutil.copy2(source, stage / relative)
            refs.append(relative)
        profile = dict(schemaVersion=1, id=character_id, name=name.strip(), version="1.0",
                       status="draft", subjectType="other", referenceImages=refs,
                       masterReference=None, brandGuide=None, fixedTraits=[],
                       variableTraits=[], designAssumptions=[], assets=[])
        (stage / "character.json").write_text(json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        validate(stage / "character.json")
        output.mkdir()  # Exclusive reservation: never overwrite another invocation.
        for item in stage.iterdir():
            shutil.move(str(item), str(output / item.name))
    return output / "character.json"


def resolve(project, character_id=None):
    project = Path(project).resolve()
    registry_path = safe_file(project, ".ip-characters/index.json")
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    if not isinstance(registry, dict) or type(registry.get("schemaVersion")) is not int or registry["schemaVersion"] != 1:
        raise ValueError("Expected registry schemaVersion 1.")
    entries = registry.get("characters")
    if not isinstance(entries, list) or not entries:
        raise ValueError("No registered characters.")
    by_id = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("Each registry entry must be an object.")
        key = identity(entry.get("id"))
        if key in by_id:
            raise ValueError("Duplicate registry id: " + key)
        by_id[key] = entry.get("profile")
    default_id = registry.get("defaultId")
    if default_id is not None and (not isinstance(default_id, str) or default_id not in by_id):
        raise ValueError("Registry defaultId does not exist.")
    selected = character_id if character_id is not None else default_id
    if selected is None:
        if len(by_id) != 1:
            raise ValueError("Choose a character id: " + ", ".join(by_id))
        selected = next(iter(by_id))
    if selected not in by_id:
        raise ValueError("Requested character is not registered: " + str(selected))
    path = safe_file(project, by_id[selected])
    profile = validate(path)
    if profile["id"] != selected:
        raise ValueError("Registry id does not match profile id.")
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init")
    init.add_argument("--id", required=True)
    init.add_argument("--name", required=True)
    init.add_argument("--reference", action="append", required=True)
    init.add_argument("--output", required=True)
    check = commands.add_parser("validate")
    check.add_argument("profile")
    select = commands.add_parser("resolve")
    select.add_argument("--project", required=True)
    select.add_argument("--id")
    args = parser.parse_args()
    try:
        if args.command == "init":
            result = {"profile": str(initialize(args.id, args.name, args.reference, args.output)), "status": "draft"}
        elif args.command == "resolve":
            result = {"profile": str(resolve(args.project, args.id))}
        else:
            p = validate(args.profile)
            result = dict(id=p["id"], version=p["version"], status=p["status"], filesValid=True,
                          note="File validation does not verify visual identity or user approval.")
        print(json.dumps(result, ensure_ascii=False))
    except (ValueError, TypeError, KeyError, OSError) as error:
        parser.exit(1, str(error) + "\n")


if __name__ == "__main__":
    main()
