import argparse
import json
import os
import subprocess
import sys
from typing import List


def die(msg: str, code: int = 1) -> None:
    print(msg, file=sys.stderr)
    raise SystemExit(code)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Test classifier REST API via curl (HTTP Basic auth).",
    )
    p.add_argument(
        "-u",
        "--user",
        default=None,
        metavar="NAME",
        help="Django username (if omitted, uses DJANGO_USER from the environment).",
    )
    p.add_argument(
        "-p",
        "--password",
        default=None,
        metavar="PASS",
        help="Django password (if omitted, uses DJANGO_PASSWORD from the environment).",
    )
    p.add_argument(
        "--base-url",
        default=None,
        metavar="URL",
        help="API base URL (default: BASE_URL env or http://127.0.0.1:8000).",
    )
    p.add_argument(
        "--image-id",
        default=None,
        metavar="ID",
        help="TobaccoImage id for GET /api/images/<id>/ (default: API_TEST_IMAGE_ID env or 1).",
    )
    return p.parse_args()


def resolve_creds(args: argparse.Namespace) -> tuple[str, str]:
    user = (args.user if args.user is not None else os.environ.get("DJANGO_USER", "")).strip()
    password = (
        args.password if args.password is not None else os.environ.get("DJANGO_PASSWORD", "")
    )
    if not user or not password:
        die(
            "Missing credentials. Use either:\n"
            "  python scripts/test_api_curl.py -u USERNAME -p PASSWORD\n"
            "or set environment variables before running:\n"
            "  export DJANGO_USER=USERNAME DJANGO_PASSWORD=PASSWORD\n"
            "  python scripts/test_api_curl.py\n"
            "\n"
            "Optional: BASE_URL, or --base-url http://127.0.0.1:8000"
        )
    return user, password


def curl_get(base_url: str, user: str, password: str, path: str) -> subprocess.CompletedProcess[str]:
    url = base_url.rstrip("/") + path
    cmd: List[str] = [
        "curl",
        "-sS",
        "-w",
        "\n%{http_code}",
        "-u",
        f"{user}:{password}",
        "-H",
        "Accept: application/json",
        url,
    ]
    return subprocess.run(
        cmd,
        check=False,
        capture_output=True,
        text=True,
    )


def split_body_status(raw: str) -> tuple[str, str]:
    """curl -w adds final line with HTTP status code."""
    raw = raw.rstrip("\n")
    if "\n" not in raw:
        return raw, ""
    *body_lines, status = raw.rsplit("\n", 1)
    body = "\n".join(body_lines)
    return body, status.strip()


def pretty_print_json(body: str) -> None:
    try:
        data = json.loads(body)
        print(json.dumps(data, indent=2))
    except json.JSONDecodeError:
        print(body)


def main() -> None:
    args = parse_args()
    base = (args.base_url or os.environ.get("BASE_URL", "http://127.0.0.1:8000")).strip()
    user, password = resolve_creds(args)

    paths = [
        "/api/statistics/",
        "/api/grade-distribution/",
        "/api/price-history/",
        "/api/images/",
    ]

    print(f"BASE_URL={base}", file=sys.stderr)
    print(f"User={user}", file=sys.stderr)
    print("", file=sys.stderr)

    any_fail = False
    for path in paths:
        print(f"=== GET {path} ===")
        proc = curl_get(base, user, password, path)
        if proc.returncode != 0:
            print(proc.stderr or proc.stdout, end="")
            any_fail = True
            print()
            continue
        raw = proc.stdout
        body, status = split_body_status(raw)
        print(f"HTTP {status}")
        pretty_print_json(body)
        if status and not status.startswith("2"):
            any_fail = True
        print()

    if args.image_id is not None:
        detail_id = str(args.image_id).strip() or "1"
    else:
        detail_id = os.environ.get("API_TEST_IMAGE_ID", "1").strip() or "1"
    path = f"/api/images/{detail_id}/"
    print(f"=== GET {path} (override id: --image-id or API_TEST_IMAGE_ID) ===")
    proc = curl_get(base, user, password, path)
    raw = proc.stdout
    body, status = split_body_status(raw)
    print(f"HTTP {status}")
    pretty_print_json(body)
    if proc.returncode != 0 or (status and not status.startswith("2")):
        any_fail = True

    if any_fail:
        die("One or more requests failed.", 2)


if __name__ == "__main__":
    main()


'''

cd /home/karoi-scale/projects/Tobacco_Classifier_Pricing
export DJANGO_USER=dere DJANGO_PASSWORD=qwerty1234
export BASE_URL=http://127.0.0.1:8000   # optional
python scripts/test_api_curl.py

'''
#!/usr/bin/env python3
"""
Run classifier REST API checks by shelling out to curl.

Requires: curl on PATH, Django dev server running.

  python scripts/test_api_curl.py -u myuser -p mypass
  # or
  export DJANGO_USER=myuser DJANGO_PASSWORD=mypass
  python scripts/test_api_curl.py

Uses HTTP Basic auth (same as DRF BasicAuthentication).
"""
#from __future__ import annotations
