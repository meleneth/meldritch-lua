#!/usr/bin/env python3
"""Validate pinned contract metadata and every application manifest."""

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: Path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def fail(message: str) -> None:
    print(f"contract validation: {message}", file=sys.stderr)
    raise SystemExit(1)


lock = load(ROOT / "contracts.lock")
api_path = ROOT / "contract/api.yaml"
api = load(api_path)
if api["version"] != lock["lua_host_api"]:
    fail("contract/api.yaml does not match contracts.lock")

annotation = (ROOT / "types/meldritch.lua").read_text(encoding="utf-8")
source_digest = hashlib.sha256(api_path.read_bytes()).hexdigest()
if f"Contract: meldritch-lua-host-api {api['version']}" not in annotation:
    fail("Lua annotations have the wrong contract version")
if f"Source: lua/api.yaml sha256:{source_digest}" not in annotation:
    fail("Lua annotations are stale")

capabilities = {item["id"] for item in api["capabilities"]}
catalog = load(ROOT / "libraries/catalog.json")
if catalog.get("catalog_version") != 1:
    fail("libraries/catalog.json has unsupported catalog_version")
catalog_libraries = {}
for item in catalog.get("libraries", []):
    identifier = item.get("id", "")
    if identifier in catalog_libraries:
        fail(f"duplicate library {identifier}")
    if not re.fullmatch(r"[a-z][a-z0-9-]*(\.[a-z][a-z0-9-]*)+", identifier):
        fail(f"invalid library identifier {identifier!r}")
    entry = Path(item.get("entry", ""))
    if entry.is_absolute() or len(entry.parts) != 1 or entry.suffix != ".lua":
        fail(f"{identifier}: unsafe library entry")
    source = ROOT / "libraries" / entry
    if not source.is_file():
        fail(f"{identifier}: missing {entry}")
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    if digest != item.get("sha256"):
        fail(f"{identifier}: sha256 mismatch")
    if item.get("lua_host_api", "").replace(" ", "") != ">=1.0.0<2.0.0":
        fail(f"{identifier}: unsupported host API range")
    catalog_libraries[identifier] = item
allowed = {
    "name", "version", "entry", "lua_host_api", "capabilities",
    "libraries", "assets", "requirements",
}
manifests = sorted((ROOT / "applications").glob("*/application.json"))
directories = sorted(path for path in (ROOT / "applications").iterdir() if path.is_dir())
if len(manifests) != len(directories):
    fail("every application directory must contain application.json")

for path in manifests:
    manifest = load(path)
    unknown = set(manifest) - allowed
    if unknown:
        fail(f"{path}: unknown fields {sorted(unknown)}")
    for field in ("name", "version", "entry", "lua_host_api", "capabilities"):
        if field not in manifest:
            fail(f"{path}: missing {field}")
    if not re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"]):
        fail(f"{path}: version is not semantic")
    if manifest["lua_host_api"].replace(" ", "") not in {"1.0.0", "1", "^1", ">=1.0.0<2.0.0"}:
        fail(f"{path}: unsupported Lua host API range")
    required = manifest["capabilities"]
    if len(required) != len(set(required)):
        fail(f"{path}: duplicate capabilities")
    missing = set(required) - capabilities
    if missing:
        fail(f"{path}: unknown capabilities {sorted(missing)}")
    requested_libraries = manifest.get("libraries", [])
    if len(requested_libraries) != len(set(requested_libraries)):
        fail(f"{path}: duplicate libraries")
    missing_libraries = set(requested_libraries) - set(catalog_libraries)
    if missing_libraries:
        fail(f"{path}: unknown libraries {sorted(missing_libraries)}")
    relative = Path(manifest["entry"])
    if relative.is_absolute() or ".." in relative.parts or relative.suffix != ".lua":
        fail(f"{path}: unsafe entry")
    if not (path.parent / relative).is_file():
        fail(f"{path}: missing entry {relative}")
    for asset in manifest.get("assets", []):
        if not (path.parent / asset).is_file():
            fail(f"{path}: missing asset {asset}")

print(
    f"validated Lua contract {api['version']}, {len(catalog_libraries)} libraries, "
    f"and {len(manifests)} applications"
)
