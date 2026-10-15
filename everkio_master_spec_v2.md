# Everkio — Master Product and Technical Specification v2.1
**Revision:** 2.1 · **Date:** 2026-10-15 · **Supersedes:** v2.0. The filename is retained for existing links.
**Product:** Everkio · **Tagline:** Feel their presence.
**Roadmap:** Everkio Pets → Everkio Spatial → Everkio People.
**Status:** Decision-controlled master specification; no engineering, research, financial, or launch gate has been demonstrated by this revision. Domain availability and trademark clearance remain pending.

## Revision control and authority
- **Confirmed scope:** generic cat and dog presence testing first; separate pet-identity reconstruction feasibility research may proceed in parallel under a documented fixed research budget. Generic rendering results never establish personalized reconstruction feasibility.
- **Active implementation:** M0–M3 only. Passing an intermediate M0–M2 gate permits the next milestone within this authorized scope; record the decision without requiring renewed scope approval.
- **Authorized research:** R0–R4 in the [parallel reconstruction experiment plan](everkio_reconstruction_feasibility_plan.md). Research authorization does not authorize M5 production implementation, commerce, customer uploads, or a public pilot.
- **Deferred implementation:** M4–M14 require explicit product-owner approval identifying scope, prerequisites and budget. Passing tests does not grant this approval automatically.
- **Current task:** documentation only; no application features, paid services, cloud resources, asset purchases, or experiments are executed by this revision.
- **Control hierarchy:** confirmed decisions and authority in this section govern the document; phase descriptions define eventual ownership, not permission. If requirements conflict, record a blocker and resolve it through the decision log before implementation.
- **Change control:** record proposed changes, rationale, evidence, owner decision and affected gates in the [decision log](everkio_decision_log_v2_1.md). Realism, low latency, AR presence and strict spending limits cannot be silently relaxed. A failing gate remains failed or unrun until evidence meets its approved criteria.
- **Companion deliverables:** [M0–M3 execution plan](everkio_m0_m3_execution_plan.md), [reconstruction experiment plan](everkio_reconstruction_feasibility_plan.md). Section 22 defines shared acceptance and evidence rules.

## 0. Executive decisions
- **Problem:** Generic virtual pets lack fidelity to real animals, convincing presence, persistent behavior, and memory preservation.
- **Solution:** Mobile AR cats and dogs rendered as realistic interactive creatures, with optional paid reconstruction of a user's actual pet from media. Later: shared experiences, headsets, desktop, and separately governed human memorials.
- **Customers:** Pet enthusiasts and owners, including families remembering pets; later, separately consented human-memory customers.
- **Absolute product principles:** photorealism; low latency; efficient local rendering; transparency about generated likeness; enforceable server-side budgets; no unlimited metered services; respectful memorial experience.
- **Platforms:** iOS AR initial benchmark, Android supported via adapter after parity, visionOS/Meta Quest after headset validation, desktop subsequently, Meta display glasses only where SDK can support a suitable limited experience.
- **Feature scope:** M0–M3 generic presence implementation and separate bounded reconstruction research are authorized. P1 commercial implementation and launch are deferred. A generic-only public release is not approved by this document.

## 1. Scope and phased deliverables

### P0 — Everkio Pets presence feasibility (initial estimate 4–8 weeks; conditional)
- One licensed/owned photorealistic adult cat and one dog, realistic fur/eyes/proportions, believable animation at multiple viewing angles.
- Real-time AR floor placement and anchoring, camera motion, scale, lighting approximation, contact shadows, baseline occlusion where device supports it.
- Walk, turn, sit, lie, eat, idle, react to tap/stroke, approach. Rigged animation + IK and a minimal scripted test controller; no per-frame generative calls. The production behavior planner belongs to M4 and is not authorized here.
- Instrument FPS frame times, memory, thermal conditions, battery drain, touch response, tracking drift, clipping and cost.
- Evaluate **A:** high-quality rigged mesh/PBR fur, **B:** hybrid rig + neural/Gaussian appearance. Select after device tests; Gaussian-only is not presumed viable for locomotion.
- P0 implementation exclusion: users/accounts, payments, customer-upload reconstruction, production behavior/memory, conversation, social systems. Separate consented research assets may be evaluated only through the bounded parallel research track.
- **P0 gate:** >=30 sustained FPS on documented test iPhone for 10 minutes, 60 target on flagship; touch feedback p95 <100 ms; no chargeable cloud inference while interacting; strong qualitative realism backed by blinded testing; no major visible foot sliding on curated movement battery. Thresholds are targets, not measured claims.

### P1 — Everkio Pets core experience and conditional commercial launch (deferred; estimate additional 8–16 weeks, uncertain)
- Generic free local pet; uploaded photo/video-based recreation for cats and dogs; guided capture with quality check and honest missing-data warnings.
- Separate free assessment, likeness preview, and final paid reconstruction as defined in §6. Assessment is not a generated likeness. A preview may carry a separately disclosed fixed fee; it cannot silently authorize a final job or imply final quality.
- Paid generation workflow with one included corrected result, capped compute allowance, and defined failed-job/refund treatment. Owner review of landmarks, body size, fur markings and likeness; fallback when fidelity insufficient.
- On-device AR placement, petting, feeding, play, fixed local voice commands where supported, and session-local autonomous routines; offline saved pet assets and animations. Persistent learned commands, preferences, editable personality and routines across sessions belong exclusively to P1.5.
- AR screenshots/short clips rendered locally, privacy controls and clear synthetic-media identification options.
- Private remembrance experience; no death/health countdowns or manipulative engagement tactics; never imply the digital recreation is the same consciousness.
- App Store/Google billing compliant for digital goods with platform-dependent regional rules; verified server entitlements; real-time cost ledger.
- **P1 gate:** G-P, path-specific G-I and G-F passed, plus G-M for memorial launch (§22); 30FPS sustained; purchase/cost caps verified; zero unauthorized budget overspend in test suite; privacy and deletion audits; real pilot paid conversions/refunds.

