# Building Resource Gather

`Resource Gather` ships as a PyInstaller-frozen executable (`ResourceGather.exe`)
and also runs directly from source.

## From source (recommended for development)

```bash
pip install -r requirements.txt
python main.py --selftest        # verify config + data + generated functions
python main.py --search "acme corp"
python main.py --gui             # optional Tkinter UI
```

## Build the standalone executable

```bash
pip install pyinstaller
pyinstaller build.spec
# -> dist/ResourceGather/ResourceGather.exe
```

`build.spec` bundles `config/` and `data/` as read-only assets (resolved at
runtime through `core.config_loader` via `sys._MEIPASS` when frozen). Generated
functions in `core.sources` are built at runtime, so no extra bundling is needed.
Writable output (`findings.csv`, `snapshots/`, `output/`) is written next to the
executable.

## One-file build (alternative)

```bash
pyinstaller --onefile --name ResourceGather ^
  --add-data "config;config" --add-data "data;data" main.py
```

## Verifying the build

```bash
dist/ResourceGather/ResourceGather.exe --selftest
dist/ResourceGather/ResourceGather.exe --count
```

## CI

`.github/workflows/ci.yml` installs dependencies, runs `python main.py --selftest`
and `python main.py --count`, and builds the executable on every push/PR.
