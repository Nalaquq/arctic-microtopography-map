# How is microtopography computed from high-resolution elevation data in Arctic and subarctic landscapes? Protocol for a systematic map

Version 0.1, draft for registration, 3 October 2026. Lead reviewer: S. Gleason. Not yet registered: search strings and decision thresholds are finalised in version 1.0, after search testing (Stage S1) and before screening starts.

## Summary

This systematic map will record how studies of Arctic and subarctic tundra and permafrost terrain compute terrain variables and delineate microforms from elevation data with a native resolution of 5 m or finer. It codes each step of the computation chain, from data acquisition through ground classification, gridding and pre-processing to the derivative algorithm, software and support scale, and scores how completely each step is reported.

The map has two uses. It is a standalone evidence synthesis (Paper 1). It also measures the spread of real practice, which will set the factor levels of a later benchmark of the LiDAR-to-terrain-variable chain (Paper 2), if a decision gate fixed in this protocol is passed.

Companion files: search_strings_v0.1.md, llm_screening_prompt_v0.1.md, codebook_v0.1.csv, extraction templates, screening_form_v0.1.csv, exclusion_codes_v0.1.csv, search_log_v0.1.csv, seed_set_v0.1.csv, recall_check.py and openalex_harvest.py.

## 1. Background

**Microtopography matters in low-relief tundra.** Decimetre-scale relief between polygon rims, troughs and centres, hummocks and hollows, or palsas and fens organises drainage, snow, soil moisture, ground temperature, vegetation and carbon exchange (Liljedahl et al., 2016; Kumar et al., 2016; Wainwright et al., 2017; Abolt et al., 2018; Kemppinen et al., 2018). Studies now quantify it from airborne, UAV and terrestrial lidar, from photogrammetry, and from satellite stereo products such as ArcticDEM.

**Every terrain variable is the end of a chain of choices.** Acquisition (sensor, point density, season), ground classification, gridding and cell size, pre-processing, the derivative algorithm, the neighbourhood or support, and the software all change the values obtained (Florinsky, 1998; Tang & Pilesjö, 2011; Gao et al., 2012; Tang et al., 2013; Riihimäki et al., 2021). Arctic studies make these choices for application-specific reasons. Del Vecchio et al. (2023) resampled ArcticDEM to suppress microtopography before computing slope; Thaler et al. (2023) used a 45 m window for curvature to smooth microtopographic roughness. Microform-extraction studies have tested resolution and parameter sensitivity (Abolt et al., 2019; Wen et al., 2025).

**The gap.** Scoping searches (dossier v0.3: 202 records, 161 logged searches) found no systematic synthesis of how Arctic studies compute and report terrain variables. The closest templates audit DEM accuracy assessment in general (Mesa-Mingorance & Ariza-López, 2020) or review close-range microtopography methods across ecosystems (Shukla et al., 2023). It is therefore unknown which choices dominate Arctic practice, how varied they are, and whether published results can be reproduced or compared.

**Intended users.** Researchers who use high-resolution terrain data in permafrost science, hydrology, ecology and geomorphology, and providers of Arctic elevation data. Outputs are an open database, an evidence atlas, a reporting audit and a practice envelope for benchmark design.

## 2. Objective and questions

**Primary question:** How are terrain variables and microforms computed from high-resolution (≤ 5 m) elevation data in studies of Arctic and subarctic tundra and permafrost landscapes, and how completely are the computation choices reported?

| Element | Definition |
| --- | --- |
| Population | Land surfaces of Arctic and subarctic tundra and permafrost-affected terrain in the circumpolar north, as defined operationally in section 4 |
| Concept | Computation of terrain variables, or delineation of microforms, from elevation data with native resolution ≤ 5 m (raster, TIN or point cloud) |
| Context | Any discipline, application or year; primary research, methods papers and data papers |

**Secondary questions**

1. SQ1 Data: Which elevation sources, platforms and acquisition conditions are used, and how has this changed over time?
2. SQ2 DTM chain: How are ground surfaces classified and gridded, at which cell sizes, by whom (provider or authors), and with what pre-processing?
3. SQ3 Variables and algorithms: Which terrain variables are computed, with which algorithms and software, and at what window or support in metres?
4. SQ4 Scale: How is the analysis scale chosen and justified, and how often are several scales used?
5. SQ5 Accuracy and sensitivity: How often do studies assess the accuracy of elevation data or derived variables, propagate uncertainty, or test whether results change with computation choices, and what do they find?
6. SQ6 Reporting: How completely is the chain reported (Reporting Completeness Index, section 8), and are code and derived data available?
7. SQ7 Patterns: How do SQ1 to SQ6 vary by application, region, landform, data source, venue and year?
8. SQ8 Practice envelope: What are the frequencies of chain configurations (section 9), and which combinations cover most practice?

