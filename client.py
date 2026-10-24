"""Two-Phase Commit (2PC) Transaction Coordinator.
100% Python Standard Library.
"""

from typing import Dict, List, Any, Optional

class TwoPhaseCommitCoordinator:
    """Atomic multi-agent distributed transaction coordinator enforcing 2PC protocol."""

    def __init__(self):
        self.transactions: Dict[str, Dict[str, Any]] = {}
        self.participants: set = set()

    def register_participant(self, participant_id: str):
        self.participants.add(participant_id)

    def begin_transaction(self, tx_id: str, payload: Any) -> Dict[str, Any]:
        self.transactions[tx_id] = {
            "tx_id": tx_id,
            "payload": payload,
            "state": "PREPARING",
            "votes": {},
            "participants": list(self.participants)
        }
        return self.transactions[tx_id]

    def vote(self, tx_id: str, participant_id: str, vote_yes: bool, reason: str = "") -> Dict[str, Any]:
        tx = self.transactions.get(tx_id)
        if not tx:
            raise ValueError(f"Unknown transaction {tx_id}")
        if tx["state"] != "PREPARING":
            raise RuntimeError(f"Cannot vote in state {tx['state']}")
        tx["votes"][participant_id] = {"vote": vote_yes, "reason": reason}
        return tx

    def decide(self, tx_id: str) -> Dict[str, Any]:
        tx = self.transactions.get(tx_id)
        if not tx:
            raise ValueError(f"Unknown transaction {tx_id}")
        all_participants = tx["participants"]
        votes = tx["votes"]

        if len(votes) < len(all_participants):
            tx["state"] = "ABORTED"
            tx["decision_reason"] = "Missing votes from one or more participants"
        else:
            all_yes = all(v["vote"] is True for v in votes.values())
            if all_yes:
                tx["state"] = "COMMITTED"
                tx["decision_reason"] = "Consensus achieved: all participants voted YES"
            else:
                tx["state"] = "ABORTED"
                rejected_by = [p for p, v in votes.items() if not v["vote"]]
                tx["decision_reason"] = f"Aborted: rejected by {rejected_by}"
        return tx