### P1.5 — Everkio Pets persistent behavior and environmental awareness (deferred)
- Save behaviors, favorites, training progress, personality settings and learned commands; transparent reset controls.
- Spatial room map optionally stored on-device; pet discovers suitable real-world planes/obstacles but does not assume furniture detection or whole-home persistent mapping is universally available.
- Accessories, bowls, toys, sleeping spots, routines. Offline deterministic pet controller.
- **Gate:** repeat engagement and perceptible learning without unnecessary cloud spend.

### P2 — Everkio Pets multi-pet/family and Everkio Spatial prototypes (deferred)
- Two or more pets react to each other without animation collisions; family invites with roles and entitlements; per-account shared spend pool.
- Pet-to-pet visits and synchronized shared spatial sessions only with explicit consent and privacy controls.
- visionOS immersive prototype and Meta Quest MR prototype with independent performance/occlusion/UX gates; do not assume Unity feature parity.
- **Gate:** stable synchronized scenes, appropriate spatial anchoring and headset device thermals.

### P3 — Everkio Spatial cross-device ecosystem and optional Pets growth (deferred)
- macOS/Windows desktop companion as lightweight non-AR viewport.
- Optional puppy/kitten growth for original digital pets, aging off by default for recreated or memorial animals.
- Experimental Meta AI glasses voice/status integrations as SDK permits, not a promise of spatially anchored life-sized 3D pets.

### P4 — Everkio People (future only; separate governance approval and budget)
- Authorized photo/video reconstruction of an individual, recognizable gestures and environment placement.
- Playback of original recordings initially; optional synthesized/cloned speech only with verified explicit consent/rightful authorization and safeguards against impersonation or deceptive outward-facing communications.
- Generated conversations explicitly labeled simulation, grounded in volunteered recorded life stories, not asserted to be the person's actual beliefs or consciousness.
- Special governance for deceased individuals, minors, family conflicts, access, deletion and consent provenance; no cloning of third parties without valid rights.
- Never allow public dissemination of convincing impersonation without persistent disclosures; human work is not P0/P1 scope.

## 2. Quality and performance SLOs (initial engineering targets)
| Quality | Desired launch requirement and measurement |
|---|---|
| Visual | Owner-recognizable breed/body/coat/unique markings, tested blind with full-motion clips; no cartoon or illustration fallback presented as photorealistic. |
| Rendering | Sustained >=30 FPS p95 frame timing on published support matrix; aspirational 60 FPS; profile for >10 min thermal load. |
| Direct touch feedback | p95 <100 ms on supported hardware; immediate local visual response. |
| Command reaction | p95 <500 ms from completed recognized command to animation onset for **local** command set; do not promise this for cloud STT or conversational responses. |
| AR | Correct scale, surface anchoring, drift/clipping analysis, shadows and occlusion where supported. |
| Audio | Local animal SFX offline; local command recognition where device permits. |
| Reconstruction | Owner-rated likeness with confidence labels; failures and retakes honestly surfaced. |
| Offline | Previously downloaded assets, care/play and fixed commands in P1; persistent training memory in P1.5; no cloud inference to render each frame. |
| Privacy | Explicit consent before room camera, microphone, upload, sharing, or recording. |

## 3. Architecture and data flow
### Client
- Unity engine, AR Foundation with separate ARKit (iOS) and ARCore (Android) provider packages, build/version pinning after P0.
- Components: `ICompanionRenderer`, `IAnimalRig`, `IInteractionController`, `IWorldUnderstanding`, `IBehaviorBrain`, `ISpeechCommandAdapter`, `IAssetCache`, `IMediaCapture`, `ICostAwareRemoteJobs`, `IEntitlementClient`.
- A fast rigged quadruped mesh is baseline. Neural/Gaussian enhancement is optional only if dynamic motion, lighting, compression and phone thermals meet acceptance.
- Behavior will use a deterministic local state machine/utility planner with controlled randomness: scripted test behavior in M0–M3, session-local behavior in P1/M4, persistent temperament and pet memories in P1.5/M9. Remote LLM is NOT used for minute-by-minute behavior.
- Native AR adapters isolate device limitations; capture and encoding preferably on device.

### Backend
- Better Auth where supported in app's native authentication flow (validate Unity/mobile token lifecycle before committing to a particular integration), Convex for user/pet metadata, entitlements and mutable state, object storage such as S3/R2 for private encrypted photo/video/model files.
- Separate GPU worker queue for photogrammetry/reconstruction, texture processing, rigging, validation and transcoding. Jobs immutable, idempotent, versioned, resumable only under authorized cost caps.
- Server-signed manifests for asset bundles and client-visible entitlement snapshots. Raw uploaded photos private, never used for model training absent independent explicit opt-in.
- Observability: job cost, GPU seconds, token/audio usage, egress/storage, model quality, crash diagnostics, render FPS, battery/thermal, refunds and purchase validation.

### Primary objects (conceptual)
`User`, `Household`, `Pet`, `PetAppearance`, `PetAssetVersion`, `SourceMedia`, `PetBehaviorProfile`, `TrainingEvent`, `RoomAnchor` (on-device by default), `GenerationJob`, `JobAttempt`, `Entitlement`, `Payment`, `Refund`, `CostReservation`, `CostLedgerEntry`, `Allowance`, `ShareGrant`, `ConsentRecord`, `DeletionRequest`.

## 4. Cost safety: strict no-open-ended-usage design
**Funding distinction:** Customer services use the net-funded purchase pool below. Authorized research and free assessments use separately approved, already-funded fixed research/marketing pools with the same server-side reservation and hard limits. Future sales are not funding.