The map does not judge which method is most accurate. That is the benchmark's job.

## 3. Review type, standards and registration

- **Type:** systematic map following the CEE Guidelines and Standards, version 5.1 (CEE, 2022) and James et al. (2016).
- **Reporting:** ROSES for systematic maps (Haddaway et al., 2018), cross-walked to PRISMA-ScR (Tricco et al., 2018) with JBI scoping-review guidance (Peters et al., 2020; Pollock et al., 2023). Searches are reported to PRISMA-S (Rethlefsen et al., 2021). The ROSES form for systematic-map protocols is completed at registration.
- **Registration:** protocol v1.0 is registered on OSF Registries before screening starts. If the map is to be published as a CEE evidence synthesis, for example in Environmental Evidence, the protocol is registered in PROCEED instead, as CEE asks for maps intended for its journal. The route is chosen in S1.
- **Unit of synthesis:** a study is one analysis of one or more elevation datasets for one study area, reported in one or more records. Several records on the same analysis are one study (companions, E7). A record with separate analyses of several areas is one study with several elevation inputs.
- **Engagement:** in S1, three to five Arctic terrain researchers and data providers (for example NGEE Arctic, NEON, USGS 3DEP and the Polar Geospatial Center) are asked to name key studies, which become seeds, and to comment on the codebook. Their input is logged.
- **Versioning:** v0.x are drafts; v1.0 is the registered protocol; later changes are dated amendments (section 12) reported as deviations.
- **AI use:** declared and validated as set out in sections 6.4, 7.2 and 14, following the 2025 joint position statement of Cochrane, Campbell, JBI and CEE (Flemyng et al., 2025) and the RAISE recommendations (Thomas et al., n.d.).

## 4. Eligibility criteria

Criteria are checked in the order of the exclusion codes, and the first failed criterion is recorded.

| Criterion | Include | Exclude (code) |
| --- | --- | --- |
| Study type | Primary research, methods papers and data papers, in any format: journal article, conference paper, thesis, report, data paper, or preprint without a peer-reviewed version | Reviews, editorials, commentaries, or only an abstract (E1); reviews are kept for citation chasing |
| Area | A site meeting at least one rule: (a) inside the Circumpolar Arctic Vegetation Map extent (Raynolds et al., 2019); (b) tundra or forest-tundra, including oroarctic tundra, north of 60°N; (c) tundra or a permafrost landform (palsa, peat plateau, thermokarst, ice-wedge polygons) in a permafrost zone of Obu et al. (2019) north of 50°N | Sites south of 50°N, Antarctica, mountains outside rules (a) to (c), boreal terrain where no tundra or permafrost landform is analysed, planetary analogues (E2) |
| Surface | Land surface, bare or vegetated | Glacier, ice sheet, sea ice, snow surface only, or seabed (E3) |
| Elevation data | Lidar, photogrammetry, satellite stereo, radar or ground-survey elevation data | No elevation data, for example microforms mapped from imagery alone (E4) |
| Resolution | At least one elevation dataset with native resolution ≤ 5 m, or a point cloud with nominal point spacing ≤ 5 m | All elevation data coarser than 5 m or sparser than 5 m spacing (E5) |
| Terrain computation | At least one terrain variable (Table 2) computed, or microforms delineated, from the ≤ 5 m data | No terrain variable or microform from the ≤ 5 m data, for example raw elevation or elevation change only (E6) |
| Duplicates | Primary report of a study | Secondary report, linked as a companion (E7) |
| Access | Full text obtained | Full text unobtainable after the steps in 6.6 (E8) |
| Language | Any language with a translatable full text | Full text that cannot be translated (E9) |
| Date | No limit | – |

Studies that compute terrain variables on a snow-free DTM to explain snow distribution are eligible. Change-detection studies are eligible only if they also compute a terrain variable or delineate microforms. Sparse altimetry tracks, such as ICESat-2, are not point clouds in this sense. Studies excluded under E2 that are methodologically close, such as Tibetan Plateau polygon studies, are flagged for the discussion but not coded.

**Table 2. Terrain-variable families**

