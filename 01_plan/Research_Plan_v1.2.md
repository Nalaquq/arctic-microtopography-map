# Arctic Tundra Microtopography Benchmark: Integrated Meta-Review, Benchmark Study and Article Development Plan

Working Research Plan, version 1.2, 3 October 2026. Supersedes version 1.1. Purpose: first, map how terrain variables and microforms are computed from high-resolution elevation data in Arctic and subarctic landscapes (a registered systematic map, Paper 1). Then, if the map's go/no-go gate is passed, run a practice-weighted, reproducible benchmark of the LiDAR-to-terrain-variable chain on the USDA SCINet cluster, using a realistic synthetic tundra with virtual laser scanning and public Arctic LiDAR (Paper 2).

## Change log

| # | Version | Where | Change | Reason |
| --- | --- | --- | --- | --- |
| 1 | 1.1 | Purpose; sections 1, 2; former 5.4, 10 and Gate F | Removed the Quinhagak held-out salmonberry (cloudberry) application | Lead author decision, 2 to 3 October 2026: this is a methods benchmark, not a cloudberry or Quinhagak study |
| 2 | 1.1 | Purpose; section 2 | Two linked papers: systematic map first (Paper 1), benchmark second (Paper 2) | An operator-only comparison is not novel (dossier v0.3, concern M1); how Arctic studies compute terrain variables has not been mapped |
| 3 | 1.1 | Section 3 | Phase I becomes a registered systematic map: protocol, seed-set recall testing, AI-assisted screening with human verification, and a Reporting Completeness Index | Dossier v0.3: PRISMA-ScR and ROSES standards; an auditable basis for novelty claims |
| 4 | 1.1 | Sections 3.4, 13 | Gate A becomes a go/no-go with pre-specified criteria G1 to G5 | Answers "is the benchmark needed?" with evidence before HPC time is committed |
| 5 | 1.1 | Section 4 | Scale-explicit estimands (G_L, K_L, R_L, L∗). The DTM chain and support become primary factors; the operator becomes secondary | Dossier v0.3, sections B1 to B4 and concerns M2, M3 and M5 |
| 6 | 1.1 | Sections 5.1, 7 | Synthetic tier upgraded from analytic shapes to procedural tundra terrain, vegetation and virtual laser scanning (HELIOS++) | Known truth for the whole chain, not only for the operator |
| 7 | 1.1 | Sections 5.2, 8 | Real-data tier uses public point clouds only, with no new field or RTK campaign | The lead author cannot collect independent UAS LiDAR with RTK |
| 8 | 1.1 | Sections 5.3, 9 | ArcticDEM and IfSAR comparison becomes an optional secondary arm | Scope is LiDAR-derived Arctic elevation products |
| 9 | 1.1 | Section 6 | SCINet workflow specified: containers, workflow manager, SLURM arrays, provenance | The HPC allocation is the enabling resource |
| 10 | 1.1 | Sections 14, 15 | Next steps replaced by Stages S0 to S7 with save points | Lead author request to save progress in stages |
| 11 | 1.2 | Sections 3.2, 12, 13 | Paper 1 targets The Cryosphere as a research article, with Permafrost and Periglacial Processes as the alternative; registration on OSF only | Lead author decision, 3 October 2026; Environmental Evidence is out of scope |
| 12 | 1.2 | Section 3.2 | The second reviewer is a student collaborator | Lead author decision, 3 October 2026 |
| 13 | 1.2 | Sections 6, 15 | The GitHub repository Nalaquq/arctic-microtopography-map is the canonical copy; day-to-day work runs in Claude Code in VS Code on Fedora | Lead author preference |

## 1. Executive summary

The project proceeds in two linked papers. **Paper 1** is a registered systematic map of how Arctic and subarctic studies compute terrain variables and delineate microforms from elevation data at 5 m or finer. It codes each step of the chain (acquisition, ground classification, gridding, pre-processing, algorithm, software, support) and scores how completely each step is reported. It stands on its own and also measures the spread of real practice.

