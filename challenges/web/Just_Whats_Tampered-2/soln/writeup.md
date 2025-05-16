## Solution
1. Obtain the JWT Token
2. Look for vulnerable endpoints from `robots.txt`
3. Vulnerable Endpoints:
   - `/wp-json/wp/v2/users` - Obtain a list of users in the website (simulates Wordpress)
   - `/wp-json/wp/v2/sitemap` - Obtain a list of endpoints (simulates Wordpress)
4. From the `/wp-json/wp/v2/sitemap` endpoint, more endpoints are exposed
   - `/jwt.js` - Crucial to understand how the JWT token was signed
   - `/keys/private.key` - Used for signing the forged token later on
   - `keys/public.key` -
5. Use the private key to sign and forge a JWT token as the `superuser` (Keep in mind the issued-at, `iat`, value; it needs to stay in the payload)
6. Obtain the flag

## Proof of Concept

After obtaining the exposed private key, you can either use a script or an online JWT encoder/decoder.
- [Working PoC Script](/web/Just_Whats_Tampered-2/soln/poc.js)
- [jwt.io](https://jwt.io/)

## Flag
- `SIG24{pre5s1ng_s1gn5tur3s}` (static)
