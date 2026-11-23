# x402 pay-per-call client for Gloom Datasets

Implements gloom.sh's documented no-account payment lane
(`gloom.sh/datasets/docs/x402.md`): x402 v2, USDC on Base, $0.03/credit —
e.g. `cds/curves` = 4 credits = **$0.12/call**.

## Setup

```
cd tools/x402 && npm install   # @x402/fetch, @x402/evm, viem (the documented stack)
```

Key file: a hex private key of a **dedicated low-balance Base wallet** —
never a main wallet — at `/root/.gloom-x402-key` (mode 600), or point
`X402_KEY_FILE` elsewhere. The script refuses anything not mode 600.

## Usage

```
node x402_fetch.mjs <url>             # paid call (signs + settles USDC on Base)
node x402_fetch.mjs <url> --dry-run   # prints the 402 payment terms; zero spend
```

Semantics that matter (from the docs): only successful answers settle — an
error or an empty batch charges nothing; one signed payment pays for exactly
one call (replays refused); 300 credits/minute per wallet, then 429.

## Verified behavior (2026-11-23, before any funding)

- `--dry-run` against `cds/curves?issuer=Oracle%20Corp&days=30` → 402 with the
  full payment block: 4 credits / $0.12, asset USDC `0x833589fC…`, network
  `eip155:8453` (Base), 120 s signature window.
- Full paid-mode run with the unfunded burner wallet →
  `402 payment_invalid: insufficient_funds … Nothing was charged.` — i.e. the
  sign-and-resend loop works end to end; the server validated the signature
  and checked the on-chain balance. Funding is the only missing step.

## Finding that unblocks item 4's parser

The 402 response's `bazaar` extension carries the **response shape** for
`cds/curves`: `data[].spreadBp` — spreads in basis points directly. The
`spreadNotation` ambiguity that `scripts/kscreen_cds.py` (correctly) refuses
to guess at belongs to the trades/sample route; **the curves route, which is
the route the K-screen should use anyway, needs no notation table.**
