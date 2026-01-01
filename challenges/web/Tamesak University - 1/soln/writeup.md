# Tamesak University - 1 Solution

## 0. Reconnaissance

Before interacting with the challenge, we first identify the services running on the target server.

```bash
nmap -sV -p- <server-ip>
```

From the results, we find 2 interesting open ports:

Port 8000 - hosting a web application

Port 2222 - running an SSH service on a non-standard port

---

## 1. Exploring the Website

Accessing the webpage at `http://<server-ip>:8000` brings you to a university website filled with information.

![Homepage](./images/homepage.png)

While browsing, you’ll notice a **Course Finder** button on the *Academics* page that leads to an interactive course-search tool.

![Course Finder Button](./images/course_finder_button.png)

![Course Finder Page](./images/course_finder_page.png)

---

## 2. Identifying the Injection Point

When performing a normal search, you’ll get relevant course names based on the similarity of your input.

![Normal Search](./images/normal_search.png)

Most symbols produce an error, **except for the semicolon (`;`)**, which allows arbitrary shell command injection.

![Invalid Search](./images/invalid_search.png)

![Command Injection Example](./images/command_injection_1.png)

---

## 3. Discovering Useful Files

Since commands can be executed on the host, we can explore the file system.  
A good place to start is `/var/www`, which commonly stores web application files.

![Command Injection 2](./images/command_injection_2.png)

Inside, we find two interesting items:

1. **A note** revealing that an SSH account named `bob` exists, but it requires an SSH key and password.  
   
   ![Note](./images/note.png)

2. **An SSH key file**, seemingly obfuscated using multiple layers of encoding.  
   
   ![SSH Key](./images/ssh_key.png)

---

## 4. Decoding the SSH Key

The note suggests checking the **Announcements** section on the homepage.  
The posts there contain hints on how to decode the SSH key, as well as the password required to unlock it.

![Announcements](./images/annoucements.png)

According to the “Cooking” post, the key must be decoded in the following order:

1. **Base85**
2. **Vigenère Cipher** (Key: `simmerandstir`)
3. **ROT Cipher** (Rotation of 6)

After applying these transformations, the decoded key is revealed.

![Decoded SSH Key](./images/decoded_ssh_key.png)

---

## 5. Accessing the SSH Account

Save the decoded SSH key and connect to the server as **bob**:

```bash
ssh -i [decoded_key_name] bob@<server_ip> -p 2222
```

Once logged in, you can retrieve the flag from **Bob**’s home directory:
 
```bash
cat ~/flag1.txt
SPARK{n0t_s0_s3cr3t_k3y_b0b}
```