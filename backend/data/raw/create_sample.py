import pandas as pd
import random
from datetime import datetime, timedelta
import os

random.seed(42)

FORUMS = ['breachforums', 'hackforums', 'darknetlive', 'raidforums', 'exploit_in']

POSTS = [
    'Selling fresh credential dump from major bank 50k accounts email password combo',
    'New ransomware as a service available contact for pricing bitcoin monero accepted',
    'Zero day exploit for windows kernel privilege escalation unpatched cve 2024',
    'Fullz available ssn dob credit card info 500 records bulk discount',
    'Botnet for hire ddos service 100gbps guaranteed uptime',
    'Malware builder with persistence keylogger and rat capabilities',
    'Fresh leak from healthcare provider 200k patient records ssn included',
    'Ransomware affiliate program 70 percent split join now',
    'Stealer logs available redline meta raccoon fresh daily',
    'Phishing kit for major bank clone looks identical',
    'Remote access trojan fud fully undetected tested on 10 av',
    'Database dump from ecommerce site 1 million records credit cards',
    'Zero day in popular cms unpatched selling to highest bidder',
    'Credential stuffing list netflix spotify amazon fresh',
    'Exploit kit for sale browser based delivery silent install',
    'Selling access to corporate vpn fortune 500 company',
    'Ransomware source code for sale fully functional',
    'Botnet 50k infected machines available for rent',
    'New stealer malware bypass windows defender tested',
    'Leak from government database 100k employee records',
    'Just had a good day out with my family at the park',
    'Looking for pizza recommendations in my city',
    'Anyone know good movies to watch this weekend',
    'Weather has been really nice lately enjoying outdoors',
    'Best programming language to learn in 2024',
]

rows = []
start_date = datetime(2024, 1, 1)

for i in range(2000):
    post = random.choice(POSTS)
    timestamp = start_date + timedelta(
        days=random.randint(0, 180),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )
    rows.append({
        'id': 'post_' + str(i + 1),
        'text': post,
        'source_forum': random.choice(FORUMS),
        'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
    })

df = pd.DataFrame(rows)
os.makedirs('data/raw', exist_ok=True)
df.to_csv('data/raw/darkdump.csv', index=False)
print('Created sample dataset with ' + str(len(df)) + ' rows')
print(df['source_forum'].value_counts())