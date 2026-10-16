# Blinded ratings input template — NOT RUN

Copy this directory into an ignored private study bundle before collecting data. Fill the manifest and real clip hashes; the empty template deliberately cannot pass validation. Do not add participant identities, personal consent records or completed study data to Git.

Before collection, freeze the cohort's anonymous IDs, eligibility, clip pair, protocol, consent and blinding method. Record the manifest hash with the dated protocol; preserve every version and exclusion reason. Use at least 20 consenting adults, with cat-first/dog-first order counts differing by at most one. References identify private consent/method records; the analyzer cannot authenticate those records or adulthood. Have an independent reviewer assess the blinding and clip design.

For every enrolled evaluator, record six rows: both species, each rated separately on `animal_realism`, `room_presence`, `natural_motion`. `clip_id` must match the frozen manifest. Order `1`/`2` is the animal clip's position and stays the same across its three dimensions. `consented_adult` must be `true`. Score is integer `1`–`5`, or blank for an explicit abstention. Use the frozen five-point anchored rubric. Preserve free-text defects and qualitative review privately with the protocol; the tool does not interpret them.

All enrolled IDs remain in each denominator, including abstentions and missing responses. Do not remove unfavorable respondents. Missing rows leave the analysis incomplete; an explicit abstention is included as not favorable. A favorable score is at least 4/5; each species/dimension needs at least 80% favorable separately. Do not pool dimensions or species.

Run `python3 tools/presence_ratings.py /private/study-bundle --output /private/new-report.json`. Exit 0 means the supplied ratings/provenance declarations pass the limited checks; 1 means FAIL/PARTIAL; 2 means malformed evidence or output collision. Reports hash the study inputs and referenced clips, reject duplicate responses, unknown cohort IDs, reused clips, changed inputs and clip paths outside the bundle. They never grant G-P. Metadata and matching hashes do not establish real footage, participation, valid consent, adequate blinding or natural-motion acceptance.

Use actual full-motion phone AR clips only for acceptance. Diagnostic/desktop drafts, fabricated responses or synthetic parser fixtures cannot satisfy the study. Independent motion/AR review, scored device sessions and a separate recorded gate decision are still required.
