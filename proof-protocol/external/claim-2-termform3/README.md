# Report Q, staged for the parent project — NOT pushed there

This directory is a **mirror**. The work belongs in the larger project,
`Middletownbooks/claim-2`, at `theorem-lab/termform3/`, on the branch
`claude/theorem-discovery-lab-jpbph1`. It is kept here only because this session
has **read** access to that repository and no permission to push to it, and the
container is ephemeral.

## What it is

`REPORT_Q.md` is the experiment the parent project's `STATUS.md` recommended
("Thread 1, informed by thread 2") in the form Report P's section 12 refined it
into: cut the receiving round's quantifier-**body** budget so that the carried
vocabulary is provably outside its reach, certify that gap by exhaustive
enumeration, and ask whether carry-over then transmits anything.

It does. `certificate.py` exhausts the receiving round's formation (599 formed
terms, no truncation) and shows none of the seven carried terms is formable there
— the first time `V₁ ⊄ reachable(V₀)` is established by enumeration in this
programme rather than assumed. Carrying those seven adds two invariants that are
certified unreachable without them, in searches whose cost-5 spaces are
**exhausted** rather than beamed:

```
is_prime_power  cost 5  ((2 * <count(k: n % (k*k))>) // <count(k: n % k)>)
odd_divisors    cost 3  gcd(<count(k: n % (k+k))>, <count(k: n % k)>)
```

Four cheaper explanations were run and eliminated (matched atom count with
self-formed units; random out-of-reach carry; carry withheld from formation;
3.7× the compute). Five of eight pre-registered predictions held, two failed and
one was struck; the failure is a measurement error worth reading — see §8.

## How to land it

Two equivalent routes. Both put it exactly where it belongs and neither touches
`termform/` or `termform2/`, which stay byte-identical.

**A bundle, preserving both commits and their messages:**

```
git -C <claim-2 checkout> fetch /path/to/termform3.bundle \
    claude/theorem-discovery-lab-jpbph1:refs/heads/report-q
git -C <claim-2 checkout> merge --ff-only report-q     # or cherry-pick the two commits
```

The bundle contains two commits on top of `7dd6935`:
the pre-registration (committed **before** any search was run, sha256 in
`PREREG.sha256`) and the report with its twelve artifacts.

**Or copy the files:** everything except `termform3.bundle` and this `README.md`
goes to `theorem-lab/termform3/`. Reproduce with
`python3 promote3.py && python3 certificate.py && python3 round3.py <COND>` for
`COND` in `A3u A3u52 C3u B3uo B3u A3 C3 D3 B3 B3all A3plus A5`, then
`python3 analyze3.py`. Total runtime about 30 minutes; `numpy` is the only
dependency beyond the repository itself.

## Provenance

Written in a session whose designated push target was
`middletownbooks/fermats-last-theorem`, branch
`claude/retrodiction-benchmark-p1-8ne806`. The parent repository was attached
read-only, so this mirror is the honest place for the work until someone with push
access moves it. Nothing here was pushed to `claim-2`.
