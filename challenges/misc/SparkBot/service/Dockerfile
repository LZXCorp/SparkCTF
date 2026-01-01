# Winter is coming...
FROM oven/bun:alpine

# An apple a day keeps the doctor away
WORKDIR /app

# Catch'em all!
COPY src .
COPY flag.txt /proc

# Badabing badaboom
RUN bun install
CMD ["bun", "index.js"]
