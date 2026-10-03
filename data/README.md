# data

Working data for the systematic map. Layout from Stage S2 onwards:

| Folder | Contents | In Git? |
| --- | --- | --- |
| `raw_exports/` | Database exports exactly as downloaded (Web of Science, Scopus, GeoRef, PQDT) | **No** – ignored by `.gitignore` |
| `openalex/` | OpenAlex harvests from `04_scripts/openalex_harvest.py` | Yes |
| `library/` | Deduplicated record library with record IDs (R00001 …) and source flags | Yes |
| `screening/` | Filled screening forms and calibration samples | Yes |
| `extraction/` | Filled extraction tables (studies, elevation_inputs, variables) | Yes |

Raw exports from licensed databases are kept out of Git because their licences generally do not allow redistribution,
and this repository may become public when the map is published. Archive them privately (for example in a private OSF
component or institutional storage) and record each file's name, date and hit count in `03_templates/search_log_v0.1.csv`.
