# CSupMNE Workshop Games — GitHub Pages deployment

Two browser games for the III.6 Protect training (HFU Schwenningen), ready to host on GitHub Pages.
No server, no build step — participants join from their phones by scanning a QR code.

| Path | Game | Session |
|---|---|---|
| `/` | Landing hub (links to both games) | — |
| `/backup/` | **Save the Student Records** — backup-plan builder + disaster simulation | Session 4 · Data Lifecycle and Backup |
| `/flaw/` | **Spot the Flaw — Human vs. Machine** — find vulnerabilities in student code, beat the LLM | Session 6 · Secure Software Development in HEIs |

## Deploy (one time, ~5 minutes)

1. Create a new GitHub repository, e.g. `csupmne-games` (public).
2. Upload **the contents of this folder** (`index.html`, `backup/`, `flaw/`, `.nojekyll`, `README.md`)
   to the repository root — on github.com: *Add file → Upload files*, drag everything in, commit.
3. Repository **Settings → Pages** → under *Build and deployment* choose
   **Deploy from a branch**, branch `main`, folder `/ (root)`, then **Save**.
4. Wait 1–2 minutes. Your games are live at:
   - `https://<your-username>.github.io/csupmne-games/` (hub)
   - `https://<your-username>.github.io/csupmne-games/backup/`
   - `https://<your-username>.github.io/csupmne-games/flaw/`

The `.nojekyll` file is required — it tells GitHub to serve the files as-is.

## On workshop day

1. On the beamer laptop, open the game URL (`/backup/` or `/flaw/`).
2. *Start the game* → **📱 With phones** → the lobby shows a **QR code + room code**.
3. Participants scan the QR with their camera app. Mobile data works fine —
   they do **not** need to be on the venue Wi-Fi.
4. Keep the host tab open for the whole session (it is the game server).
   If you accidentally reload, click **Resume** — the room code stays the same
   and phones reconnect automatically.
5. No network? Both games fully work in **Classic mode** (host clicks everything).

## If phones get stuck on "connecting…"

Some networks (eduroam, strict carriers) block direct WebRTC connections.

- **Quick fix:** ask affected participants to switch to mobile data.
- **Proper fix (recommended before the workshop):** in the game lobby open
  *"Phones stuck on connecting…? Add a TURN relay"*, create a free account at
  [metered.ca](https://www.metered.ca) (20 GB/month free), create an app + API key,
  and enter `appname:apikey`. It is saved on the laptop and embedded in the QR code,
  so all phones use the relay automatically.

## Updating the games

Replace `backup/index.html` or `flaw/index.html` with a new version and commit.
GitHub Pages caches for ~10 minutes — after an update, hard-refresh the host page
(Ctrl/Cmd+Shift+R) and have phones rescan the QR.

## Privacy

- No accounts, no tracking, no data stored on any server.
- Game traffic flows peer-to-peer between the host laptop and the phones (WebRTC);
  the PeerJS public broker is used only to establish the connection.
- Participants enter a first name only; everything vanishes when the tab closes.

---
CSupMNE · Erasmus+ (ERASMUS-EDU-2024-CBHE-STRAND-3 / 101179688) · Hochschule Furtwangen
