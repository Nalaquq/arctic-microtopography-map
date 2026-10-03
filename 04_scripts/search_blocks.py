# -*- coding: utf-8 -*-
"""Search concept blocks v0.1 for the Arctic microtopography systematic map.

Single source of truth for every platform string. build_templates.py renders them into
search_strings_v0.1.md and the protocol's Appendix A; openalex_harvest.py imports the same lists.
"""

VERSION = "v0.1"

# Block A - Arctic / subarctic / permafrost context (population)
A = [
    "arctic", "subarctic", '"sub-arctic"', "oroarctic", '"oro-arctic"', '"high latitude*"', '"high-latitude*"',
    "tundra", "permafrost", "periglacial", '"ice wedge*"', '"ice-wedge*"', '"polygonal ground"',
    '"patterned ground"', '"polygonal tundra"', '"polygonal terrain"', "palsa*", '"peat plateau*"',
    "thermokarst", "pingo*", '"frost boil*"', "mudboil*", '"earth hummock*"',
    "alaska*", '"North Slope"', "yukon", '"Northwest Territories"', "nunavut", "nunavik", "labrador",
    "greenland*", "svalbard", "spitsbergen", "siberia*", "yakutia", "yamal", "taymyr", "chukotka",
    '"Lena Delta"', '"Mackenzie Delta"', "lapland", "abisko", "kilpisj*", "utqiagvik",
    '"Barrow Peninsula"', '"Barrow Environmental Observatory"', '"Prudhoe Bay"', '"Seward Peninsula"',
    "toolik", '"Trail Valley"',
]

# Block B - elevation data (high-resolution sources and generic DEM terms)
B_HR = [  # terms that by themselves imply high-resolution elevation data
    "lidar", '"light detection and ranging"', '"laser scan*"', '"laser altimet*"', '"airborne laser"',
    '"terrestrial laser"', '"point cloud*"', "ALS", "TLS", "ULS", "photogrammetr*",
    '"structure from motion"', '"structure-from-motion"', "SfM", "UAV", "UAVs", "UAS", "drone*",
    '"unmanned aerial"', '"uncrewed aerial"', '"remotely piloted"', "ArcticDEM", '"Arctic DEM"', "IfSAR",
    '"high-resolution topograph*"', '"high resolution topograph*"',
]
B_GENERIC = [
    '"digital elevation model*"', '"digital terrain model*"', '"digital surface model*"', '"elevation model*"',
    '"terrain model*"', '"elevation data"', "DEM", "DEMs", "DTM", "DTMs", "DSM", "DSMs", '"topographic data"',
    '"topographic survey*"',
]
B = B_HR + B_GENERIC

# Block C - terrain variables and microtopography (concept)
C_MICRO = [  # microtopography, microform and feature vocabulary
    "microtopograph*", '"micro-topograph*"', "microrelief", '"micro-relief"', "microform*", '"micro-form*"',
    '"fine-scale topograph*"', '"fine scale topograph*"', "mesotopograph*", "hummock*", "hollow*", "trough*",
    '"polygon rim*"', '"polygon cent*"', '"low-cent*"', '"high-cent*"', '"flat-cent*"', '"water track*"',
    '"ice-wedge polygon*"', '"ice wedge polygon*"', "geomorphon*", '"landform classif*"', '"landform mapping"',
]
C_GENERIC = [  # terrain-variable vocabulary
    '"terrain attribute*"', '"terrain variable*"', '"terrain parameter*"', '"terrain derivative*"',
    '"terrain feature*"', '"terrain analys*"', '"terrain index"', '"terrain indices"', '"terrain metric*"',
    '"topographic attribute*"', '"topographic variable*"', '"topographic index"', '"topographic indices"',
    '"topographic metric*"', '"topographic position"', '"topographic heterogeneity"', '"land surface parameter*"',
    '"land-surface parameter*"', '"land surface variable*"', '"land-surface variable*"', '"elevation derivative*"',
    '"DEM derivative*"', '"topographic derivative*"', "geomorphometr*", "morphometr*", "slope*", "hillslope*",
    '"topographic gradient*"', '"terrain gradient*"', '"surface gradient*"', "curvature*", "roughness",
    "rugosity", "ruggedness", '"relative elevation"', '"relative height"', '"local relief"', '"residual relief"',
    '"wetness index"', "TWI", '"flow accumulation"', '"contributing area"', '"depth-to-water"',
    '"depth to water"', '"height above"', "TPI",
]
C = C_MICRO + C_GENERIC

BLOCKS = {"A": A, "B": B, "C": C}