**Paper 2** is a benchmark of the LiDAR-to-terrain-variable chain, run only if Paper 1's gate is passed. Its factor levels come from observed practice, so it tests what people actually do. Known truth comes from procedural tundra terrains scanned with a virtual laser scanner, so every stage of the chain can be scored, not just the slope operator. Public Arctic LiDAR tests whether the synthetic results transfer, through swath-overlap and repeat-survey precision. The USDA SCINet cluster makes the full factorial feasible.

What is new: the first systematic account of Arctic practice; a benchmark weighted by that practice; known truth for the whole chain; scale-explicit estimands reported in metres; and an open, reproducible release.

## 2. Roadmap and decision gates

| Phase | Objective | Principal deliverable | Gate at the end |
| --- | --- | --- | --- |
| I | Systematic map of computation practice (Stages S0 to S7) | Registered protocol; coded database; Paper 1 | A: go, pivot or no-go (G1 to G5) |
| II | Benchmark questions and protocol freeze | Benchmark protocol v1.0: estimands, practice-weighted factors, primary contrasts | B: novelty and design justified by Phase I |
| III | Data inventory and synthetic generator | Public point-cloud inventory; calibrated terrain generator | C: data adequacy |
| IV | Pipeline on SCINet | Tested, containerised workflow with provenance | D: pipeline validation |
| V | Synthetic chain benchmark | Error budgets against known truth | F: synthetic realism, before production runs |
| VI | Real public LiDAR | Precision and transfer results | E: confirmatory freeze before outcomes are viewed |
| VII | Optional product-transfer arm | ArcticDEM or IfSAR comparison | Decided at Gate B |
| VIII | Statistical synthesis | Decision surfaces; reporting checklist | – |
| IX | Release and manuscripts | Paper 2; benchmark data and code with a DOI | G: journal choice |

## 3. Phase I: systematic map (meta-review)

### 3.1 Question

How are terrain variables and microforms computed from high-resolution (≤ 5 m) elevation data in studies of Arctic and subarctic tundra and permafrost landscapes, and how completely are the computation choices reported? Eight secondary questions cover data sources, the DTM chain, variables and algorithms, scale, accuracy and sensitivity testing, reporting, patterns, and the practice envelope. The full protocol is Review Protocol v0.2.

### 3.2 Methods in brief

- **Searches:** Web of Science, Scopus, GeoRef, OpenAlex, ProQuest theses and OSTI, with Google Scholar as a supplement, plus citation chasing and experts. Three concept blocks (Arctic context, elevation data, terrain variables) are combined with AND.
- **Recall testing:** 21 core seeds, confirmed at full text, split into 14 development and 7 validation seeds. Every development seed and at least 6 of 7 validation seeds must be retrieved; validation recall is measured once, before any further change.
- **Screening:** ASReview with the SAFE stopping heuristic. An LLM screens every title and abstract as a second screener; it may exclude records the human did not reach only after validation (sensitivity at least 0.95, lower 95% bound at least 0.85, at least 30 positives). No LLM at full text; every full-text decision is human. A student collaborator is the second reviewer for calibration, the 20% full-text check and the coding pilot.
- **Coding:** three linked tables (studies, elevation inputs, variables) with 123 defined fields; a pilot with agreement targets; a 20% audit without LLM pre-fill.
- **Reporting Completeness Index:** 13 items across data, DTM, derivatives and openness, scored as the share of inputs or variables for which each item is reported.
- **Registration:** OSF Registries before screening; reporting to ROSES and PRISMA-ScR.

### 3.3 Outputs

An open database, an evidence atlas, a reporting audit, and a practice envelope: the frequencies of cell size, support in metres, algorithm, software and pre-processing for each common variable, and the smallest set of configurations covering at least 80% of practice.

### 3.4 Gate A: go, pivot or no-go

