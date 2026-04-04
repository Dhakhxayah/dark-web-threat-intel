import pandas as pd
import random
import os
from datetime import datetime, timedelta

random.seed(42)

FORUMS = ['breachforums', 'hackforums', 'darknetlive', 'raidforums', 'exploit_in']

TEMPLATES = [
    "selling {quantity} {data_type} from {target} {price} {payment}",
    "fresh {data_type} dump {quantity} records {target} {payment} accepted",
    "new {attack_type} available {feature} contact for {price}",
    "{attack_type} as a service {feature} {payment} only serious buyers",
    "zero day in {software} {feature} unpatched selling {price}",
    "exploit for {software} {feature} {price} escrow available",
    "{quantity} {data_type} from {target} verified {payment}",
    "buying {data_type} from {target} paying {price} in {payment}",
    "leak from {target} {quantity} records includes {data_type}",
    "{attack_type} source code {feature} {price} limited offer",
    "access to {target} network {feature} {price} {payment}",
    "fresh {attack_type} logs {quantity} lines {feature} daily",
    "{data_type} stuffing list {target} {quantity} checked {payment}",
    "malware builder {feature} bypass {software} {price}",
    "phishing kit {target} clone {feature} {payment}",
]

QUANTITIES = ["50k", "100k", "200k", "500k", "1 million", "10k", "5k", "2 million"]
DATA_TYPES = ["credential", "fullz", "ssn", "credit card", "combolist", "database", "logs", "account"]
TARGETS = ["major bank", "healthcare provider", "fortune 500", "government", "ecommerce site", "university", "hospital", "retailer", "social media", "crypto exchange"]
PRICES = ["negotiable", "500 usd", "1000 usd", "0.5 btc", "bulk discount", "pm for price", "auction"]
PAYMENTS = ["bitcoin", "monero", "xmr", "crypto", "btc", "usdt"]
ATTACK_TYPES = ["ransomware", "malware", "botnet", "stealer", "rat", "keylogger", "ddos", "spyware", "crypter", "backdoor"]
FEATURES = ["fud fully undetected", "bypass av", "persistent", "silent install", "no logs", "tested", "guaranteed", "encrypted", "automated", "modular"]
SOFTWARE = ["windows kernel", "apache server", "wordpress", "ios browser", "android", "office365", "vpn client", "router firmware", "database server", "web application"]

rows = []
start = datetime(2024, 1, 1)
used_texts = set()

attempts = 0
while len(rows) < 2000 and attempts < 10000:
    attempts += 1
    template = random.choice(TEMPLATES)
    text = template.format(
        quantity=random.choice(QUANTITIES),
        data_type=random.choice(DATA_TYPES),
        target=random.choice(TARGETS),
        price=random.choice(PRICES),
        payment=random.choice(PAYMENTS),
        attack_type=random.choice(ATTACK_TYPES),
        feature=random.choice(FEATURES),
        software=random.choice(SOFTWARE),
    )

    if text in used_texts:
        continue

    used_texts.add(text)
    timestamp = start + timedelta(
        days=random.randint(0, 180),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )
    rows.append({
        'id': 'post_' + str(len(rows) + 1),
        'text': text,
        'source_forum': random.choice(FORUMS),
        'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
    })

df = pd.DataFrame(rows)
os.makedirs('data/raw', exist_ok=True)
df.to_csv('data/raw/darkdump.csv', index=False)
print('Created ' + str(len(df)) + ' rows with ' + str(df['text'].nunique()) + ' unique posts')