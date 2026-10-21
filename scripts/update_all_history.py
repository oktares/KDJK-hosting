import subprocess, json

# 1. Update workflow_history
sql_fetch_h = 'SELECT nodes FROM workflow_history WHERE "versionId" = \'150eb971-424a-4da0-bdc9-ee514d7bae30\';'
cmd = ['docker', 'exec', '-i', 'n8n_postgres', 'psql', '-U', 'n8n_admin', '-d', 'n8n_db', '-t', '-A', '-c', sql_fetch_h]
out = subprocess.check_output(cmd)
nodes = json.loads(out)

for n in nodes:
    creds = n.get('credentials', {})
    if 'telegramApi' in creds:
        creds['telegramApi'] = {'id': 'ZJgioklOFZpvg5j7', 'name': 'Telegram account'}
    if 'postgres' in creds:
        creds['postgres'] = {'id': 'bdSHEy7ZlxpgBCkC', 'name': 'Postgres account'}

with open('/tmp/updated_history_nodes.json', 'w') as f:
    f.write(json.dumps(nodes))

subprocess.check_call(['docker', 'cp', '/tmp/updated_history_nodes.json', 'n8n_postgres:/tmp/updated_history_nodes.json'])

sql_update_h = """
UPDATE workflow_history 
SET nodes = pg_read_file('/tmp/updated_history_nodes.json')::json,
    "updatedAt" = CURRENT_TIMESTAMP
WHERE "versionId" = '150eb971-424a-4da0-bdc9-ee514d7bae30';

UPDATE workflow_entity
SET nodes = pg_read_file('/tmp/updated_history_nodes.json')::json,
    active = true,
    "updatedAt" = CURRENT_TIMESTAMP
WHERE id = 'veHMz9UkgGMlUh4n';
"""
subprocess.check_call(['docker', 'exec', '-i', 'n8n_postgres', 'psql', '-U', 'n8n_admin', '-d', 'n8n_db', '-c', sql_update_h])
print("Successfully updated workflow_history and workflow_entity with user's real credentials!")
