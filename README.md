# TimeSeal

**Local-first crew time and attendance evidence sealer for field operators.**

Offline. Deterministic. Pay once. Compatible with QuantumGuard CONTRACT-v1 and the Operator Pages suite.

## Why TimeSeal?

Disputes over crew hours, overtime, or "who was on site" cost operators money.  
TimeSeal captures structured time logs (crew members, clock-in/out, tasks, locations, notes) and seals them into a client-verifiable QuantumGuard evidence bundle.

- No SaaS. No subscription. Runs completely offline after key setup.
- Clients (or auditors) verify with free QuantumGuard verifier (`qg verify`).
- Deterministic: same inputs → same sealed pack.
- Pairs with DailySeal, BinderSeal, FuelSeal, EquipmentSeal.

## Quick Start

```bash
pip install cryptography

python3 src/timeseal.py --demo
python3 src/timeseal.py --json samples/time-001.json --out sealed-time.json
```

Verify:
```bash
qg verify sealed-time.json
```
Expected: **PASS**.

## What you can sell

| SKU       | Price | Includes                                      |
|-----------|-------|-----------------------------------------------|
| Operator  | $49   | CLI + sample templates + key setup guide + 1-year email support |
| Command   | $149  | + batch mode + CSV export + reseller rights |
| Agency    | $399  | + white-label + multi-site key management |

**Buy Operator Pack (test mode):** Use Stripe product `prod_VakZfTZH1D5NdG` / price `price_1UZZ4QAAQSB4Mr7sWkQjtiDd`.  
Contact: danpennic@gmail.com  
Repo: https://github.com/danpennic-sys/timeseal

Source free under Apache-2.0 OR MIT. Commercial packs sold separately.

## License

Apache-2.0 OR MIT
