from client import TwoPhaseCommitCoordinator

class MockParticipant:
    def __init__(self):
        self.state = "INIT"
    def prepare(self, tx_id, data):
        return True
    def commit(self, tx_id):
        self.state = "COMMITTED"
    def abort(self, tx_id):
        self.state = "ABORTED"

def main():
    print("=== Testing Two-Phase Commit Coordinator ===")
    p1 = MockParticipant()
    p2 = MockParticipant()
    coord = TwoPhaseCommitCoordinator({"p1": p1, "p2": p2})
    ok, status = coord.execute_transaction("tx_101", {"action": "TRANSFER"})
    print("Transaction status:", status)

    assert ok and status == "COMMITTED"
    assert p1.state == "COMMITTED" and p2.state == "COMMITTED"
    print("=== All tests passed successfully! ===")

if __name__ == "__main__":
    main()
