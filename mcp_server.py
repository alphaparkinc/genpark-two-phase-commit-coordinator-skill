import sys
import json
from client import TwoPhaseCommitCoordinator

class SimpleParticipant:
    def prepare(self, tx_id, data): return True
    def commit(self, tx_id): pass
    def abort(self, tx_id): pass

def main():
    coord = TwoPhaseCommitCoordinator({"db1": SimpleParticipant(), "db2": SimpleParticipant()})
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        req = json.loads(line)
        method = req.get("method")
        params = req.get("params", {})
        if method == "execute":
            ok, status = coord.execute_transaction(params.get("tx_id"), params.get("data", {}))
            res = {"success": ok, "status": status}
        else:
            res = {"error": "unknown method"}
        sys.stdout.write(json.dumps({"id": req.get("id"), "result": res}) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