# Block D - benchmark vocabulary, used only for the Stage S6 novelty search (B_hr AND C_generic AND D,
# with no area block), which checks gate criterion G4 against benchmarks the map itself would exclude.
D = [
    "benchmark*", "synthetic", "simulat*", '"virtual laser"', '"laser scanning simulat*"', '"ground truth"',
    '"known truth"', "analytic*", "intercompar*", '"error propagation"', '"error budget"',
]

# Explicit variants used by openalex_harvest.py where a wildcard sits inside a quoted phrase and
# stemming cannot recover the word (OpenAlex does not document phrase wildcards).
OA_EXPAND = {
    '"micro-topograph*"': ['"micro-topography"', '"micro-topographic"', '"micro-topographical"'],
    '"fine-scale topograph*"': ['"fine-scale topography"', '"fine-scale topographic"'],
    '"fine scale topograph*"': ['"fine scale topography"', '"fine scale topographic"'],
    '"high-resolution topograph*"': ['"high-resolution topography"', '"high-resolution topographic"'],
    '"high resolution topograph*"': ['"high resolution topography"', '"high resolution topographic"'],
    '"polygon cent*"': ['"polygon center"', '"polygon centers"', '"polygon centre"', '"polygon centres"'],
    '"low-cent*"': ['"low-centered"', '"low-centred"', '"low-center"', '"low-centre"'],
    '"high-cent*"': ['"high-centered"', '"high-centred"', '"high-center"', '"high-centre"'],
    '"flat-cent*"': ['"flat-centered"', '"flat-centred"', '"flat-center"', '"flat-centre"'],
    '"landform classif*"': ['"landform classification"', '"landform classifications"', '"landform classified"'],
    '"terrain analys*"': ['"terrain analysis"', '"terrain analyses"'],
    '"laser altimet*"': ['"laser altimetry"', '"laser altimeter"', '"laser altimeters"'],
    '"laser scan*"': ['"laser scan"', '"laser scanning"', '"laser scanner"', '"laser scanners"'],
    '"laser scanning simulat*"': ['"laser scanning simulation"', '"laser scanning simulator"'],
}


def ors(terms):
    return " OR ".join(terms)


def wos():
    return "\n".join([f"#1  TS=({ors(A)})", f"#2  TS=({ors(B)})", f"#3  TS=({ors(C)})", "#4  #1 AND #2 AND #3"])


def scopus():
    return (f"TITLE-ABS-KEY({ors(A)})\nAND TITLE-ABS-KEY({ors(B)})\nAND TITLE-ABS-KEY({ors(C)})")


def ebsco():
    out = []
    for i, blk in enumerate((A, B, C)):
        s = ors(blk)
        out.append(("" if i == 0 else "AND ") + f"(TI ({s}) OR AB ({s}) OR SU ({s}))")
    return "\n".join(out)


def proquest():
    return f"noft({ors(A)})\nAND noft({ors(B)})\nAND noft({ors(C)})"


def openalex():
    return ("filter=title_and_abstract.search:(A),title_and_abstract.search:(B),title_and_abstract.search:(C)\n"
            "(blocks as listed in A.1; openalex_harvest.py splits the longest block into sub-queries to stay under\n"
            " the ~4,000-character URL limit and unions the results by OpenAlex ID)")


GOOGLE_SCHOLAR = [
    'tundra lidar microtopography slope OR curvature OR "relative elevation"',
    '"ice-wedge polygon" lidar OR "digital elevation model" troughs',
    'palsa OR "peat plateau" lidar OR UAV "digital elevation model" microtopography',
    'arctic tundra lidar "topographic wetness index" OR "terrain attributes"',
    'permafrost "terrain attributes" OR "terrain variables" lidar OR ArcticDEM',
]

OSTI = ('(microtopography OR "terrain attributes" OR "ice wedge polygon*" OR "polygonal tundra") AND '
        '(lidar OR "digital elevation model" OR DEM) AND (arctic OR tundra OR permafrost)')


def novelty():
    return (f"B_hr AND C_generic AND D   (no area block; run at Stage S6)\n\nD = {ors(D)}")


def two_arm():
    return (f"Arm 1:  A AND B AND C_micro\nArm 2:  A AND B_hr AND C_generic\n\n"
            f"C_micro   = {ors(C_MICRO)}\n\nC_generic = {ors(C_GENERIC)}\n\nB_hr      = {ors(B_HR)}")


if __name__ == "__main__":
    for k, v in BLOCKS.items():
        print(k, len(v), "terms,", len(ors(v)), "chars")
    print(len(scopus()), "chars Scopus")