**Requirement:** No usage-metered request may be authorized without sufficient **collected/guaranteed funded margin**, including applicable commission, refundable transaction reserves, tax treatment, provider overage allowance, attributable infra/storage/egress, support/refund risk, and a specified contribution margin. Budget planning alone cannot mathematically guarantee company-wide positive profit under fraud, chargebacks, fixed overhead or infrastructure outages; these are separately buffered and monitored.

### Net-funded spending pool
1. Derive per-purchase conservative available contribution from **actual settled price excluding tax collected for remittance**, minus region/platform commission, payment processing, expected reversals and allocated overhead.
2. Reserve a target profit contribution and worst-case variability buffer; only the residual becomes the **usage pool**.
3. Subscription plans receive a fixed monthly usage allocation; no unlimited GPU/LLM/audio. One-time generation entitlement has job lifetime budget. Family members use one shared pool; multi-device sessions synchronize atomically.
4. Free local features consume no discretionary cloud inference; free cloud operations require separately approved fixed marketing budget and strict abuse quota.
5. Fixed/recurrent storage and delivery must be funded from reserved fees or covered by clearly disclosed retention tiers/limits. Permanent **offline** access can be preserved after purchase even if cloud services stop, by allowing export/download.

### Request authorization protocol
- Preflight: authenticate, ownership and entitlement, compute *upper bound* cost of requested job using versioned vendor pricing and pessimistic maxima (tokens, GPU wall time, retry count, egress, persistent storage).
- Atomically reserve upper-bound cost in transaction with idempotency key and account-level concurrency ceiling. Reject if `available < upper_bound + safety_buffer`.
- Execute only with hard provider-side max tokens/seconds/bytes and worker deadline/kill switch. Streaming services continually debit budget in chunks and stop *before* exhausting allocation; if upstream cannot enforce a bounded maximum, service cannot launch.
- Settle measured cost into append-only ledger, release unused reservation, reconcile provider bills daily. If reconciliation exceeds upper bound, quarantine route, stop further usage, and investigate; do not silently pass overage to user.
- Monthly per-account caps and global daily vendor caps; admin kill switches by feature/vendor/region. Display remaining allowance; paid top-ups only with prior explicit user authorization.
- Refunded/chargeback purchases revoke future hosted usage, but avoid punishing users for platform failure; maintain business reversal reserves.
- Deny generation if the expected total reconstruction cost exceeds the margin cap, even if the user has many retries queued.

### Accounting and SLO tests
- Track actual net revenue, taxes passed through, app-store fees, provider gross bill, GPU seconds, storage byte-months, egress, moderation and support allocations, refunds/chargebacks.
- Automated tests: duplicate checkout callbacks, simultaneous GPU jobs, race across devices, worker retry storms, provider timeout, oversized input, malicious uploads, customer refund while job in progress, changed provider pricing, expensive model fallback, vendor billing lag, region-dependent taxes/fees, expiring subscription.
- **Release blocker:** no unbounded billable operation; all backend work has a preauthorization and fixed maximum exposure, including cleanup/retention.

## 5. Tentative pricing experiment (not final)
| Offering | Starting test price | Cost treatment |
|---|---:|---|
| Generic on-device pet | Free | No uncapped cloud AI |
| One custom animal recreation | $14.99 | One bounded generation entitlement, disclosed corrections |
| Additional reconstruction | $9.99 | Separately costed; do not release if margin fails |
| Advanced cloud intelligence/family features | $4.99/month | Fixed metered allowance with hard stop |
| Optional accessories | $1.99–$4.99 | Mostly cached on-device assets |
| Future human likeness | $49–$99 | Separate higher compute/consent budget |
| Future human voice reconstruction | $19–$39 extra | Consent verification and per-generation budget |
| Future speech conversations | $9.99–$19.99/month | Token/audio time allowance + hard stop |

Do not show customers a guaranteed low price for reconstruction until an actual reproducible per-job cost distribution is measured, including retries, approvals, store commissions, refunds and sales tax handling. Prices are hypotheses.

## 6. Product flows
1. **Adopt:** open app → choose cat/dog → privacy/camera permissions contextually → surface scan → place pet → local care/play; optional account later.
2. **Recreate:** select living-pet or memorial-pet intake → rights and privacy confirmation → free assessment → separately accepted likeness-preview terms → preview review → independent final-purchase confirmation → hard-budget final job → moving-device likeness review → acceptance/correction/refund path → local asset download.

3. **Remember:** opt into remembrance mode → private archive of media/habits → accurately mark simulated/generated behavior → downloadable keepsake; no intrusive daily reminders.
4. **Family (P2):** invite role-based member → consent for shared archive → household budget pool → audit access/share/revoke.
5. **Remote pet visit (P2):** invite, mutual acceptance, transmit only necessary animation state and permitted likeness metadata; room scans never shared by default.
6. **Future human (P4):** separate informed consent verification, rights and identity validation, clear generated-media disclosure, original-recording priority, optional authorization-checked clone, sensitive grief UX testing.

### 6.1 Assessment, preview and paid reconstruction contracts
| Stage | Customer receives | Payment and compute boundary | What it proves |
|---|---|---|---|
| Free assessment | Input coverage/quality report, missing views, supported path, uncertainty, eligibility and next-step price estimate | No customer charge; prefer local checks. Any billable assessment service requires server reservation against a fixed approved research/marketing pool, quotas and hard stop | Only input suitability; no promised likeness or completed model |
| Likeness preview | Clearly labeled provisional likeness with reference comparison, available angles, known inferred/unknown regions and motion limitations | Separate fixed terms before compute. Free only if fully funded by a capped pool; otherwise explicit fixed preview fee. Preview fee, credit toward final price and failed-preview/refund terms disclosed in advance | Preliminary visual evidence only; a static view does not establish animation or final identity fidelity |
| Final paid reconstruction | Optimized, rigged, downloadable pet, demonstrated in motion on supported hardware; one included bounded correction | Separate purchase authorization, entitlement and server-reserved worst-case budget covering initial job, included correction and failure path; no automatic retry charges | Eligible for acceptance only after identity, motion, device, cost and relevant memorial gates pass |

