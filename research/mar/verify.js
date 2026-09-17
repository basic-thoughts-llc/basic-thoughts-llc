"use strict";
document.getElementById("verify").addEventListener("click", async () => {
  const result = document.getElementById("result");
  const file = document.getElementById("file").files[0];
  const manifest = document.getElementById("manifest").files[0];
  if (!file || !manifest) { result.textContent = "Select a public file and its SHA256SUMS manifest."; return; }
  if (!globalThis.crypto?.subtle) { result.textContent = "Web Crypto is unavailable here. Use sha256sum -c SHA256SUMS locally."; return; }
  try {
    const entries = (await manifest.text()).split(/\r?\n/).map(line => line.match(/^([0-9a-f]{64})  (.+)$/i)).filter(Boolean);
    const matches = entries.filter(entry => entry[2] === file.name);
    if (matches.length !== 1) { result.textContent = "The manifest must contain exactly one entry for this filename."; return; }
    const digest = await crypto.subtle.digest("SHA-256", await file.arrayBuffer());
    const actual = Array.from(new Uint8Array(digest), b => b.toString(16).padStart(2, "0")).join("");
    result.textContent = (actual === matches[0][1].toLowerCase() ? "MATCH — " : "MISMATCH — ") + file.name + " · SHA-256 " + actual;
  } catch { result.textContent = "Could not read or verify the selected files. Try again or use sha256sum locally."; }
});
