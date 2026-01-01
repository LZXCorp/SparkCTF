# DORA The Explorer


Desmond is a server administrator who's been managing the company's Red Hat Linux infrastructure for years. Recently, he discovered some interesting network patterns while reviewing system logs. 

Despite hugging the linux penguin everyday, Desmond has an unusual obsession with mac and cheese,  particularly savoring the last 4 pieces of macaroni in every bowl. His colleagues often joke about how he relates everything back to his favourite comfort food, even network protocols.

Desmond has been wanting to achieve his Class C licence, but he's been distracted studying two different network ranges: 172.16.91.0/23 and 192.168.100.0/25. Lately, he's been spending extra time near the wireless access points, mumbling about "the perfect combination of the last 4" and something about+
hiding his treasure at a special place, and he is planning to exit the country via a port after hiding the treasure.

**Your task:** Find the treasure that Desmond has hidden away somewhere on this platform.

**Defined Host:** `desmond.sparkctf.org`

## Summary
- **Author:** Edwin
- **Category:** Forensics
- **Learning Objective:** Analyse Wireless/DHCP logs to identify network devices and decode hardware addresses to locate hidden services.

## Files
- [`journalctl.txt`](./dist/journalctl.txt)

## Services
- [`doratheexplorer`](./service/Dockerfile) (port 34598:34598)

## Flags
- `SPARK{k67A_DORA_8nh2_des0}`
