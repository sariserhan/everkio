# Everkio — M0–M3 Engineering Execution Plan v2.1

Date: 2026-10-15. Governing document: [master specification v2.1](everkio_master_spec_v2.md).
Product: **Everkio — Feel their presence.** Track: **Everkio Pets generic presence**.

## Authority and current status
M0–M3 implementation is authorized; this revision only documents the work. No milestone has run and no application code or cloud resources are delivered here. R0–R4 is a separate research track. M4–M14 and public release require explicit approval. Passing M0–M2 permits progression within M0–M3; it does not grant additional scope.

Use one generic adult cat and one generic adult dog. Build only the scene, rig/animation, input test controller and instrumentation necessary to evaluate presence. Accounts, commerce, uploads, production memory, learned commands, social features, headsets and human reconstruction are excluded from this track.

## M0 — Freeze the feasibility contract
**Work:** name engineering/art/test owners; inventory physical devices; select baseline and flagship iPhone models and OS versions; document any unsupported hardware. Pin engine/package candidates after compatibility and licensing verification. Record asset procurement ceilings, rights requirements, test rooms, benchmark method and evidence storage. Establish repository/versioning and a local benchmark scaffold in the later engineering task.

**Acceptance:** reproducible build/run instructions; named physical baseline device available; performance budgets and measurement timestamps defined; two lighting conditions and two usable room configurations selected; licensing and asset plan documented; no hidden billable dependency. Choose a first-run/build warm-up policy and freeze it before scored runs. Record battery health, starting charge, ambient conditions and thermal state.

**Evidence:** device/dependency/license matrix, benchmark schema, protocol revision, named owners, risk register and source commit. If a real device is unavailable, preparation may be PARTIAL but M0 cannot pass.

**Stop:** unsupported toolchain, no legitimate asset path, no suitable physical-device access or unapproved expenditure. Do not provision cloud infrastructure to work around these blockers.

## M1 — Licensed animals and motion
**Work:** obtain assets only within approved procurement limits; verify redistribution in downloadable builds/assets. Prepare PBR mesh/fur/eyes, rigs, animation clips and initial LODs for both species. Review idle/breathing, gaze/reaction, walk/start/stop/turn, approach, sit/lie, and simple eating/contact clips. Use scripted sequences; production autonomy remains M4.

**Acceptance:** both animals remain photorealistic from front/back/sides and close/room-distance views; no material missing-motion coverage, severe deformation or visible rig breaks. Foot plants and body weight are plausible in the curated sequence. License records permit intended distribution; asset provenance and versions are recorded.

**Evidence:** source/license records, asset hashes, animation/contact review clips, rig/LOD/material inventory and defect log. These clips are preparation for G-P, not proof of AR presence.

**Stop:** unclear rights, cartoon substitution, unfixable deformation or proposed asset exceeding procurement cap. Resolve or report FAIL/PARTIAL; do not lower the appearance bar.

## M2 — Real-room AR test harness
**Work:** implement floor placement/scale/anchors, camera motion, lighting approximation, contact shadows, supported occlusion and tracking-loss recovery. Add touch/stroke feedback and scripted locomotion with IK. Instrument local input-to-visible-response timing, frame times, thermal/battery/memory and tracking/contact observations. Use the rigged mesh baseline; any hybrid sample is optional and bounded by the same local scope and budget.

**Acceptance:** both animals can be placed at correct scale and viewed while walking around them. Show placement, turn/approach/contact and safe freeze/re-anchor after tracking interruption. Record capability fallbacks; unsupported occlusion must be disclosed rather than portrayed as working. No network inference is required for interaction.

**Evidence:** real-device recordings, capability matrix, raw logs, annotated drift/clipping/contact defects, offline/network trace and reproducible scripted input sequence.

**Stop:** repeatable loss of anchoring, severe clipping/foot sliding, no measurable local input response or cloud inference on the interaction path. A build that compiles cannot pass M2 without physical-device evidence.

## M3 — Presence gate G-P
### Instrumented runs
- Per animal and baseline/flagship device, run three scored sessions of at least 10 continuous minutes after the fixed warm-up. Cover both selected lighting conditions and both room configurations across the sessions. If only baseline hardware is available, flagship/60 FPS results stay NOT RUN and the supported-device claim stays restricted to tested hardware.
- Retain every frame time and calculate p95 per session: **≤33.3 ms**, with sustained ≥30 FPS throughout, including the final thermal-load interval. Report one-minute windows, stalls and worst windows; a pooled average cannot conceal degradation. Define sustained as each one-minute window averaging ≥30 FPS. 60 FPS is aspirational, not a replacement for the baseline gate.
- Collect ≥100 timestamped touch events per animal/device across sessions: p95 visible feedback **<100 ms**. Use high-speed video or a validated input/presentation timing method and disclose measurement error.
- Log thermal state, battery start/end, memory peak, crashes and interruptions. No crash, OS thermal warning/shutdown or performance failure is acceptable. Freeze any additional device-specific battery/memory thresholds at M0; report values even when no numeric release limit has yet been approved.
- Repeat an offline session and verify zero chargeable cloud inference during interaction. Record any non-inference network traffic separately.

### Motion and AR review
Use the same walk/start/stop/turn/sit/lie/approach/reaction sequence for both animals, including camera orbit, nearby furniture/occlusion where supported and tracking interruption. Two independent reviewers must find **zero major defects** in scored sequences. A major defect visibly breaks presence at ordinary viewing distance: sliding planted feet, gross anatomy deformation, floating contact, persistent floor penetration, scale jumps or repeated anchor displacement. Record minor defects and disagreement; a third reviewer adjudicates using the frozen rubric. Preserve videos and observations; do not hide failed clips.

### Blinded presence evaluation
Use at least 20 adult evaluators, balanced clip order and unlabeled candidate variants. Include full-motion real-device AR clips of both species; conceal rendering method, not the fact that participants are evaluating digital companions. Ask separately about animal realism, grounded room presence and natural motion on a five-point anchored scale. For **each species and each dimension**, ≥80% must rate ≥4/5. Also report free-text defects and score distributions. This is a controlled perception result, not a claim that people believe a real animal exists or proof of personalized identity.

### Gate decision
G-P passes only if the required baseline runs, latency, motion/AR review and blinded evaluation all pass. Compare any neural/hybrid candidate against the same protocol; reject it if it fails thermals, motion or cost requirements. A failed optional candidate does not invalidate a passing baseline. Record the chosen renderer and reasons in an architecture decision. No real-device evidence means NOT RUN, never PASS.

## Handoff and stop rules
Each M0–M3 handoff includes commit/artifact digest, reproducible setup, device/OS/build, raw logs, videos, test counts, costs if any, defects, blocker owner and PASS/PARTIAL/FAIL/NOT RUN. Initial status of every milestone and G-P is **NOT RUN**; blockers B01/B02/B07 in the master spec are unresolved.

After a failed gate, record the failure and a bounded corrective plan within authorized scope. If two evaluated rendering iterations cannot meet presence criteria, stop expansion and request a feasibility decision; do not rebrand a less realistic result as success. M3 completion produces a decision packet for M4 approval, not permission to begin M4 or launch. Reconstruction outcomes are reported separately.
