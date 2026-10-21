import subprocess, json

# 1. Fetch current nodes
sql_fetch = "SELECT nodes FROM workflow_entity WHERE id = 'veHMz9UkgGMlUh4n';"
out = subprocess.check_output(['docker', 'exec', '-i', 'n8n_postgres', 'psql', '-U', 'n8n_admin', '-d', 'n8n_db', '-t', '-A', '-c', sql_fetch])
nodes = json.loads(out)

# 2. Update credentials in nodes
for n in nodes:
    creds = n.get('credentials', {})
    if 'telegramApi' in creds:
        creds['telegramApi'] = {'id': 'ZJgioklOFZpvg5j7', 'name': 'Telegram account'}
    if 'postgres' in creds:
        creds['postgres'] = {'id': 'bdSHEy7ZlxpgBCkC', 'name': 'Postgres account'}

# 3. Save back to database
updated_nodes_json = json.dumps(nodes)
with open('/tmp/updated_nodes.json', 'w') as f:
    f.write(updated_nodes_json)

subprocess.check_call(['docker', 'cp', '/tmp/updated_nodes.json', 'n8n_postgres:/tmp/updated_nodes.json'])
sql_update = """
UPDATE workflow_entity 
SET nodes = pg_read_file('/tmp/updated_nodes.json')::json,
    active = true,
    "updatedAt" = CURRENT_TIMESTAMP
WHERE id = 'veHMz9UkgGMlUh4n';
"""
subprocess.check_call(['docker', 'exec', '-i', 'n8n_postgres', 'psql', '-U', 'n8n_admin', '-d', 'n8n_db', '-c', sql_update])
print("Successfully updated nodes with user's Telegram and Postgres credentials!")
