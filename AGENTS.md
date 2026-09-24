# AGENTS.md

This repository contains the snap packaging (and colocated YARF UI tests) for
the **lunar-client** snap, published by kenvandine.

## Automated maintenance

This repository is maintained in part by the `automated-ken` fleet-maintenance
system (https://github.com/kenvandine/automated-ken). Automated agents may:

- Open pull requests bumping the packaged application/runtime version
- Queue YARF UI test runs on a registered remote runner (real hardware polling the
  automated-ken dashboard for jobs) against candidate/edge builds before promoting a
  release
- Review and comment on PRs, including AI-assisted screenshot review of UI test
  results

## Tests

YARF UI test suites belong under `tests/suite/` in this repository. They are
executed by a registered remote runner (physical/real hardware enrolled with the
automated-ken dashboard), which polls the dashboard for queued jobs, downloads/
installs the target snap build, runs the YARF suite locally, and uploads
screenshots/results directly back to the dashboard. No GitHub Actions workflow is
involved in running tests.

## Conventions

- Do not remove the `tests/suite/` directory; it is required for automated release
  validation. There is no test-running GitHub Actions workflow in this repo by
  design — tests run on a registered remote runner.
- Redundant upstream-polling / sync-release workflows that duplicate automated-ken's
  own version-bump automation should be removed to avoid conflicting/duplicate PRs.

## Upstream release detection

Lunar Client is closed-source with no public GitHub repository or
releases feed — automated-ken's generic GitHub/GitLab/PyPI/Launchpad
upstream checkers **do not apply** here. The upstream download endpoint
must be queried directly:

1. Resolve the redirect target of
   `https://api.lunarclientprod.com/site/download?os=linux`, e.g.:
   `curl -sIL -o /dev/null -w '%{url_effective}' "https://api.lunarclientprod.com/site/download?os=linux"`
2. Extract the version from the resulting URL, which looks like
   `.../Lunar%20Client-<VERSION>-ow...` — the version is the
   `[0-9.]+` sequence immediately following `Lunar%20Client-`.
3. Compare against the **currently published edge-channel snap
   version** (not any value stored in this repo) via the Snap Store API:
   `curl -s -H "Snap-Device-Series: 16" https://api.snapcraft.io/v2/snaps/info/lunar-client`,
   reading
   `.["channel-map"][] | select(.channel.name=="edge" and .channel.architecture=="amd64") | .version`.
4. If the two differ, a new upstream build is available. There is no
   `version:` field to bump in `snap/snapcraft.yaml` for this snap —
   instead, trigger this repo's `snap.yaml` build workflow, which
   downloads and repackages the latest AppImage at build time.

This is a fully custom check outside automated-ken's generic upstream
scanner (`snap_dashboard.snapcraft.upstream.get_latest_version`); it
cannot be automated without a dedicated Lunar Client checker.