| Family | Examples |
| --- | --- |
| Slope or gradient | slope angle, gradient magnitude, LS factor |
| Aspect | aspect, northness, eastness |
| Curvature | profile, plan, tangential, mean, Laplacian |
| Relative position | TPI, relative elevation, local or residual relief, DEV, depression depth |
| Roughness | standard deviation of elevation, TRI, VRM, surface-area ratio |
| Hydrological or compound | flow accumulation, contributing area, TWI, SPI, HAND, depth-to-water |
| Solar | potential insolation, heat load |
| Morphometric classification | geomorphons, landform classes |
| Microform delineation | polygon centres, rims and troughs; hummocks and hollows; palsas; water tracks; thermokarst pits |
| Spectral or texture | wavelet, Fourier, variogram and fractal metrics |
| Point-cloud geometry | normals, local plane or quadric fits |

## 5. Searching

### 5.1 Sources

| Source | Platform | Role |
| --- | --- | --- |
| Web of Science Core Collection | Clarivate, institutional | Primary |
| Scopus | Elsevier, institutional | Primary |
| GeoRef | EBSCOhost or ProQuest, institutional | Primary; geoscience indexing, reports and theses |
| OpenAlex | API, free (Priem et al., 2022) | Primary; open and scriptable |
| ProQuest Dissertations & Theses Global | ProQuest, institutional | Theses |
| ASTIS (Arctic Science and Technology Information System) | Arctic Institute of North America, free | Arctic literature and reports |
| OSTI.gov | US Department of Energy | Reports, including NGEE Arctic |
| Google Scholar | Publish or Perish; first 300 results per query | Supplementary only (Gusenbauer & Haddaway, 2020) |
| eLIBRARY.ru | Russian-language search, if a Russian-reading collaborator joins | Optional; reduces language bias |
| Citation chasing | citationchaser, which uses Lens.org (Haddaway et al., 2022), or the OpenAlex API | Backward and forward, all included studies |
| Scoping records | Evidence Matrix v0.3 (202 records) | Screened like search results |
| Experts | 3 to 5 Arctic terrain researchers and data providers | Seeds, missing studies |

### 5.2 Strategy

Three concept blocks are combined with AND: A, Arctic, subarctic and permafrost context; B, elevation data; C, terrain variables and microtopography. The blocks and platform syntax are in Appendix A; fully expanded strings are in search_strings_v0.1.md. There are no date, language or document-type limits.

### 5.3 Search development and recall testing (Stage S1)

1. **Confirm seeds.** Every core seed is checked against section 4 at full text; seeds that fail move to the calibration set. Key studies named by experts are added to the validation set.
2. **Split.** The 21 core seeds were split at random (seed 20261003) into 14 development and 7 validation seeds. Nine boundary records and five expected exclusions are kept for screening calibration (seed_set_v0.1.csv).
3. **Develop.** Strings are revised against development seeds only, until every development seed is retrieved by the union of the primary databases (Web of Science, Scopus, GeoRef, OpenAlex).
4. **Validate once.** Validation recall is then measured once on that union, and reported per database, before any further change. Target: at least 6 of 7 (at least 85% if experts enlarge the set).
5. **Keep validation independent.** If strings change after the validation test, the new strings are tested on fresh validation seeds from experts or from citation chasing of development seeds, and both results are reported. Every miss is diagnosed (indexing, vocabulary or scope) with recall_check.py --diagnose.
6. **Log.** Every iteration is logged with date, string version, platform, hit count and seeds retrieved.
7. **Yield check.** If A AND B AND C returns more than 8,000 unique records after deduplication, the two-arm restriction (Appendix A.3) is tested and adopted only if the recall targets still hold.
8. **Freeze.** Strings that meet the targets become version 1.0 at registration.

### 5.4 Supplementary searches

One round of backward and forward citation chasing on all included studies, with a second round if the first adds more than 5% new inclusions. Reviews found during screening are chased backward. Experts receive the list of included studies and are asked for omissions. Records from the scoping matrix are screened like search results.

### 5.5 Managing records

Exports keep full records with abstracts and are named source_date_stringversion. They are never edited. Records are deduplicated by DOI, then by normalised title, year and first author, with near-duplicates checked by hand. Each unique record gets an ID (R00001 onwards). Counts at each step feed the flow diagram.

### 5.6 Updating

If more than 12 months pass between the searches and submission, all searches are rerun and new records screened.

## 6. Screening

### 6.1 Stages

