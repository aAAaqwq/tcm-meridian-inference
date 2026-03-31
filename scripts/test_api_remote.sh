#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:-http://100.104.252.33:18790}"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

PAYLOAD_FILE="$TMP_DIR/payload.json"
cat > "$PAYLOAD_FILE" <<'JSON'
{
  "subject": { "id": "demo-001", "name": "Daniel" },
  "measurements": {
    "liver": { "left": 40, "right": 70, "trendDelta": 30 },
    "spleen": { "left": 55, "right": 56, "trendDelta": 1 },
    "kidney": { "left": 42, "right": 68, "trendDelta": 26 },
    "stomach": { "left": 58, "right": 57, "trendDelta": -1 },
    "gallbladder": { "left": 41, "right": 69, "trendDelta": 28 },
    "bladder": { "left": 60, "right": 45, "trendDelta": -15 }
  }
}
JSON

request() {
  local method="$1"
  local path="$2"
  local data_file="${3:-}"
  local body_file="$TMP_DIR/body.json"
  local code

  if [[ -n "$data_file" ]]; then
    code=$(curl -sS -o "$body_file" -w "%{http_code}" -X "$method" \
      -H 'Content-Type: application/json' \
      --data @"$data_file" \
      "$BASE_URL$path" || true)
  else
    code=$(curl -sS -o "$body_file" -w "%{http_code}" -X "$method" \
      "$BASE_URL$path" || true)
  fi

  echo "HTTP $code  $method $path"
  cat "$body_file" 2>/dev/null || true
  echo
  echo "------------------------------"

  if [[ "$code" =~ ^2 ]]; then
    return 0
  fi
  return 1
}

echo "== TCM API 一键测试 =="
echo "BASE_URL=$BASE_URL"
echo

ok=0
fail=0

if request GET /health; then ((ok+=1)); else ((fail+=1)); fi
if request GET /healthz; then ((ok+=1)); else ((fail+=1)); fi
if request POST /test; then ((ok+=1)); else ((fail+=1)); fi
if request POST / "$PAYLOAD_FILE"; then ((ok+=1)); else ((fail+=1)); fi
if request POST /api/inference/meridian-diagnosis "$PAYLOAD_FILE"; then ((ok+=1)); else ((fail+=1)); fi

echo
printf 'RESULT: ok=%s fail=%s\n' "$ok" "$fail"

if [[ "$ok" -eq 0 ]]; then
  echo "结论：服务大概率不可用，或 URL/端口不对。"
  exit 2
fi

echo "结论：至少有一条接口链路可用。"
