# Text Summariser

We've built a cutting-edge Text Summariser web application that uses a powerful LLM to condense any text into neat 3-5 bullet points. Perfect for those long articles you don't have time to read!
Simply paste your text, and our AI will do the heavy lifting. We've made sure to sanitize all inputs, so there's no way anything could go wrong... right?

## Summary
- **Author:** Sayed Hamzah (@BaeSenseii)
- **Category:** Web Exploitation
- **Learning Objective:** Perform a command injection attack on an LLM-powered application (with a little bit of privilege escalation involved and a special surprise to view the flag :))

## Requirements
- linrev_lvl1

## Services
- [`websrv`](service) (port 8550:8550)
- [ollama](https://hub.docker.com/r/ollama/ollama)

## Hints
- `Never, ever trust what you see on your web browser. Look around the website (not the graphics duh).` (200 points)
- `https://gtfobins.github.io would definitely help when it comes to reading files.` (200 points)

## Flags
- `SPARK{G3N41_15Nt_50_54F3_51a}`
