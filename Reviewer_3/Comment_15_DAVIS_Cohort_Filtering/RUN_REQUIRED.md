# Comment 15 cohort audit completed

No new model training is required for Reviewer 3 Comment 15.

The cohort audit now establishes the following:

- The main FGgraphDTA and PVgraphDTA DAVIS benchmark experiments used the complete 442-target / 30,056-interaction DAVIS population.
- Complete PconsC4 contact maps and alignment files were available for all 442 target entries used in the main benchmark workflow.
- The main DAVIS protocol used the reported 80/10/10 interaction split: 24,044 train, 3,006 validation, and 3,006 test interactions.
- The 287-target / 19,516-interaction population was specific to the additional cold-target experiment.
- The 287-target table contains 268 unique sequence strings and retains explicit modified target entries; it is therefore not a canonical-wild-type-only subset.
- The cold-target comparison used 229 training targets / 15,572 interactions and 58 held-out targets / 3,944 interactions.
- DGraphDTA and FGgraphDTA were compared on the same cold-target cohort and partition.

The historical construction record for the pre-filtered 287-target table does not preserve a complete auditable first-failure reason for all 155 omitted DAVIS target entries. Do not retrospectively attribute those omissions to PconsC4 failure, shallow MSAs, or strict wild-type curation.

Use `RESPONSE_AND_MANUSCRIPT_CHANGES.txt` for the finalized reviewer response and exact manuscript edits.
