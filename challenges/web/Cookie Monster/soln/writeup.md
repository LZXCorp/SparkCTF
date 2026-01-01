# Cookie Monster - Solution Writeup

## Overview
The challenge is a web-based CTF where participants interact with a web application that stores the user's role in a cookie. By default, all users are assigned the role `guest` and cannot access the admin page. The flag is revealed only if the server sees a role of `admin`.

---

## Step 1: Access the application
- Open the landing page at `/` and observe the current role: `guest`.
- Attempting to access `/admin` directly shows:

---

## Step 2: Inspect cookies
- Use browser developer tools (F12) → **Application → Storage → Cookies**.
- Observe a cookie value, e.g. eyJyb2xlIjoiZ3Vlc3QifQ==

- This is **base64-encoded**.

---

## Step 3: Decode the cookie
- Decode the base64 string:

eyJyb2xlIjoiZ3Vlc3QifQ== → {"role":"guest"}

---

## Step 4: Modify the cookie
- Change `"role":"guest"` → `"role":"admin"`:

- Re-encode in base64:

{"role":"admin"} → eyJyb2xlIjoiYWRtaW4ifQ==


---

## Step 5: Update cookie and reload
- Replace the cookie value in the browser with the new base64 string.
- Reload `/admin`.

---

## Step 6: Obtain the flag
- The admin page now displays:

Congratulations — here is the flag:
SPARK{c00kies_d0_h3ve_p0w3r}

