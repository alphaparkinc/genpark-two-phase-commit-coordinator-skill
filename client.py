class TwoPhaseCommitCoordinator:
    """
    Two-Phase Commit (2PC) Coordinator.
    Orchestrates distributed atomic transactions across participant nodes.
    """
    def __init__(self, participants):
        self.participants = participants
        self.log = []

    def execute_transaction(self, tx_id, tx_data):
        self.log.append(("START", tx_id))
        votes = {}
        for name, p in self.participants.items():
            vote = p.prepare(tx_id, tx_data)
            votes[name] = vote
            if not vote:
                break

        if all(votes.values()) and len(votes) == len(self.participants):
            self.log.append(("COMMIT", tx_id))
            for p in self.participants.values():
                p.commit(tx_id)
            return True, "COMMITTED"
        else:
            self.log.append(("ABORT", tx_id))
            for p in self.participants.values():
                p.abort(tx_id)
            return False, "ABORTED"
