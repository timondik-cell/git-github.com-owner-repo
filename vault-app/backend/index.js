const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const Database = require('better-sqlite3');

const db = new Database('data/db.sqlite');
// simple tables
db.prepare(`CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, pubkey TEXT, created_at TEXT)`).run();
db.prepare(`CREATE TABLE IF NOT EXISTS secrets (id TEXT PRIMARY KEY, owner_id TEXT, ciphertext TEXT, meta TEXT, created_at TEXT)`).run();

const app = express();
app.use(cors());
app.use(bodyParser.json());

app.post('/api/users', (req, res) => {
  const { id, pubkey } = req.body;
  db.prepare('INSERT OR REPLACE INTO users (id,pubkey,created_at) VALUES (?,?,datetime("now"))').run(id,pubkey);
  res.json({ ok: true });
});

app.post('/api/secrets', (req, res) => {
  const { id, owner_id, ciphertext, meta } = req.body;
  db.prepare('INSERT OR REPLACE INTO secrets (id,owner_id,ciphertext,meta,created_at) VALUES (?,?,?,?,datetime("now"))').run(id,owner_id,ciphertext,meta);
  res.json({ ok: true });
});

app.get('/api/secrets/:id', (req, res) => {
  const id = req.params.id;
  const row = db.prepare('SELECT id,owner_id,ciphertext,meta,created_at FROM secrets WHERE id = ?').get(id);
  if(!row) return res.status(404).json({error:'not found'});
  res.json(row);
});

app.get('/api/health', (req,res)=>res.json({ok:true}));

app.listen(4000, ()=>console.log('vault backend listening on 4000'));
