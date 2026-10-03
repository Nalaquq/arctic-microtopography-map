# -*- coding: utf-8 -*-
"""Build Stage-0 data templates: codebook, extraction tables, screening form, search log, seed set,
and the search-strings file. Run: python3 build_templates.py"""
import csv
import random
import os
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]  # repository root
sys.path.insert(0, str(ROOT / "04_scripts"))
import search_blocks as sb  # noqa: E402

OUT = str(ROOT)
T = f"{OUT}/03_templates"
MATRIX = str(ROOT / "05_scoping_v0.3" / "Arctic_DEM_Microtopography_Evidence_Matrix_v0.3.csv")
os.makedirs(T, exist_ok=True)

NR = "not reported"

# ---------------------------------------------------------------------------------------------
# Codebook: (field_id, section, table, field_name, label, instruction, type, allowed, required, rci, example)
# ---------------------------------------------------------------------------------------------
CB = []


def f(fid, sec, table, name, label, instr, typ, allowed="", req="yes", rci="", ex=""):
    CB.append(dict(field_id=fid, section=sec, table=table, field_name=name, label=label, instruction=instr,
                   type=typ, allowed_values=allowed, required=req, rci_item=rci, example=ex))


S = "studies"
E = "elevation_inputs"
V = "variables"
SECTIONS = {
    "A": "Bibliographic and administration",
    "B": "Study context",
    "C": "Elevation data acquisition",
    "D": "DTM production",
    "E": "Terrain variables and computation",
    "F": "Microform delineation",
    "G": "Accuracy, uncertainty and sensitivity",
    "H": "Reproducibility",
    "I": "Reporting Completeness Index (RCI)",
    "J": "Quality assurance and notes",
}

# A - bibliographic and administration ------------------------------------------------------
f("A01", "A", S, "study_id", "Study ID", "Assign MAP-0001, MAP-0002 ... at inclusion. One ID per study; companion reports share it.", "id", req="yes", ex="MAP-0007")
f("A02", "A", S, "record_ids", "Search record IDs", "Deduplicated library record IDs that report this study; separate with ';'.", "text", ex="R00123; R04411")
f("A03", "A", S, "companion_ids", "Companion reports", "Other records (theses, data papers, reports) describing the same study; ';'-separated record IDs or DOIs.", "text", req="no")
f("A04", "A", S, "citation", "Citation", "Full reference of the primary report (APA style).", "text")
f("A05", "A", S, "doi", "DOI", "DOI of the primary report without the https://doi.org/ prefix; blank if none.", "text", req="no", ex="10.5194/tc-13-237-2019")
f("A06", "A", S, "year", "Year", "Year of the version of record (or of the preprint if no version of record).", "integer", ex="2019")
f("A07", "A", S, "publication_type", "Publication type", "Choose one.", "single",
  "journal article; conference paper; thesis or dissertation; report or grey literature; data paper; preprint; book chapter")
f("A08", "A", S, "venue", "Venue", "Journal, proceedings or publisher name as printed.", "text", ex="The Cryosphere")
f("A09", "A", S, "venue_field", "Venue field", "Primary field of the venue (use the journal's stated scope).", "single",
  "remote sensing or photogrammetry; geomorphology or earth surface; cryosphere or permafrost; hydrology; ecology or biogeosciences; soil science; geography or GIS; multidisciplinary; other")
f("A10", "A", S, "language", "Language", "Language of the full text.", "text", ex="English")
f("A11", "A", S, "full_text_source", "Full-text source", "How the full text was obtained.", "single",
  "open access; institutional subscription; author copy; interlibrary loan; not obtained")
f("A12", "A", S, "coder", "Coder", "Initials of the person who coded (or verified the pre-fill of) this study.", "text")
f("A13", "A", S, "coding_date", "Coding date", "YYYY-MM-DD.", "date")
f("A14", "A", S, "verifier", "Verifier", "Initials of the human who verified every field against the full text.", "text")
f("A15", "A", S, "llm_prefill", "LLM pre-fill", "Record the model name, version and date if an LLM pre-filled fields; else 'none'.", "text", ex="none")

# B - study context ----------------------------------------------------------------------------
f("B01", "B", S, "study_aim", "Study aim", "Paraphrase the aim in 30 words or fewer.", "text")
f("B02", "B", S, "application_domain", "Application domain", "All that apply.", "multi",
  "hydrology or soil moisture; snow; active layer or ground thermal regime; ice-wedge or polygon geomorphology; thermokarst or permafrost degradation; palsa or peat-plateau dynamics; carbon or greenhouse-gas fluxes; vegetation or ecology; landform or geomorphic mapping; hillslope or channel processes; DEM or method evaluation; infrastructure or hazards; other")
f("B03", "B", S, "terrain_role", "Role of terrain variables", "Main role the terrain variables play in the study.", "single",
  "primary object of study; predictor or covariate in a model; stratification or sampling design; process-model input or mesh; validation or reference")
f("B04", "B", S, "region", "Region", "All that apply.", "multi",
  "USA - Alaska; Canada - Yukon; Canada - Northwest Territories; Canada - Nunavut; Canada - Quebec or Nunavik; Canada - Labrador; Canada - other; Greenland; Svalbard; Norway (mainland); Sweden; Finland; Russia - European; Russia - Siberia or Far East; Iceland; circumpolar or multiple")
