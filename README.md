# Symmetry Seal

Three motions enter the square. One composite gesture leaves it.

The owner freezes three to eight public transformation artifacts. Validators translate each artifact into one bounded element of the eight-member symmetry group of a square. Contract code composes the corner permutations in source order. Identity closes the loop as `CLOSED`; every other transform remains visible as `DRIFT`.

The model identifies gestures. It never decides closure. Exact artifact digests, codes, and the final named transformation stay on-chain.

Fixtures are operator-authored demonstrations, not independent authorities.

```bash
genvm-lint contracts/contract.py
python -m pytest -q
```

## Live seal

- Contract: [`0x84925293887DA9e1e895dA072D62f72cf842F658`](https://explorer-studio.genlayer.com/address/0x84925293887DA9e1e895dA072D62f72cf842F658)
- Reviewed source: [`6b840e2`](https://github.com/liwaw008-svg/symmetry-seal/tree/6b840e22cc790024e6d788f25cffb8d3ff361d31)
- Live seal: `SEAL-1791758206`, final state `CLOSED`, codes `[1,2,1]`, composite `IDENTITY`.
- Verification: finalized, majority agree, successful execution, exact deployed-source match.
