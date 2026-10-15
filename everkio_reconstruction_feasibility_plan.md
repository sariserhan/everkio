# Everkio — Parallel Pet Reconstruction Feasibility Plan v2.1

Date: 2026-10-15. Governing document: [master specification v2.1](everkio_master_spec_v2.md).
Track: **Everkio Pets identity research**, independent of M0–M3 presence implementation.

## Purpose, authority and boundaries
Determine whether authorized pet media can produce a photorealistic, recognizable, animatable cat/dog within a defensible hard cost ceiling. Generic animal rendering is not evidence of personalized reconstruction feasibility. Living and memorial paths receive separate results and go/no-go decisions.

R0–R4 research is authorized subject to its budget and rights prerequisites. This documentation task runs no experiments, creates no cloud resources and spends no money. Research authorization does not include a production upload service, customer sales, M5 implementation, human reconstruction or voice cloning. Research may use isolated scripts, disposable artifacts and private mockups after prerequisites are satisfied; do not build production features under the research label.

## R0 — Freeze numerical budget and protocol
Before any billable call, the product/finance owner must approve and record actual currency amounts for:

| Required field | Initial value |
|---|---|
| Total study cap and funding source | UNSET — billable execution blocked |
| Living-path and memorial-path allocations | UNSET |
| Per-pet lifetime cap including one correction | UNSET |
| Per-attempt GPU/runtime/output/storage/egress maxima | UNSET |
| Maximum concurrency and daily vendor cap | UNSET |
| Assessment/preview allocation and retention/export/deletion reserve | UNSET |
| Contingency and provider pricing/version validity | UNSET |
| Proposed SKU/territory contribution floor for commercial evaluation | UNSET — commercial G-F blocked |

Total reservations plus settled costs and outstanding liabilities must never exceed funded study capacity. Allocate budget across two rounds and reporting/cleanup before starting, rather than spending everything on initial generations. No automatic top-ups or third generation attempt; each pet permits one initial attempt and at most one bounded correction. If the budget cannot fund the specified cohort, report a smaller study as PARTIAL; do not shrink the gate silently.

A minimal research server-side reservation mechanism must atomically reserve the complete worst-case bill before dispatch, persist idempotency keys and cost entries, enforce concurrency and vendor/runtime/byte limits, and settle/reconcile usage. Local spreadsheet estimates or client checks alone are insufficient. Fund research from the approved research pool, not presumed future sales. All billable assessment, preview, reconstruction, QC, storage and cleanup use this control. If a vendor cannot bound billing even after cancellation, do not use that route. Validate duplicate dispatch, concurrent requests, timeout/retry, delayed telemetry and budget-exhaustion rejection before billable execution using nonbillable fakes. This is research infrastructure only, not approval for production M6.

**R0 acceptance:** named owners, numerical caps and funding approved; enforceable vendor limits verified from current primary sources/terms; rights/retention protocol and test rubric frozen; reservation/fault tests pass. Initial status: NOT RUN, BLOCKED by missing budgets/vendors/cohort.

## R1 — Consent, intake and evaluation cohort
Use at least **20 distinct pets per path** intended for a passing G-I result: at least 10 cats and 10 dogs in each path. Recruit for variation in coat length/color, distinctive markings, body proportions and source-media quality; report coverage gaps. Do not claim breed-wide generalization from this sample. An earlier smaller exploratory cohort is useful but cannot pass G-I.

- **Living path:** obtain owner permission and source rights; guide multi-view photo/video capture, scale reference and a separate held-out capture for evaluation. Retakes allowed before intake lock, with burden and failures recorded.
- **Memorial path:** use voluntarily contributed existing archives and optional owner-described identity traits; no requirement for new capture. Record known/unknown regions and archive limitations. Consent includes study evaluation, access, withdrawal and deletion; participation may stop without pressure.
- Assess all screened cases before generation; log eligibility and exclusions with reasons. Freeze the eligible cohort before scored generation. Report screening rejection rate alongside eligible-cohort success rate. Failures, abstentions and budget stops after eligibility remain in the scored denominator.
- Separate pipeline input media from held-out reference views where available. For archives without independent views, explicitly report weak validation coverage; do not invent evidence. Insufficient evidence for an identity dimension blocks a full acceptance for that case.
- Encrypt private media, restrict access, use pseudonymous case IDs, record source provenance, and set approved retention/deletion dates before intake. No model-training reuse without separate opt-in.

**R1 evidence:** consent/rights register, cohort manifest, coverage matrix, input/holdout split, locked scoring protocol and missing-data register. Stop ingestion on rights uncertainty or privacy failure.