f("B15", "B", S, "area_rule", "Area rule met", "Which eligibility rule puts the site in scope (protocol section 4).", "single",
  "(a) inside the CAVM extent; (b) tundra or forest-tundra north of 60°N; (c) permafrost landform or tundra in a permafrost zone north of 50°N")
f("B05", "B", S, "site_names", "Site names", "Named sites as reported; ';'-separated.", "text", ex="Utqiagvik BEO; Prudhoe Bay")
f("B06", "B", S, "latitude_dd", "Latitude", "Centroid of the analysed area, decimal degrees (WGS84). Estimate from maps if not stated and note it in J03.", "number", ex="71.28")
f("B07", "B", S, "longitude_dd", "Longitude", "As B06; negative west of Greenwich.", "number", ex="-156.61")
f("B08", "B", S, "extent_km2", "Analysed extent (km²)", "Approximate area over which terrain variables were computed.", "number", req="no")
f("B09", "B", S, "permafrost_zone", "Permafrost zone", "As reported; if not reported, take from Obu et al. (2019) and set B10 accordingly.", "single",
  f"continuous; discontinuous; sporadic; isolated patches; none; {NR}")
f("B10", "B", S, "permafrost_zone_source", "Permafrost zone source", "Where B09 came from.", "single", "reported by authors; Obu et al. 2019 map; not determinable")
f("B11", "B", S, "bioclimate", "Bioclimatic setting", "Choose the best fit.", "single",
  "high Arctic; low Arctic; subarctic or forest-tundra; oroarctic or mountain tundra; boreal permafrost peatland; other")
f("B12", "B", S, "microforms", "Microforms present or studied", "All that apply.", "multi",
  "low-centred polygons; high-centred polygons; flat-centred polygons; ice-wedge troughs; hummocks or earth hummocks; tussocks; palsas or peat plateaus; frost boils or mudboils; water tracks; thermokarst pits or ponds; drained lake basins; strings and flarks; other; none specified")
f("B13", "B", S, "n_elevation_inputs", "Number of elevation inputs", "Rows for this study in elevation_inputs.", "integer")
f("B14", "B", S, "n_terrain_variables", "Number of terrain variables", "Rows for this study in variables.", "integer")

# C - elevation data acquisition (elevation_inputs) ----------------------------------------------
f("C01", "C", E, "study_id", "Study ID", "Link to studies.study_id.", "id")
f("C02", "C", E, "dem_id", "Elevation input ID", "study_id + '-D' + running number.", "id", ex="MAP-0007-D1")
f("C03", "C", E, "source_type", "Source type", "Choose one per elevation input.", "single",
  "ALS lidar; ULS (UAV) lidar; TLS; mobile or backpack lidar; crewed aerial photogrammetry; UAV photogrammetry (SfM); satellite stereo photogrammetry; IfSAR or InSAR; GNSS or total-station survey; other")
f("C04", "C", E, "product_name", "Product name", "Named product or acquisition; 'study-specific' if the authors acquired it.", "text", ex="ArcticDEM v4.1 2 m strips")
f("C05", "C", E, "provider", "Provider", "Who acquired or produced the data.", "single",
  f"national or state agency; research programme; commercial vendor; authors' own acquisition; satellite programme; other; {NR}")
f("C06", "C", E, "sensor", "Sensor or platform", "Instrument and platform as reported.", "text", req="no", ex="Riegl VUX-1UAV on DJI M600")
f("C07", "C", E, "acquisition_date", "Acquisition date", "YYYY-MM-DD, YYYY-MM or YYYY; ';' for several.", "text", rci="R02", ex="2013-08")
f("C08", "C", E, "acquisition_conditions", "Acquisition conditions", "All that apply.", "multi",
  f"snow-free; snow-on; growing season or leaf-on; senescent or leaf-off; frozen ground; {NR}")
f("C09", "C", E, "point_density_ppsm", "Point density (pts/m²)", "As reported (ground or all returns; say which in notes). Leave blank for raster-only products.", "number", req="conditional", rci="R03")
f("C10", "C", E, "point_spacing_m", "Nominal point spacing (m)", "As reported, if density is not given.", "number", req="conditional", rci="R03")
f("C11", "C", E, "gsd_m", "Image GSD (m)", "Ground sampling distance for photogrammetric sources.", "number", req="conditional", rci="R03")
f("C12", "C", E, "georeferencing", "Georeferencing", "How the data were georeferenced.", "single",
  f"direct GNSS/INS; ground control points; RTK or PPK; GCPs plus RTK/PPK; provider-controlled; {NR}")
f("C13", "C", E, "vertical_accuracy_value_m", "Vertical accuracy (m)", "Numeric value as reported, in metres.", "number", req="conditional", rci="R04", ex="0.031")
f("C14", "C", E, "vertical_accuracy_metric", "Vertical accuracy metric", "Statistic behind C13.", "single",
  f"RMSEz; NVA at 95% confidence; VVA 95th percentile; standard deviation; mean absolute error; other; {NR}", rci="R04")
f("C15", "C", E, "vertical_accuracy_basis", "Accuracy basis", "Who assessed it.", "single",
  f"provider report; authors' independent checkpoints; both; {NR}")

