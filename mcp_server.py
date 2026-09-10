import sys
import json
from client import ReedSolomonCodec

def main():
    rs = ReedSolomonCodec()
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        req = json.loads(line)
        method = req.get("method")
        params = req.get("params", {})
        if method == "encode":
            c = rs.encode(params.get("msg", []))
            res = {"codeword": c}
        elif method == "verify":
            syn = rs.verify_syndromes(params.get("codeword", []))
            res = {"syndromes": syn, "valid": all(s == 0 for s in syn)}
        else:
            res = {"error": "unknown method"}
        sys.stdout.write(json.dumps({"id": req.get("id"), "result": res}) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
