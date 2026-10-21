import subprocess, json

sql = "SELECT nodes FROM workflow_entity WHERE id = 'veHMz9UkgGMlUh4n';"
cmd = ['docker', 'exec', '-i', 'n8n_postgres', 'psql', '-U', 'n8n_admin', '-d', 'n8n_db', '-t', '-A', '-c', sql]
out = subprocess.check_output(cmd)
nodes = json.loads(out)
for n in nodes:
    if 'telegramTrigger' in n.get('type', ''):
        print(json.dumps(n, indent=2))