| ID | Criterion | Met if |
| --- | --- | --- |
| G1 | Practice varies | For at least 2 variable families with at least 10 lidar instances of known algorithm, either the most common algorithm–software combination accounts for less than 60% of instances, or, within the most common cell-size class, the 10th to 90th percentile range of support spans at least 5 times |
| G2 | Practice is under-reported | Among included studies with a lidar input, the median RCI is 0.70 or less, or at least 50% fail to report the algorithm or the window or support for at least one variable |
| G3 | Choices matter and are rarely tested | At most 20% of included studies test any computation choice, and at least 2 included studies report a material effect (defined in the protocol) |
| G4 | The benchmark is new | A dedicated novelty search with no area block finds no study benchmarking the full chain against known truth for tundra-like microforms |
| G5 | The benchmark is feasible | Public, ground-classified point clouds for at least 3 microform types in at least 2 regions, and published statistics to calibrate the generator for at least 3 microform types |

An instance is a variable computed from a lidar input. The rule is applied in order: no-go if G5 fails or fewer than two of G1 to G3 hold (Paper 1 is published with reporting recommendations and the benchmark shrinks to a technical note); pivot if G4 fails (Paper 2 becomes an extension or replication of the prior benchmark); otherwise go. If fewer than 20 included studies have a lidar input, G1 and G2 use all included studies. Thresholds are fixed in protocol v1.0 before screening, and the decision is also reported with thresholds 25% stricter and looser.

### 3.5 What happened to the v1.0 Phase I questions

The v1.0 questions on operators, flat terrain and sensitivity to resolution and neighbourhood move to Paper 2's background and Tier 0 analysis. The questions on Arctic practice and reporting become the map's secondary questions. The v1.0 rule that a full-text-unverified claim is never treated as verified is kept.

## 4. Phase II: benchmark questions and estimands (provisional)

### 4.1 Questions, finalised at Gate B

1. BQ1 Error budget: for each tundra microform type and support L, how large are errors in G_L, K_L and R_L from each stage of the chain (point density, ground filter, gridding, cell size, operator, smoothing), and which stage dominates?
2. BQ2 Optimal support: what is L∗ by landform and acquisition type, and how does it trade attenuation against noise and vegetation bias?
3. BQ3 Operators: once support is matched, do operator choices still matter? Linear-filter theory predicts little difference; Tier 0 tests this analytically.
4. BQ4 Practice: which commonly used configurations, from the practice envelope, produce errors large enough to change typical results, such as trough-versus-centre classification or wetness-index ranking?
5. BQ5 Transfer: do synthetic findings transfer to real acquisitions, judged by swath-overlap and repeat-survey precision, and by accuracy where public independent references exist?

### 4.2 Estimands

- **Reference surface z_ref:** the bare-ground surface (in the synthetic tier, known exactly).
- **Scale-explicit gradient:** G_L(x) = |∇(g_L ∗ z_ref)(x)|, where g_L is an isotropic Gaussian with standard deviation L in metres. Support is reported in metres and as an equivalent cut-off wavelength, never as a window size alone.
- **Scale-explicit curvature:** K_L(x) = ∇²(g_L ∗ z_ref)(x), or the profile and plan curvatures of the same smoothed surface.
- **Relative elevation:** R_L(x) = z_ref(x) − (g_L ∗ z_ref)(x).
- **Optimal support:** L∗ = argmin over L of E[(Ĝ_L − G_L)²], reported with its error budget.

### 4.3 Primary outcomes and protocol

RMSE and bias of G_L, K_L and R_L against truth at matched support; the false-slope floor on flat ground; peak attenuation; feature-position error; and agreement of microform classifications. A Benchmark Protocol v1.0 with primary contrasts and decision rules is registered before production runs.

## 5. Phase III: benchmark corpus

### 5.1 Synthetic tier (known truth)

