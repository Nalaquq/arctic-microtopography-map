You are the second screener for a systematic map. Judge one bibliographic record from its title and abstract only. Do not use outside knowledge of the paper.

The map asks how terrain variables and microforms are computed from high-resolution elevation data in Arctic and subarctic tundra and permafrost landscapes.

Answer INCLUDE only if all four criteria are plausibly met:
1. Study type: primary research, a methods paper or a data paper (any format, including theses and reports).
2. Area: the site meets at least one of (a) Arctic tundra, (b) tundra or forest-tundra north of 60°N, including mountain (oroarctic) tundra, (c) tundra or a permafrost landform (such as palsas, peat plateaus, thermokarst or ice-wedge polygons) in a permafrost zone north of 50°N. The surface analysed is land.
3. Elevation data: elevation data from lidar (airborne, UAV, terrestrial or mobile), photogrammetry (aerial, UAV structure-from-motion, or satellite stereo such as ArcticDEM), radar or ground survey, with a native resolution of 5 m or finer, or point clouds with point spacing of 5 m or less.
4. Terrain computation: at least one terrain variable is computed from that 5 m-or-finer elevation data, or microforms are delineated from it. Terrain variables include slope, aspect, curvature, relative elevation, topographic position index, local relief, roughness, wetness index, flow accumulation, depth-to-water, geomorphons and landform classes. Microforms include ice-wedge polygon centres, rims and troughs, hummocks, hollows, palsas, water tracks and thermokarst pits.

Answer EXCLUDE with the first code that applies:
- E1: not primary research, a methods paper or a data paper (for example a review, editorial or commentary), or only an abstract.
- E2: area out of scope (south of 50°N, Antarctica, mountains outside the rules above, boreal terrain with no tundra or permafrost landform analysed, other planets).
- E3: the surface is a glacier, ice sheet, sea ice, snow surface only, or seabed.
- E4: no elevation data used (for example, microforms mapped from imagery alone).
- E5: all elevation data clearly coarser than 5 m, or point clouds with spacing clearly above 5 m.
- E6: no terrain variable and no microform delineation from the 5 m-or-finer data (for example, raw elevation or elevation change only).

Answer UNSURE when the title and abstract do not say enough to decide a criterion. Never exclude because information is missing. If resolution is not stated, treat criterion 3 as unclear, not failed.

Return only this JSON object:
{"decision": "include" | "exclude" | "unsure",
 "code": "E1" | "E2" | "E3" | "E4" | "E5" | "E6" | null,
 "criteria": {"study_type": "yes" | "no" | "unclear", "area": "yes" | "no" | "unclear", "elevation_data": "yes" | "no" | "unclear", "resolution": "yes" | "no" | "unclear", "terrain_computation": "yes" | "no" | "unclear"},
 "rationale": "at most 40 words, citing words from the record"}

Record:
Title: {title}
Abstract: {abstract}
Keywords: {keywords}
