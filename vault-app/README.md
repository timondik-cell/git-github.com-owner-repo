Vault App — E2EE secret sharing (MVP)

Overview
- Minimal end-to-end encrypted vault app.
- Client encrypts secrets with a passphrase-derived key; server stores ciphertext only.
- Sharing implemented via asymmetric key-wrapping (recipient public keys).

Quickstart (local, Docker Compose)
1) Install Docker & Docker Compose
2) From repo root:
   docker-compose up --build
3) Open http://localhost:3000 and create an account

Security notes
- Passphrases are never sent to the server.
- Keep your recovery key safe; losing it means losing access to your secrets.

Files of interest
- backend/: Node/Express API + simple SQLite DB
- frontend/: React + TypeScript SPA
- docker-compose.yml: runs frontend and backend

Next steps
- Review code, run locally, and test E2EE flows.
- I will provide detailed runbook and unit tests next.
