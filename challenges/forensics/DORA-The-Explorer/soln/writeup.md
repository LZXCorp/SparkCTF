# DORA The Explorer - Solution Writeup

## Challenge Overview

Participants must analyze DHCP logs to identify a specific device, extract its MAC address, convert it to a port number, and access the website hosted on docker to retrieve the flag

## Solution Steps

### Step 1: Understand the Class C Hint

The challenge description mentions Desmond wanting to achieve his "Class C licence" and studying two network ranges:
- 172.16.91.0/23 (Class B private range)
- 192.168.100.0/25 (Class C private range)

The "Class C licence" hint directs participants to focus on the Class C range: 192.168.100.0/25.

### Step 2: Analyze the DHCP Logs

Open `journalctl.txt` and filter for devices in the 192.168.100.0/25 subnet.

Devices found in the Class C range:
- 192.168.100.33 - a4:5e:60:c7:89:12
- 192.168.100.42 - b4:2e:99:8a:71:33
- 192.168.100.65 - 9c:d9:17:00:87:26
- 192.168.100.89 - 20:7c:14:95:3a:bf
- 192.168.100.91 - 3c:97:0e:2f:1a:88
- 192.168.100.108 - 3c:a8:2a:4b:77:c9

### Step 3: Apply the MAC Address Hint

The challenge mentions Desmond's obsession with "the last 6 pieces of macaroni" and "the perfect combination of the last 4."

This refers to the last 4 hexadecimal characters of MAC addresses.

### Step 4: Extract and Convert MAC Addresses

For each device, take the last 4 characters of the MAC address and convert from hexadecimal to decimal:

- a4:5e:60:c7:89:12 → 89:12 → 8912 → 35090
- b4:2e:99:8a:71:33 → 71:33 → 7133 → 28979
- 9c:d9:17:00:87:26 → 87:26 → 8726 → 34598
- 20:7c:14:95:3a:bf → 3a:bf → 3abf → 15039
- 3c:97:0e:2f:1a:88 → 1a:88 → 1a88 → 6792
- 3c:a8:2a:4b:77:c9 → 77:c9 → 77c9 → 30665

### Step 5: Test Port Numbers

The challenge mentions Desmond planning to "exit the country via a port." This suggests connecting to a service on the calculated port numbers.

Test each calculated port with the provided host:

```bash
curl http://[PROVIDED_HOST]:34598
```

### Step 6: Retrieve the Flag

Accessing port 34598 (from MAC 9c:d9:17:00:87:26) returns a webpage containing the flag:

**Flag:** `SPARK{k67A_DORA_8nh2_des0}`

## Key Learning Points

- Network log analysis and filtering
- Understanding IP address classes and subnetting
- MAC address manipulation and hex-to-decimal conversion
- Service discovery through calculated parameters
