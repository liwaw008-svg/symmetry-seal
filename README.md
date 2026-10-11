# Symmetry Seal

Three motions enter the square. One composite gesture leaves it.

The owner freezes three to eight public transformation artifacts. Validators translate each artifact into one bounded element of the eight-member symmetry group of a square. Contract code composes the corner permutations in source order. Identity closes the loop as `CLOSED`; every other transform remains visible as `DRIFT`.

The model identifies gestures. It never decides closure. Exact artifact digests, codes, and the final named transformation stay on-chain.

Fixtures are operator-authored demonstrations, not independent authorities.

```bash
genvm-lint contracts/contract.py
python -m pytest -q
```
