#!/usr/bin/env bash
# Test classifier REST API with curl.
# Requires a Django user (staff not required). APIs use IsAuthenticated.
#
# Usage:
#   export DJANGO_USER=myuser DJANGO_PASSWORD=mypass
#   export BASE_URL=http://127.0.0.1:8000   # optional
#   ./scripts/test_api.sh basic            # HTTP Basic (simplest)
#   ./scripts/test_api.sh session         # login form + session cookie
#
# Optional: pipe through jq for pretty JSON:
#   ./scripts/test_api.sh basic | jq .

set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:8000}"
MODE="${1:-basic}"

die() { echo "error: $*" >&2; exit 1; }

require_creds() {
  [[ -n "${DJANGO_USER:-}" ]] && [[ -n "${DJANGO_PASSWORD:-}" ]] \
    || die "set DJANGO_USER and DJANGO_PASSWORD"
}

pretty() {
  if command -v jq >/dev/null 2>&1; then
    jq .
  else
    cat
  fi
}

api_basic() {
  local path="$1"
  curl -sS -u "${DJANGO_USER}:${DJANGO_PASSWORD}" \
    -H "Accept: application/json" \
    "${BASE_URL}${path}"
}

api_session() {
  local path="$1"
  curl -sS -b "${COOKIE_JAR}" -c "${COOKIE_JAR}" \
    -H "Accept: application/json" \
    "${BASE_URL}${path}"
}

login_session() {
  COOKIE_JAR="$(mktemp)"
  export COOKIE_JAR
  trap 'rm -f "${COOKIE_JAR}"' EXIT

  local login_html csrf
  login_html="$(mktemp)"
  curl -sS -c "${COOKIE_JAR}" "${BASE_URL}/accounts/login/" -o "${login_html}"

  csrf="$(sed -n 's/.*name="csrfmiddlewaretoken" value="\([^"]*\)".*/\1/p' "${login_html}" | head -1)"
  rm -f "${login_html}"
  [[ -n "${csrf}" ]] || die "could not parse CSRF token from login page"

  code="$(curl -sS -b "${COOKIE_JAR}" -c "${COOKIE_JAR}" -X POST "${BASE_URL}/accounts/login/" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -H "Referer: ${BASE_URL}/accounts/login/" \
    --data-urlencode "username=${DJANGO_USER}" \
    --data-urlencode "password=${DJANGO_PASSWORD}" \
    --data-urlencode "csrfmiddlewaretoken=${csrf}" \
    -o /dev/null -w '%{http_code}')"
  [[ "${code}" == "302" || "${code}" == "200" ]] \
    || die "login failed (HTTP ${code}; check user/password and BASE_URL)"
}

run_tests() {
  echo "=== GET /api/statistics/ ==="
  curl_api /api/statistics/ | pretty
  echo
  echo "=== GET /api/grade-distribution/ ==="
  curl_api /api/grade-distribution/ | pretty
  echo
  echo "=== GET /api/price-history/ ==="
  curl_api /api/price-history/ | pretty
  echo
  echo "=== GET /api/images/ (first page) ==="
  curl_api /api/images/ | pretty
  echo
  echo "=== GET /api/images/1/ (adjust id if missing) ==="
  curl_api /api/images/1/ | pretty || true
  echo
}

case "${MODE}" in
  basic)
    require_creds
    curl_api() { api_basic "$@"; }
    run_tests
    ;;
  session)
    require_creds
    login_session
    curl_api() { api_session "$@"; }
    run_tests
    ;;
  -h|--help|help)
    sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'
    exit 0
    ;;
  *)
    die "usage: $0 basic|session"
    ;;
esac