Records are screened on title and abstract, then on full text, against section 4 and the decision guide in Appendix B. At title and abstract, any doubt sends a record to full text.

### 6.2 Consistency checks

Before each stage, S. Gleason and a second human reviewer independently screen a random sample: 200 titles and abstracts, which also serves as SAFE phase 1 (it estimates the share of relevant records), then 20 full texts. The target is Cohen's kappa of at least 0.61, substantial agreement on the Landis and Koch (1977) scale (Cohen, 1960). Below target, disagreements are discussed, Appendix B is clarified, and a new sample is screened. A second human is needed for these checks and for the coding pilot (7.2); if none can be found, the validated LLM screener takes this role, and this is reported as a limitation. Nobody screens a study they authored.

### 6.3 Title and abstract screening

S. Gleason screens in ASReview (van de Schoot et al., 2021). Its starting labels come from the calibration sample, never from the seeds, so finding the development seeds is a real check; "unsure" is labelled relevant. Screening follows the SAFE heuristic (Boetje & van de Schoot, 2024). Phase 2 stops only when all development seeds are found, at least twice the estimated number of relevant records and at least 10% of all records have been screened, and 50 consecutive irrelevant records have been seen. In phase 3 a different model re-ranks the unscreened records until 50 more consecutive irrelevant records are seen. Both models are named with versions. SAFE phase 4, an independent check of excluded records, is supplied by the LLM screener or, if the LLM fails validation, by a second human.

The LLM screener independently screens 100% of records. Records are routed as follows:

| Reached by the human? | Human decision | LLM decision | Route |
| --- | --- | --- | --- |
| Yes | Include or unsure | Any | Full text |
| Yes | Exclude | Include or unsure | Full text |
| Yes | Exclude | Exclude | Excluded |
| No (below the stopping point) | – | Exclude | Excluded, only if the LLM passed validation (6.4) |
| No (below the stopping point) | – | Include or unsure | S. Gleason screens it; his decision is final |

### 6.4 AI assistance and safeguards

- **Tools:** ASReview LAB and one LLM with a frozen prompt (Appendix D; llm_screening_prompt_v0.1.md). Names, versions, settings such as temperature, and dates are recorded.
- **Role:** the LLM can add records to the full-text set. It excludes records on its own only below the human stopping point, and only after passing validation. It is not used for full-text screening.
- **Validation:** "positive" means include or unsure, for both screeners. Before the stopping rule is applied, LLM sensitivity is computed against S. Gleason's decisions on every record he screened. The LLM may exclude records below the stopping point only if there are at least 30 human-positive records, its sensitivity is at least 0.95, and the lower bound of the exact 95% confidence interval is at least 0.85. Otherwise the prompt is revised once (v0.2) and validated on records not used before. If it fails again, S. Gleason screens every record, or a second human performs SAFE phase 4.
- **Reporting:** tools, versions, settings, prompts, agreement statistics and all conflicts are reported, following Flemyng et al. (2025).

### 6.5 Full-text screening

S. Gleason screens every full text. A second human screens a random 20% plus every record marked unsure. If no second human is available, S. Gleason re-screens the same 20% at least two weeks later and reports intra-rater kappa. Disagreements are resolved with a recorded reason. Excluded full texts are listed with their codes.

### 6.6 Full-text retrieval

Open-access copies first, then institutional subscriptions, then interlibrary loan, then one request to the authors with one reminder after three weeks. Records still unobtainable are coded E8 and listed.

## 7. Data coding

### 7.1 Structure

Coding uses three linked tables. **studies** has one row per study. **elevation_inputs** has one row per elevation product used to compute terrain variables. **variables** has one row per terrain variable per elevation input. Field definitions and allowed values are in codebook_v0.1.csv (overview in Appendix C).

### 7.2 Process

1. **Pilot.** Two coders code the same 10 studies independently, without LLM pre-fill, chosen to span source types. Targets: at least 90% agreement on closed fields and 80% on free-text fields judged equivalent. Fields below target are redefined and re-piloted on 5 new studies; the codebook becomes v0.2.
2. **Pre-fill check.** The LLM also pre-fills the 10 pilot studies, citing a page and quote for each value. Its accuracy per field is the share of values that match the consensus coding. Fields below 90% are coded without pre-fill.
3. **Main coding.** For the remaining fields, the LLM may pre-fill values with page and quote, and the human coder verifies or corrects every field against the text.
4. **Audit.** 20% of studies are coded again independently and without pre-fill, by a second human where possible. Field-level agreement is reported, and a field below 90% is re-checked across all studies.

