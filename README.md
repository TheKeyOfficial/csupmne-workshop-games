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

## Pre-workshop check (do this once, takes 2 minutes)

1. Open the game on the host laptop → *With phones* → lobby.
2. Open **"🧪 Connection self-test"** and click *Run self-test*. It verifies both
   signaling brokers, the room, and (if configured) the TURN relay end-to-end.
3. Join once with your own phone. Green pill = you're done.
4. The lobby and the phone join screen show a **build stamp** (e.g. `build v2.2`) —
   if host and phones show different builds, someone has a cached old version
   (hard-refresh / rescan the QR).

## If phones get stuck on "connecting…"

The games connect through public signaling brokers with automatic failover
(the official PeerJS cloud is frequently rate-limited — HTTP 429 — so a reliable
community broker is tried first, and the chosen broker travels inside the QR code).
The lobby shows live status under the room code: "✓ room open — phones can join".

Beyond that, some networks (eduroam, strict carriers) block direct WebRTC connections.

- **Quick fix:** ask affected participants to switch to mobile data.
- **Proper fix (recommended before the workshop):** in the game lobby open
  *"Phones stuck on connecting…? Add a TURN relay"*, create a free account at
  [metered.ca](https://www.metered.ca) (20 GB/month free), create an app + API key,
  and enter `appname:apikey`. It is saved on the laptop and embedded in the QR code,
  so all phones use the relay automatically.

## Fully offline: local network mode + Mac hotspot

No internet at the venue? The kit in this folder runs everything offline:

1. Copy this whole folder onto the host MacBook.
2. Double-click **`start-workshop-hotspot.command`** (first run: right-click → Open).
   It creates the Wi-Fi hotspot **CSupMNE-Workshop** (password `workshop_game`),
   starts the local game server, and prints the game addresses.
   **Ctrl+C stops hotspot and server.**
3. Open the printed address (e.g. `http://192.168.2.1:8080/backup/`) on the laptop,
   choose **🏠 Local network** in the game — the QR appears.
4. Participants join the hotspot Wi-Fi, ignore the "no internet" warning,
   and scan the QR. Everything runs on the laptop; no brokers, no TURN, no internet.

Notes:
- **Disconnect from any Wi-Fi network first** (⌥-click the Wi-Fi menu icon →
  Disconnect). A Mac cannot be a hotspot and a Wi-Fi client at the same time —
  this is the #1 reason the hotspot silently fails to start.
- macOS has no official CLI for Internet Sharing. The script tries two scripted
  start methods and, if macOS blocks them, opens the Sharing pane so you toggle
  Internet Sharing ON once ("Internetfreigabe" on German systems) — it detects
  the hotspot and does everything else, including shutdown on Ctrl+C.
- If the hotspot name/password don't apply on your macOS version, set them once
  in *System Settings → General → Sharing → Internet Sharing (ⓘ)*.
- No-hotspot Plan B: use any phone's personal hotspot — laptop and all phones
  join it, run `python3 server.py` in this folder, open the printed address.
  Same game, same QR, zero macOS quirks.
- The server (`server.py`) needs Python 3 (comes with Apple's command line tools).
- You can also use local mode on any existing Wi-Fi/LAN without the hotspot:
  `python3 server.py` in this folder, then open the printed address.

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
