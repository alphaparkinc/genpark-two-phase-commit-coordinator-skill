"""MCP Server for GenPark Two-Phase Commit Coordinator.
100% Python Standard Library.
"""

import json
import sys
from client import TwoPhaseCommitCoordinator

coordinator = TwoPhaseCommitCoordinator()

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "register_participant",
                        "description": "Register an agent or service participant in the 2PC pool",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "participant_id": {"type": "string"}
                            },
                            "required": ["participant_id"]
                        }
                    },
                    {
                        "name": "begin_transaction",
                        "description": "Start a new 2PC transaction across all registered participants",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "tx_id": {"type": "string"},
                                "payload": {"type": "object"}
                            },
                            "required": ["tx_id"]
                        }
                    },
                    {
                        "name": "vote_transaction",
                        "description": "Submit a participant vote (YES/NO) on a pending transaction",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "tx_id": {"type": "string"},
                                "participant_id": {"type": "string"},
                                "vote_yes": {"type": "boolean"},
                                "reason": {"type": "string"}
                            },
                            "required": ["tx_id", "participant_id", "vote_yes"]
                        }
                    },
                    {
                        "name": "decide_transaction",
                        "description": "Reach final consensus and transition transaction to COMMITTED or ABORTED",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "tx_id": {"type": "string"}
                            },
                            "required": ["tx_id"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "register_participant":
            pid = args.get("participant_id")
            coordinator.register_participant(pid)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": f"Registered participant: {pid}"}]}
            }
        elif name == "begin_transaction":
            tx_id = args.get("tx_id")
            payload = args.get("payload", {})
            tx = coordinator.begin_transaction(tx_id, payload)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(tx, indent=2)}]}
            }
        elif name == "vote_transaction":
            tx_id = args.get("tx_id")
            pid = args.get("participant_id")
            v_yes = args.get("vote_yes", True)
            reason = args.get("reason", "")
            tx = coordinator.vote(tx_id, pid, v_yes, reason)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(tx, indent=2)}]}
            }
        elif name == "decide_transaction":
            tx_id = args.get("tx_id")
            tx = coordinator.decide(tx_id)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(tx, indent=2)}]}
            }

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