### 7.3 Missing and inferred information

"Not reported" and "not applicable" are separate codes. Unreported settings are never assumed. Where a named software tool implies an algorithm through its defaults, the inferred algorithm is coded with algorithm_basis set to "inferred from software default"; it earns no reporting credit.

### 7.4 Contacting authors

Authors are contacted for missing items only in studies that tested sensitivity to computation choices or whose data are candidates for the benchmark, with one email and one reminder.

## 8. Reporting completeness and study validity

Each study gets a Reporting Completeness Index (RCI) from 13 items in four domains. Items R01 to R07 are judged for each elevation input, R08 to R12 for each terrain variable, and R13 once per study. An input or variable earns an item only if every part of the item is reported for it. Information counts as reported if it is in the main text, the supplement, a companion record, or a specific cited source that documents the same data or processing. A study's item score is the share of applicable inputs or variables that earn it, from 0 to 1. The RCI is the mean of applicable item scores, and each domain also gets its own mean.

{{RCI_TABLE}}

**Not applicable.** R03 is NA for a named public product with a persistent identifier, because its provider documents density. R05 and R06 are NA for a provider DTM with a persistent identifier, because the authors did no ground classification or gridding. Because these rules change denominators, RCI by data source is reported with and without the NA items.

A systematic map does not rate risk of bias. Instead it records whether and how accuracy was assessed (codebook section G) and how completely the chain is reported (RCI).

## 9. Synthesis and outputs

- **Descriptive synthesis:** counts and proportions for every coded field, and cross-tabulations such as variable family by algorithm, variable family by software, source type by cell size, and region by source type.
- **Evidence atlas:** an interactive map of study sites by source type and application.
- **Gap maps:** heat maps of variable family by computation choice, and of application by reporting completeness.
- **Trends:** sensors, software, cell sizes and RCI by publication year.
- **Exploratory associations:** RCI against year, venue field and data source, labelled exploratory.
- **Practice envelope (SQ8):** a configuration is a combination of variable family, algorithm family, software family, cell-size class (≤ 0.25, 0.25–0.5, 0.5–1, 1–2 and 2–5 m), support class (native 3 × 3; up to 5 m; 5–20 m; over 20 m) and pre-processing class (none, smoothing, resampling, other). The envelope reports configuration frequencies and the smallest set covering at least 80% of instances.
- **Sensitivity evidence:** a narrative synthesis of studies that tested computation choices.
- **Release:** the database with a data dictionary, code and figures, with a DOI on OSF or Zenodo; the ROSES form; and the flow diagram.

## 10. Decision gate: is the benchmark warranted?

The gate is evaluated at Stage S6 against thresholds fixed in protocol v1.0 before screening. An instance is a row of the variables table computed from a lidar input. "Not reported" and "other" are left out of denominators. The decision is also reported with every threshold made 25% stricter and 25% looser.

| ID | Criterion | Met if |
| --- | --- | --- |
| G1 | Practice varies | For at least 2 variable families with at least 10 instances of known algorithm, either the most common algorithm–software combination accounts for less than 60% of instances, or, within the most common cell-size class, the 10th to 90th percentile range of support in metres spans at least 5 times |
| G2 | Practice is under-reported | Among included studies with a lidar input, the median RCI is 0.70 or less, or at least 50% fail to report the algorithm (R09) or the window or support (R12) for at least one variable |
| G3 | Choices matter and are rarely tested | At most 20% of included studies test any computation choice, and at least 2 included studies report a material effect: at least a 10% relative change in a model-performance metric, at least 5 percentage points in classification accuracy, or a change in the sign or significance of an effect |
| G4 | The benchmark is new | A dedicated novelty search (Appendix A.5; no area block) finds no study that benchmarks the full chain (point cloud, ground classification, gridding and terrain variables at stated support) against known truth (synthetic surfaces, or an independent reference at least 5 times denser) for tundra-like microforms |
| G5 | The benchmark is feasible | A data check at S6 finds public, ground-classified point clouds for at least 3 microform types (codebook microforms categories) in at least 2 regions, and published statistics for at least 3 microform types to calibrate the synthetic terrain generator |

The decision rule is applied in this order:

1. **No-go** if G5 fails or fewer than two of G1 to G3 are met. Paper 1 is published with reporting recommendations, and the benchmark shrinks to a short technical note.
2. **Pivot** if G4 fails. The prior benchmark is read in full and Paper 2 becomes an extension (new landforms, sensors or supports) or a replication.
3. **Go** otherwise. Benchmark factor levels come from the practice envelope.

