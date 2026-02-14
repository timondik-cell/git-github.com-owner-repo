Vault App — Security notes

Design choices
- E2EE: all secret encryption and decryption must happen client-side using WebCrypto or libsodium.
- Server stores only ciphertext and metadata.
- Key derivation: use Argon2 or PBKDF2 with high iteration count in client (Argon2 recommended).

Operational guidance
- Do not paste secrets in chat. Use the app UI to create and share secrets.
- Keep recovery key safe. If lost, secrets cannot be recovered.
- For production use, get a third-party security review.
