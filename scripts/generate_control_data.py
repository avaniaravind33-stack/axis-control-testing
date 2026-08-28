"""
Axis Bank - Control Testing Simulation Dataset Generator
Generates realistic transaction data with embedded control testing scenarios
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seeds for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
NUM_TRANSACTIONS = 15000
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2024, 12, 31)

# Control Definitions
CONTROLS = {
    'C001': {
        'name': 'Maker/Checker Approval',
        'description': 'All transactions >₹5L require independent approval',
        'risk': 'Unauthorized transactions',
        'threshold': 500000,
        'control_type': 'Preventive',
        'ownership': 'Operations',
    },
    'C002': {
        'name': 'Authorization Limit Compliance',
        'description': 'Officers cannot approve beyond their limit',
        'risk': 'Excess authorization',
        'threshold': 'Role-based',
        'control_type': 'Preventive',
        'ownership': 'Compliance',
    },
    'C003': {
        'name': 'Segregation of Duties',
        'description': 'Same user cannot be maker and checker',
        'risk': 'Fraud/override',
        'threshold': 'All transactions',
        'control_type': 'Preventive',
        'ownership': 'IT Security',
    },
    'C004': {
        'name': '4-Eyes Principle',
        'description': 'High-value transactions need 2 approvals',
        'risk': 'Unauthorized high-value txns',
        'threshold': '>₹10L',
        'control_type': 'Preventive',
        'ownership': 'Operations',
    },
    'C005': {
        'name': 'Duplicate Detection',
        'description': 'System flags potential duplicate txns',
        'risk': 'Duplicate processing',
        'threshold': 'Same amount, date, beneficiary',
        'control_type': 'Detective',
        'ownership': 'Operations',
    },
}

# Transaction Types
TRANSACTION_TYPES = ['Fund Transfer', 'Cheque Processing', 'Remittance', 'Standing Order', 'Sweep']
CHANNELS = ['Branch', 'ATM', 'Online', 'Mobile', 'SWIFT']
OFFICER_ROLES = ['Clerk', 'Officer', 'Senior Officer', 'Manager', 'Director']

def generate_transaction_date():
    """Generate random transaction date"""
    time_diff = END_DATE - START_DATE
    random_days = random.randint(0, time_diff.days)
    return START_DATE + timedelta(days=random_days, hours=random.randint(0, 23), minutes=random.randint(0, 59))

def get_officer_limit(role):
    """Get authorization limit by role"""
    limits = {
        'Clerk': 50000,
        'Officer': 500000,
        'Senior Officer': 2000000,
        'Manager': 5000000,
        'Director': float('inf'),
    }
    return limits.get(role, 50000)

def generate_transaction():
    """Generate single transaction with control testing attributes"""
    tx_id = f"ATX{datetime.now().year}{random.randint(100000, 999999)}"
    tx_date = generate_transaction_date()
    tx_type = random.choice(TRANSACTION_TYPES)
    channel = random.choice(CHANNELS)

    # Amount
    amount = round(np.random.lognormal(mean=np.log(200000), sigma=1.2), 0)
    amount = max(50000, min(25000000, amount))

    # Officer roles
    maker_role = np.random.choice(OFFICER_ROLES, p=[0.3, 0.35, 0.20, 0.10, 0.05])
    maker_id = f"OFF{random.randint(1000, 9999)}"

    # Checker (should be different for SOD control)
    checker_role = np.random.choice(OFFICER_ROLES, p=[0.1, 0.3, 0.35, 0.15, 0.10])
    checker_id = f"OFF{random.randint(1000, 9999)}"

    maker_limit = get_officer_limit(maker_role)
    checker_limit = get_officer_limit(checker_role)

    # Simulate control issues (realistic failure rates)
    rand = random.random()

    # C001: Maker/Checker (2% failure rate)
    if amount > 500000 and rand < 0.02:
        approval_status = 'Missing'
        approval_date = None
        c001_status = 'Fail'
        c001_exception = 'No independent approval'
    else:
        approval_status = 'Approved'
        approval_date = (tx_date + timedelta(hours=random.randint(1, 8))).strftime('%Y-%m-%d %H:%M:%S')
        c001_status = 'Pass' if amount <= 500000 or approval_status == 'Approved' else 'Fail'
        c001_exception = '' if c001_status == 'Pass' else 'Approval missing'

    # C002: Authorization Limit (3% failure rate)
    if amount > maker_limit and rand < 0.03:
        c002_status = 'Fail'
        c002_exception = 'Amount exceeds maker limit'
    else:
        c002_status = 'Pass'
        c002_exception = ''

    # C003: Segregation of Duties (ensure different officers)
    if maker_id == checker_id and rand < 0.05:  # 5% create SOD violation
        checker_id = maker_id  # Force violation
        c003_status = 'Fail'
        c003_exception = 'Same officer as maker'
    else:
        c003_status = 'Pass'
        c003_exception = ''

    # C004: 4-Eyes Principle for high-value (1% failure rate)
    if amount > 1000000 and rand < 0.01:
        c004_status = 'Fail'
        c004_exception = 'High-value requires 2 approvals'
    else:
        c004_status = 'Pass'
        c004_exception = ''

    # C005: Duplicate Detection (0.5% duplicates)
    is_duplicate = 'Yes' if rand < 0.005 else 'No'
    if is_duplicate == 'Yes':
        c005_status = 'Detected'
        c005_exception = 'Potential duplicate flagged'
    else:
        c005_status = 'Pass'
        c005_exception = ''

    # Deficiency classification
    deficiencies = []
    if c001_status == 'Fail':
        deficiencies.append('Critical')
    if c002_status == 'Fail' or c003_status == 'Fail':
        deficiencies.append('Major')
    if c004_status == 'Fail':
        deficiencies.append('Major')
    if c005_status == 'Detected':
        deficiencies.append('Minor')

    deficiency_class = deficiencies[0] if deficiencies else 'None'

    return {
        'Transaction ID': tx_id,
        'Date': tx_date.strftime('%Y-%m-%d'),
        'Time': tx_date.strftime('%H:%M:%S'),
        'Transaction Type': tx_type,
        'Channel': channel,
        'Amount (INR)': amount,
        'Maker ID': maker_id,
        'Maker Role': maker_role,
        'Maker Limit': maker_limit,
        'Checker ID': checker_id,
        'Checker Role': checker_role,
        'Checker Limit': checker_limit,
        'Approval Status': approval_status,
        'Approval Date': approval_date if approval_date else '',
        'C001_Maker_Checker': c001_status,
        'C001_Exception': c001_exception,
        'C002_Auth_Limit': c002_status,
        'C002_Exception': c002_exception,
        'C003_SOD': c003_status,
        'C003_Exception': c003_exception,
        'C004_4Eyes': c004_status,
        'C004_Exception': c004_exception,
        'C005_Duplicate': c005_status,
        'C005_Exception': c005_exception,
        'Deficiency Class': deficiency_class,
    }

def generate_dataset(num_transactions=NUM_TRANSACTIONS):
    """Generate complete dataset"""
    print(f"Generating {num_transactions} transactions with control testing attributes...")

    transactions = []
    for i in range(num_transactions):
        if (i + 1) % 2000 == 0:
            print(f"  Generated {i + 1} transactions...")
        transactions.append(generate_transaction())

    df = pd.DataFrame(transactions)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)

    return df

def validate_dataset(df):
    """Validate control testing effectiveness"""
    print("\n" + "="*70)
    print("CONTROL TESTING EFFECTIVENESS ANALYSIS")
    print("="*70)

    # Overall statistics
    print(f"\nTotal Transactions Tested: {len(df):,}")
    print(f"Testing Period: {df['Date'].min().date()} to {df['Date'].max().date()}")

    # Control-wise analysis
    controls_analysis = {
        'C001': ('Maker/Checker Approval', 'C001_Maker_Checker'),
        'C002': ('Authorization Limit', 'C002_Auth_Limit'),
        'C003': ('Segregation of Duties', 'C003_SOD'),
        'C004': ('4-Eyes Principle', 'C004_4Eyes'),
        'C005': ('Duplicate Detection', 'C005_Duplicate'),
    }

    print(f"\n{'Control':<8} {'Name':<30} {'Pass':<8} {'Fail':<8} {'Exception %':<12}")
    print("-" * 70)

    for ctrl_id, (ctrl_name, col_name) in controls_analysis.items():
        pass_count = len(df[df[col_name] == 'Pass'])
        fail_count = len(df[df[col_name] != 'Pass'])
        exception_pct = (fail_count / len(df) * 100)
        print(f"{ctrl_id:<8} {ctrl_name:<30} {pass_count:<8} {fail_count:<8} {exception_pct:>10.2f}%")

    # Deficiency breakdown
    print(f"\n{'Deficiency Class':<20} {'Count':<10} {'Percentage':<12}")
    print("-" * 70)
    for deficiency in ['None', 'Minor', 'Major', 'Critical']:
        count = len(df[df['Deficiency Class'] == deficiency])
        pct = (count / len(df) * 100)
        print(f"{deficiency:<20} {count:<10} {pct:>10.2f}%")

    # Transaction type analysis
    print(f"\n{'Transaction Type':<25} {'Count':<10}")
    print("-" * 70)
    for tx_type in df['Transaction Type'].unique():
        count = len(df[df['Transaction Type'] == tx_type])
        print(f"{tx_type:<25} {count:<10}")

    print("\n" + "="*70)

def main():
    # Generate data
    df = generate_dataset()

    # Validate
    validate_dataset(df)

    # Save to CSV
    output_path = 'data/control_testing_transactions.csv'
    df.to_csv(output_path, index=False)
    print(f"\n✓ Dataset saved to {output_path}")

    return df

if __name__ == '__main__':
    main()
