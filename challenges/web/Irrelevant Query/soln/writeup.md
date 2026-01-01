## Solution

1. Visit `/`
2. Inspect and analyse the source code
3. Attempt to access any of the images at `/img/filename` (e.g. `/img/ket.png`)
4. Intercept the image request with Burpsuite
5. Alter the requests being sent
    - Add the `X-Internal-Origin` Header with value `/` (From source code)
    - Alter the image file name being requested to `flag.txt`
