# Bill Splitter Algorithm
"""
Inputs:
    - BillDetails: {
        total_bill: float,
        tax_percentage: float,
        tip_percentage: float
    }
    - Expenses: [
        {
            "payer": str,
            "amount": float,
            "description": str,
            "involved": [str],
            "split": {"payer 1": float, "payer 2": float, "payer 3": float}
        }
    ]

Outputs:
    - Balances: {
        "payer 1": float,
        "payer 2": float,
        "payer 3": float
    }
    - Settlements: [
        {"from": "payer 1", "to": "payer 2", "amount": float},
        {"from": "payer 3", "to": "payer 1", "amount": float}
    ]
    - Summary per person: {
        "payer 1": {
            "total_paid": float,
            "total_owed": float,
            "net_balance": float
        },
        ...
    }

Description:
    This algorithm takes a total bill amount, tax and tip percentages,
    and a list of expenses with details on who paid and how the expenses
    are split among participants. It calculates:
        - total amount each participant owes
        - their net balance (paid - owed)
        - minimal settlements to balance debts.

Optimizations:
    - Efficiently handles varying numbers of participants and expenses.
    - Minimizes the number of transactions needed.
    - Provides clear summaries per participant.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional


# -----------------------
# Input Data Structures
# -----------------------

@dataclass
class Participant:
    name: str
    total_paid: float = 0.0
    total_owed: float = 0.0
    net_balance: float = 0.0


@dataclass
class BillDetails:
    total_bill: float
    tax_percentage: float = 0.0
    tip_percentage: float = 0.0


@dataclass
class Expense:
    payer: str                # Who paid
    amount: float             # Expense amount
    description: Optional[str] = None
    involved: Optional[List[str]] = None
    split: Optional[Dict[str, float]] = None  # Ratios (e.g., {"Raju": 0.6, "Shyam": 0.4})

    def __post_init__(self):
        if self.involved is None:
            self.involved = []
        if self.split is None:
            self.split = {}
        # Default: equal split among involved participants
        if not self.split and self.involved:
            equal_share = 1 / len(self.involved)
            self.split = {person: equal_share for person in self.involved}


@dataclass
class Group:
    participants: List[Participant]
    expenses: List[Expense]


# -----------------------
# Output Data Structures
# -----------------------

@dataclass
class Balance:
    participant: str
    net_amount: float   # positive = should receive, negative = owes


@dataclass
class Transaction:
    payer: str
    receiver: str
    amount: float


@dataclass
class SettlementResult:
    balances: List[Balance]
    transactions: List[Transaction]
    summary: Dict[str, Dict[str, float]]
    total_bill_summary: BillDetails


# -----------------------
# Helper Functions
# -----------------------

def process_expenses(group: Group, participant_map: Dict[str, Participant]) -> None:
    """Process each expense, updating paid and owed amounts."""
    for expense in group.expenses:
        if expense.payer not in participant_map:
            raise ValueError(f"Unknown payer: {expense.payer}")
        participant_map[expense.payer].total_paid += expense.amount

        for person, ratio in expense.split.items():
            if person not in participant_map:
                raise ValueError(f"Unknown participant in split: {person}")
            participant_map[person].total_owed += expense.amount * ratio


def distribute_tax_tip(bill: BillDetails, group: Group, participant_map: Dict[str, Participant]) -> None:
    """Distribute tax and tip proportionally to owed amounts."""
    total_expenses = sum(exp.amount for exp in group.expenses)
    if total_expenses == 0:
        return

    tax_amount = total_expenses * (bill.tax_percentage / 100)
    tip_amount = total_expenses * (bill.tip_percentage / 100)
    extra = tax_amount + tip_amount

    for p in participant_map.values():
        share_ratio = p.total_owed / total_expenses if total_expenses > 0 else 0
        p.total_owed += share_ratio * extra



def compute_balances(participant_map: Dict[str, Participant]) -> List[Balance]:
    """Compute net balances for all participants (with rounding correction)."""
    balances = []
    for p in participant_map.values():
        p.net_balance = p.total_paid - p.total_owed
        balances.append(Balance(participant=p.name, net_amount=round(p.net_balance, 2)))

    # Ensure total sum of balances is exactly 0
    total_balance = round(sum(b.net_amount for b in balances), 2)
    if abs(total_balance) > 1e-6:
        # Assign rounding difference to the participant with the largest absolute balance
        adjust_target = max(balances, key=lambda b: abs(b.net_amount))
        adjust_target.net_amount -= total_balance

    return balances



def generate_transactions(balances: List[Balance]) -> List[Transaction]:
    """Generate settlement transactions using a greedy approach with rounding correction."""
    creditors = [(b.participant, b.net_amount) for b in balances if b.net_amount > 0]
    debtors = [(b.participant, -b.net_amount) for b in balances if b.net_amount < 0]

    creditors.sort(key=lambda x: x[1], reverse=True)
    debtors.sort(key=lambda x: x[1], reverse=True)

    transactions: List[Transaction] = []
    i, j = 0, 0

    while i < len(debtors) and j < len(creditors):
        debtor, debt_amt = debtors[i]
        creditor, credit_amt = creditors[j]

        settled_amt = min(debt_amt, credit_amt)
        settled_amt = round(settled_amt, 2)  # round per transaction
        if settled_amt > 0:
            transactions.append(Transaction(payer=debtor, receiver=creditor, amount=settled_amt))

        debtors[i] = (debtor, round(debt_amt - settled_amt, 2))
        creditors[j] = (creditor, round(credit_amt - settled_amt, 2))

        if debtors[i][1] == 0:
            i += 1
        if creditors[j][1] == 0:
            j += 1

    # Final correction: ensure balances cancel out
    total_balance = round(sum(b.net_amount for b in balances), 2)
    if abs(total_balance) > 1e-6 and transactions:
        transactions[-1].amount = round(transactions[-1].amount - total_balance, 2)

    return transactions




# -----------------------
# Main Algorithm
# -----------------------

def calculate_settlement(group: Group, bill: BillDetails) -> SettlementResult:
    # Step 1: Map participants
    participant_map = {p.name: p for p in group.participants}

    # Step 2: Process all expenses
    process_expenses(group, participant_map)

    # Step 3: Adjust for tax & tip
    distribute_tax_tip(bill, group, participant_map)

    # Step 4: Compute net balances
    balances = compute_balances(participant_map)

    # Step 5: Generate settlements (Greedy)
    transactions = generate_transactions(balances)

    # Step 6: Build summary
    summary = {
        p.name: {
            "total_paid": round(p.total_paid, 2),
            "total_owed": round(p.total_owed, 2),
            "net_balance": round(p.net_balance, 2),
        }
        for p in participant_map.values()
    }

    return SettlementResult(
        balances=balances,
        transactions=transactions,
        summary=summary,
        total_bill_summary=bill
    )


# -----------------------
# Test Cases
# -----------------------

def run_tests():
    # -------------------
    # Test Case 1: Equal Split
    # -------------------
    print("\n--- Test Case 1: Equal Split ---")
    participants = [Participant("Deepak"), Participant("Raju"), Participant("Shyam")]
    expenses = [
        Expense(payer="Deepak", amount=90, involved=["Deepak", "Raju", "Shyam"])
    ]
    group = Group(participants=participants, expenses=expenses)
    bill = BillDetails(total_bill=90, tax_percentage=0, tip_percentage=0)

    result = calculate_settlement(group, bill)
    print("Summary:", result.summary)
    print("Transactions:", result.transactions)

    # -------------------
    # Test Case 2: Custom Split
    # -------------------
    print("\n--- Test Case 2: Custom Split ---")
    participants = [Participant("Raju"), Participant("Shyam"), Participant("Deepak"), Participant("Shrinivas")]
    expenses = [
        Expense(
            payer="Deepak",
            amount=100,
            split={"Deepak": 0.4, "Raju": 0.3, "Shyam": 0.2, "Shrinivas": 0.1}
        )
    ]
    group = Group(participants=participants, expenses=expenses)
    bill = BillDetails(total_bill=100)

    result = calculate_settlement(group, bill)
    print("Summary:", result.summary)
    print("Transactions:", result.transactions)

    # -------------------
    # Test Case 3: Uneven Payments
    # -------------------
    print("\n--- Test Case 3: Uneven Payments ---")
    participants = [Participant("Deepak"), Participant("Raju"), Participant("Shyam"), Participant("Babu Rao")]
    expenses = [
        Expense(payer="Deepak", amount=60, involved=["Deepak", "Raju", "Shyam"]),
        Expense(payer="Raju", amount=30, involved=["Deepak", "Raju", "Shyam", "Babu Rao"]),
    ]
    group = Group(participants=participants, expenses=expenses)
    bill = BillDetails(total_bill=90)

    result = calculate_settlement(group, bill)
    print("Summary:", result.summary)
    print("Transactions:", result.transactions)

    # -------------------
    # Test Case 4: With Tax + Tip
    # -------------------
    print("\n--- Test Case 4: With Tax + Tip ---")
    participants = [Participant("Deepak"), Participant("Raju"), Participant("Shyam"), Participant("Babu Rao")]
    expenses = [
        Expense(payer="Deepak", amount=100, involved=["Deepak", "Raju", "Shyam", "Babu Rao"]),
    ]
    group = Group(participants=participants, expenses=expenses)
    bill = BillDetails(total_bill=100, tax_percentage=10, tip_percentage=10)

    result = calculate_settlement(group, bill)
    print("Summary:", result.summary)
    print("Transactions:", result.transactions)


if __name__ == "__main__":
    run_tests()
