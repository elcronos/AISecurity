#!/bin/bash
set -e

OLLAMA_URL="${OLLAMA_BASE_URL:-http://ollama:11434}"
MODEL="${MODEL_NAME:-llava:7b}"

echo "⏳  Waiting for Ollama at $OLLAMA_URL ..."
until curl -sf "$OLLAMA_URL/api/tags" > /dev/null 2>&1; do
    printf '.'
    sleep 3
done
echo ""
echo "✅  Ollama is ready"

echo "🔍  Checking model: $MODEL"
EXISTS=$(curl -s "$OLLAMA_URL/api/tags" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    names = [m['name'] for m in data.get('models', [])]
    base = '$MODEL'.split(':')[0]
    print('yes' if any(base in n for n in names) else 'no')
except:
    print('no')
")

if [ "$EXISTS" = "no" ]; then
    echo "📥  Pulling $MODEL — this may take several minutes on first run (~4.7 GB)..."
    curl -s -X POST "$OLLAMA_URL/api/pull" \
         -H "Content-Type: application/json" \
         -d "{\"name\": \"$MODEL\"}" \
         --no-buffer | python3 -c "
import sys, json
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        d = json.loads(line)
        status = d.get('status', '')
        total  = d.get('total', 0)
        compl  = d.get('completed', 0)
        if total and compl:
            pct = int(compl / total * 100)
            print(f'  {status} — {pct}%', flush=True)
        elif status:
            print(f'  {status}', flush=True)
    except:
        pass
"
    echo "✅  Model ready"
else
    echo "✅  Model $MODEL already available"
fi

echo ""
echo "🚀  Starting VistaGuard Multimodal Security Lab on http://0.0.0.0:8080 ..."
exec uvicorn main:app --host 0.0.0.0 --port 8080 --workers 1
