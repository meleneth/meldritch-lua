# meldritch-lua

Independent musical applications and reusable author-side Lua libraries for
Meldritch. This repository consumes the public Lua host contract and contains
no Rust implementation or runtime bootstrap code.

## Validate and test

```sh
make check
```

This validates every `application.json`, checks all Lua syntax, exercises the
contract-derived mock discovery API, and unit-tests the reusable arpeggiator.
Only Python 3 and Lua 5.4 are required; no Rust checkout or build is needed.
LuaLS annotations are in `types/meldritch.lua`.

## Run an application

Pass either an application directory or a direct Lua entry to an already-built
compatible engine:

```sh
meldritch perform applications/groovebox
meldritch perform /unrelated/path/to/meldritch-lua/applications/serum-playground
```

The engine validates the manifest's host API range, capabilities, and declared
libraries before evaluating the entry script. Configure it with
`MELDRITCH_LUA_CATALOG=/absolute/path/to/libraries/catalog.json`; the integrated
runner does this automatically. Relative includes resolve from the application
directory. Optional devices, plugins, assets, and environment requirements are
declared in each manifest.

`applications/` contains independently loadable applications. `libraries/`
contains author-side musical behavior. `examples/` contains lower-level engine
and authoring examples; those are syntax checked but are not release apps.

## Contract updates

`contracts.lock` pins an immutable `meldritch-contracts` revision and artifact
digest. `contract/api.yaml`, `schemas/application.schema.json`, and
`types/meldritch.lua` must be copied from that exact release. Run `make check`
after an update. New application behavior may use only capabilities declared by
the pinned manifest; adding behavior within those capabilities does not require
Rust source access or a rebuild.
