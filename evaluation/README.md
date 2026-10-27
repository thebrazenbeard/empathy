# Synthetic response-policy discrimination pilot

Run from the repository root:

```sh
python -m evaluation.policy_discrimination
python -m unittest discover -s tests -v
```

This pilot supplies **12 hand-authored minimal pairs (24 scenarios)** to the
research-only `choose_policy` API. Within each pair, the observable utterance is
identical. The typed, caller-admitted observations change a decisive condition:
reciprocal play versus withdrawal, task versus celebration, direct correction,
historical versus current evidence, or authenticated person scope.

For a deliberately weak negative control, `lexical_only_baseline()` sees only
the utterance. It cannot discriminate a same-wording pair by construction. Its
score is an engineering sanity check, not a competitive natural-language model
baseline. The selector receives **already-classified evidence** and does not
infer those observations from language, verify them, or know that they are
authentic, current, or consensual.

**Falsifiers:** any selector mismatch, any pair in which the selector chooses
the same policy despite opposite expected contextual effects, or any
cross-person/history promotion invalidates this narrow contract benchmark.
The expected decisions are written by the authors from the current documented
policy; these examples are neither an independent human-annotated corpus nor
held-out data. Passing cannot establish calibrated confidence, real-world
empathic accuracy, genuine care, model training, or a deployed Vera runtime.

Do not insert private relationship cases into this public repository. Future
evaluation should use consented, separately governed human annotations and
blind, preregistered comparisons, keeping policy selection distinct from
perceived warmth and actual human impact.