**Thin corpus.** If fewer than 20 included studies have a lidar input, G1 and G2 are computed on all included studies, and the gate report says so.

## 11. Stages, deliverables and save points

| Stage | Work | Deliverables | Save point |
| --- | --- | --- | --- |
| S0 | Protocol, templates, seed set, plan update | Protocol v0.1; plan v1.1; templates; scripts | S0 package (this release) |
| S1 | Seed confirmation, expert seeds, search development and recall testing, ROSES form, registration | Strings v1.0; search log; protocol v1.0 registered | S1 package; registration |
| S2 | Full searches, exports, deduplication | Raw exports; deduplicated library; flow counts | S2 package; raw exports archived |
| S3 | Title and abstract screening | Screening log; kappa; LLM validation report | S3 package |
| S4 | Full-text retrieval and screening | Full-text log; exclusions with reasons | S4 package |
| S5 | Coding: pilot, pre-fill check, main, audit | Database v1 (three tables); agreement report | S5 package |
| S6 | Synthesis, novelty search, data check, decision gate | Figures, tables and atlas; gate report; benchmark specification if Go | S6 package |
| S7 | Write-up and release | Paper 1; ROSES form; data and code DOI | S7 package; public release |

At every save point, PROJECT_STATUS.md and CHANGELOG.md are updated, file versions are bumped, and the stage package is archived (with a Git tag if a repository is used). Indicative part-time durations: S1 2 to 3 weeks; S2 1 week; S3 3 to 6 weeks; S4 4 to 6 weeks; S5 6 to 8 weeks; S6 3 weeks; S7 6 weeks.

## 12. Amendments

| Version | Date | Section | Change | Reason |
| --- | --- | --- | --- | --- |
| 0.1 | 3 Oct 2026 | All | First draft | – |

## 13. Anticipated limitations

- English search terms will under-retrieve non-English work, notably Russian-language literature on permafrost microrelief; the optional eLIBRARY.ru search depends on a Russian-reading collaborator.
- If no second human reviewer is available, an LLM fills that role in calibration; this is weaker than two humans and is reported.
- Resolution cannot be searched, so the 5 m limit is applied at screening.
- Missing methods cannot be coded; under-reporting is itself a finding.

## 14. Declarations

- **Funding:** to be added.
- **Competing interests:** to be added.
- **Contributions:** S. Gleason, conception, protocol, screening and coding; second reviewer to be confirmed.
- **AI use:** this draft was prepared with help from Claude (Anthropic), a large language model, for scoping searches, drafting and template construction. The lead reviewer is responsible for all content. AI use in screening and coding is described in sections 6.4 and 7.2.

## References

Abolt, C. J., Young, M. H., Atchley, A. L., & Harp, D. R. (2018). Microtopographic control on the ground thermal regime in ice wedge polygons. The Cryosphere, 12, 1957–1968. https://doi.org/10.5194/tc-12-1957-2018

Abolt, C. J., Young, M. H., Atchley, A. L., & Wilson, C. J. (2019). Brief communication: Rapid machine-learning-based extraction and measurement of ice wedge polygons in high-resolution digital elevation models. The Cryosphere, 13, 237–245. https://doi.org/10.5194/tc-13-237-2019

Boetje, J., & van de Schoot, R. (2024). The SAFE procedure: a practical stopping heuristic for active learning-based screening in systematic reviews and meta-analyses. Systematic Reviews, 13, 81. https://doi.org/10.1186/s13643-024-02502-7

Collaboration for Environmental Evidence (CEE). (2022). Guidelines and Standards for Evidence Synthesis in Environmental Management, Version 5.1 (A. S. Pullin, G. K. Frampton, B. Livoreil, & G. Petrokofsky, Eds.). www.environmentalevidence.org/information-for-authors

Cohen, J. (1960). A coefficient of agreement for nominal scales. Educational and Psychological Measurement, 20(1), 37–46. https://doi.org/10.1177/001316446002000104

Del Vecchio, J., Zwieback, S., Rowland, J. C., DiBiase, R. A., & Palucis, M. C. (2023). Hillslope-channel transitions and the role of water tracks in a changing permafrost landscape. Journal of Geophysical Research: Earth Surface, 128(9), e2023JF007156. https://doi.org/10.1029/2023JF007156

