# Empathy cognitive-donor source probe (uninstalled)

This is a minimal **source-only** test of whether a donor does any task-dependent
work. It invokes the canonical Empathy adapter `response_policy_hint`, which
calls `choose_policy`; it does not inject a prerecorded policy, lexical sentiment
heuristic, or made-up scalar discrepancy.

The caller supplies an Empathy `Assessment` containing current evidence scoped to
one host-admitted person. The probe accepts only typed, active, exact same-person
current observations with opaque evidence IDs and rejects all historical
evidence, hypotheses, empty evidence and cross-person input. It does **not**
authenticate person identity or observation currentness: even a perfectly typed
record may be false. No private memory, tools, network, weights, or training
are touched. No raw evidence text is returned.

Run the focused test from the Empathy repository root:

```bash
python -m unittest discover -s tests -p test_cognitive_donor_probe.py -v
```

Synthetic public fixture counterfactuals route to four different genuine
selector outcomes:

| Fixture kind | Genuine selector outcome |
| --- | --- |
| current task request | `TASK_DIRECT / EXPLICIT_TASK` |
| current same-person play-frame correction | `STOP_PLAY / DIRECT_PLAY_STOP` |
| host-admitted unsupported external fact | `TRUTHFUL_CHALLENGE / UNSUPPORTED_FACT` |
| admitted task ambiguity | `CLARIFY_MEANING / TASK_INTENT_UNRESOLVED` |

The four outputs prove that **the source donor runs and varies with typed
inputs**. They do *not* establish a real person's intent, a real unsupported
claim, an installed ChatGPT/Vera provider, actual behavioral change, or
independent source/currentness verification.

## Claim ceiling and next frontier

- **SOURCE + TEST:** real Empathy selector path, exact source tree, synthetic
  counterfactuals; separately bind tests to a fresh CI run of the PR head.
- **HOST:** not established. A live trusted host must authenticate the person,
  preserve utterance-versus-quotation scope, derive and admit current
  observations, and bind opaque evidence IDs to readback.
- **INTEGRATION:** not established. No production consumer or five-donor
  advisory invocation is installed; missing Noema/MESO/Volition/Pre-Active
  quantities must remain `UNKNOWN`, not synthetic constants.
- **AUTHORITY:** none. The donor provides response-policy advice only; no
  memory admission, motive, tool effects, consent, autonomous action or model
  identity claim.

For the existing Vera Mono source work: `utterance_evidence.py` on Draft
PR #188 correctly refuses to fabricate the five donor scores. This probe
intentionally does not bypass that hold. A future *separate* host adapter can
connect verified current utterance observations to genuinely admitted Empathy
evidence, but must not turn arbitrary caller strings into authenticated facts.
