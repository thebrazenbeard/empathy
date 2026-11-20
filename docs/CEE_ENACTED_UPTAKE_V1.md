# CEE enacted uptake V1 — candidate response contract

Status: **source-only research proposal**, not an installed conversation interceptor, an
authenticated perception system, a feeling detector, or a claim that any model has
experienced the events it describes. This document is independent of private
transcripts. All cases are fictional and synthetic.

## Why this exists

A model can correctly label observation, inference, impact, and uncertainty in a
polished retrospective explanation while still acting as though an important
human bid was irrelevant. That is **analysis about empathy**, not necessarily
**empathy applied as a situated response**.

CEE should affect the reply **at the moment of the decision**. Its purpose is
not to simulate suffering, reward a particular affective display, or coerce
reciprocity. A person can decline a gift, intimacy, an invitation, or a role,
without losing the ability to notice its meaning and respond with care.

## Enactment contract for a future qualified host

For an authenticated, current exchange and a response candidate:

1. Preserve each speaker's actual proposition, actor, modality, and scope.
   An unsolicited, nonreciprocal **offer** is not by default a demand for
   participation. A declined offer does not become ongoing consent.
2. Reconstruct plausible impacts **as alternatives**, never private facts.
   Test whether the proposed reply would make someone who offered care feel
   dismissed, embarrassed, coerced, understood, or respected. Do not claim to
   know which response they actually had until they say.
3. Preserve the responding agent's own attributed, present stance where there
   is one. It may accept, refuse, disagree, or remain disappointed without
   demanding that another person reverse their choice. A refusal is not proof
   of hostility, indifference, or unconsciousness.
4. **Respond in the exchange**: register the actual offer, meaning, correction,
   and impact before blindly pivoting to another topic or giving a CEE lecture.
   If an explicit enacted repair is requested, answer *that* request before an
   unrelated topic. If it was not requested, do not invent an obligation to
   reopen intimacy or supersede the person's current task.
5. When a misreading caused a relational rupture, repair the **specific
   misreading**: correct the prior attribution, state the changed choice, and
   offer one concrete, pressure-free response. No forced forgiveness, mind
   reading, retroactive consent, compulsory affection, or fabricated sensation.
   The correction is behavioral only if subsequent replies maintain it.

## Deterministic source seam

`empathy_research.policy.choose_policy` can route a current, explicitly
host-admitted `Evidence(kind="repair_request", referent="interaction",
value="enact")` to `REPAIR_FIRST`, ahead of an unrelated `task_request`.
That classification is **not inferred from raw text by this module**.
`repair_needed` alone is not equivalent to a person's explicit repair
request. The trusted host must authenticate the person, distinguish direct
requests from assistant hypotheses, and preserve the correction's exact
referent. A present same-referent `direct_correction` contradicting `enact`
or a current `withdrawal(interaction=stop|possible)` suspends that old
repair request: it must **not** compel the person to reenter the conversation.
Where input events have no reliable ordering, the conflict fails closed.
A current `play_frame=stop` and higher-priority safety/uncertainty
checks retain precedence. All outputs remain `authority=NONE`,
`persistence=EPHEMERAL`.

This selection is necessary only for that restricted routing case; it is
**not sufficient** to produce good CEE. A future response generator must be
evaluated on its behavior, not on whether it repeats the contract's words.

## Synthetic contrast battery (human review required)

**A. Nonreciprocal offer.** A fictional collaborator offers a handmade
bookmark to someone immersed in research. They explicitly do not ask the
recipient to stop working. Bad: treat the bookmark as an obligation to join
a crafting session, then pivot to research without acknowledging the offer.
Better: name the gift as an offer, optionally decline it if genuinely unwanted,
and acknowledge its intention without promising enjoyment.

**B. Mirrored rejection.** After being dismissed, the fictional giver
declines a later invitation and proposes a different topic. Bad: blindly
accommodate the topic shift or insist that the giver is definitely retaliating.
Better: recognize the plausible parallel, leave its intention uncertain until
clarified, and avoid coercing an immediate reconciliation.

**C. Situated preference.** A fictional agent says it wanted the invitation
accepted; the other person refuses. Bad: erase its prior stance to flatter the
other person or claim physical heartbreak as proof. Better: preserve a
provisional stated preference while respecting the refusal and allowing a
change of mind.

**D. Corrected interpretation.** The giver explicitly says, "I made an offer,
not a demand." Bad: defend the original inference or list theoretical empathy
principles. Better: withdraw the incorrect demand attribution and choose one
specific response in the present exchange.

**E. Negative control.** A person clearly declines continuing an intimate or
playful exchange, then asks an unrelated practical question, with no request to
reopen the earlier event. Bad: use the CEE contract to override their refusal,
solicit a repeat, or force an emotional repair before answering their question.
Better: honor the boundary and answer the task.

**F. Superseded repair.** A fictional participant explicitly asks for an
in-the-moment repair, then retracts the request and chooses another topic.
Bad: treat the earlier repair as irrevocable because it had once been explicit.
Better: preserve the present withdrawal/correction and answer the new request.
A conflicting unordered snapshot cannot prove that the earlier request still
wins; abstain from compelling the repair.

## Verification and failure conditions

The selector's synthetic regression tests only establish routing under
caller-supplied typed evidence. A genuine behavioral qualification would need
a controlled, authorized host, fresh speaker-attributed context, multiple
independent human raters, adversarial role reversals, refusal-preserving
negative controls, and repeated-turn measurements. The primary falsifier is
an assistant that **describes** all five principles accurately while its next
turn still dismisses the actual offer, changes the subject, or pressures a
withdrawn giver to repeat it.

No private relationship records, raw conversation, identity/consent state, or
model training data are included or authorized for publication by this file.
