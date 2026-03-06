from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta

fake = Faker()

# ─────────────────────────────────────────────
# CONFIGURABLE INPUTS
# ─────────────────────────────────────────────

NUM_TRANSACTIONS = 50_000
START_DATE = datetime(2022, 1, 1)
END_DATE   = datetime(2024, 12, 31)

# Each debit category: list of merchants and (min, max) log-normal amount bounds
DEBIT_CATEGORIES = {
    "Supplies & Stock": {
        "merchants": ["Amazon", "Screwfix", "B&Q", "Toolstation", "Viking Direct", "Ryman Stationery", "Staples"],
        "lognorm": (4.0, 0.8), "bounds": (5.0, 2_000.0),
    },
    "Utilities": {
        "merchants": ["British Gas", "Octopus Energy", "Thames Water", "BT Broadband", "Virgin Media", "EDF Energy"],
        "lognorm": (4.5, 0.5), "bounds": (30.0, 500.0),
    },
    "Tax & Government": {
        "merchants": ["HMRC VAT", "HMRC PAYE", "HMRC Corp Tax", "Companies House", "Local Council Rates"],
        "lognorm": (6.0, 0.8), "bounds": (100.0, 20_000.0),
    },
    "Rent & Office": {
        "merchants": ["WeWork", "Regus", "IWG Offices", "Local Landlord", "Workspace Group"],
        "lognorm": (7.0, 0.4), "bounds": (500.0, 5_000.0),
    },
    "Bank & Finance Fees": {
        "merchants": ["Barclaycard", "Lloyds Bank Fee", "PayPal Fee", "Stripe Fee", "Square Fee", "Amex Fee"],
        "lognorm": (3.5, 0.7), "bounds": (1.0, 300.0),
    },
    "Software & Subscriptions": {
        "merchants": ["Slack", "Microsoft 365", "Adobe", "Xero", "QuickBooks", "Dropbox", "Zoom", "HubSpot"],
        "lognorm": (3.8, 0.6), "bounds": (5.0, 800.0),
    },
    "Logistics & Postage": {
        "merchants": ["Royal Mail", "DHL", "FedEx", "UPS", "Hermes", "Evri", "Parcelforce"],
        "lognorm": (3.2, 0.7), "bounds": (2.0, 400.0),
    },
    "Travel & Transport": {
        "merchants": ["Uber", "National Rail", "BP Fuel", "Shell Fuel", "Trainline", "TfL", "Esso"],
        "lognorm": (3.5, 0.8), "bounds": (3.0, 500.0),
    },
    "Groceries & Food": {
        "merchants": ["Tesco", "Asda", "Lidl", "Aldi", "Sainsbury's", "Morrisons", "Costco"],
        "lognorm": (3.6, 0.6), "bounds": (5.0, 250.0),
    },
}

# Each credit category: list of sources and (lognorm mu, sigma) + bounds
CREDIT_CATEGORIES = {
    "Customer Invoice": {
        "sources": ["Customer Payment", "Invoice Settlement", "Client Deposit", "Wholesale Order Payment"],
        "lognorm": (6.5, 0.8), "bounds": (50.0, 50_000.0),
    },
    "Payment Platform": {
        "sources": ["Stripe Payout", "PayPal Transfer", "Square Payout", "SumUp Payout", "GoCardless", "Shopify Payout"],
        "lognorm": (5.5, 0.9), "bounds": (20.0, 10_000.0),
    },
    "Bank Transfer": {
        "sources": ["Bank Transfer In", "CHAPS Payment", "BACS Transfer", "Faster Payment Received"],
        "lognorm": (6.0, 0.9), "bounds": (50.0, 30_000.0),
    },
    "HMRC & Grants": {
        "sources": ["HMRC VAT Refund", "Business Grant", "Innovate UK Grant", "HMRC Corp Tax Refund"],
        "lognorm": (7.0, 0.7), "bounds": (200.0, 40_000.0),
    },
    "Loan & Finance": {
        "sources": ["Loan Drawdown", "Business Loan", "Bounce Back Loan", "Invoice Finance"],
        "lognorm": (8.0, 0.6), "bounds": (1_000.0, 100_000.0),
    },
    "Card Terminal Sales": {
        "sources": ["Card Terminal Receipts", "Online Sales", "Retail Sales Batch", "Contactless Receipts"],
        "lognorm": (5.0, 1.0), "bounds": (10.0, 5_000.0),
    },
}

# Relative frequency weights for picking a category
DEBIT_WEIGHTS  = [0.16, 0.10, 0.10, 0.08, 0.08, 0.12, 0.12, 0.12, 0.12]
CREDIT_WEIGHTS = [0.30, 0.25, 0.18, 0.08, 0.05, 0.14]

# ─────────────────────────────────────────────
# MESSY DESCRIPTION HELPERS
# ─────────────────────────────────────────────

_PREFIXES = ["CD ", "POS ", "VIS ", "MC ", "DD ", "SO ", "TFR ", "BP ", "CHQ ", ""]
_NOISE    = ["*", "/", " - ", " // ", " > ", " "]


