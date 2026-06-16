# OpenFDA Field Mapping

This document records the OpenFDA/DailyMed fields used by the formulation knowledge-base extraction workflow. It was assembled from the local OpenFDA extraction script and the approved OpenFDA output folder; full label text exports are not copied here.

## Source Materials

- Extraction code: local OpenFDA/DailyMed excipient extraction script (`fetch_openfda_excipients.py`).
- Output folder: approved local OpenFDA output folder containing public label-query examples.
- Output example: METFORMIN(2).txt
- Output example: NATAZIA.txt
- Output example: NIFEDIPINE (2).txt
- Output example: TELMISARTAN (2).txt

## API Endpoints And Query Fields

| Purpose | Field or endpoint | Repository use |
| --- | --- | --- |
| Primary label retrieval | `https://api.fda.gov/drug/label.json` | Queries structured drug-label records. |
| DailyMed fallback | `https://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json` and `drugInfo.cfm?setid=` | Used only when OpenFDA records do not provide usable inactive-ingredient evidence. |
| Brand-name search | `openfda.brand_name` | Matches target branded products such as PROCARDIA XL, ADALAT CC, AFEDITAB CR, NIFEDICAL XL, MICARDIS, GLUCOPHAGE XR, GLUMETZA, FORTAMET, and NATAZIA. |
| Generic-name search | `openfda.generic_name` | Matches generic drug names such as NIFEDIPINE, TELMISARTAN, and METFORMIN HYDROCHLORIDE. |
| Substance-name search | `openfda.substance_name` | Alternative target matching when brand or generic fields are incomplete. |
| API key handling | `OPENFDA_API_KEY` environment variable | Optional rate-limit helper; no API key is stored in the repository. |

## Extracted Output Columns

| Output column | Source field or derivation | Notes |
| --- | --- | --- |
| `drug_target` | Script target display name plus release-mechanism classification | Used to group comparable sustained-release formulations. |
| `label_id` | OpenFDA record `id` | Label-level provenance. |
| `set_id` | OpenFDA `set_id` or `openfda.spl_set_id` | SPL set identifier for traceability. |
| `effective_time` | OpenFDA `effective_time` | Label version date when available. |
| `brand_names` | `openfda.brand_name` | Semicolon-joined brand names. |
| `generic_names` | `openfda.generic_name` | Semicolon-joined generic names. |
| `dosage_forms` | `openfda.dosage_form` | Also used for tablet/extended-release filtering. |
| `routes` | `openfda.route` | Administration-route metadata. |
| `excipient_name` | `inactive_ingredient` or strict extraction from label text | Normalized excipient term. |
| `evidence_quote` | `inactive_ingredient` field or an explicit inactive-ingredients line | Short evidence trace for the extracted excipient list. |
| `source_note` | Query field/value plus source label | Documents whether the row came from OpenFDA or DailyMed fallback. |

## Filters

- Tablet-oriented records are prioritized by checking dosage-form strings for terms such as `TABLET`, `EXTENDED`, `SUSTAINED`, or `CONTROLLED`, depending on the target product.
- Mechanism tags are heuristic labels derived from formulation text. Osmotic terminology maps to `osmotic_pump_like`; hydrophilic-matrix terms such as HPMC map to `hydrophilic_matrix`; otherwise the mechanism is `unknown`.
- Full OpenFDA/DailyMed label text is treated as source evidence and is not duplicated in this repository document.