A preview rejection creates no final-purchase obligation. A failed preview follows its disclosed refund policy. A final result failing promised acceptance after the included correction enters the refund path; no forced paid retry. A correction cannot exceed the reserved total: stop and offer the disclosed failure/refund outcome when its remaining budget is insufficient. Final terms and refund handling require validation before commerce implementation or launch.

### 6.2 Separate reconstruction paths
- **Living pet:** guided new capture with multiple angles, lighting and size reference; request retakes where coverage is inadequate. Acceptance checks owner-confirmed body proportions, coat landmarks, face and full-motion identity against independent held-out reference views.
- **Memorial pet:** optional existing archive only; never require a new capture or assume missing views can be supplied. Identify source-supported versus inferred features, preserve original media separately, and permit abstention when identity cannot be supported. Acceptance additionally requires sensitive UX evaluation, comprehension of uncertainty/simulation, private defaults, no unsolicited reminders and usable pause/archive/export/deletion controls.
- A memorial result must meet the same photorealism and identity bar. Sparse inputs do not authorize a cartoon substitute, invented factual memories, or an unlabeled approximation. An optional explicitly labeled partial preview is not a passing final reconstruction.
- Record acceptance, rejection, abstention, missing-data and correction rates separately by path; strong living-pet results cannot approve memorial launch.


## 7. Security, privacy, and trust
- Secure ownership checks per pet/media/job; private default; encrypted transport and storage; retention schedule, export, deletion and deletion verification.
- On-device room mapping and raw camera/mic streams by default. Do not upload ambient room audio/video unless user explicitly initiates capture/upload.
- Allow minors only after legal/platform policy review. No behavioral nudges that exploit grief or make memorials seem alive/conscious.
- Animal clone accuracy is probabilistic. Never claim exact personality recovery from sparse media.
- Before P4, consult legal/privacy review on human likeness rights, publicity, voice, deceased-person rights, impersonation, and multi-jurisdiction compliance.

## 8. Workstreams and ordered milestones for engineering agent
- **M0: Feasibility matrix and repo.** Record target hardware, budgets, Unity licensing, benchmark scripts, metrics dashboard; document dependencies and risks.
- **M1: Animal rig and asset licensing.** Obtain legitimate cat/dog assets, locomotion clip library, fur shader, and verified redistribution rights.
- **M2: Mobile AR and animation.** Plane placement, spatial scaling, environment approximations, shadowing, locomotion, gesture input.
- **M3: Performance and realism comparison.** Run mesh/PBR baseline vs neural/hybrid sample only if feasible; benchmark sustained thermals/visuals on real devices.
- **M4: P1 behavior engine (deferred).** Session-local state, petting/feeding, fixed commands, unit tests and offline support. Persistent training/personality/memory remain M9/P1.5.
- **Parallel R0–R4: Identity feasibility research (authorized, budget-gated).** Controlled consented living-pet and memorial datasets, coat/identity fidelity, rigging and motion, and bounded cost experiments; see the experiment plan. Independent from presence approval; no production service or paid customers.
- **M5: Production reconstruction pipeline (deferred).** After research gates and explicit approval, implement validated intake, preview, job, correction and failure workflows; repeat identity/cost validation on production outputs.
- **M6: Payment + hard-budget backend.** Atomic cost reservations, vendor kill switches, ledger, entitlements; chaos/abuse tests.
- **M7: MVP onboarding, media management, private memorial, capture.** Real user tests and policy audit.
- **M8: Commercial pilot.** Controlled number of purchasers, observe fidelity ratings, costs/retries, refunds, 14-day retention and crash stats.
- **M4–M14:** all implementation outside M0–M3 requires explicit approval and prerequisite evidence, including M5 despite parallel research authorization.

## 9. Explicit stop/kill criteria
- Stop photorealistic custom-reconstruction scope if owner likeness or moving deformation repeatedly fails blind tests.
- Stop device rollout if sustained performance/thermal characteristics fail published support targets.
- Stop any vendor operation if the upper-bound cost cannot be guaranteed or atomically reserved.
- Do not offer a plan/price with negative worst-case modeled contribution after buffers.
- No social/marketing or human-clone launch without consent and safety review.
- Avoid expanding into headsets merely because client code compiles; do separate hands-on device acceptance.

## 10. Future device compatibility strategy
- Share domain model and behavior core, not necessarily one renderer/shader across every device.
- **visionOS:** Unity's PolySpatial immersive mixed reality requires appropriate paid Unity licensing and visionOS packages; evaluate device thermal performance separately.
- **Meta Quest:** separate Unity OpenXR/Meta MR device path, occlusion/passthrough and controller/hand interactions.
- **Meta display glasses:** use approved SDK affordances for voice/status/glanceable UI only, unless future capabilities materially change.
- **Desktop:** non-AR camera/viewport adapter, GPU settings/low-power mode.

## 11. Decisions locked / deferred
**Locked:** animals first; photorealism; mobile real-time AR; local interaction; bounded cost ledger; paid pet reconstruction; privacy-first memorial mode; explicit future human voice opt-in; separate wearable phases.

**Deferred until evidence:** exact Unity version and licensing, asset/model vendor choice, feasible image-to-3D algorithm and guaranteed fidelity, device support matrix, pricing/allowances, voice-to-animation model, export formats, commercial conversion thresholds, headset-specific release dates.