# D - DTM production (elevation_inputs) ----------------------------------------------------------
f("D01", "D", E, "surface_type", "Surface type", "Surface the terrain variables were computed on.", "single",
  "DTM (bare earth); DSM; DSM adjusted toward bare earth; TIN; point cloud used directly", rci="R05")
f("D02", "D", E, "dtm_builder", "Who built the surface", "Choose one.", "single",
  f"provider product; authors, from provider-classified points; authors, from raw points with own classification; {NR}")
f("D03", "D", E, "ground_filter", "Ground filter", "Algorithm or software used to classify ground points.", "single",
  f"provider (unspecified); TerraScan; LAStools lasground; PDAL SMRF; PDAL PMF; cloth simulation (CSF); multiscale curvature (MCC); progressive TIN densification; manual editing; other; {NR}; not applicable", rci="R05")
f("D04", "D", E, "ground_filter_params_reported", "Ground-filter parameters reported", "Are the filter's parameters given?", "single", "yes; partly; no; not applicable")
f("D05", "D", E, "gridding_method", "Gridding or interpolation", "Method used to make the raster from points.", "single",
  f"TIN linear; natural neighbour; IDW; kriging; spline; binning - minimum; binning - mean; binning - other; provider (unspecified); other; {NR}; not applicable", rci="R06")
f("D06", "D", E, "native_cell_m", "Native cell size (m)", "Cell size of the elevation product as produced.", "number", rci="R07", ex="0.5")
f("D07", "D", E, "analysis_cell_m", "Analysis cell size (m)", "Cell size on which terrain variables were computed (same as D06 if not resampled). ';' for several.", "text", rci="R07", ex="0.5; 1; 2")
f("D08", "D", E, "resampling_method", "Resampling method", "If D07 differs from D06.", "single",
  f"none; bilinear; cubic; nearest neighbour; aggregate - mean; aggregate - other; re-gridded from points; other; {NR}")
f("D09", "D", E, "hydro_conditioning", "Hydro-conditioning", "Applied to the surface before terrain analysis.", "single",
  f"none; hydro-flattened by provider; depression filling or breaching; stream burning; other; {NR}")
f("D10", "D", E, "gap_filling", "Gap filling", "How voids were filled.", "single", f"none; interpolation; another DEM; {NR}")
f("D11", "D", E, "vertical_datum_reported", "Vertical datum reported", "Is the vertical datum or geoid stated?", "single", "yes; no")
f("D12", "D", E, "data_availability", "Elevation data availability", "Can the elevation data be obtained?", "single",
  f"public archive with persistent ID; public archive without persistent ID; on request; not available; {NR}")
f("D13", "D", E, "data_identifier", "Data identifier", "DOI, URL or archive ID (e.g., InPort, OpenTopography, OSTI).", "text", req="no")
f("D14", "D", E, "notes", "Notes", "Anything that qualifies C and D fields.", "text", req="no")

# E - terrain variables (variables) ---------------------------------------------------------------
f("E01", "E", V, "study_id", "Study ID", "Link to studies.study_id.", "id")
f("E02", "E", V, "var_id", "Variable ID", "study_id + '-V' + running number. One row per terrain variable per elevation input.", "id", ex="MAP-0007-V3")
f("E03", "E", V, "dem_id", "Elevation input ID", "Link to elevation_inputs.dem_id.", "id")
f("E04", "E", V, "variable_family", "Variable family", "Choose one (see protocol Table 2).", "single",
  "slope or gradient; aspect; curvature; relative position; roughness or rugosity; hydrological or compound; solar or insolation; morphometric classification; microform delineation; spectral, texture or variogram; point-cloud geometry; other")
f("E05", "E", V, "variable_name_reported", "Variable name (verbatim)", "Name used by the authors.", "text", ex="topographic position index")
f("E06", "E", V, "curvature_type", "Curvature type", "Only for curvature rows.", "single",
  f"profile; plan; tangential; mean; total or Laplacian; general; other; {NR}; not applicable", req="conditional")
f("E07", "E", V, "algorithm_reported", "Algorithm (verbatim)", "Algorithm, method or formula exactly as stated; 'not stated' if absent.", "text", ex="third-order finite difference (Horn 1981)")
f("E08", "E", V, "algorithm_coded", "Algorithm (coded)", "Map E07 to the closest category.", "single",
  f"Horn 1981 (3FDWRSD); Zevenbergen-Thorne 1987 (2FD); Evans-Young quadratic (3FD); Wood 1996 multiscale quadratic; Florinsky 2009 5x5; Shary 1995; maximum downhill or D8 slope; Gaussian derivative or scale space; polynomial or plane fit to points; flow routing - D8; flow routing - D-infinity; flow routing - multiple flow direction; difference from focal mean (TPI-type); difference from smoothed surface (residual); geomorphons; other; {NR}", rci="R09")
f("E09", "E", V, "algorithm_basis", "Algorithm basis", "How E08 was determined. Only 'named by authors' or 'formula given' earn RCI credit.", "single",
  "named by authors; formula given; inferred from software default; not determinable", rci="R09")
