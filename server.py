#!/usr/bin/env python3
"""
CSupMNE Workshop Games - local relay server (zero dependencies, Python 3.7+).

Serves the game files AND relays game messages between the host screen and
the phones over plain HTTP - fully offline, perfect for a laptop hotspot.

Usage:
    python3 server.py [--port 8080] [--ip AUTO] [--dir .]

The games auto-detect this server: choose the mode "Local network" in the
game lobby. Phones join the same Wi-Fi and scan the QR code.
"""
import argparse
import json
import socket
import subprocess
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

MAX_ROOMS = 50
MAX_ACTIONS = 1000
CLIENT_LIVE_S = 6
HOST_LIVE_S = 12

rooms = {}          # code -> {snap, v, actions:[(seq,cid,msg)], seq, seen:{cid:ts}, host_seen:ts}
lock = threading.Lock()


def get_room(code, create=False):
    code = (code or '').upper()[:8]
    if not code:
        return None
    with lock:
        if code not in rooms:
            if not create:
                return None
            if len(rooms) >= MAX_ROOMS:
                oldest = min(rooms, key=lambda k: rooms[k]['host_seen'])
                del rooms[oldest]
            rooms[code] = {'snap': None, 'v': 0, 'actions': [], 'seq': 0,
                           'seen': {}, 'host_seen': 0}
        return rooms[code]


def detect_ip(prefer=None):
    if prefer:
        return prefer
    # 1. hotspot bridge (macOS Internet Sharing)
    try:
        out = subprocess.run(['ipconfig', 'getifaddr', 'bridge100'],
                             capture_output=True, text=True, timeout=3)
        ip = out.stdout.strip()
        if ip:
            return ip
    except Exception:
        pass
    # 2. default-route trick (no packet is sent)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
        s.close()
        if ip and not ip.startswith('127.'):
            return ip
    except Exception:
        pass
    return '192.168.2.1'


class Handler(SimpleHTTPRequestHandler):
    server_ip = None
    server_port = None

    def log_message(self, fmt, *args):  # keep the console calm
        pass

    def _json(self, obj, code=200):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        try:
            n = int(self.headers.get('Content-Length', 0))
            if n <= 0 or n > 512 * 1024:
                return None
            return json.loads(self.rfile.read(n).decode())
        except Exception:
            return None

    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        now = time.time()

        if u.path == '/api/ping':
            return self._json({'ok': True, 'ip': self.server_ip,
                               'port': self.server_port, 'name': 'csmne-local'})

        if u.path == '/api/state':
            room = get_room(q.get('room', [''])[0])
            cid = q.get('cid', [''])[0][:32]
            try:
                v = int(q.get('v', ['0'])[0])
            except ValueError:
                v = 0
            if not room:
                return self._json({'exists': False})
            with lock:
                if cid:
                    room['seen'][cid] = now
                host_ok = (now - room['host_seen']) < HOST_LIVE_S
                out = {'exists': host_ok, 'v': room['v']}
                if room['v'] > v and room['snap'] is not None:
                    out['snap'] = room['snap']
            return self._json(out)

        if u.path == '/api/actions':
            room = get_room(q.get('room', [''])[0], create=True)
            try:
                since = int(q.get('since', ['0'])[0])
            except ValueError:
                since = 0
            with lock:
                room['host_seen'] = now
                acts = [{'cid': c, 'msg': m} for (s, c, m) in room['actions'] if s > since]
                live = [c for c, ts in room['seen'].items() if now - ts < CLIENT_LIVE_S]
            return self._json({'seq': room['seq'], 'actions': acts, 'live': live})

        # static files
        self.headers.replace_header('Accept-Encoding', 'identity') if self.headers.get('Accept-Encoding') else None
        return super().do_GET()

    def do_POST(self):
        u = urlparse(self.path)
        now = time.time()

        if u.path == '/api/host':
            data = self._read_json()
            if not data or 'room' not in data:
                return self._json({'ok': False}, 400)
            room = get_room(data['room'], create=True)
            with lock:
                room['snap'] = data.get('snap')
                room['v'] += 1
                room['host_seen'] = now
            return self._json({'ok': True, 'v': room['v']})

        if u.path == '/api/action':
            data = self._read_json()
            if not data or 'room' not in data or 'msg' not in data:
                return self._json({'ok': False}, 400)
            room = get_room(data['room'], create=True)
            cid = str(data.get('cid', ''))[:32]
            with lock:
                room['seq'] += 1
                room['actions'].append((room['seq'], cid, data['msg']))
                if len(room['actions']) > MAX_ACTIONS:
                    room['actions'] = room['actions'][-MAX_ACTIONS:]
                if cid:
                    room['seen'][cid] = now
            return self._json({'ok': True, 'seq': room['seq']})

        return self._json({'ok': False, 'error': 'unknown endpoint'}, 404)

    def end_headers(self):
        # never let phones cache a stale game build from this server
        if not self.path.startswith('/api/'):
            self.send_header('Cache-Control', 'no-cache')
        super().end_headers()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--port', type=int, default=8080)
    ap.add_argument('--ip', default=None, help='LAN IP to advertise (auto-detected if omitted)')
    ap.add_argument('--dir', default=None, help='directory with the game files (default: this script\'s folder)')
    args = ap.parse_args()

    import os
    base = args.dir or os.path.dirname(os.path.abspath(__file__))
    os.chdir(base)

    ip = detect_ip(args.ip)
    Handler.server_ip = ip
    Handler.server_port = args.port

    srv = ThreadingHTTPServer(('0.0.0.0', args.port), Handler)
    print('CSupMNE local game server')
    print('  serving : ' + base)
    print('  open    : http://%s:%d/            (hub)' % (ip, args.port))
    print('  backup  : http://%s:%d/backup/     (Session 4)' % (ip, args.port))
    print('  flaw    : http://%s:%d/flaw/       (Session 6)' % (ip, args.port))
    print('  In the game choose:  Local network')
    print('  Stop with Ctrl+C')
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print('\nserver stopped')


if __name__ == '__main__':
    main()