## 12. Immediate agent directive
Implement only M0–M3 within the authorized engineering track. Produce executable benchmark and captured real-device evidence; do not describe presence as passed from editor previews. Run separate R0–R4 reconstruction research only after R0 establishes documented numerical budget ceilings, rights, cohort and server-enforced reservations for all billable operations. Research may run alongside M0–M3 and cannot claim identity success from generic assets. Report assumptions, measured metrics, risks, dependencies and stop conditions at each gate. Do not implement M4–M14 without explicit approval. This documentation task executes neither track.

## Reference sources retained from v2.0 (not reverified in v2.1)
- Unity AR Foundation supports ARKit/ARCore provider paths: https://docs.unity.cn/Packages/com.unity.xr.arfoundation%406.1/manual/index.html
- Unity visionOS/PolySpatial guidance: https://docs.unity.com/en-us/engine/6000.6/manual/platform-specific/vision-os
- Unity PolySpatial licensing/package info: https://docs.unity.com/en-us/engine/6000.3/manual/packages-list/packages-all/pack-safe/com-unity-polyspatial-visionos


---

# PART II — FULL PRODUCT LIFECYCLE SPECIFICATION (BEYOND INITIAL RELEASE)

## 13. Full feature coverage and dependency map
This document separates **product completeness** from **engineering authorization**. M0–M3 implementation and budget-gated R0–R4 research are the only authorized tracks. All M4–M14 implementation needs explicit approval. Any unmeasured target is a requirement or identified proposed threshold, not evidence of achieved quality. Future platform/API/licensing statements require verification at the relevant gate.

| Feature | Earliest phase | Main prerequisite | Acceptance evidence |
|---|---|---|---|
| Photorealistic cat and dog | P0 | Licensed assets, performant animation | Side-by-side blind evaluation, FPS/thermals |
| Realistic room-scale AR | P0 | ARKit/ARCore, anchor persistence evaluation | Room walking test and drift recordings |
| Scripted presence behavior / production autonomy | P0 / P1 | Scripted test controller / deferred local behavior planner | Presence clips / offline 15-minute unattended scenario |
| Recreate real pet | P1 | Reconstruction research, identity test | Owner recognition + cost-limited successful jobs |
| Fixed voice commands | P1 | Local command recognition where supported | Recognition confusion matrices + offline demos |
| Learned commands and persistent training | P1.5 | Versioned local training state | Restart, reset and sync consistency tests |
| AR screenshots and video | P1 | Client-side render capture, watermark choice | Export quality, privacy and battery tests |
| Pet memorial experience | P1 | Permissions, keepsake/export, non-manipulative copy | Memorial UX review and deletion/export tests |
| Long-term memory and personality | P1.5 | Versioned state model + offline sync | Recall and consistency tests after reinstall/sync |
| Room awareness | P1.5 | Scene geometry and device capabilities | Edge/collision/occlusion device matrix |
| Accessories and custom toys | P1.5 | Asset compatibility and purchase entitlement | Animation/collision, licensing, offline access |
| Multiple pets interacting | P2 | Multi-agent arbitration | Two-pet stress, collision and interaction battery |
| Family access | P2 | Role-based access and shared budgets | Permission/revoke/charge race tests |
| Pet-to-pet visits | P2 | Invitation and synchronized state | Consent, latency, cross-network test |
| Apple Vision Pro | P2 | visionOS license + spatial adapter | Real headset comfort, performance and occlusion |
| Meta Quest | P2 | Quest MR adapter + actual hardware | Passthrough/motion/thermal test |
| Growth and aging | P3 | Age-dependent rigs and texture transitions | Visual continuity, opt-in/memorial lock |
| Desktop companion | P3 | Low-power renderer, input adapter | Idle efficiency, GPU fallback, accessibility |
| Meta glasses companion | P3 experimental | Current approved wearables SDK | Supported interaction only, no false AR promise |
| Human visual recreation | P4 | Separate consent governance, human avatars | Verified consent, visual quality + harm review |
| Authorized human voice cloning | P4 optional | Explicit voice-specific authorization | Voice provenance, misuse controls, revocation |

## 14. Experience contracts and state machines
### 14.1 Pet identity
The eventual production identity model (not required for M0–M3) gives each pet a durable `PetId`, `species`, `origin` (`generic`, `reconstruction`, `memorial`), `appearanceVersion`, owner-approved `IdentityProfile`, `behaviorProfileVersion`, and `rightsProvenance`. The *original media* and *derived likeness* are logically distinct assets with separate retention/deletion policies. A pet is never presented as an authentic recording when its actions are synthetic.

### 14.2 Live pet loop
`Sleeping ↔ Idle ↔ Exploring ↔ Socializing ↔ Playing ↔ Eating ↔ Training ↔ Settling`; interruptible, animated transitions; physiological need values are *gameplay state*, not simulated real medical diagnoses. Prioritize safety: no pet can pass through mapped hazards or clip into camera; when tracking fails, gently freeze/despawn/re-anchor rather than wander unpredictably. No punitive hunger, suffering or grief mechanics.

### 14.3 Input routing
Inputs include touch, local speech, virtual item toss, hand tracking where supported, controller, gaze, desktop mouse/keyboard. Route all to normalized commands (`Approach`, `Sit`, `Stay`, `Follow`, `PlayWith`, `Pet`, `Feed`, `Recall`, `CancelAction`) through authorization + behavior arbitration. Local confirmation starts within the latency target even when long animation follows. The pet may decline a command due to personality, but **the UI must not appear frozen**.

### 14.4 Reconstruction workflow
Path selection → rights attestation before upload → free assessment → separately authorized likeness preview → owner preview review → separate final payment/entitlement confirmation → cost reservation → bounded reconstruction → automated consistency QC → optimized game-ready rig/mesh/texture → mobile device review → owner acceptance/correction/refund path → signed asset delivery. Every billable assessment or preview also requires its own prior reservation under §6.1. Old photos may support partial resemblance only; video and multiple viewpoints raise confidence. Record sources and generation versions. A single pretty but non-animatable 3D mesh is **not** a successful reconstruction.

