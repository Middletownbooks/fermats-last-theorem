# Held out — do not show this directory to a scored agent

These files contain the after-boards and the transformation labels. Everything in P1 that could be
called a result depends on an agent never having seen them.

- `tools/pack.py` cannot read this directory. Its `_read()` refuses any path resolving under
  `heldout/`, so the agent-visible bundle cannot accidentally include an answer.
- `tools/validate.py` fails the tree if any 8-word run of an after-board appears anywhere in the
  corresponding `before.json`.

Every file here is labelled by one contaminated rater. `second_blind_label` is `null` throughout:
**no label κ exists yet**, so no claim about the taxonomy's operational status can be made from this
tree as it stands.
