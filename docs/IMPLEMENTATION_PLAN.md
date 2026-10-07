# Implementation Plan

How the retention strategy moves from recommendation to execution: who owns each initiative, when it ships, how
success is judged, and what could go wrong. Phases follow the roadmap in the main README.

## Owners

| Workstream | Accountable owner | Supporting teams |
|---|---|---|
| Re-order widget and contextual nudges | Product manager, Growth | Engineering, Data science, Design |
| Proactive delay credits and one-tap issue resolution | Product manager, Customer experience | Operations, Finance, Engineering |
| Personalization engine v1 | Product manager, Discovery | Data science, Engineering |
| Swiggy One Lite (targeted loyalty tier) | Product manager, Membership | Finance, Marketing |
| Measurement and experiments | Analytics lead | Product, Finance |
| Budget and unit-economics guardrails | Finance business partner | Analytics |

## Timeline and go/no-go gates

| Phase | Months | Ships | Gate to proceed |
|---|---|---|---|
| **1. Fix trust, start the habit** | 1–2 | Re-order widget (A/B test), delay auto-credits, one-tap missing-item flow | Widget lifts 30-day re-order rate by ≥2 pts at 95% confidence with no guardrail breach; credit cost per order stays inside the agreed budget |
| **2. Build switching costs** | 3–4 | Personalization v1, Swiggy One Lite trial for users before their 3rd order, weekly streaks | Loyalty tier on track for the churn reduction the unit-economics model requires; personalization lifts orders per user without cutting AOV |
| **3. Scale what worked** | 5–6 | Roll out winning variants; streak and referral expansion; Food Wrapped | Each scaled feature beats control on orders per user per month; cumulative discount spend per order flat or down |

A feature that misses its gate is paused or redesigned. It is not rolled out because it was on the roadmap.

## Why the loyalty tier is targeted, not universal

The unit-economics model (`model/unit_economics.xlsx`) shows that at Swiggy's reported Q1 FY2027 food-delivery
margin, an average active user generates about ₹51 of Adjusted EBITDA a month. A ₹25 per member per month
benefit given to every user needs monthly churn to fall from an assumed 10% to about 4.6% just to break even.
The habit-ladder analysis shows return rates rise sharply between a customer's first and third orders. So the tier
is offered **only to users who have not yet reached their third order**, where each retained customer is worth
the most and the benefit is paid to the fewest people.

## Review cadence

| Forum | Frequency | Looks at |
|---|---|---|
| Growth stand-up | Weekly | Experiment health, sample accrual, guardrail alerts |
| Retention review | Fortnightly | D30 retention by cohort and segment, orders per user, feature adoption |
| Business review | Monthly | Unit economics: discount spend per order, credit cost, LTV/CAC trend vs model |

## Risks and mitigations

| Risk | Likelihood | Mitigation |
|---|---|---|
| Delay credits are gamed or become expected | Medium | Cap credits per user per month; credit only on platform-attributable delays; monitor repeat claimants |
| Loyalty tier cannibalises orders that would have happened anyway | High | Holdout group that never sees the tier; measure incremental orders, not member orders |
| Novelty effect inflates early experiment results | Medium | Run tests for at least the full 30-day observation window; compare weeks 1–2 with weeks 3–4 |
| Personalization narrows choice and hurts restaurant partners | Medium | Guardrail on restaurant GMV distribution; keep an Explore mode |
| Retention gains bought with margin | Medium | Finance owns a discount-spend-per-order guardrail; any test breaching it stops |