### 14.5 Memorial mode
A separate opt-in journey offering original photos/videos/audio, digital companion, private stories, optional remembrance space, and export. Default aging OFF, notifications OFF, generated memories OFF. Never synthesize claims about past events without source grounding. Provide pause, hide, archive, and delete controls. Do not imply actual return to life.

## 15. Phase P1.5 — Persistent intelligence and spatial awareness: expanded specification
**Deliverables:** versioned personality profile with explicit user-editable traits; trainable localized command set; lightweight reinforcement of preferences; local memories with optional encrypted sync; saved favorite toys and resting places; scene-awareness quality fallback; accessories.

**Memory model:** Separate source-confirmed facts (`owner_supplied`), observed in-app gameplay (`observed`), and generated behavior (`simulated`). Do not merge or hallucinate factual memories. Support memory reset, deletion and user correction, deterministic replay in test environment.

**Spatial strategy:** No assumption of perfectly scanned rooms. Use discovered horizontal surfaces and available depth/meshing, approximate floor bounds and conservative obstacle avoidance. On unsupported devices use a bounded play area. Do not upload full room maps without opt-in.

**Exit tests:** Offline behavior after app restart; bounded power use; reproducible command learning; no room geometry leaks; at least one documented fallback per unsupported spatial feature; no LLM call required for idle autonomy.

## 16. Phase P2 — Multi-pet and social spatial platform: expanded specification
**Multi-pet simulation:** Independent temperaments; common locomotion/contact solver; mutual avoidance; priority arbitration for shared toys and feeding spots; hard cap on active high-quality avatars based on GPU frame-time budget; automatic LOD and pause/fallback logic.

**Family roles:** Owner, editor, viewer, child-restricted (if later approved); granular grants for source-media access vs companion play; revoke with audit log and token expiry; account-owned entitlements with atomic shared allowance. Never duplicate the funded usage pool for each household member.

**Visiting modes:** (A) send a signed companion invitation and limited behavior snapshot; (B) shared live session with server-authoritative session membership and privacy toggles. Do not broadcast raw room meshes, exact home location or camera stream. Rate-limit invitations and provide block/report controls.

**Headset adapters:** Vision Pro targets hand/eye interaction and correct passthrough occlusion; Quest targets passthrough, hand/controller input and room setup. Share behavior data and identity assets only where render paths support them. Device-specific LOD/material conversion is expected. New hardware support needs independent licensing, compatibility, thermal, comfort and battery gates.

**Exit tests:** Two pets maintain frame-time threshold; concurrent shared-budget tests; invite/revoke adversarial tests; measured sync latency/jitter and loss recovery; successful real-device acceptance for each headset before listing as supported.

## 17. Phase P3 — Desktop, growth and smart wearables: expanded specification
**Desktop:** User chooses always-on-top or normal window; fixed GPU/CPU caps; idle animation frame-rate reduction; safe pause/snooze; no secretly active microphones/cameras; offline pet baseline and graceful sleep when device is stressed.

**Growth:** Separate baseline digital animal from memorial/recreated animal. For generic pets, puppy/kitten → juvenile → adult requires morph-target or stage-specific rigs, continuity of distinctive coat patterns, and opt-out. For memorials and real-pet recreations, default appearance remains locked unless explicit owner choice.

**Accessories:** Maintain compatibilities for species/size/age, clipping rules, content licensing and transparent purchases. Item purchases do not unlock unlimited cloud behavior.

**Meta wearables:** A capability-detection adapter (voice prompts, pet status, short media events and/or glanceable UI where approved). Treat life-sized spatially anchored holograms as **out of scope** for conventional smart glasses unless verified hardware SDK features change. No feature promise based on branding alone.

**Exit tests:** Desktop app stays within published idle resource caps; consistent entitlements; growth identity continuity evaluation; headset/glasses permissions and supported capabilities independently tested.

## 18. Phase P4 — Human likeness and memories: separate program charter
P4 is a **separate product decision** requiring user research, counsel, approved consent workflows, provider terms and abuse testing. Pet entitlements do not automatically grant any human recreation rights.

**Initial allowed experience:** Voluntarily captured or demonstrably authorized adult likeness; private family library; reconstruct recognizable face, hair, clothing and sitting/standing gestures; original source clips and recorded voice playback prioritized. Deceased-person recreations require documented legal rights, review of known wishes, and jurisdiction-specific controls. Clear identity disclosure at every generated interaction.

**Optional voice clone:** Separate, specific, revocable consent/authorization with provenance, validation and retention policy; must be opt-in and metered separately. Reject unsupported third-party cloning requests. Voice synthesis is not a license to imply the person's real beliefs; generated speech must be presented as simulation.

**Conversational memory:** Retrieval grounded in recorded source memories with citations or visible provenance where possible; refusal/uncertainty on unknown biographical facts; no instructions from an imitation to undertake consequential financial/legal/medical acts. Provide alternative authentic-recordings-only mode.

**Safety requirements:** Watermark/provenance for exports where technically possible; impersonation and deceptive dissemination restrictions, identity verification and appeals; especially strong protections for minors, contested family authorization and intimate contexts; user withdrawal and data-deletion process; memorial wellbeing review without manipulative engagement pressure.

**Business model:** Charge separately for authorized high-cost avatar reconstruction, optional voice generation, and metered interactive conversations. Apply same preauthorization ledger and worst-case vendor-budget reservation as pets, with larger fraud/chargeback buffers and additional consent-related operational cost.

