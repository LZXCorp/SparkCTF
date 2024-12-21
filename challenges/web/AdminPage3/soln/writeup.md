# Solution

1. When clicking on any of the profiles, I noticed that there is a 'Session ID:' below, indicating that there might be a way to obtain it for session hijacking.
![Tiffany](tiff.png)

2. Within the browsers **Network** tab consisted of a GET request. There seems to be a `sessionid` there.
![network](network.png)

3. You can make use of it to escalate to user tiffany!
![loggedin](loggedin.png)

4. There is a **Flag 3.5**
![sig24](sig24.png)

5. Based off the description, we can make use of the JWT Encoder to encode a JWT token to escalate to admin.
![jwt](jwt.png)

```js
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZG1pbiI6dHJ1ZSwiaWF0IjoxNzM0MzMxMzYyfQ.OLjEh-cw7TR-yMG4uJeyK5s7aRNHWOkGb3ggS-GV11U
```

6. Thus, the successful escalation from tiffany to admin.
![admin](admin.png)