# Physical Systems Node releases

This public repository contains **release tooling only**. It does not contain
the private managed Node repository, source archives, credentials, hardware
configuration, or private CI reports. It does not build Node from source.

The separately downloadable `physicalsystems-node` preview contains 26
explicitly selected physical-host Python modules plus a minimal initializer.
Python wheels contain readable source; this is a licensing/distribution
boundary, not source-code concealment. The wheel remains proprietary under
its included [preview notice](policy/node-preview-notice.txt). The new release
tooling in this repository is Apache-2.0, under [LICENSE](LICENSE); that license
does not relicense the Node wheel or its dependencies. Runtime, NumPy and
OpenCV remain separate distributions under their own licenses.

## Promotion boundary

1. An authorized operator verifies the private main candidate, its package
   allowlist and complete private test evidence locally. The private exporter
   emits only the approved wheel and canonical `release.json`. Neither the
   private exporter nor its source/evidence is uploaded here.
2. The operator stages a **draft GitHub release targeting `main`** here, with
   exactly those two assets, and reviews the raw SHA-256 of `release.json`.
   GitHub asset metadata must expose matching SHA-256 and size. Assets are not
   committed to Git. Only bytes approved for the public distribution may be
   staged: Actions logs and artifacts in this repository are public.
3. Manually dispatch `publish.yml` on this repository's current `main`, passing
   `candidate_release_id` and `release_metadata_sha256`. The workflow reads only
   this repository and anonymous official PyPI endpoints. It has no private
   repository credential or access requirement.
4. The exact pinned wheel and dependencies pass six fresh isolated installs:
   Ubuntu 22.04 and Windows 2022, each with CPython 3.10, 3.11 and 3.12. Fetching
   happens in a separate authenticated step; installed code receives no
   repository or publishing credential. Tests check installation identity,
   Runtime/NumPy/OpenCV imports and a tiny in-memory image conversion. They do
   not discover devices, import camera/motion code, capture, or move hardware.
5. The `physical-node-pypi` environment requires a named human reviewer and
   exact custom branch policy `main` (type `branch`), with admin bypass disabled.
   Repository variable `PHYSICAL_NODE_PUBLISH_POLICY` must equal
   `v1-minimal-node-preview`. A founder may dispatch and personally approve;
   automated approval is not implemented. No step modifies these settings.
6. After human approval, the workflow rechecks current main, exact draft
   asset bytes, all six same-run/current-attempt successful job receipts, and
   every dependency's public unyanked hash/URL. OIDC publishes **one prebuilt
   minimal wheel**, not an sdist, Runtime wheel, private report or source archive.
   Configure the PyPI Trusted Publisher separately for this repository,
   `publish.yml`, and environment `physical-node-pypi` before dispatch.
7. Anonymous PyPI readback must match the exact uploaded bytes. Only then are
   six genuine `physicalsystems-node-install-v1` manifests emitted as public
   Actions artifacts. Only readback is retried for brief registry propagation;
   upload is never retried or silently skipped. Review a failed upload/readback
   before deciding what to do next.

If any prerequisite is absent, promotion fails closed. A draft or a successful
test run is not evidence that a package is already published. Installing this
experimental preview never authorizes physical execution or certifies safety.

## Capsule v1

Canonical JSON uses sorted keys, compact separators, ASCII escapes, finite
values, UTF-8 and **no trailing newline**. Unknown or duplicate fields fail.

```text
contractVersion = "physicalsystems-node-release-capsule-v1"
distribution = "physicalsystems-node"
version = "0.2.0"
runtimeVersion = "0.2.0"
sourceManifestSha256 = SHA256(canonical embedded package source manifest)
wheel = {filename, sha256, bytes}
targets = [{platform, python, publicDependencies: [{name, version, filename,
                                                  sha256, bytes, url}]}]
```

There must be exactly six unique targets (`linux-x64`/`win32-x64` ×
`3.10`/`3.11`/`3.12`) and exactly three dependency records per target:
`tinyedge-runtime==0.2.0`, `numpy==1.26.4`, and
`opencv-python-headless==4.10.0.84`. Wheels must be compatible with their target;
URLs must be exact credential-free `files.pythonhosted.org` URLs. Runtime's
approved wheel SHA is pinned in the verifier; a rebuild with another hash does
not satisfy this gate. Metadata contains no private commit/run/repository URLs,
raw reports, signatures of invented authority, local paths, or Node URL
placeholder. The source-manifest fingerprint identifies only included files.

The capsule itself is not an installer manifest. Public install manifests are
created only after the real Node PyPI URL is verified. The trust chain is the
operator's explicit metadata pin, inspected wheel contents, fresh public CI,
human-protected promotion and final exact public readback. This repository does
not claim independently to have observed the private CI proof.

## Local regression tests

```sh
python -m pip install packaging==26.3 pytest==8.4.2
python -m pytest -q tests
```

These tests use synthetic in-memory package fixtures and mocked registries;
they do not publish, require credentials, discover devices or open hardware.
Generated wheelhouses/venvs and private evidence belong outside source control.
Windows install probes use a short temporary path and reject environment roots
over 126 characters to leave margin for native wheel DLL paths. `pip check`
alone cannot establish that a native module will load.
