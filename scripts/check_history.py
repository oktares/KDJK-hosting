import subprocess, json

sql = 'SELECT nodes FROM workflow_history WHERE "versionId" = \'150eb971-424a-4da0-bdc9-ee514d7bae30\';'
cmd = ['docker', 'exec', '-i', 'n8n_postgres', 'psql', '-U', 'n8n_admin', '-d', 'n8n_db', '-t', '-A', '-c', sql]
out = subprocess.check_output(cmd)
nodes = json.loads(out)
for n in nodes:
    if 'credentials' in n:
        print(n.get('name'), '->', n.get('credentials'))