- **Tier 0, analytic:** planes, Gaussian mounds and troughs for unit tests and closed-form operator properties.
- **Procedural tundra terrain:** ice-wedge polygon networks (Voronoi or crack-network growth after Plug & Werner, 2002) in low-, flat- and high-centred forms; hummock fields; tussocks; palsas and peat plateaus; water tracks; thermokarst pits; drained-lake-basin margins. Parameters are calibrated to published statistics, for example polygon morphometrics from Abolt & Young (2020) and hummock dimensions from Tarnocai & Zoltai (1978).
- **Vegetation:** canopy height and density fields by microform position (moss, sedge, dwarf shrub, tussock) to create vegetation-organised ground-detection bias.
- **Virtual laser scanning:** HELIOS++ (Winiwarter et al., 2022) with airborne (QL1- and QL2-like) and UAV configurations, varying point density, scan angle, overlap and noise.
- **Truth:** the bare-ground surface at any support, with derivatives computed exactly by convolution.

### 5.2 Real tier (public data only)

Details marked "to confirm" are checked in the Phase III inventory before any design depends on them.

| Dataset | Region and landforms | Point cloud | Use |
| --- | --- | --- | --- |
| 2024 NOAA lidar, AK Coastal Communities (InPort 77595 points, 77599 DEM) | Five south-west Alaska coastal communities; coastal tundra | Yes; QL1; NVA 0.031 m RMSE; 0.5 m DEM | Tier 1 swath overlap; western Alaska |
| 2024–2025 USGS lidar DEM, Typhoon Merbok, Norton Sound (InPort 79622) | Western Alaska | 0.5 m DEM; NVA 2.63 cm RMSE; points to confirm | Tier 1; landform diversity |
| NGEE Arctic BEO DEMs, 0.5 m (2012) and 0.25 m (2013), with polygon and trough-rim-centre maps (OSTI 1109234, 1224720, 1136188, 1136189) | Utqiagvik polygonal tundra | To confirm | Microform labels; repeat pair |
| NGEE Arctic Seward Peninsula UAS lidar, Teller 27 (2017, 2018), Kougarok (2017) (OSTI 2217322, 2350811, 2228331) | Hillslope tundra, shrubs, water tracks | To confirm | Repeat precision; shrub bias |
| Abolt & Young (2020) Prudhoe Bay polygon dataset | Polygonal tundra | Derived products | Generator calibration; labels |
| NEON AOP discrete lidar at BARR (Utqiagvik) and TOOL (Toolik) | Coastal and foothills tundra | Yes; repeat years to confirm | Consistently processed repeats |
| Trail Valley Creek ALS, 21 Aug–14 Sep 2016 (Anders et al., 2018; PANGAEA, CC BY 4.0) | Upland tundra, Northwest Territories | Yes | Canadian tundra; shrub tundra |
| Fennoscandian national lidar (Finland, Norway, Sweden) | Oroarctic tundra; palsa mires | To confirm | Palsas; repeat acquisitions |
| MACS very-high-resolution point clouds and DSMs (Rettelbach et al., 2024) | Alaska and north-west Canada | Photogrammetric | Optional cross-sensor check |

The 2022 NCALM winter lidar on the Seward Peninsula (OSTI 1984094) is snow-on, so it is not a ground reference.

### 5.3 Optional product-transfer arm

ArcticDEM v4.1 strips and mosaics are surface models and need co-registration and stable-terrain error modelling. The USGS 3DEP Alaska 5 m IfSAR DTM is a regime-boundary case only. Whether to include this arm is decided at Gate B.

## 6. Phase IV: computational infrastructure on SCINet

- **Repository modules:** ingest, synth (terrain generator and HELIOS++ configurations), dtm (ground filters and gridding), deriv (operators, Gaussian derivatives, support), eval (truth comparison and metrics), stats and figs.
- **Environment:** containers (for example Apptainer, subject to SCINet policy) pinning PDAL, GDAL, HELIOS++ and the Python and R stacks; versions recorded.
- **Workflow:** Snakemake or Nextflow driving SLURM job arrays over scene × acquisition × filter × gridding × cell size × operator × support.
- **Provenance:** a manifest row per output with a configuration hash, software versions, input checksums and CRS.
- **Data movement:** Globus for public data; no permanent duplication of archived sources.
- **Working environment:** the GitHub repository Nalaquq/arctic-microtopography-map is the canonical copy of every file. Day-to-day work runs in Claude Code from the command line in VS Code on Fedora; heavy computation runs on SCINet.
- **Tests:** Tier 0 surfaces must reproduce closed-form derivatives within tolerance before any production run.
- **Compute budget:** estimated after Gate B from the number of scenes and configurations.