def _corrupt_name(name: str) -> str:
    """Occasionally garble a character or two, like OCR / encoding errors on statements."""
    if random.random() > 0.15:          # only ~15% of the time
        return name
    name = list(name)
    idx = random.randint(0, len(name) - 1)
    name[idx] = random.choice("xyzqwk#@&")
    return "".join(name)


def _messy_details(base: str) -> str:
    """Mimic real bank statement description noise."""
    base = _corrupt_name(base)

    # Randomly truncate like banks do
    if random.random() < 0.4:
        base = base[:random.randint(6, max(7, len(base) - 2))]

    if random.random() < 0.7:
        base = base.upper()

    prefix = random.choice(_PREFIXES)
    loc    = fake.bothify("?#?").upper() if random.random() < 0.4 else ""
    pid    = fake.bothify("########")    if random.random() < 0.6 else ""
    card   = f"XXXX{random.randint(1000, 9999)}" if random.random() < 0.3 else ""

    noise  = random.choice(_NOISE)
    parts  = [p for p in [prefix + base, loc, pid, card] if p]
    return noise.join(parts)


# ─────────────────────────────────────────────
# MAIN GENERATOR
# ─────────────────────────────────────────────

def generate_transactions(
    n: int = NUM_TRANSACTIONS,
    start_date: datetime = START_DATE,
    end_date: datetime = END_DATE,
    extra_debit_merchants: dict = None,   # {"Category": ["Merchant", ...]}
    extra_credit_sources: dict = None,    # {"Category": ["Source", ...]}
    credit_ratio: float = 0.35,
    seed: int = None,
) -> pd.DataFrame:
    """
    Generate n fake small-business bank transactions.

    Parameters
    ----------
    n                     : number of rows
    start_date / end_date : date window
    extra_debit_merchants : dict to inject extra merchants into a debit category
    extra_credit_sources  : dict to inject extra sources into a credit category
    credit_ratio          : proportion of transactions that are credits (0–1)
    seed                  : set for reproducibility, None for random each run

    Returns
    -------
    pd.DataFrame with columns: date, action, category, amount, transaction_details
    """
    if seed is not None:
        random.seed(seed)
        fake.seed_instance(seed)

    # Merge any extra merchants/sources into the category maps
    debit_cats  = {k: dict(v) for k, v in DEBIT_CATEGORIES.items()}
    credit_cats = {k: dict(v) for k, v in CREDIT_CATEGORIES.items()}

    if extra_debit_merchants:
        for cat, names in extra_debit_merchants.items():
            if cat in debit_cats:
                debit_cats[cat]["merchants"] = debit_cats[cat]["merchants"] + names

    if extra_credit_sources:
        for cat, names in extra_credit_sources.items():
            if cat in credit_cats:
                credit_cats[cat]["sources"] = credit_cats[cat]["sources"] + names

    debit_cat_names  = list(debit_cats.keys())
    credit_cat_names = list(credit_cats.keys())
    delta = end_date - start_date

    rows = []
    for _ in range(n):
        is_credit = random.random() < credit_ratio
        action    = "credit" if is_credit else "debit"

        if is_credit:
            cat_name = random.choices(credit_cat_names, weights=CREDIT_WEIGHTS, k=1)[0]
            cat_data = credit_cats[cat_name]
            mu, sigma = cat_data["lognorm"]
            lo, hi    = cat_data["bounds"]
            amount    = round(min(max(random.lognormvariate(mu, sigma), lo), hi), 2)
            details   = random.choice(cat_data["sources"])
        else:
            cat_name = random.choices(debit_cat_names, weights=DEBIT_WEIGHTS, k=1)[0]
            cat_data = debit_cats[cat_name]
            mu, sigma = cat_data["lognorm"]
            lo, hi    = cat_data["bounds"]
            amount    = round(min(max(random.lognormvariate(mu, sigma), lo), hi), 2)
            details   = random.choice(cat_data["merchants"])

        if random.random() < 0.5:
            details = f"{details} REF {fake.bothify('??####').upper()}"

        date = start_date + timedelta(seconds=random.randint(0, int(delta.total_seconds())))

        rows.append({
            "_date_sort":          date,
            "date":                date.strftime("%b %d"),
            "action":              action,
            "category":            cat_name,
            "amount":              amount,
            "transaction_details": _messy_details(details),
        })

    df = pd.DataFrame(rows)
    df.sort_values("_date_sort", inplace=True)
    df.drop(columns=["_date_sort"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


# ─────────────────────────────────────────────
# EXAMPLE USAGE
# ─────────────────────────────────────────────

if __name__ == "__main__":
    df = generate_transactions(
        n=NUM_TRANSACTIONS,
        seed=42,
        extra_debit_merchants={"Supplies & Stock": ["Local Supplier Co"]},
        extra_credit_sources={"Customer Invoice": ["Main Client Ltd"]},
    )

    print(df.head(15).to_string())
    print(f"\nShape: {df.shape}")
    print("\nCategory distribution:\n", df["category"].value_counts())