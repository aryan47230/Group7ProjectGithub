import pdfplumber 
import pandas as pd

PDF = "test_file.pdf"
DATES = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

text_pdf = extract_text_from_pdf(PDF)

transactions = []
months = DATES
for line in text_pdf.splitlines():
    if line.strip().startswith(months):
        transactions.append(line)





import re

records = []
for line in transactions:
    m = re.match(
        r'^(\w{3} \d{2})\s+(\w{3} \d{2})\s+'  # two dates
        r'(.*?)\s+'                               # middle detail
        r'\$?\s*([\d,]+\.\d{2})$',                # amount
        line
    )
    if not m:
        continue

    trans_date, post_date, detail, amount = m.groups()

    # Parse type, card ref, and description
    if detail.startswith('Zelle Payment From'):
        txn_type = 'Zelle'
        card_ref = ''
        desc = detail[len('Zelle Payment From'):].strip()
    elif detail.startswith('Debit Purchase'):
        txn_type = 'Debit'
        rest = detail[len('Debit Purchase'):].strip()
        card_match = re.match(r'^(\d{4}\s+\d{4})\s+(.*)', rest)
        if card_match:
            card_ref, desc = card_match.group(1), card_match.group(2)
        else:
            card_ref, desc = '', rest
    else:
        txn_type = 'Other'
        card_ref = ''
        desc = detail

    # Try to split description from location (e.g. "CHICAGO IL US")
    loc_match = re.search(r'^(.*?)\s+([\w\-\.]+(?:\s+[\w\-\.]+)?)\s+([A-Z]{2})\s+(US)$', desc)
    if loc_match and txn_type == 'Debit':
        description = loc_match.group(1)
        location = f"{loc_match.group(2)}, {loc_match.group(3)}"
    else:
        description = desc
        location = ''

    records.append({
        'Trans Date': trans_date,
        'Post Date': post_date,
        'Type': txn_type,
        'Card Ref': card_ref,
        'Description': description,
        'Location': location,
        'Amount': float(amount.replace(',', ''))
    })

df = pd.DataFrame(records)
df = df.sort_values('Trans Date').reset_index(drop=True)
print(df)
