import pandas as pd
import random
import os
from datetime import datetime, timedelta

random.seed(42)

FORUMS = ['breachforums', 'hackforums', 'darknetlive', 'raidforums', 'exploit_in']

POSTS = [
    'Selling fresh credential dump from major bank 50k accounts email password combo',
    'New ransomware as a service available contact for pricing bitcoin monero accepted',
    'Zero day exploit for windows kernel privilege escalation unpatched cve 2024',
    'Fullz available ssn dob credit card info 500 records bulk discount',
    'Botnet for hire ddos service 100gbps guaranteed uptime',
    'Malware builder with persistence keylogger and rat capabilities fud',
    'Fresh leak from healthcare provider 200k patient records ssn included',
    'Ransomware affiliate program 70 percent split join now limited slots',
    'Stealer logs available redline meta raccoon fresh daily updated',
    'Phishing kit for major bank clone looks identical bypass 2fa',
    'Remote access trojan fud fully undetected tested on 10 antivirus',
    'Database dump from ecommerce site 1 million records credit cards cvv',
    'Zero day in popular cms unpatched selling to highest bidder escrow',
    'Credential stuffing list netflix spotify amazon hbo fresh combolist',
    'Exploit kit for sale browser based delivery silent install dropper',
    'Selling access to corporate vpn fortune 500 company rdp',
    'Ransomware source code for sale fully functional builder decryptor',
    'Botnet 50k infected machines available for rent per hour',
    'New stealer malware bypass windows defender fully tested crypted',
    'Leak from government database 100k employee records pii',
    'Selling corporate email access ceo credentials office365',
    'Fresh combo list 10 million email password pairs checked',
    'Crypter fud 2024 bypass all antivirus tools guaranteed',
    'Ddos attack service cheap reliable fast layer7 layer4',
    'Selling exploit for apache vulnerability remote code execution',
    'Data breach notification upcoming major retailer payment data',
    'Buying valid credit cards cvv fullz with high balance',
    'Selling access to hospital network ransomware ready domain admin',
    'Keylogger with screenshot capture ftp exfil silent install',
    'Underground market new vendor trusted escrow accepts crypto',
    'Spyware for android ios undetected remote monitoring tool',
    'Vulnerabilities in banking app selling poc exploit code',
    'Fresh logs from infostealer 500k lines parsed sorted',
    'Mass email spam service 1 million per day inbox delivery',
    'Hacked paypal accounts verified balance ready cashout',
    'Selling rdp access to us company domain admin privileges',
    'New cryptominer silent install bypass av fud tested',
    'Account takeover service email phone verified bulk',
    'Leaked source code from major software company github',
    'Selling zero day for ios browser rce no interaction needed',
]

EXTRAS = [
    'dm for info price negotiable bulk discount available',
    'trusted vendor 500 deals completed escrow accepted',
    'limited time offer first 10 buyers get discount',
    'contact via telegram only no email serious buyers',
    'sample available before purchase verified by mods',
]

rows = []
start = datetime(2024, 1, 1)

for i in range(2000):
    post = random.choice(POSTS)
    extra = random.choice(EXTRAS) if random.random() > 0.5 else ''
    text = post + (' ' + extra if extra else '')
    rows.append({
        'id': 'post_' + str(i + 1),
        'text': text,
        'source_forum': random.choice(FORUMS),
        'timestamp': (start + timedelta(
            days=random.randint(0, 180),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )).strftime('%Y-%m-%d %H:%M:%S'),
    })

df = pd.DataFrame(rows)
os.makedirs('data/raw', exist_ok=True)
df.to_csv('data/raw/darkdump.csv', index=False)
print('Done! ' + str(len(df)) + ' rows, ' + str(df['text'].nunique()) + ' unique posts')