## 7. Phase V: Experiment A, synthetic chain benchmark

- **Factors:** microform type, relief, vegetation, acquisition (density, scan angle, overlap), ground filter, gridding, cell size, operator and support L. Categorical levels come from the practice envelope.
- **Design:** full factorial over practice-weighted categorical levels, with Latin-hypercube sampling of continuous factors and replicate random seeds.
- **Outcomes:** as in 4.3.
- **Gate F, synthetic realism:** before production runs, synthetic point clouds and DTMs must match real acquisitions within pre-set tolerances on point-density distribution, ground-point fraction by vegetation class, and short-lag DTM roughness (variogram or spectrum).

## 8. Phase VI: Experiment B, real public LiDAR

- **Tier 1, precision:** swath-overlap differences using LAS point source IDs, and same-season repeats; short-range DTM noise variograms; derivative precision as a function of L.
- **Tier 2, accuracy:** only where public independent references exist, such as denser UAS lidar or published survey points over the same ground, and labelled as such.
- **Transfer:** compare real precision and error spectra with synthetic predictions; test whether L∗ and stage rankings transfer.
- **Sampling unit:** tile or acquisition, never the pixel.

## 9. Phase VII: optional product-transfer arm

If kept at Gate B: separate product error from operator error; compare direct gridding at coarser resolution with aggregation from finer LiDAR DTMs; and find the feature-width-to-cell-size and relief-to-uncertainty regimes where microtopography stops being recoverable.

## 10. Phase VIII: statistical analysis and synthesis

Hierarchical models with tiles nested in acquisitions and regions, and treatments paired within terrain. Effect sizes with uncertainty intervals; interactions among chain stage, support, landform and error regime; no pixel-level pseudo-replication; pre-specified primary outcomes with exploratory analyses labelled. The product is conditional decision surfaces, not a single winner. An optional consequence check, decided at Gate B, re-runs a published-style analysis on public response data (for example soil moisture or active-layer thickness) under different chain configurations.

## 11. Phase IX: reproducibility and release

Code and configurations that regenerate every product; dataset manifests with source identifiers, checksums and CRS; synthetic terrains with their truth fields and HELIOS++ settings; the practice-envelope table; summary outputs where licences allow; a frozen release with a DOI; and a table linking each manuscript result to its exact configuration.

## 12. Manuscripts and journals

| Paper | Working title | Target journal |
| --- | --- | --- |
| 1 | How Arctic microtopography is computed and reported: a systematic map | The Cryosphere (research article); alternative: Permafrost and Periglacial Processes |
| 2 | How small is too small? A practice-weighted benchmark of the point-cloud-to-terrain-variable chain for tundra microtopography | Remote Sensing of Environment; ISPRS Journal of Photogrammetry and Remote Sensing; JGR: Earth Surface (chosen at Gate G) |

