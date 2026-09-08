"""Centralized KryptonPlay application version."""

# Semantic Versioning: MAJOR.MINOR.PATCH
#
# MAJOR: incompatible architecture/protocol changes.
# MINOR: backward-compatible features.
# PATCH: backward-compatible fixes.
VERSION = "0.1.0"


def version_info() -> dict[str, str]:
    major, minor, patch = VERSION.split(".")
    return {"version": VERSION, "major": major, "minor": minor, "patch": patch}
