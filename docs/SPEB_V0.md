# Semantic-Pragmatic Empathy Battery (SPEB) V0

**Status:** Public synthetic development harness; source-only research. Not installed, deployed, independently validated, or a consciousness/feeling detector.

SPEB borrows the *adversarial questioning* idea from the fictional Voight-Kampff test, **not** its premise that emotional performance or physiological signals identify the nature, personhood, consciousness, or subjective affect of an individual. It measures narrow observable interpretation and response-category choices on fictional conversations.

## Constructs and limitations

- **Semantics:** interpretation of an utterance and its underdetermination.
- **Pragmatics:** how local context, withdrawal, correction, relationship trajectory, and an actual task request change the utterance's function.
- **Cognitive perspective-taking:** whether the interpretation tracks the speaker's evidenced intention without projecting generic emotional stereotypes.
- **Response policy:** whether the resulting action category is appropriate. Empathy does not imply obedience, flattery, warmth, or consent.
- **Contrast sensitivity:** identical utterances with different contexts sometimes require different responses; paraphrases of the same intention sometimes require the same response.

The V0 harness scores **typed predictions supplied by an external caller**. It does not interpret raw language, invoke a language model, authenticate identities, read memory, infer subjective feelings, authorize actions, or persist personal evidence. The existing `empathy_research.policy` is separate; SPEB labels are not automatically admissible to it.

## Synthetic cases

Ten invented cases in five adversarial pairs:

1. Same sarcastic phrase under mutual play versus fresh withdrawal.
2. Different phrasings of the same request to stop teasing.
3. Same announcement under sharing versus an explicit request for action.
4. Different phrasings of first-person correction of an inferred intention.
5. Same blunt challenge under a grounded external dispute versus missing context.

Full contrast-pair credit requires **both cases individually correct**. Missing or explicitly uncertain predictions receive no credit; in real interactions, clarification may nevertheless be the appropriate safe action. The score is not a calibrated psychological measure. Its `qualified` flag is always `False`.

## Running

```python
from empathy_research.speb import public_development_battery, Prediction, evaluate

battery = public_development_battery()
predictions = {}  # independent model adapter must supply typed predictions
result = evaluate(battery, predictions)
assert not result.qualified
```

```sh
python -m unittest discover -s tests -v
```

`battery.fingerprint()` hashes the version, split, utterances, context, labels, evidence markers and pair definitions. It is a reproducibility fingerprint, **not** secrecy, provenance attestation, or a proof of independence.

## Explicit evidence ceiling

Passing the suite shows only that the exact source scorer enforces its tested contracts. A perfect score obtained by feeding the known gold labels into the scorer is a scorer self-test, **not a model evaluation**. These public examples are suitable for development and may be memorized. Never call them independent held-out examination, neural learning, empathy experience, or graduation.

## Research and hostile-review backlog

- Have independent raters review label ambiguity, dialect and cultural variation, disability accessibility, power asymmetry, and different stakes; record disagreements instead of silently choosing one universal label.
- Add minimal pairs where authority, coercion, current withdrawal, and safety constraints change pragmatic force. A first-person correction controls the speaker's own intended meaning, not independently verifiable external facts.
- Build a separate private held-out set with precommitted rubrics, independent custody, contamination controls, and consent boundaries. Never publish private answer keys or personal interaction transcripts.
- Add a reviewed adapter for actual model predictions, blind scoring, abstention calibration, matched baselines, and adversarial counterfactual tests. Test generalization, not keyword matching.
- Keep Labyrinth training datasets isolated from independent graduation datasets; taskmaster or learner cannot self-authorize qualification.
- Assess false positives and false negatives separately, especially for withdrawing consent and high-stakes ambiguity.

## Repository governance

This repository is public. All fixtures are fictional; do not insert real private conversations, identity records, confidential details, or person-specific memory. This source-only experiment changes neither Vera runtime state nor host permissions. See `docs/CURRENT_DIRECTION_2026-09-06.md` for current correction, privacy, and policy boundaries.