Flemyng, E., Noel-Storr, A., Macura, B., et al. (2025). Position statement on artificial intelligence (AI) use in evidence synthesis across Cochrane, the Campbell Collaboration, JBI and the Collaboration for Environmental Evidence 2025. Cochrane Database of Systematic Reviews, 10, ED000178. https://doi.org/10.1002/14651858.ED000178

Florinsky, I. V. (1998). Accuracy of local topographic variables derived from digital elevation models. International Journal of Geographical Information Science, 12(1), 47–61. https://doi.org/10.1080/136588198242003

Gao, J., Burt, J. E., & Zhu, A.-X. (2012). Neighborhood size and spatial scale in raster-based slope calculations. International Journal of Geographical Information Science, 26(10), 1959–1978. https://doi.org/10.1080/13658816.2012.657201

Gusenbauer, M., & Haddaway, N. R. (2020). Which academic search systems are suitable for systematic reviews or meta-analyses? Evaluating retrieval qualities of Google Scholar, PubMed, and 26 other resources. Research Synthesis Methods, 11(2), 181–217. https://doi.org/10.1002/jrsm.1378

Haddaway, N. R., Grainger, M. J., & Gray, C. T. (2022). Citationchaser: A tool for transparent and efficient forward and backward citation chasing in systematic searching. Research Synthesis Methods, 13(4), 533–545. https://doi.org/10.1002/jrsm.1563

Haddaway, N. R., Macura, B., Whaley, P., & Pullin, A. S. (2018). ROSES RepOrting standards for Systematic Evidence Syntheses: pro forma, flow-diagram and descriptive summary of the plan and conduct of environmental systematic reviews and systematic maps. Environmental Evidence, 7, 7. https://doi.org/10.1186/s13750-018-0121-7

James, K. L., Randall, N. P., & Haddaway, N. R. (2016). A methodology for systematic mapping in environmental sciences. Environmental Evidence, 5, 7. https://doi.org/10.1186/s13750-016-0059-6

Kemppinen, J., Niittynen, P., Riihimäki, H., & Luoto, M. (2018). Modelling soil moisture in a high-latitude landscape using LiDAR and soil data. Earth Surface Processes and Landforms, 43. https://doi.org/10.1002/esp.4301

Kumar, J., Collier, N., Bisht, G., Mills, R. T., Thornton, P. E., Iversen, C. M., & Romanovsky, V. (2016). Modeling the spatiotemporal variability in subsurface thermal regimes across a low-relief polygonal tundra landscape. The Cryosphere, 10, 2241–2274. https://doi.org/10.5194/tc-10-2241-2016

Landis, J. R., & Koch, G. G. (1977). The measurement of observer agreement for categorical data. Biometrics, 33(1), 159–174. https://doi.org/10.2307/2529310

Liljedahl, A. K., et al. (2016). Pan-Arctic ice-wedge degradation in warming permafrost and its influence on tundra hydrology. Nature Geoscience, 9(4). https://doi.org/10.1038/ngeo2674

Mesa-Mingorance, J. L., & Ariza-López, F. J. (2020). Accuracy assessment of digital elevation models (DEMs): a critical review of practices of the past three decades. Remote Sensing, 12(16), 2630. https://doi.org/10.3390/rs12162630

Obu, J., et al. (2019). Northern Hemisphere permafrost map based on TTOP modelling for 2000–2016 at 1 km² scale. Earth-Science Reviews, 193, 299–316. https://doi.org/10.1016/j.earscirev.2019.04.023

Peters, M. D. J., Marnie, C., Tricco, A. C., et al. (2020). Updated methodological guidance for the conduct of scoping reviews. JBI Evidence Synthesis, 18(10), 2119–2126. https://doi.org/10.11124/JBIES-20-00167

Pollock, D., Peters, M. D. J., Khalil, H., et al. (2023). Recommendations for the extraction, analysis, and presentation of results in scoping reviews. JBI Evidence Synthesis, 21(3), 520–532.

Priem, J., Piwowar, H., & Orr, R. (2022). OpenAlex: A fully-open index of scholarly works, authors, venues, institutions, and concepts. arXiv:2205.01833. https://arxiv.org/abs/2205.01833

Raynolds, M. K., et al. (2019). A raster version of the Circumpolar Arctic Vegetation Map (CAVM). Remote Sensing of Environment, 232, 111297. https://doi.org/10.1016/j.rse.2019.111297