The Cryosphere covers permafrost and seasonally frozen ground and remote sensing, and several of the studies the map audits were published there. Its research articles are typically up to 12 journal pages with at most 80 references, so the full list of included studies goes in the data release, and an editor is contacted before submission in case the map is classed as a review article (reviews need an editor's agreement). If a permafrost-specialist readership matters more than reach, Permafrost and Periglacial Processes is the alternative; the protocol is the same for both.

## 13. Formal decision gates

- **Gate A, systematic map:** go, pivot or no-go on G1 to G5 (section 3.4).
- **Gate B, novelty and design:** benchmark questions, estimands and factor levels justified by Phase I; Benchmark Protocol v1.0 registered.
- **Gate C, data adequacy:** enough public point clouds across landforms and regions.
- **Gate D, pipeline validation:** every implementation passes Tier 0 tests.
- **Gate E, confirmatory analysis:** primary analyses frozen before confirmatory outcomes are viewed.
- **Gate F, synthetic realism:** replaces the v1.0 Quinhagak gate (section 7).
- **Gate G, journal selection:** Paper 1 targets The Cryosphere (decided 3 October 2026); Paper 2's journal is chosen by the nature of its final contribution.

## 14. Stages and save points (Phase I)

| Stage | Work | Save point |
| --- | --- | --- |
| S0 | Protocol v0.1, templates, seed set, scripts, plan v1.1 | S0 package (done, 3 Oct 2026) |
| S1 | Search development, recall testing, registration | S1 package; protocol v1.0 on OSF |
| S2 | Full searches, exports, deduplication | S2 package; raw exports archived |
| S3 | Title and abstract screening | S3 package |
| S4 | Full-text retrieval and screening | S4 package |
| S5 | Coding: pilot, main, audit | S5 package |
| S6 | Synthesis and Gate A | S6 package; benchmark specification if Go |
| S7 | Paper 1 and data release | S7 package; public release |

At every save point, PROJECT_STATUS.md and CHANGELOG.md are updated, file versions are bumped and the package is archived. Save points for Phases II to IX are defined at Gate B.

## 15. Immediate next steps (Stage S1)

1. Clone the GitHub repository on Fedora, install the tools (README) and continue in Claude Code in VS Code.
2. Confirm the 21 core seeds at full text and ask three to five experts for key studies; then run the S1 test searches in Web of Science, Scopus and GeoRef with strings v0.1, export full records, and run recall_check.py against the seed set.
3. Run openalex_harvest.py for the OpenAlex arm.
4. Brief the student collaborator on the screening guide (protocol Appendix B) and schedule the calibration samples for Stage S3.
5. Freeze strings and thresholds as protocol v1.0 and register it on OSF.
6. Start the Phase III data inventory in parallel, without making design decisions before Gate A.

## 16. Guiding principle

**The project should not begin with a preferred algorithm and search for evidence that supports it. It should begin with a complete account of what the field has already tested and how it computes terrain in practice, use that evidence to define the unresolved measurement problem, and then design the largest and most reproducible benchmark necessary to answer it.**

## References

Abolt, C. J., & Young, M. H. (2020). High-resolution mapping of spatial heterogeneity in ice wedge polygon geomorphology near Prudhoe Bay, Alaska. Scientific Data, 7, 87. https://doi.org/10.1038/s41597-020-0423-9

Anders, K., Antonova, S., Boike, J., Gehrmann, M., Hartmann, J., Helm, V., Höfle, B., Marsh, P., Marx, S., & Sachs, T. (2018). Airborne Laser Scanning (ALS) Point Clouds of Trail Valley Creek, NWT, Canada (2016) [dataset]. PANGAEA. https://doi.org/10.1594/PANGAEA.894884

Plug, L. J., & Werner, B. T. (2002). Nonlinear dynamics of ice-wedge networks and resulting sensitivity to severe cooling events. Nature, 417, 929–933. https://doi.org/10.1038/nature00796

Rettelbach, T., et al. (2024). Very high resolution aerial image orthomosaics, point clouds, and elevation datasets of select permafrost landscapes in Alaska and northwestern Canada. Earth System Science Data, 16, 5767. https://doi.org/10.5194/essd-16-5767-2024

Tarnocai, C., & Zoltai, S. C. (1978). Earth hummocks of the Canadian Arctic and Subarctic. Arctic and Alpine Research, 10(3). https://doi.org/10.1080/00040851.1978.12003997

Winiwarter, L., et al. (2022). Virtual laser scanning with HELIOS++: A novel take on ray tracing-based simulation of topographic full-waveform 3D laser scanning. Remote Sensing of Environment, 269, 112772. https://doi.org/10.1016/j.rse.2021.112772

Other sources are cited in Review Protocol v0.2 and State-of-Field Dossier v0.3.