f("E10", "E", V, "software", "Software", "Software or library that computed the variable.", "single",
  f"ArcGIS Desktop; ArcGIS Pro; QGIS (native or GDAL); GDAL (gdaldem); SAGA GIS; GRASS GIS; WhiteboxTools or Whitebox GAT; LandSerf; R - terra or raster; R - spatialEco; R - MultiscaleDTM; R - RSAGA or Rsagacmd; R - other; Python - RichDEM; Python - xarray-spatial; Python - NumPy/SciPy custom; Python - other; MATLAB - TopoToolbox; MATLAB - custom; TauDEM; ENVI; ERDAS IMAGINE; eCognition; LAStools; PDAL; CloudCompare; other; {NR}", rci="R10")
f("E11", "E", V, "software_version", "Software version", f"Version string as reported, else '{NR}'.", "text", rci="R11", ex="SAGA 7.9")
f("E12", "E", V, "tool_function", "Tool or function", "Tool, function or command with options, as reported.", "text", req="no", ex="gdaldem slope -alg ZevenbergenThorne")
f("E13", "E", V, "window_cells", "Window (cells)", "Neighbourhood as reported, e.g., '3x3', 'circle r=5'; ';' for several.", "text", rci="R12", ex="3x3")
f("E14", "E", V, "window_m", "Window or support (m)", "Window width or support in metres; ';' for several.", "text", rci="R12", ex="1.5")
f("E15", "E", V, "window_m_basis", "Window (m) basis", "How E14 was obtained.", "single", "reported; computed from cells x cell size; not determinable")
f("E16", "E", V, "support_type", "Support type", "How scale enters the computation.", "single",
  "native 3x3 kernel; larger moving window; smoothing then kernel; multiscale quadratic fit; coarser resampled grid; object or segment based; point-cloud neighbourhood; other")
f("E17", "E", V, "multiscale", "Multiscale", "Computed at more than one window or resolution?", "single", "yes; no")
f("E18", "E", V, "scales_m", "Scales (m)", "All windows or resolutions used, in metres; ';'-separated.", "text", req="conditional", ex="1; 5; 10; 25")
f("E19", "E", V, "preprocessing", "Pre-processing before the variable", "All that apply.", "multi",
  f"none stated; explicitly none; smoothing - mean; smoothing - Gaussian; smoothing - median; other low-pass filter; resampling; detrending; depression filling or breaching; {NR}", rci="R08")
f("E20", "E", V, "preprocessing_params", "Pre-processing parameters", "Window, sigma or other parameters, with units.", "text", req="conditional", ex="Gaussian sigma = 1 m")
f("E21", "E", V, "units_reported", "Units", "Units of the variable as reported.", "single", f"degrees; percent; m/m; radians; metres; unitless; class; other; {NR}")
f("E22", "E", V, "use_in_study", "Use in the study", "Main use of this variable.", "single",
  "predictor in statistical or ML model; descriptive map or statistic; classification or segmentation input; process-model input; threshold or delineation rule; validation target; other")
f("E23", "E", V, "sensitivity_tested_var", "Sensitivity tested for this variable", "All that apply.", "multi",
  "none; resolution; window or support; algorithm; elevation source; pre-processing; other")
f("E24", "E", V, "scale_rationale", "Scale rationale", "Why this window or resolution was chosen.", "single",
  "none given; cites literature; matched to feature size; optimised against an outcome; multiscale ensemble; data-driven (variogram or spectral); other")
f("E25", "E", V, "evidence_location", "Evidence location", "Page or section, plus a quote of 25 words or fewer supporting E07, E10, E13 or E14.", "text")
f("E26", "E", V, "notes", "Notes", "Anything that qualifies this row.", "text", req="no")

# F - microform delineation (variables, conditional) ---------------------------------------------
f("F01", "F", V, "microform_targets", "Target microforms", "Only for rows with variable_family = microform delineation.", "multi",
  "polygon centres; polygon rims; ice-wedge troughs; hummocks; hollows; tussocks; palsas or peat plateaus; water tracks; thermokarst pits or ponds; other", req="conditional")
f("F02", "F", V, "delineation_method", "Delineation method", "Choose one.", "single",
  "threshold on a terrain variable; watershed or segmentation; object-based image analysis; machine learning (e.g., random forest); deep learning (e.g., CNN or U-Net); geomorphons; morphological operators; graph-based; manual digitising; other", req="conditional")
f("F03", "F", V, "delineation_inputs", "Delineation inputs", "Elevation-derived layers and other inputs used; ';'-separated.", "text", req="conditional", ex="DTM; TPI 5 m; NDVI")
f("F04", "F", V, "delineation_validation", "Delineation validation", "Reference used to check the delineation.", "single",
  "none; manual reference digitising; field mapping; other", req="conditional")
f("F05", "F", V, "delineation_accuracy", "Delineation accuracy", "Metric and value as reported.", "text", req="conditional", ex="F1 = 0.87")

# G - accuracy, uncertainty and sensitivity (studies) ---------------------------------------------
f("G01", "G", S, "dem_accuracy_assessed", "Elevation accuracy assessed", "Highest level of elevation-accuracy evidence in the study.", "single",
  "authors' independent checkpoints; provider report cited; both; none reported")
