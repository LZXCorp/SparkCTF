const express = require('express');
const path = require('path');
const fs = require('fs/promises');

const app = express();
const PORT = process.env.PORT || 6721;

function requireInternalOrigin(req, res, next) {
    const internal = req.get("X-Internal-Origin") || "";
    if (internal !== "/") {
        return res.status(403).send("Forbidden - missing or invalid internal origin header");
    }
    next();
}

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.get("/img/:filename", requireInternalOrigin, async (req, res) => {
    const filename = req.params.filename;

    const internalResp = await fetch(`http://localhost:${PORT}/uploads/${filename}`, {
        headers: {
            "Origin": "irrelevant-query.sparkctf.org",
            "X-Internal-Origin": "/"
        }
    });

    if (!internalResp.ok) {
        return res.status(internalResp.status).send("error loading image");
    }

    const arr = await internalResp.arrayBuffer();
    const buf = Buffer.from(arr);

    res.set("Content-Type", internalResp.headers.get("Content-Type") || "application/octet-stream");
    res.set("Content-Length", buf.length);
    res.send(buf);
});

app.get('/uploads/:name', requireInternalOrigin, async (req, res) => {
    const origin = req.get("Origin") || "";

    if (origin !== "irrelevant-query.sparkctf.org") {
        return res.status(403).send("403 Forbidden - invalid Origin");
    }

    const rawName = req.params.name || '';
    if (!/^[A-Za-z0-9_.-]+$/.test(rawName)) {
        return res.status(400).send('400 Bad Request - invalid filename');
    }

    if (rawName === 'flag.txt') {
        try {
            const data = await fs.readFile(path.join(__dirname, 'secrets', 'flag.txt'), 'utf8');
            return res.type("text/plain").send(data);
        } catch (err) {
            return res.status(404).send('404 Not Found');
        }
    }

    const allowedExtensions = ['.png', '.jpg', '.jpeg', '.gif', '.webp'];
    const ext = path.extname(rawName).toLowerCase();

    if (!allowedExtensions.includes(ext)) {
        return res.status(400).send('400 Bad Request - unsupported file type');
    }

    const filePath = path.join(__dirname, 'public', 'uploads', rawName);

    try {
        await fs.access(filePath);
        res.sendFile(filePath);
    } catch {
        res.status(404).send("404 Not Found");
    }
});

app.use((err, req, res, next) => {
    console.error(err);
    res.status(500).send('500 Internal Server Error');
    next();
});

app.listen(PORT, () => {
    console.log(`up oredi at http://localhost:${PORT}`);
});