Rethlefsen, M. L., Kirtley, S., Waffenschmidt, S., et al. (2021). PRISMA-S: an extension to the PRISMA Statement for Reporting Literature Searches in Systematic Reviews. Systematic Reviews, 10, 39. https://doi.org/10.1186/s13643-020-01542-z

Riihimäki, H., Kemppinen, J., Kopecký, M., & Luoto, M. (2021). Topographic wetness index as a proxy for soil moisture: the importance of flow-routing algorithm and grid resolution. Water Resources Research, 57, e2021WR029871. https://doi.org/10.1029/2021WR029871

Shukla, T., Tang, W., Trettin, C. C., Chen, G., Chen, S., & Allan, C. (2023). Quantification of microtopography in natural ecosystems using close-range remote sensing. Remote Sensing, 15(9), 2387. https://doi.org/10.3390/rs15092387

Tang, J., & Pilesjö, P. (2011). Estimating slope from raster data: a test of eight different algorithms in flat, undulating and steep terrain. WIT Transactions on Ecology and the Environment (River Basin Management VI), 143–154. https://doi.org/10.2495/RM110131

Tang, J., Pilesjö, P., & Persson, A. (2013). Estimating slope from raster data: a test of eight algorithms at different resolutions in flat and steep terrain. Geodesy and Cartography, 39(2), 41–52. https://doi.org/10.3846/20296991.2013.806702

Thaler, E. A., Uhlemann, S., Rowland, J. C., Schwenk, J., Wang, C., Dafflon, B., & Bennett, K. E. (2023). High-resolution maps of near-surface permafrost for three watersheds on the Seward Peninsula, Alaska derived from machine learning. Earth and Space Science, 10, e2023EA003015. https://doi.org/10.1029/2023EA003015

Thomas, J., Flemyng, E., Noel-Storr, A., et al. (n.d.). Responsible use of AI in evidence SynthEsis (RAISE) 1: recommendations for practice. Open Science Framework. https://doi.org/10.17605/OSF.IO/FWAUD

Tricco, A. C., et al. (2018). PRISMA Extension for Scoping Reviews (PRISMA-ScR): checklist and explanation. Annals of Internal Medicine, 169(7), 467–473. https://doi.org/10.7326/M18-0850

van de Schoot, R., de Bruin, J., Schram, R., et al. (2021). An open source machine learning framework for efficient and transparent systematic reviews. Nature Machine Intelligence, 3, 125–133. https://doi.org/10.1038/s42256-020-00287-7

Wainwright, H. M., Liljedahl, A. K., Dafflon, B., Ulrich, C., Peterson, J. E., Gusmeroli, A., & Hubbard, S. S. (2017). Mapping snow depth within a tundra ecosystem using multiscale observations and Bayesian methods. The Cryosphere, 11, 857–875. https://doi.org/10.5194/tc-11-857-2017

Wen, A., Wu, T., Zhu, X., Chen, J., Shi, J., Lou, P., Wang, D., Ma, X., & Wu, X. (2025). Evaluation of the Geomorphon approach for extracting troughs in polygonal patterned ground across different permafrost environments. Remote Sensing, 17(6), 1040. https://doi.org/10.3390/rs17061040

## Appendix A. Search strings (v0.1)

{{APPENDIX_A}}

## Appendix B. Screening decision guide

Answer the questions in order and record the first code that applies. At title and abstract, "unclear" never excludes: the record goes to full text.

1. Is it primary research, a methods paper or a data paper, with more than an abstract? No: E1.
2. Does the site meet area rule (a), (b) or (c) in section 4? No: E2.
3. Is the surface land, not glacier, ice sheet, sea ice, snow surface only, or seabed? No: E3.
4. Does it use elevation data? No: E4.
5. Is at least one elevation dataset 5 m or finer at native resolution, or a point cloud with spacing of 5 m or less? No: E5.
6. Does it compute at least one terrain variable, or delineate microforms, from that 5 m-or-finer data? No: E6.
7. At full text only: is it a secondary report (E7), unobtainable (E8) or untranslatable (E9)?

If no code applies, include. For calibration, the boundary records in seed_set_v0.1.csv are expected to be "unsure" at title and abstract and resolved at full text; the expected exclusions carry their expected code.

## Appendix C. Codebook overview

{{CODEBOOK_OVERVIEW}}

## Appendix D. LLM screening prompt (v0.1)

The prompt is frozen at registration; any change creates a new version that is validated again (section 6.4). Placeholders in braces are filled from each record.

{{LLM_PROMPT}}