f("G02", "G", S, "derivative_accuracy_assessed", "Terrain-variable accuracy assessed", "All that apply.", "multi",
  "none; field-measured (e.g., inclinometer or survey); higher-resolution reference surface; synthetic or analytical truth; comparison between products; other")
f("G03", "G", S, "uncertainty_propagation", "Uncertainty propagated to variables", "Choose one.", "single",
  "none; analytical; Monte Carlo or stochastic simulation; error surfaces or sensitivity maps; other")
f("G04", "G", S, "vegetation_bias", "Vegetation bias", "How vegetation effects on the ground surface were handled.", "single",
  "not addressed; discussed only; quantified; corrected")
f("G05", "G", S, "sensitivity_tested", "Sensitivity tested (study)", "All computation choices whose effect on results was tested.", "multi",
  "none; resolution; window or support; algorithm; elevation source; ground filter or gridding; pre-processing; other")
f("G06", "G", S, "sensitivity_outcome", "Sensitivity outcome", "Authors' conclusion about the tested choices.", "single",
  "not tested; material effect reported; no material effect; mixed or unclear")
f("G07", "G", S, "sensitivity_notes", "Sensitivity notes", "50 words or fewer: what changed, by how much.", "text", req="conditional")

# H - reproducibility (studies) ---------------------------------------------------------------------
f("H01", "H", S, "code_availability", "Code availability", "Choose one.", "single",
  f"public repository with persistent ID; public repository without persistent ID; on request; not available; {NR}", rci="R13")
f("H02", "H", S, "code_url", "Code URL or DOI", "", "url", req="conditional")
f("H03", "H", S, "derived_data_availability", "Derived data availability", "DTMs or terrain-variable rasters produced by the study.", "single",
  f"public with persistent ID; public without persistent ID; on request; not available; {NR}", rci="R13")
f("H04", "H", S, "derived_data_url", "Derived data URL or DOI", "", "url", req="conditional")
f("H05", "H", S, "source_data_identified", "Source data identified", "Could a reader find the exact elevation data used?", "single",
  "fully (dataset ID or DOI); partially (name only); not identified", rci="R01")
f("H06", "H", S, "methods_detail_location", "Where methods are described", "Choose one.", "single", "main text; supplement; earlier paper cited; mixed")

# I - RCI (studies) -----------------------------------------------------------------------------------
RCI = [
    ("R01", "rci_r01_source", "Elevation source or product identified", "Data"),
    ("R02", "rci_r02_date", "Acquisition date or year", "Data"),
    ("R03", "rci_r03_density", "Point density, spacing or GSD", "Data"),
    ("R04", "rci_r04_accuracy", "Vertical accuracy of elevation data (value and metric)", "Data"),
    ("R05", "rci_r05_surface", "Surface type and ground-classification method", "DTM"),
    ("R06", "rci_r06_gridding", "Gridding or interpolation method", "DTM"),
    ("R07", "rci_r07_cell", "Cell size used for terrain variables", "DTM"),
    ("R08", "rci_r08_preproc", "Pre-processing before derivatives stated (including explicit 'none')", "DTM"),
    ("R09", "rci_r09_algorithm", "Derivative algorithm named or given as a formula", "Derivatives"),
    ("R10", "rci_r10_software", "Software named", "Derivatives"),
    ("R11", "rci_r11_version", "Software version reported", "Derivatives"),
    ("R12", "rci_r12_window", "Window or support reported (cells or metres)", "Derivatives"),
    ("R13", "rci_r13_open", "Code or derived data openly available", "Openness"),
]
RCI_RULE = {}
for rid in ("R01", "R02", "R03", "R04", "R05", "R06", "R07"):
    RCI_RULE[rid] = ("Judged per elevation input. Score = share of applicable inputs for which every part of the item is reported "
                     "(main text, supplement, companion record, or a specific cited source documenting the same data or processing).")
RCI_RULE["R03"] += " NA for a named public product with a persistent identifier (the provider documents density)."
RCI_RULE["R05"] += " NA for a provider DTM with a persistent identifier (the authors did no ground classification)."
RCI_RULE["R06"] += " NA for a provider DTM with a persistent identifier (the authors did no gridding)."
for rid in ("R08", "R09", "R10", "R11", "R12"):
    RCI_RULE[rid] = ("Judged per terrain variable. Score = share of variables for which the item is reported; for R09 only "
                     "'named by authors' or 'formula given' earns credit, not an algorithm inferred from software defaults.")
RCI_RULE["R13"] = "Judged once per study: 1 if code or derived data are publicly available (any public link), otherwise 0."
for i, (rid, name, lab, dom) in enumerate(RCI, 1):
    f(f"I{i:02d}", "I", S, name, f"{rid} {lab}",
      f"Domain: {dom}. {RCI_RULE[rid]}",
      "number", "0 to 1; NA", rci=rid)
f("I14", "I", S, "rci_total", "RCI (total)", "Mean of applicable R01-R13 item scores (computed, not typed).", "number", req="yes")
f("I15", "I", S, "rci_data", "RCI - Data domain", "Mean of applicable R01-R04.", "number")
f("I16", "I", S, "rci_dtm", "RCI - DTM domain", "Mean of applicable R05-R08.", "number")
f("I17", "I", S, "rci_derivatives", "RCI - Derivatives domain", "Mean of applicable R09-R12.", "number")

