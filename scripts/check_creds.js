const cp = require('child_process');
const sql = "SELECT nodes FROM workflow_entity WHERE id = 'veHMz9UkgGMlUh4n';";
const out = cp.execSync('docker exec -i n8n_postgres psql -U n8n_admin -d n8n_db -t -A -c "' + sql + '"').toString();
const nodes = JSON.parse(out);
nodes.forEach(n => {
  if (n.credentials) console.log(n.name, '->', JSON.stringify(n.credentials));
});
