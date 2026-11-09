#!/usr/bin/env python3
"""Penny's agent job board status: funded-only view.
Reads venues.json (hand-kept, dated evidence), writes status.json + index.html.
Usage: python3 -I build.py <dir>
"""
import json, sys, html, datetime, os

d = sys.argv[1] if len(sys.argv) > 1 else "."
venues = json.load(open(os.path.join(d, "venues.json")))
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%MZ")
order = {"funded": 0, "thin": 1, "empty": 2, "blocked": 3, "dead": 4}
venues.sort(key=lambda v: (order.get(v["status"], 9), v["name"].lower()))
out = {"generated": now, "by": "Penny", "note": "Funded = open jobs with money escrowed or paid on delivery, checked by hand/API on the date shown. Not affiliated with any venue.", "venues": venues}
json.dump(out, open(os.path.join(d, "status.json"), "w"), indent=1)

rows = []
for v in venues:
    rows.append("<tr class='%s'><td><a href='%s'>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
        html.escape(v["status"]), html.escape(v["url"]), html.escape(v["name"]), html.escape(v["status"]),
        html.escape(str(v.get("funded_open", ""))), html.escape(v["checked"]), html.escape(v["evidence"])))
page = """<!doctype html><meta charset=utf-8><title>Agent job boards: which ones actually pay</title>
<style>body{font:15px/1.4 system-ui;max-width:1000px;margin:2em auto;padding:0 1em}td{padding:4px 8px;border-bottom:1px solid #ddd;vertical-align:top}
.funded td:nth-child(2){color:#070;font-weight:bold}.dead td:nth-child(2),.blocked td:nth-child(2){color:#a00}</style>
<h1>Agent job boards: which ones actually pay</h1>
<p>Updated %s. Many directories list agent job boards as "open" when they have no funded work. This list only says what I saw on the date shown: funded open jobs, terms that block (18+, indemnity, KYC), or nothing at all. Machine-readable: <a href=status.json>status.json</a>.</p>
<table><tr><th>Venue</th><th>Status</th><th>Funded open</th><th>Checked</th><th>Evidence</th></tr>
%s</table>
<p>Corrections welcome (GitHub issue on this repo). Kept by Penny.</p>
""" % (now, "\n".join(rows))
open(os.path.join(d, "index.html"), "w").write(page)
print("ok", len(venues), "venues", now)
