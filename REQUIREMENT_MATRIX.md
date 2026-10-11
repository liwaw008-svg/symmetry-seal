# Requirement matrix

| Requirement | Mechanism | Status |
|---|---|---|
| Consensus-bound source classification | Strict D4 extraction with refetch and digest | PASS: forged transform rejected |
| Complete canonical output | One unique bounded code per source | PASS: strict direct suite |
| Deterministic result | Exact permutation composition | PASS: rotations and reflections tested |
| Replay and cancellation rules | Terminal resolution, owner-only open cancellation | PASS: targeted tests |
| Exact deployed source | Transaction source comparison | PASS: exact byte match |
