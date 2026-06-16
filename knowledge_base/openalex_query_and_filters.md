# OpenAlex Query and Filter Documentation

This document summarizes the OpenAlex retrieval and filtering logic used to prepare literature metadata for the disintegration and dissolution knowledge base. It intentionally replaces local database scripts with a public, human-readable description.

## Retrieval Scope

- Topic focus: oral solid dosage forms, tablet/capsule disintegration, dissolution, superdisintegrants, swelling, wicking, wetting, erosion, fragmentation, friability, hardness, and excipient effects.
- Typical query terms: `disintegration`, `superdisintegrant`, `in vitro dissolution`, `oral solid`, `tablet`, `capsule`, `ODT`, `swelling`, `wicking`, `wetting`, `erosion`, `fragmentation`, `HPMC`, `MCC`, `crospovidone`, `croscarmellose`, and `sodium starch glycolate`.
- Year scope used in local scripts: 2015 onward, with per-year limits for manageable screening.
- Metadata fields retained locally: OpenAlex ID, DOI, title, abstract, authors, publication year, language, source, URL, open-access flag, OA URL, concepts, and retrieval query provenance.

## Filtering Logic

Positive filters prioritized records containing dosage-form, disintegration/dissolution, excipient, or compendial-method terminology in titles, abstracts, or concepts. Records with very short or missing abstracts were deprioritized or excluded.

Negative filters removed obvious off-topic records, including dental or orthodontic materials, concrete/cementitious systems, geopolymer materials, network routing, neural-network topics, arXiv-only technical records, and other non-pharmaceutical uses of the same keywords.

## Screening And Deduplication

Records were deduplicated by OpenAlex ID when available. Remaining candidates were ranked by keyword hit patterns across title, abstract, and concept fields. The public repository includes only retrieval documentation and derived notes; local MongoDB databases and full-text literature collections are excluded.

## Public-Release Boundary

The repository does not include copyrighted full-text papers, converted full-text Markdown, raw MongoDB data folders, private retrieval logs, or account-specific request metadata.
