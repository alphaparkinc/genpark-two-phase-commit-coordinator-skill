"""Example usage for GenPark Two-Phase Commit Coordinator.
100% Python Standard Library.
"""

from client import TwoPhaseCommitCoordinator

def main():
    coordinator = TwoPhaseCommitCoordinator()
    
    # Register participating agents
    coordinator.register_participant("agent_database")
    coordinator.register_participant("agent_ledger")
    coordinator.register_participant("agent_notifier")
    
    # Transaction 1: Successful commit
    tx1 = coordinator.begin_transaction("tx_3001", {"transfer_amount": 500, "currency": "USD"})
    print("Initiated TX 1:", tx1["state"])
    
    coordinator.vote("tx_3001", "agent_database", True)
    coordinator.vote("tx_3001", "agent_ledger", True)
    coordinator.vote("tx_3001", "agent_notifier", True)
    
    decision1 = coordinator.decide("tx_3001")
    print("Decision TX 1:", decision1["state"], "Reason:", decision1["decision_reason"])
    
    # Transaction 2: Abort due to participant rejection
    tx2 = coordinator.begin_transaction("tx_3002", {"transfer_amount": 9000000})
    coordinator.vote("tx_3002", "agent_database", True)
    coordinator.vote("tx_3002", "agent_ledger", False, "Limit exceeded")
    coordinator.vote("tx_3002", "agent_notifier", True)
    
    decision2 = coordinator.decide("tx_3002")
    print("Decision TX 2:", decision2["state"], "Reason:", decision2["decision_reason"])

if __name__ == "__main__":
    main()