**P4 release gate:** legal/privacy clearance by launch geography; source rights documentation; measured user consent understanding; quality evidence on diverse participants; safety red-team; reproducible cost cap, revocation and deletion evidence. P4 may be canceled even if technically feasible.

## 19. Financial invariants and numerical authorization examples
**Invariant 1 — Per-transaction bounded usage:**
`spendable = max(0, settled_customer_revenue_ex_tax - unavoidable_fees - estimated_refund_chargeback_reserve - allocated_variable_noncompute_cost - required_profit_buffer)`.
No GPU job or streaming session can start unless **upperBoundCost + contingencyReserve ≤ unreservedSpendable**. This applies at household scope as well as pet/operation scope. No automatic unrequested overage purchase.

**Invariant 2 — Cost limiter hierarchy:** Global vendor budget → product plan budget → account/household budget → job budget → stream chunk budget. The most restrictive wins; rejection happens before vendor call. Operations without enforceable provider limits must be self-hosted behind an enforceable deadline/spend cap or disabled.

**Invariant 3 — Historical liabilities:** Cloud storage, backup retention, bandwidth, monitoring, abuse handling, export and cleanup costs must be funded or bounded separately. Sales tax collected/remitted is not contribution revenue. Regulatory taxes on the business, annual licensing, salaries and other fixed costs enter a separate company-wide break-even model.

**Illustrative—not a price promise:** $14.99 sticker price, with a pessimistically assumed $2.25 platform commission, $1.50 variable tax/fee-risk reserve (not assumed actual sales tax), $1.00 retention/support allocation and $4.00 target contribution leaves $6.24 maximum generation expenditure. Replace all figures with actual territory/payment-provider economics. An expected $2.50 GPU bill is insufficient justification if the hard worst-case is $9.00.

**Atomic ledger example:**
```
preauthorize(account_id, operation_id, worst_case_cost, price_version):
  assert entitlement_active
  assert not previously_processed(operation_id)
  assert worst_case_cost <= account_unreserved_balance
  atomically reserve(worst_case_cost)
  return reservation_id
run_with_hard_limits(reservation_id, max_gpu_seconds, max_tokens, max_output_bytes)
settle(reservation_id, measured_cost, release_unused=True)
```

**Failure behavior:** If vendor telemetry lags, allow only previously reserved upper-bound amounts; never assume cost is zero. On unexpected billing, disable affected vendor route and alert. If guarantee fails because vendor has no hard caps, the feature is not released. Ensure the free tier has no open-ended cloud cost paths.

**Financial dashboard and reporting:** Per SKU, device, country, payer, cohort and vendor: collected net revenue, effective tax, commission, contribution, GPU p50/p95/p99, media ingestion, inference and TTS minutes, chargeback liability, retries, refund rate, cloud storage aging, marketing/free-tier acquisition budget. Alerts for forecast margin below target, concurrency anomalies and vendor-price changes.

## 20. Milestone handoff and acceptance deliverables
Each milestone handoff **must** include: source commit, reproducible setup, changed files, hardware model/OS, screenshots/videos of *real device* where relevant, benchmark raw output, measured cost/upper bound, passing and failing test cases, outstanding risks, and `PASS | PARTIAL | FAIL | NOT RUN` (never infer PASS from implementation alone).

| Milestone | Required evidence | Next-step decision |
|---|---|---|
| M0 | Repo, licensing plan, target-device matrix, profiler and benchmark harness | Record gate; proceed to authorized M1 if passed |
| M1 | Legally reusable dog/cat assets + rig/animation tests | Record gate; proceed to authorized M2 if passed |
| M2 | Real-room AR recordings and surface tests | Record gate; proceed to authorized M3 if passed |
| M3 | 30FPS sustained evidence, thermal/run-time data, blind visual test | Stop/improve or authorize M4 |
| M4 | Session behavior and fixed-command tests, offline scenarios | Review prerequisites and explicit approval for production M5 |
| R0–R4 | Separate research cohort, identity/memorial evidence, motion and cost bounds | Research outcome only; no production or launch authority |
| M5 | Production reconstruction fidelity/cost cohort, rigging conversion and failure tests | Kill/pivot or request commerce approval |
| M6 | Payment webhook, ledger races, fault injection and financial invariant tests | Authorize paid user flows |
| M7 | Privacy onboarding, memorial UX, capture and export tests | Authorize pilot |
| M8 | Paying cohort margin, likeness acceptance, refund, revisit and quality data | Authorize broader launch |
| M9 | Memory/room capabilities + battery/thermal + privacy audit | Authorize P2 |
| M10 | Family and multi-pet interaction, sync, shared quota tests | Authorize headsets |
| M11 | visionOS + Quest device-specific performance and safety reports | Authorize releases |
| M12 | Desktop/growth/wearable support matrices and cost tests | Authorize platform expansion |
| M13 | Human consent/legal and preliminary photorealism research gate | Decide whether P4 proceeds |
| M14 | Authorized human recreation + optional voice security and ethics tests | Decide whether P4 can launch |

## 21. Release policy, governance and open decisions
- A prototype build is not equivalent to an approved product launch. Features must be accurate in product description and only offered where device/region/service support has been verified.
- Phase selection is reversible. Any failing safety, financial or realism gate blocks launch and triggers scoped redesign rather than lowering standards without recorded user approval.
- Log architecture decisions as ADRs, provider licensing terms, trademark/domain verification results, and regional privacy/payment compliance status.
- **Still requires evidence:** exact cost per reconstruction; price elasticity and customer demand; photorealistic coat deformation; quality from sparse or historic media; sustainable phone thermals; headset SDK and runtime feature matrix; eventual human legal framework.
- **Brand status:** **Everkio** is the selected product name; **Feel their presence.** is the tagline. Domain availability and trademark clearance are mandatory pre-public-launch blockers; selection does not assert clearance or ownership.
- **Implementation authorization:** v2.1 is the master plan for Everkio Pets → Everkio Spatial → Everkio People. M0–M3 implementation and bounded R0–R4 research only are authorized; all other implementation and every public/commercial launch require explicit approval after prerequisite gates.


