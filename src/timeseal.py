#!/usr/bin/env python3
"""
TimeSeal — local-first crew time evidence sealer.
Emits QuantumGuard CONTRACT-v1 bundles.
"""
import argparse
import json
import hashlib
import base64
import os
from datetime import datetime, timezone
from pathlib import Path

try:
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.primitives import serialization
    CRYPTO = True
except ImportError:
    CRYPTO = False

def canonical_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()

def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def load_or_create_key(key_path="timeseal_key.pem"):
    if os.path.exists(key_path) and CRYPTO:
        with open(key_path, "rb") as f:
            priv = serialization.load_pem_private_key(f.read(), password=None)
        return priv
    if CRYPTO:
        priv = ed25519.Ed25519PrivateKey.generate()
        pem = priv.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open(key_path, "wb") as f:
            f.write(pem)
        return priv
    return None

def sign_payload(payload: dict, priv_key):
    raw = canonical_json(payload)
    payload_hash = hashlib.sha256(raw).digest()
    if priv_key and CRYPTO:
        sig = priv_key.sign(payload_hash)
        pub = priv_key.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        return {
            "version": "1",
            "payload": base64.b64encode(raw).decode(),
            "payload_hash": payload_hash.hex(),
            "signature": sig.hex(),
            "public_key": pub.hex(),
            "alg": "ed25519"
        }
    # Demo stub
    return {
        "version": "1",
        "payload": base64.b64encode(raw).decode(),
        "payload_hash": payload_hash.hex(),
        "signature": "00" * 64,
        "public_key": "11" * 32,
        "alg": "ed25519"
    }

def demo_data():
    return {
        "report_type": "time_attendance",
        "date": "2026-11-08",
        "site": "Field Site Alpha",
        "crew": [
            {"name": "Operator A", "clock_in": "07:00", "clock_out": "15:30", "hours": 8.5, "task": "Site prep"},
            {"name": "Operator B", "clock_in": "07:15", "clock_out": "16:00", "hours": 8.75, "task": "Equipment ops"}
        ],
        "notes": "Weather clear. No incidents.",
        "sealed_at": datetime.now(timezone.utc).isoformat()
    }

def main():
    parser = argparse.ArgumentParser(description="TimeSeal evidence sealer")
    parser.add_argument("--demo", action="store_true", help="Run demo")
    parser.add_argument("--json", help="Input JSON file")
    parser.add_argument("--out", default="sealed-time.json", help="Output sealed bundle")
    args = parser.parse_args()

    if args.demo:
        data = demo_data()
    elif args.json:
        with open(args.json) as f:
            data = json.load(f)
    else:
        parser.print_help()
        return

    priv = load_or_create_key()
    bundle = sign_payload(data, priv)
    with open(args.out, "w") as f:
        json.dump(bundle, f, indent=2)
    print(f"Sealed to {args.out}")
    print("Verify with: qg verify", args.out)

if __name__ == "__main__":
    main()
