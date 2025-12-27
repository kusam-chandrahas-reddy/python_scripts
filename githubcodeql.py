####script to get the codeql database for a repository

import sys
import requests
import json
import csv
import pandas as pd

org = sys.argv[1]
repository = sys.argv[2]

keyfile='GitAPIKeys.json'

with open(keyfile) as f:
    data = json.load(f)
    APIKey = data['APIKey']

apibaseurl="https://api.github.com/"

codealerts_org='/orgs/{org}/code-scanning/alerts'
codealerts_repo='/repos/{owner}/{repo}/code-scanning/alerts'

headers = {
    'Authorization': f'token {APIKey}',
    'Accept': 'application/vnd.github+json'
}

response = requests.get(apibaseurl + codealerts_repo.format(owner=org, repo=repository), headers=headers)

data = response.json()

if response.status_code != 200:
    print(f"Error: {response.status_code}")
    print(data)
    sys.exit(1)

output_file = 'codeql_results.csv'

# field names
fields = ['Alert Number', 'State', 'Created At', 'Fixed At', 'Dismissed Reason', 'Dismissed At', 'Dismissed By', 'Rule ID', 'Rule Severity', 'Security Severity Level', 'Rule Description', 'Full Description', 'Help Text', 'Tool Name', 'URL', 'Location Details']

# Sort data by Security Severity Level
# Define severity rank (smaller number = higher severity)
severity_rank = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3, 'note': 4, 'none': 5}

def get_severity_rank(alert):
    level = alert.get('rule', {}).get('security_severity_level', 'none')
    # If None or unknown, treat as lowest priority (none)
    if level is None: 
        level = 'none'
    return severity_rank.get(level.lower(), 100)

data.sort(key=get_severity_rank)

# Prepare rows for DataFrame and CSV
rows = []
for alert in data:
    most_recent = alert.get('most_recent_instance', {})
    location = most_recent.get('location', {})
    location_details = f"{location.get('path', '')}:{location.get('start_line', '')}-{location.get('end_line', '')}"

    rows.append({
        'Alert Number': alert.get('number'),
        'State': alert.get('state'),
        'Created At': alert.get('created_at'),
        'Fixed At': alert.get('fixed_at'),
        'Dismissed Reason': alert.get('dismissed_reason'),
        'Dismissed At': alert.get('dismissed_at'),
        'Dismissed By': (alert.get('dismissed_by') or {}).get('login'),
        'Rule ID': alert.get('rule', {}).get('id'),
        'Rule Severity': alert.get('rule', {}).get('severity'),
        'Security Severity Level': alert.get('rule', {}).get('security_severity_level'),
        'Rule Description': alert.get('rule', {}).get('description'),
        'Full Description': alert.get('rule', {}).get('full_description'),
        'Help Text': alert.get('rule', {}).get('help'),
        'Tool Name': alert.get('tool', {}).get('name'),
        'URL': alert.get('html_url'),
        'Location Details': location_details
    })

# Write to CSV
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

# Write to Excel
output_excel = 'codeql_results.xlsx'
df = pd.DataFrame(rows)
df.to_excel(output_excel, index=False)

print(f"Successfully converted to {output_file} and {output_excel}")


