# The Phantom Page
A mysterious web experience: a haunted webpage hides a phantom script. Your task is to uncover the invisible JavaScript and reveal the secret flag.

## Summary
- **Author:** Aldric Liew
- **Category:** Web Exploitation
- **Learning Objective:** Practice inspecting web pages, analyzing client-side JavaScript, decoding obfuscated strings, and understanding how hidden assets can contain sensitive information.

## Files
- [`story.txt`](./dist/story.txt)

## Services
- [`thephantompage`](./service/Dockerfile) (port 5001:???)

## Hints
- `The real secret isn’t visible on the page. Check the network tab for hidden JS assets.` (200 points)
- `Look for base64-encoded strings or small string shards in the scripts.` (200 points)
- `Concatenate and decode to uncover the flag.` (200 points)

## Flags
- `SPARK{j3_l0oks_a2e_dec3ivi4g}`