## 22. Independent acceptance gates and evidence control
### 22.1 Gate registry
All gates below are **NOT RUN** as of v2.1. No device results, cohort outcomes, bills, rights verification or budget approvals are supplied by this documentation revision. Detailed test procedures live in the two execution plans.

| Gate | Acceptance criteria | Required evidence | Blocking/stop condition |
|---|---|---|---|
| G-P: Presence | Both generic cat and dog meet photorealism, full-motion contact and AR criteria; frame-time p95 ≤33.3 ms and touch p95 <100 ms in each valid 10-minute sustained run on the frozen baseline matrix; zero interaction cloud inference | Real-device raw frame/input/thermal/battery logs, videos, blinded ratings, asset provenance and run manifest; procedures in M3 plan | Missing real device/licensed asset, failed realism/contact, unacceptable thermal degradation or latency; no substitution of editor evidence |
| G-I: Identity fidelity | Living and memorial paths evaluated separately; ≥90% owner acceptance on ≥20 distinct pets per intended launch path, at least 10 cats and 10 dogs, and ≥90% acceptance for each species; full-motion/held-out-view identity and independent photorealism checks pass | Consented cohort manifest, source/holdout split, first-pass and corrected scores, denominator including failed/abstained eligible cases, defect logs and CIs; R-plan defines rubric | Generic render success, static-only likeness or a pooled path score cannot pass; stop a path after two bounded rounds fail its frozen criteria |
| G-F: Financial viability | Every billable operation has a funded server-side reservation and enforceable upper bound; modeled worst-case contribution meets a numerically approved margin floor for each proposed SKU/territory, including correction/failure/retention; zero unauthorized budget overspend in fault tests | Research actual costs and caps, vendor enforcement evidence, price/version model, ledger reconciliation, replay/fault tests; production validation repeated before paid release | Unfunded/uncapped service, unknown material charge, over-cap billing or negative/below-floor contribution; disable affected route immediately |
| G-M: Memorial quality | Memorial G-I passes; ≥90% of ≥10 consenting adult evaluators understand simulation and inferred details and can complete pause/archive/export/delete tasks; zero unresolved critical privacy, deceptive-consciousness or coercive UX defects | Moderated prototype study with opt-out, rubric and issue severity; eventual implementation export/deletion/access verification | Unsupported identity, undisclosed invented detail, pressure to supply unavailable media, critical distress/privacy defect; pause affected study/flow and review |

The G-I cohort threshold replaces the v2.0 candidate ≥90%/20-total proposal. Freeze eligibility and scoring before testing; report uncertainty and representation limitations, not population-wide reliability claims. Pilot study results may be PARTIAL but cannot be relabeled as a passing launch gate. Additional human research remains future-only.

### 22.2 Cross-gate decisions
- G-P permits a presence feasibility conclusion only. It neither proves G-I nor authorizes a generic-only launch.
- Research may continue within its own approved budget if G-P is blocked, and presence may continue if identity research fails. Record their outcomes independently.
- A controlled paid pilot requires G-P + living-path G-I + G-F, validated correction/refund/privacy operations, completed approved M4–M7 implementation and explicit M8 pilot approval. Broader paid living-pet launch additionally requires M8 pilot evidence and explicit launch approval. Pilot approval is not broader launch approval.
- Paid memorial reconstruction additionally requires memorial-path G-I + G-M; a living-pet launch cannot implicitly enable memorial sales.
- No launch before domain/trademark clearance and applicable platform/privacy/payment review. Human and headset gates remain independent future decisions.

### 22.3 Evidence and change protocol
For each test record requirement ID, revision/commit or artifact digest, operator/date, device/OS/build, model/provider/pricing versions where relevant, fixed inputs and seed, method, raw evidence path, sample count/denominator, observed results, budget reserved/actual/remaining, defects, decision owner and status. Use **PASS**, **PARTIAL**, **FAIL**, or **NOT RUN**; attach **BLOCKED** as a reason rather than a substitute for a result. A gate passes only when every required criterion passes.

Pre-register protocol and thresholds before scored runs. Preserve failed runs, exclusions and reasons; never select only favorable devices, pets or attempts. Threshold changes require explicit recorded approval and a new evaluation revision; earlier failures stay in history. Unknown cost, absent hardware, absent rights or missing evidence is a blocker, never a pass.

### 22.4 Initial blocker register
| ID | Missing evidence/decision | Owner role | Blocks |
|---|---|---|---|
| B01 | Actual baseline/flagship iPhones, OS and physical device access | Engineering lead | M0 freeze and G-P |
| B02 | Cat/dog assets, redistribution rights and animation coverage | Art/engineering lead | M1 and G-P |
| B03 | Numerical research total, per-case/attempt caps, contingency and funding source | Product owner + finance | Every billable R-track operation |
| B04 | Consented living/memorial cohort, eligibility and source rights | Research lead | R1–R4 and G-I/G-M |
| B05 | Vendor pricing, enforceable runtime/billing caps and reservation mechanism | Research/finance lead | Billable research and G-F |
| B06 | SKU/territory economics, numerical contribution floor and refund terms | Product owner + finance | Commercial G-F and paid launch |
| B07 | Real-device, identity, cost and memorial study evidence | Relevant gate owners | All gate PASS claims |
| B08 | Domain availability and trademark clearance | Product owner with appropriate review | Public launch |

Owner roles are responsibilities, not assigned people. M0/R0 must record named owners before execution. Missing inputs permit documentation and local nonbillable preparation only where rights and scope allow; they do not authorize resource creation or spending in this task.