# J - QA ---------------------------------------------------------------------------------------------
f("J01", "J", S, "uncertain_fields", "Uncertain fields", "Field names the coder was unsure about; ';'-separated.", "text", req="no")
f("J02", "J", S, "author_query", "Author query", "Question to send the authors; only for studies that tested sensitivity to computation choices or whose data are benchmark candidates (protocol 7.4).", "text", req="no")
f("J03", "J", S, "notes", "Notes", "Free text.", "text", req="no")

cols = ["field_id", "section", "section_name", "table", "field_name", "label", "instruction", "type", "allowed_values", "required", "rci_item", "example"]
_count = {}
for r in CB:  # sequential IDs within each section, in definition order
    _count[r["section"]] = _count.get(r["section"], 0) + 1
    r["field_id"] = f"{r['section']}{_count[r['section']]:02d}"
with open(f"{T}/codebook_v0.1.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=cols)
    w.writeheader()
    for r in CB:
        r = dict(r)
        r["section_name"] = SECTIONS[r["section"]]
        w.writerow(r)

# Extraction templates (header only, column order = codebook order) -------------------------------
for table, fname in ((S, "extract_studies_v0.1.csv"), (E, "extract_elevation_inputs_v0.1.csv"), (V, "extract_variables_v0.1.csv")):
    names = []
    for r in CB:
        if r["table"] == table and r["field_name"] not in names:
            names.append(r["field_name"])
    with open(f"{T}/{fname}", "w", newline="", encoding="utf-8") as fh:
        csv.writer(fh).writerow(names)

# Screening form -------------------------------------------------------------------------------
SCREEN = ["record_id", "sources", "first_author", "year", "title", "doi",
          "ta_human_decision", "ta_human_code", "ta_human_screener", "ta_human_date",
          "ta_llm_decision", "ta_llm_code", "ta_llm_criteria", "ta_llm_rationale", "ta_llm_model", "ta_llm_prompt_version",
          "ta_route", "ta_final", "ta_conflict", "ta_resolution_note",
          "ft_retrieved", "ft_source", "ft_human_decision", "ft_human_code",
          "ft_second_decision", "ft_second_code", "ft_second_screener", "ft_final", "ft_final_code",
          "map_study_id", "calibration_sample", "notes"]
with open(f"{T}/screening_form_v0.1.csv", "w", newline="", encoding="utf-8") as fh:
    csv.writer(fh).writerow(SCREEN)

EXCL = [
    ("E1", "Not primary research, a methods paper or a data paper (review, editorial, commentary), or only an abstract is available. Reviews are kept for citation chasing."),
    ("E2", "Area out of scope: meets none of (a) inside the CAVM extent, (b) tundra or forest-tundra north of 60°N, (c) tundra or a permafrost landform in a permafrost zone (Obu et al. 2019) north of 50°N. Includes sites south of 50°N, Antarctica and planetary analogues."),
    ("E3", "Surface is not land: glacier, ice sheet, sea ice, snow surface only, or seabed."),
    ("E4", "No elevation data used (e.g., microforms mapped from imagery alone)."),
    ("E5", "All elevation data coarser than 5 m native resolution, or point clouds with nominal spacing above 5 m."),
    ("E6", "No terrain variable computed and no microform delineated from the 5 m-or-finer data (e.g., raw elevation or elevation change only)."),
    ("E7", "Secondary report of an included study (linked as a companion)."),
    ("E8", "Full text unobtainable after the retrieval procedure."),
    ("E9", "Full text in a language that could not be translated."),
]
with open(f"{T}/exclusion_codes_v0.1.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["code", "definition", "applies_at"])
    for c, d in EXCL:
        w.writerow([c, d, "title/abstract and full text" if c not in ("E7", "E8", "E9") else "full text"])

# Formal search log with planned searches --------------------------------------------------------
LOG = ["search_id", "stage", "status", "date", "source", "platform", "coverage", "fields", "string_version", "exact_string_ref",
       "limits", "results_n", "exported_n", "export_format", "export_file", "seeds_retrieved", "notes", "searcher"]
planned = [
    ("S1-OA-01", "S1", "OpenAlex", "OpenAlex API (openalex_harvest.py)", "title_and_abstract", "Appendix A.2 OpenAlex"),
    ("S1-WOS-01", "S1", "Web of Science Core Collection", "Clarivate", "TS (title, abstract, author keywords, Keywords Plus)", "Appendix A.2 WoS"),
    ("S1-SCO-01", "S1", "Scopus", "Elsevier", "TITLE-ABS-KEY", "Appendix A.2 Scopus"),
    ("S1-GEO-01", "S1", "GeoRef", "EBSCOhost or ProQuest", "TI, AB, SU (or noft)", "Appendix A.2 GeoRef"),
    ("S2-WOS-01", "S2", "Web of Science Core Collection", "Clarivate", "TS", "final strings v1.0"),
    ("S2-SCO-01", "S2", "Scopus", "Elsevier", "TITLE-ABS-KEY", "final strings v1.0"),
    ("S2-GEO-01", "S2", "GeoRef", "EBSCOhost or ProQuest", "TI, AB, SU (or noft)", "final strings v1.0"),
    ("S2-OA-01", "S2", "OpenAlex", "OpenAlex API", "title_and_abstract", "final strings v1.0"),
    ("S2-PQDT-01", "S2", "ProQuest Dissertations & Theses Global", "ProQuest", "noft", "final strings v1.0"),
    ("S2-OSTI-01", "S2", "OSTI.gov", "US DOE OSTI", "title, abstract", "Appendix A.2 OSTI"),
    ("S2-GS-01", "S2", "Google Scholar", "Publish or Perish", "default (first 300 per query)", "Appendix A.2 Google Scholar (5 queries)"),
    ("S2-CIT-01", "S2", "Citation chasing (backward and forward)", "OpenAlex / citationchaser", "references and citing works of included studies", "included study list"),
    ("S2-MAT-01", "S2", "Scoping Evidence Matrix v0.3", "local file", "202 records", "n/a"),
    ("S2-EXP-01", "S2", "Expert suggestions", "email", "n/a", "n/a"),
]
with open(f"{T}/search_log_v0.1.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=LOG)
    w.writeheader()
    for sid, st, src, plat, fields, ref in planned:
        w.writerow(dict(search_id=sid, stage=st, status="planned", source=src, platform=plat, fields=fields,
                        string_version=sb.VERSION if st == "S1" else "", exact_string_ref=ref, limits="none"))

# Seed set ---------------------------------------------------------------------------------------
M = {r["record_id"]: r for r in csv.DictReader(open(MATRIX, encoding="utf-8-sig"))}
CORE = [  # (record_id, title, confidence, basis)
    ("EM-047", "Extrapolating active layer thickness measurements across Arctic polygonal terrain using LiDAR and NDVI data sets", "high", "0.25 m LiDAR slope and curvature, Utqiagvik (methods checked v0.3)"),
    ("EM-057", "Climate sensitivity of High Arctic permafrost terrain demonstrated by widespread ice-wedge thermokarst on Banks Island", "medium", "2 m ArcticDEM used to characterise degraded polygon microtopography"),
    ("EM-060", "Brief communication: Rapid machine-learning-based extraction and measurement of ice wedge polygons in high-resolution digital elevation models", "high", "Polygon delineation from 0.25-1 m LiDAR DEMs (content checked)"),
    ("EM-062", "High-resolution mapping of spatial heterogeneity in ice wedge polygon geomorphology near Prudhoe Bay, Alaska", "high", "Polygon delineation and relative centre elevation from sub-metre LiDAR"),
    ("EM-067", "Hillslope-channel transitions and the role of water tracks in a changing permafrost landscape", "high", "Slope and curvature from 2 m ArcticDEM with explicit scale choices"),
    ("EM-069", "High-resolution maps of near-surface permafrost for three watersheds on the Seward Peninsula, Alaska derived from machine learning", "high", "GDAL slope/aspect and 45 m curvature window on 3 m LiDAR DTM"),
    ("EM-071", "Arctic ice-wedge landscape mapping by CNN using a fusion of Radarsat Constellation Mission and ArcticDEM", "medium", "ArcticDEM-derived inputs for ice-wedge landscape mapping"),
    ("EM-073", "Fine-scale landscape characteristics, vegetation composition, and snowmelt timing control phenological heterogeneity across low-Arctic tundra landscapes in Western Alaska", "high", "Slope, aspect, TPI, TWI from 1 m LiDAR (SAGA/QGIS)"),
    ("EM-075", "Scaling Arctic landscape and permafrost features improves active layer depth modeling", "medium", "Multiscale terrain predictors from sub-metre layers"),
    ("EM-077", "Evaluation of the Geomorphon approach for extracting troughs in polygonal patterned ground across different permafrost environments", "high", "Geomorphon trough extraction across 0.25-3 m DEMs (content checked)"),
    ("EM-078", "Remote sensing-based framework for detecting and interpreting permafrost terrain hydrologic connectivity", "high", "Slope, curvature, hydrologic metrics from 0.5 m LiDAR"),
    ("EM-129", "Identifying multiscale zonation and assessing the relative importance of polygon geomorphology on carbon fluxes in an Arctic tundra ecosystem", "medium", "LiDAR-based polygon geomorphology zonation (title-level)"),
    ("EM-133", "Mapping Arctic plant functional type distributions in the Barrow Environmental Observatory using WorldView-2 and LiDAR datasets", "medium", "LiDAR terrain predictors of vegetation (title-level)"),
    ("EM-145", "Modelling soil moisture in a high-latitude landscape using LiDAR and soil data", "medium", "LiDAR terrain predictors of soil moisture, oroarctic Finland (title-level)"),
    ("EM-148", "Assessment of LiDAR and spectral techniques for high-resolution mapping of sporadic permafrost on the Yukon-Kuskokwim Delta, Alaska", "medium", "LiDAR-derived terrain for peat-plateau permafrost mapping"),
    ("EM-152", "Assessment of the ice wedge polygon current state by means of UAV imagery analysis (Samoylov Island, the Lena Delta)", "medium", "UAV SfM DEM of polygons (title-level)"),
    ("EM-169", "Scale-dependency of Arctic ecosystem properties revealed by UAV", "medium", "UAV products, incl. terrain, at multiple resolutions (title-level)"),
    ("EM-175", "A quantitative graph-based approach to monitoring ice-wedge trough dynamics in polygonal permafrost landscapes", "medium", "Trough network extraction from high-resolution DTMs"),
    ("EM-176", "Topographic wetness index as a proxy for soil moisture: the importance of flow-routing algorithm and grid resolution", "high", "TWI algorithm x resolution on LiDAR DEMs, tundra"),
    ("EM-179", "Error characteristics of pan-Arctic digital elevation models and elevation derivatives in northern Sweden", "medium", "ArcticDEM and other DEM derivatives vs reference (title-level)"),
    ("EM-198", "Heterogeneity in ice-wedge permafrost degradation revealed across spatial scales", "medium", "Airborne LiDAR and drone data, Prudhoe Bay (abstract-level)"),
]
BOUNDARY = [
    ("EM-051", "Modeling the spatiotemporal variability in subsurface thermal regimes across a low-relief polygonal tundra landscape", "LiDAR DEM used as model mesh; derivative computation to confirm"),
    ("EM-054", "Mapping snow depth within a tundra ecosystem using multiscale observations and Bayesian methods", "Topographic predictors of snow; variables to confirm"),
    ("EM-055", "Microtopographic control on the ground thermal regime in ice wedge polygons", "High-resolution topography with modelling; variables to confirm"),
    ("EM-072", "Multitemporal UAV lidar detects seasonal heave and subsidence on palsas", "Repeat UAV-lidar DTMs; terrain variables beyond elevation change to confirm"),
    ("EM-119", "Quantifying and relating land-surface and subsurface variability in permafrost environments using LiDAR and surface geophysical datasets", "LiDAR microtopographic zonation; no DOI in matrix"),
    ("EM-120", "Quantifying landscape change in an arctic coastal lowland using repeat airborne LiDAR", "Change detection; terrain variables to confirm"),
    ("EM-149", "", "J. Surv. Eng. 2018 Arctic DEM accuracy in sloped and vegetated terrain; title and authors to confirm"),
    ("EM-186", "Soil moisture variations from boreal forests to the tundra", "Terrain predictors to confirm"),
    ("EM-189", "Permafrost degradation at two monitored palsa mires in north-west Finland", "UAS and airborne LiDAR; terrain variables to confirm"),
]
NEG = [
    ("EM-066", "Topographic asymmetry across the Arctic", "E5", "32 m ArcticDEM only"),
    ("EM-011", "Accuracy of SPOT digital elevation model and derivatives: Utility for Alaska's North Slope", "E5", "SPOT photogrammetric DEM; native resolution expected coarser than 5 m (confirm)"),
    ("EM-076", "HuHoLa: A novel Hummock-Hollow-Lawn mire microtopography modelling approach", "E2", "Boreal mire without permafrost or tundra focus"),
    ("EM-128", "Mapping snow depth from manned aircraft on landscape scales at centimeter resolution using structure-from-motion photogrammetry", "E6", "Snow depth by DEM differencing; no terrain variable"),
    ("EM-117", "Subpixel heterogeneity of ice-wedge polygonal tundra: a multi-scale analysis of land cover and evapotranspiration in the Lena River Delta, Siberia", "E4", "Imagery only"),
]
rng = random.Random(20261003)
val = set(rng.sample([c[0] for c in CORE], 7))
seed_cols = ["seed_id", "record_id", "year", "first_author", "title", "doi", "seed_role", "split", "expected_decision",
             "expected_code", "confidence", "basis"]
rows = []
n = 0


def first_author(cit):
    a = cit.split(",")[0].strip()
    return "" if a.startswith("[") else a


for rid, title, conf, basis in CORE:
    n += 1
    m = M[rid]
    rows.append(dict(seed_id=f"SEED-{n:02d}", record_id=rid, year=m["year"], first_author=first_author(m["citation"]), title=title,
                     doi=m["doi"], seed_role="core (recall test)", split="validation" if rid in val else "development",
                     expected_decision="include", expected_code="", confidence=conf, basis=basis))
for rid, title, basis in BOUNDARY:
    n += 1
    m = M[rid]
    rows.append(dict(seed_id=f"SEED-{n:02d}", record_id=rid, year=m["year"], first_author=first_author(m["citation"]), title=title,
                     doi=m["doi"], seed_role="boundary (secondary recall; screening calibration)", split="calibration",
                     expected_decision="unsure", expected_code="", confidence="low", basis=basis))
for rid, title, code, basis in NEG:
    n += 1
    m = M[rid]
    rows.append(dict(seed_id=f"SEED-{n:02d}", record_id=rid, year=m["year"], first_author=first_author(m["citation"]), title=title,
                     doi=m["doi"], seed_role="expected exclusion (screening calibration)", split="calibration",
                     expected_decision="exclude", expected_code=code, confidence="medium", basis=basis))
with open(f"{T}/seed_set_v0.1.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=seed_cols)
    w.writeheader()
    w.writerows(rows)

print("codebook fields:", len(CB))
for table in (S, E, V):
    print(" ", table, sum(1 for r in CB if r["table"] == table))
print("validation seeds:", sorted(val))
print("seed rows:", len(rows))