## R2 — Assessment and likeness preview experiment
Test the three contracts in master §6.1 using private research prototypes, without taking payments:
1. Free assessment reports suitability/unknowns and a prospective price; measure its own real cost.
2. Likeness preview shows provisional appearance, multiple available views, inferred regions and any motion limitations. Test understanding of an optional separate fixed preview fee and lack of final-purchase obligation.
3. Final reconstruction is evaluated as a distinct optimized rigged result, including full-motion review, one bounded correction and proposed failure/refund outcomes.

Record compute and human effort separately for each stage. Do not use a static preview to score final animation quality. Pre-register capture/preview acceptance prompts before owners see results. No funding requirement is waived because a future customer-facing stage is called “free.”

## R3 — Bounded reconstruction and identity tests
Run the selected candidate pipeline on the frozen cohort. Record model/version/seed, asset topology/rig/materials, runtime, storage/egress, worker termination behavior and cost reservations. Use identical full-motion review sequences: front/side/back inspection, idle, walk, turn, sit/lie and approach, plus held-out-view comparison. Evaluate on the baseline phone once available; until then motion/device evidence is PARTIAL and cannot establish full G-I.

**Case acceptance requires all of:**
- Owner rates “recognizably my pet” ≥4/5 after reference comparison.
- Owner rates face, body proportions and distinctive coat markings ≥4/5 each; no unresolved critical identity error such as missing/wrong distinctive markings.
- Two independent blinded reviewers rate photorealism and identity preservation during motion ≥4/5, with zero major rig/deformation/contact defects. Use a third reviewer for disagreement under the frozen rubric.
- Required views/evidence are available; output is rigged, optimized and demonstrably animatable on the target device, not merely a flattering still image.

G-I requires ≥90% accepted cases for **each path separately**, including failed jobs and post-eligibility abstentions in the denominator. Report each species separately as well; neither species may fall below 90% in a passing path. Report first-pass success, success after the one correction, failures and exact counts with a binomial 95% confidence interval. Small-sample results remain limited evidence, not a guaranteed customer success rate.

Compare independent reviewer scores with owner ratings; owner enthusiasm cannot waive a realism failure. Do not count repeated attempts as additional pets. Two bounded rounds mean initial generation plus the one included correction, not repeated cohort replacement. If a path still fails after these rounds or reaches its cap, stop it and report FAIL/PARTIAL with causes; no automatic additional spend.

## R4 — Finance, failure handling and memorial review
### G-F research evidence
Report stage-level and end-to-end costs, p50/p95/observed maximum, attempt counts, manual processing minutes and outstanding storage liabilities. Observed cost distributions do not establish a hard upper bound; demonstrate that separately from provider enforcement and reserved limits. Compute proposed worst-case contribution by SKU/territory after actual fees, taxes, correction, failed-job/refund risk, support, delivery, retention and required margin. Until prices, margin floor and liabilities are approved, commercial viability remains NOT RUN/PARTIAL even if the experiment stayed within budget.

Exercise rejected input, low-confidence preview, initial failure, failed correction, worker timeout, duplicate delivery, cancellation, unexpected bill, deletion and simulated refund paths. Show the ledger never authorizes beyond funded limits and the proposed customer outcome does not require a surprise payment. Unexpected over-cap billing immediately disables the route and fails its financial gate. Research tests inform production design; production M6 must later repeat commerce/entitlement/refund tests before launch.

### G-M memorial quality
With ≥10 consenting adult evaluators, test private prototype screens and eligible memorial results. Permit skipping and withdrawal. At least 90% must correctly explain generated versus original content, identify inferred/unknown appearance, understand preview/final-charge separation, and independently complete each pause/archive/export/delete prototype task. Report each measure separately. Two reviewers classify defects; unresolved critical issues block the gate. Critical means deceptive identity/consciousness claims, fabricated history presented as fact, coercive engagement, source exposure, inability to withdraw, or a flow likely to cause material avoidable distress. Pause affected testing upon a critical issue and review before resuming.

Prototype task completion supports UX feasibility only. G-M launch approval additionally requires memorial-path G-I and verified production access controls, export and deletion. Sensitive evaluation is not a clinical wellbeing claim.

## Research decision packet
Deliver protocol revision, consented cohort/coverage summary, protected evidence locations, case-level input/output/holdout comparisons, full-motion/device clips, raw cost ledger, enforcement/fault evidence, first/corrected acceptance rates with uncertainty, memorial findings, limitations and blockers. Record G-I living, G-I memorial, G-F and G-M separately as PASS/PARTIAL/FAIL/NOT RUN with named decision owner.

All research stages and gates start **NOT RUN**. Budgets, cohort rights, provider enforcement, device evidence and prototype study results remain absent. Findings may support a proposal for M5; they never authorize M4–M14, sales or launch. If identity is infeasible, continue only the independently authorized generic presence work and bring the product decision back explicitly; do not silently redefine personalized reconstruction.
