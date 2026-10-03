# Search strings v0.1 – Arctic microtopography systematic map

Development version for Stage S1 testing (3 October 2026). Final strings become v1.0 at registration. Generated from search_blocks.py, which the scripts also use, so every platform string comes from one source.

## A.1 Concept blocks (v0.1)

Each block is one OR-group; the blocks are combined with AND. No date, language or document-type limits.

**Block A – Arctic, subarctic and permafrost context** (50 terms)

```
arctic OR subarctic OR "sub-arctic" OR oroarctic OR "oro-arctic" OR "high latitude*" OR "high-latitude*" OR tundra OR permafrost OR periglacial OR "ice wedge*" OR "ice-wedge*" OR "polygonal ground" OR "patterned ground" OR "polygonal tundra" OR "polygonal terrain" OR palsa* OR "peat plateau*" OR thermokarst OR pingo* OR "frost boil*" OR mudboil* OR "earth hummock*" OR alaska* OR "North Slope" OR yukon OR "Northwest Territories" OR nunavut OR nunavik OR labrador OR greenland* OR svalbard OR spitsbergen OR siberia* OR yakutia OR yamal OR taymyr OR chukotka OR "Lena Delta" OR "Mackenzie Delta" OR lapland OR abisko OR kilpisj* OR utqiagvik OR "Barrow Peninsula" OR "Barrow Environmental Observatory" OR "Prudhoe Bay" OR "Seward Peninsula" OR toolik OR "Trail Valley"
```

**Block B – Elevation data** (40 terms; the first 26 are the high-resolution subset B_hr)

```
lidar OR "light detection and ranging" OR "laser scan*" OR "laser altimet*" OR "airborne laser" OR "terrestrial laser" OR "point cloud*" OR ALS OR TLS OR ULS OR photogrammetr* OR "structure from motion" OR "structure-from-motion" OR SfM OR UAV OR UAVs OR UAS OR drone* OR "unmanned aerial" OR "uncrewed aerial" OR "remotely piloted" OR ArcticDEM OR "Arctic DEM" OR IfSAR OR "high-resolution topograph*" OR "high resolution topograph*" OR "digital elevation model*" OR "digital terrain model*" OR "digital surface model*" OR "elevation model*" OR "terrain model*" OR "elevation data" OR DEM OR DEMs OR DTM OR DTMs OR DSM OR DSMs OR "topographic data" OR "topographic survey*"
```

**Block C – Terrain variables and microtopography** (69 terms; the first 23 are the microform subset C_micro)

```
microtopograph* OR "micro-topograph*" OR microrelief OR "micro-relief" OR microform* OR "micro-form*" OR "fine-scale topograph*" OR "fine scale topograph*" OR mesotopograph* OR hummock* OR hollow* OR trough* OR "polygon rim*" OR "polygon cent*" OR "low-cent*" OR "high-cent*" OR "flat-cent*" OR "water track*" OR "ice-wedge polygon*" OR "ice wedge polygon*" OR geomorphon* OR "landform classif*" OR "landform mapping" OR "terrain attribute*" OR "terrain variable*" OR "terrain parameter*" OR "terrain derivative*" OR "terrain feature*" OR "terrain analys*" OR "terrain index" OR "terrain indices" OR "terrain metric*" OR "topographic attribute*" OR "topographic variable*" OR "topographic index" OR "topographic indices" OR "topographic metric*" OR "topographic position" OR "topographic heterogeneity" OR "land surface parameter*" OR "land-surface parameter*" OR "land surface variable*" OR "land-surface variable*" OR "elevation derivative*" OR "DEM derivative*" OR "topographic derivative*" OR geomorphometr* OR morphometr* OR slope* OR hillslope* OR "topographic gradient*" OR "terrain gradient*" OR "surface gradient*" OR curvature* OR roughness OR rugosity OR ruggedness OR "relative elevation" OR "relative height" OR "local relief" OR "residual relief" OR "wetness index" OR TWI OR "flow accumulation" OR "contributing area" OR "depth-to-water" OR "depth to water" OR "height above" OR TPI
```

## A.2 Platform syntax

### Web of Science Core Collection (Advanced Search)

```
#1  TS=(arctic OR subarctic OR "sub-arctic" OR oroarctic OR "oro-arctic" OR "high latitude*" OR "high-latitude*" OR tundra OR permafrost OR periglacial OR "ice wedge*" OR "ice-wedge*" OR "polygonal ground" OR "patterned ground" OR "polygonal tundra" OR "polygonal terrain" OR palsa* OR "peat plateau*" OR thermokarst OR pingo* OR "frost boil*" OR mudboil* OR "earth hummock*" OR alaska* OR "North Slope" OR yukon OR "Northwest Territories" OR nunavut OR nunavik OR labrador OR greenland* OR svalbard OR spitsbergen OR siberia* OR yakutia OR yamal OR taymyr OR chukotka OR "Lena Delta" OR "Mackenzie Delta" OR lapland OR abisko OR kilpisj* OR utqiagvik OR "Barrow Peninsula" OR "Barrow Environmental Observatory" OR "Prudhoe Bay" OR "Seward Peninsula" OR toolik OR "Trail Valley")
#2  TS=(lidar OR "light detection and ranging" OR "laser scan*" OR "laser altimet*" OR "airborne laser" OR "terrestrial laser" OR "point cloud*" OR ALS OR TLS OR ULS OR photogrammetr* OR "structure from motion" OR "structure-from-motion" OR SfM OR UAV OR UAVs OR UAS OR drone* OR "unmanned aerial" OR "uncrewed aerial" OR "remotely piloted" OR ArcticDEM OR "Arctic DEM" OR IfSAR OR "high-resolution topograph*" OR "high resolution topograph*" OR "digital elevation model*" OR "digital terrain model*" OR "digital surface model*" OR "elevation model*" OR "terrain model*" OR "elevation data" OR DEM OR DEMs OR DTM OR DTMs OR DSM OR DSMs OR "topographic data" OR "topographic survey*")
#3  TS=(microtopograph* OR "micro-topograph*" OR microrelief OR "micro-relief" OR microform* OR "micro-form*" OR "fine-scale topograph*" OR "fine scale topograph*" OR mesotopograph* OR hummock* OR hollow* OR trough* OR "polygon rim*" OR "polygon cent*" OR "low-cent*" OR "high-cent*" OR "flat-cent*" OR "water track*" OR "ice-wedge polygon*" OR "ice wedge polygon*" OR geomorphon* OR "landform classif*" OR "landform mapping" OR "terrain attribute*" OR "terrain variable*" OR "terrain parameter*" OR "terrain derivative*" OR "terrain feature*" OR "terrain analys*" OR "terrain index" OR "terrain indices" OR "terrain metric*" OR "topographic attribute*" OR "topographic variable*" OR "topographic index" OR "topographic indices" OR "topographic metric*" OR "topographic position" OR "topographic heterogeneity" OR "land surface parameter*" OR "land-surface parameter*" OR "land surface variable*" OR "land-surface variable*" OR "elevation derivative*" OR "DEM derivative*" OR "topographic derivative*" OR geomorphometr* OR morphometr* OR slope* OR hillslope* OR "topographic gradient*" OR "terrain gradient*" OR "surface gradient*" OR curvature* OR roughness OR rugosity OR ruggedness OR "relative elevation" OR "relative height" OR "local relief" OR "residual relief" OR "wetness index" OR TWI OR "flow accumulation" OR "contributing area" OR "depth-to-water" OR "depth to water" OR "height above" OR TPI)
#4  #1 AND #2 AND #3
```

TS searches title, abstract, author keywords and Keywords Plus. Web of Science treats hyphens as spaces and needs at least three characters before a right-hand wildcard; there is no limit on Boolean operators in TS searches.

### Scopus (Advanced document search)

```
TITLE-ABS-KEY(arctic OR subarctic OR "sub-arctic" OR oroarctic OR "oro-arctic" OR "high latitude*" OR "high-latitude*" OR tundra OR permafrost OR periglacial OR "ice wedge*" OR "ice-wedge*" OR "polygonal ground" OR "patterned ground" OR "polygonal tundra" OR "polygonal terrain" OR palsa* OR "peat plateau*" OR thermokarst OR pingo* OR "frost boil*" OR mudboil* OR "earth hummock*" OR alaska* OR "North Slope" OR yukon OR "Northwest Territories" OR nunavut OR nunavik OR labrador OR greenland* OR svalbard OR spitsbergen OR siberia* OR yakutia OR yamal OR taymyr OR chukotka OR "Lena Delta" OR "Mackenzie Delta" OR lapland OR abisko OR kilpisj* OR utqiagvik OR "Barrow Peninsula" OR "Barrow Environmental Observatory" OR "Prudhoe Bay" OR "Seward Peninsula" OR toolik OR "Trail Valley")
AND TITLE-ABS-KEY(lidar OR "light detection and ranging" OR "laser scan*" OR "laser altimet*" OR "airborne laser" OR "terrestrial laser" OR "point cloud*" OR ALS OR TLS OR ULS OR photogrammetr* OR "structure from motion" OR "structure-from-motion" OR SfM OR UAV OR UAVs OR UAS OR drone* OR "unmanned aerial" OR "uncrewed aerial" OR "remotely piloted" OR ArcticDEM OR "Arctic DEM" OR IfSAR OR "high-resolution topograph*" OR "high resolution topograph*" OR "digital elevation model*" OR "digital terrain model*" OR "digital surface model*" OR "elevation model*" OR "terrain model*" OR "elevation data" OR DEM OR DEMs OR DTM OR DTMs OR DSM OR DSMs OR "topographic data" OR "topographic survey*")
AND TITLE-ABS-KEY(microtopograph* OR "micro-topograph*" OR microrelief OR "micro-relief" OR microform* OR "micro-form*" OR "fine-scale topograph*" OR "fine scale topograph*" OR mesotopograph* OR hummock* OR hollow* OR trough* OR "polygon rim*" OR "polygon cent*" OR "low-cent*" OR "high-cent*" OR "flat-cent*" OR "water track*" OR "ice-wedge polygon*" OR "ice wedge polygon*" OR geomorphon* OR "landform classif*" OR "landform mapping" OR "terrain attribute*" OR "terrain variable*" OR "terrain parameter*" OR "terrain derivative*" OR "terrain feature*" OR "terrain analys*" OR "terrain index" OR "terrain indices" OR "terrain metric*" OR "topographic attribute*" OR "topographic variable*" OR "topographic index" OR "topographic indices" OR "topographic metric*" OR "topographic position" OR "topographic heterogeneity" OR "land surface parameter*" OR "land-surface parameter*" OR "land surface variable*" OR "land-surface variable*" OR "elevation derivative*" OR "DEM derivative*" OR "topographic derivative*" OR geomorphometr* OR morphometr* OR slope* OR hillslope* OR "topographic gradient*" OR "terrain gradient*" OR "surface gradient*" OR curvature* OR roughness OR rugosity OR ruggedness OR "relative elevation" OR "relative height" OR "local relief" OR "residual relief" OR "wetness index" OR TWI OR "flow accumulation" OR "contributing area" OR "depth-to-water" OR "depth to water" OR "height above" OR TPI)
```

### GeoRef – EBSCOhost

```
(TI (arctic OR subarctic OR "sub-arctic" OR oroarctic OR "oro-arctic" OR "high latitude*" OR "high-latitude*" OR tundra OR permafrost OR periglacial OR "ice wedge*" OR "ice-wedge*" OR "polygonal ground" OR "patterned ground" OR "polygonal tundra" OR "polygonal terrain" OR palsa* OR "peat plateau*" OR thermokarst OR pingo* OR "frost boil*" OR mudboil* OR "earth hummock*" OR alaska* OR "North Slope" OR yukon OR "Northwest Territories" OR nunavut OR nunavik OR labrador OR greenland* OR svalbard OR spitsbergen OR siberia* OR yakutia OR yamal OR taymyr OR chukotka OR "Lena Delta" OR "Mackenzie Delta" OR lapland OR abisko OR kilpisj* OR utqiagvik OR "Barrow Peninsula" OR "Barrow Environmental Observatory" OR "Prudhoe Bay" OR "Seward Peninsula" OR toolik OR "Trail Valley") OR AB (arctic OR subarctic OR "sub-arctic" OR oroarctic OR "oro-arctic" OR "high latitude*" OR "high-latitude*" OR tundra OR permafrost OR periglacial OR "ice wedge*" OR "ice-wedge*" OR "polygonal ground" OR "patterned ground" OR "polygonal tundra" OR "polygonal terrain" OR palsa* OR "peat plateau*" OR thermokarst OR pingo* OR "frost boil*" OR mudboil* OR "earth hummock*" OR alaska* OR "North Slope" OR yukon OR "Northwest Territories" OR nunavut OR nunavik OR labrador OR greenland* OR svalbard OR spitsbergen OR siberia* OR yakutia OR yamal OR taymyr OR chukotka OR "Lena Delta" OR "Mackenzie Delta" OR lapland OR abisko OR kilpisj* OR utqiagvik OR "Barrow Peninsula" OR "Barrow Environmental Observatory" OR "Prudhoe Bay" OR "Seward Peninsula" OR toolik OR "Trail Valley") OR SU (arctic OR subarctic OR "sub-arctic" OR oroarctic OR "oro-arctic" OR "high latitude*" OR "high-latitude*" OR tundra OR permafrost OR periglacial OR "ice wedge*" OR "ice-wedge*" OR "polygonal ground" OR "patterned ground" OR "polygonal tundra" OR "polygonal terrain" OR palsa* OR "peat plateau*" OR thermokarst OR pingo* OR "frost boil*" OR mudboil* OR "earth hummock*" OR alaska* OR "North Slope" OR yukon OR "Northwest Territories" OR nunavut OR nunavik OR labrador OR greenland* OR svalbard OR spitsbergen OR siberia* OR yakutia OR yamal OR taymyr OR chukotka OR "Lena Delta" OR "Mackenzie Delta" OR lapland OR abisko OR kilpisj* OR utqiagvik OR "Barrow Peninsula" OR "Barrow Environmental Observatory" OR "Prudhoe Bay" OR "Seward Peninsula" OR toolik OR "Trail Valley"))
AND (TI (lidar OR "light detection and ranging" OR "laser scan*" OR "laser altimet*" OR "airborne laser" OR "terrestrial laser" OR "point cloud*" OR ALS OR TLS OR ULS OR photogrammetr* OR "structure from motion" OR "structure-from-motion" OR SfM OR UAV OR UAVs OR UAS OR drone* OR "unmanned aerial" OR "uncrewed aerial" OR "remotely piloted" OR ArcticDEM OR "Arctic DEM" OR IfSAR OR "high-resolution topograph*" OR "high resolution topograph*" OR "digital elevation model*" OR "digital terrain model*" OR "digital surface model*" OR "elevation model*" OR "terrain model*" OR "elevation data" OR DEM OR DEMs OR DTM OR DTMs OR DSM OR DSMs OR "topographic data" OR "topographic survey*") OR AB (lidar OR "light detection and ranging" OR "laser scan*" OR "laser altimet*" OR "airborne laser" OR "terrestrial laser" OR "point cloud*" OR ALS OR TLS OR ULS OR photogrammetr* OR "structure from motion" OR "structure-from-motion" OR SfM OR UAV OR UAVs OR UAS OR drone* OR "unmanned aerial" OR "uncrewed aerial" OR "remotely piloted" OR ArcticDEM OR "Arctic DEM" OR IfSAR OR "high-resolution topograph*" OR "high resolution topograph*" OR "digital elevation model*" OR "digital terrain model*" OR "digital surface model*" OR "elevation model*" OR "terrain model*" OR "elevation data" OR DEM OR DEMs OR DTM OR DTMs OR DSM OR DSMs OR "topographic data" OR "topographic survey*") OR SU (lidar OR "light detection and ranging" OR "laser scan*" OR "laser altimet*" OR "airborne laser" OR "terrestrial laser" OR "point cloud*" OR ALS OR TLS OR ULS OR photogrammetr* OR "structure from motion" OR "structure-from-motion" OR SfM OR UAV OR UAVs OR UAS OR drone* OR "unmanned aerial" OR "uncrewed aerial" OR "remotely piloted" OR ArcticDEM OR "Arctic DEM" OR IfSAR OR "high-resolution topograph*" OR "high resolution topograph*" OR "digital elevation model*" OR "digital terrain model*" OR "digital surface model*" OR "elevation model*" OR "terrain model*" OR "elevation data" OR DEM OR DEMs OR DTM OR DTMs OR DSM OR DSMs OR "topographic data" OR "topographic survey*"))
AND (TI (microtopograph* OR "micro-topograph*" OR microrelief OR "micro-relief" OR microform* OR "micro-form*" OR "fine-scale topograph*" OR "fine scale topograph*" OR mesotopograph* OR hummock* OR hollow* OR trough* OR "polygon rim*" OR "polygon cent*" OR "low-cent*" OR "high-cent*" OR "flat-cent*" OR "water track*" OR "ice-wedge polygon*" OR "ice wedge polygon*" OR geomorphon* OR "landform classif*" OR "landform mapping" OR "terrain attribute*" OR "terrain variable*" OR "terrain parameter*" OR "terrain derivative*" OR "terrain feature*" OR "terrain analys*" OR "terrain index" OR "terrain indices" OR "terrain metric*" OR "topographic attribute*" OR "topographic variable*" OR "topographic index" OR "topographic indices" OR "topographic metric*" OR "topographic position" OR "topographic heterogeneity" OR "land surface parameter*" OR "land-surface parameter*" OR "land surface variable*" OR "land-surface variable*" OR "elevation derivative*" OR "DEM derivative*" OR "topographic derivative*" OR geomorphometr* OR morphometr* OR slope* OR hillslope* OR "topographic gradient*" OR "terrain gradient*" OR "surface gradient*" OR curvature* OR roughness OR rugosity OR ruggedness OR "relative elevation" OR "relative height" OR "local relief" OR "residual relief" OR "wetness index" OR TWI OR "flow accumulation" OR "contributing area" OR "depth-to-water" OR "depth to water" OR "height above" OR TPI) OR AB (microtopograph* OR "micro-topograph*" OR microrelief OR "micro-relief" OR microform* OR "micro-form*" OR "fine-scale topograph*" OR "fine scale topograph*" OR mesotopograph* OR hummock* OR hollow* OR trough* OR "polygon rim*" OR "polygon cent*" OR "low-cent*" OR "high-cent*" OR "flat-cent*" OR "water track*" OR "ice-wedge polygon*" OR "ice wedge polygon*" OR geomorphon* OR "landform classif*" OR "landform mapping" OR "terrain attribute*" OR "terrain variable*" OR "terrain parameter*" OR "terrain derivative*" OR "terrain feature*" OR "terrain analys*" OR "terrain index" OR "terrain indices" OR "terrain metric*" OR "topographic attribute*" OR "topographic variable*" OR "topographic index" OR "topographic indices" OR "topographic metric*" OR "topographic position" OR "topographic heterogeneity" OR "land surface parameter*" OR "land-surface parameter*" OR "land surface variable*" OR "land-surface variable*" OR "elevation derivative*" OR "DEM derivative*" OR "topographic derivative*" OR geomorphometr* OR morphometr* OR slope* OR hillslope* OR "topographic gradient*" OR "terrain gradient*" OR "surface gradient*" OR curvature* OR roughness OR rugosity OR ruggedness OR "relative elevation" OR "relative height" OR "local relief" OR "residual relief" OR "wetness index" OR TWI OR "flow accumulation" OR "contributing area" OR "depth-to-water" OR "depth to water" OR "height above" OR TPI) OR SU (microtopograph* OR "micro-topograph*" OR microrelief OR "micro-relief" OR microform* OR "micro-form*" OR "fine-scale topograph*" OR "fine scale topograph*" OR mesotopograph* OR hummock* OR hollow* OR trough* OR "polygon rim*" OR "polygon cent*" OR "low-cent*" OR "high-cent*" OR "flat-cent*" OR "water track*" OR "ice-wedge polygon*" OR "ice wedge polygon*" OR geomorphon* OR "landform classif*" OR "landform mapping" OR "terrain attribute*" OR "terrain variable*" OR "terrain parameter*" OR "terrain derivative*" OR "terrain feature*" OR "terrain analys*" OR "terrain index" OR "terrain indices" OR "terrain metric*" OR "topographic attribute*" OR "topographic variable*" OR "topographic index" OR "topographic indices" OR "topographic metric*" OR "topographic position" OR "topographic heterogeneity" OR "land surface parameter*" OR "land-surface parameter*" OR "land surface variable*" OR "land-surface variable*" OR "elevation derivative*" OR "DEM derivative*" OR "topographic derivative*" OR geomorphometr* OR morphometr* OR slope* OR hillslope* OR "topographic gradient*" OR "terrain gradient*" OR "surface gradient*" OR curvature* OR roughness OR rugosity OR ruggedness OR "relative elevation" OR "relative height" OR "local relief" OR "residual relief" OR "wetness index" OR TWI OR "flow accumulation" OR "contributing area" OR "depth-to-water" OR "depth to water" OR "height above" OR TPI))
```

### GeoRef or ProQuest Dissertations & Theses – ProQuest

```
noft(arctic OR subarctic OR "sub-arctic" OR oroarctic OR "oro-arctic" OR "high latitude*" OR "high-latitude*" OR tundra OR permafrost OR periglacial OR "ice wedge*" OR "ice-wedge*" OR "polygonal ground" OR "patterned ground" OR "polygonal tundra" OR "polygonal terrain" OR palsa* OR "peat plateau*" OR thermokarst OR pingo* OR "frost boil*" OR mudboil* OR "earth hummock*" OR alaska* OR "North Slope" OR yukon OR "Northwest Territories" OR nunavut OR nunavik OR labrador OR greenland* OR svalbard OR spitsbergen OR siberia* OR yakutia OR yamal OR taymyr OR chukotka OR "Lena Delta" OR "Mackenzie Delta" OR lapland OR abisko OR kilpisj* OR utqiagvik OR "Barrow Peninsula" OR "Barrow Environmental Observatory" OR "Prudhoe Bay" OR "Seward Peninsula" OR toolik OR "Trail Valley")
AND noft(lidar OR "light detection and ranging" OR "laser scan*" OR "laser altimet*" OR "airborne laser" OR "terrestrial laser" OR "point cloud*" OR ALS OR TLS OR ULS OR photogrammetr* OR "structure from motion" OR "structure-from-motion" OR SfM OR UAV OR UAVs OR UAS OR drone* OR "unmanned aerial" OR "uncrewed aerial" OR "remotely piloted" OR ArcticDEM OR "Arctic DEM" OR IfSAR OR "high-resolution topograph*" OR "high resolution topograph*" OR "digital elevation model*" OR "digital terrain model*" OR "digital surface model*" OR "elevation model*" OR "terrain model*" OR "elevation data" OR DEM OR DEMs OR DTM OR DTMs OR DSM OR DSMs OR "topographic data" OR "topographic survey*")
AND noft(microtopograph* OR "micro-topograph*" OR microrelief OR "micro-relief" OR microform* OR "micro-form*" OR "fine-scale topograph*" OR "fine scale topograph*" OR mesotopograph* OR hummock* OR hollow* OR trough* OR "polygon rim*" OR "polygon cent*" OR "low-cent*" OR "high-cent*" OR "flat-cent*" OR "water track*" OR "ice-wedge polygon*" OR "ice wedge polygon*" OR geomorphon* OR "landform classif*" OR "landform mapping" OR "terrain attribute*" OR "terrain variable*" OR "terrain parameter*" OR "terrain derivative*" OR "terrain feature*" OR "terrain analys*" OR "terrain index" OR "terrain indices" OR "terrain metric*" OR "topographic attribute*" OR "topographic variable*" OR "topographic index" OR "topographic indices" OR "topographic metric*" OR "topographic position" OR "topographic heterogeneity" OR "land surface parameter*" OR "land-surface parameter*" OR "land surface variable*" OR "land-surface variable*" OR "elevation derivative*" OR "DEM derivative*" OR "topographic derivative*" OR geomorphometr* OR morphometr* OR slope* OR hillslope* OR "topographic gradient*" OR "terrain gradient*" OR "surface gradient*" OR curvature* OR roughness OR rugosity OR ruggedness OR "relative elevation" OR "relative height" OR "local relief" OR "residual relief" OR "wetness index" OR TWI OR "flow accumulation" OR "contributing area" OR "depth-to-water" OR "depth to water" OR "height above" OR TPI)
```

### OpenAlex (API; run with openalex_harvest.py)

```
filter=title_and_abstract.search:(A),title_and_abstract.search:(B),title_and_abstract.search:(C)
(blocks as listed in A.1; openalex_harvest.py splits the longest block into sub-queries to stay under
 the ~4,000-character URL limit and unions the results by OpenAlex ID)
```

OpenAlex needs upper-case AND/OR/NOT and at least three characters before a wildcard, and it stems search terms. Its documentation does not say whether wildcards work inside quoted phrases, so the script expands such phrases to explicit variants where stemming cannot recover the word, and otherwise drops the trailing wildcard. With the v0.1 blocks it runs 3 sub-queries. Expansions:

```
"micro-topograph*" -> "micro-topography" OR "micro-topographic" OR "micro-topographical"
"fine-scale topograph*" -> "fine-scale topography" OR "fine-scale topographic"
"fine scale topograph*" -> "fine scale topography" OR "fine scale topographic"
"high-resolution topograph*" -> "high-resolution topography" OR "high-resolution topographic"
"high resolution topograph*" -> "high resolution topography" OR "high resolution topographic"
"polygon cent*" -> "polygon center" OR "polygon centers" OR "polygon centre" OR "polygon centres"
"low-cent*" -> "low-centered" OR "low-centred" OR "low-center" OR "low-centre"
"high-cent*" -> "high-centered" OR "high-centred" OR "high-center" OR "high-centre"
"flat-cent*" -> "flat-centered" OR "flat-centred" OR "flat-center" OR "flat-centre"
"landform classif*" -> "landform classification" OR "landform classifications" OR "landform classified"
"terrain analys*" -> "terrain analysis" OR "terrain analyses"
"laser altimet*" -> "laser altimetry" OR "laser altimeter" OR "laser altimeters"
"laser scan*" -> "laser scan" OR "laser scanning" OR "laser scanner" OR "laser scanners"
"laser scanning simulat*" -> "laser scanning simulation" OR "laser scanning simulator"
```

### Google Scholar (Publish or Perish; first 300 results per query, by relevance)

```
GS1: tundra lidar microtopography slope OR curvature OR "relative elevation"
GS2: "ice-wedge polygon" lidar OR "digital elevation model" troughs
GS3: palsa OR "peat plateau" lidar OR UAV "digital elevation model" microtopography
GS4: arctic tundra lidar "topographic wetness index" OR "terrain attributes"
GS5: permafrost "terrain attributes" OR "terrain variables" lidar OR ArcticDEM
```

### OSTI.gov

```
(microtopography OR "terrain attributes" OR "ice wedge polygon*" OR "polygonal tundra") AND (lidar OR "digital elevation model" OR DEM) AND (arctic OR tundra OR permafrost)
```

## A.3 Two-arm restriction (only if A AND B AND C exceeds 8,000 unique records)

Arm 1 keeps every elevation term but only microform vocabulary. Arm 2 keeps every terrain-variable term but only high-resolution elevation terms. Adopt only if the recall targets in 5.3 still hold.

```
Arm 1:  A AND B AND C_micro
Arm 2:  A AND B_hr AND C_generic

C_micro   = microtopograph* OR "micro-topograph*" OR microrelief OR "micro-relief" OR microform* OR "micro-form*" OR "fine-scale topograph*" OR "fine scale topograph*" OR mesotopograph* OR hummock* OR hollow* OR trough* OR "polygon rim*" OR "polygon cent*" OR "low-cent*" OR "high-cent*" OR "flat-cent*" OR "water track*" OR "ice-wedge polygon*" OR "ice wedge polygon*" OR geomorphon* OR "landform classif*" OR "landform mapping"

C_generic = "terrain attribute*" OR "terrain variable*" OR "terrain parameter*" OR "terrain derivative*" OR "terrain feature*" OR "terrain analys*" OR "terrain index" OR "terrain indices" OR "terrain metric*" OR "topographic attribute*" OR "topographic variable*" OR "topographic index" OR "topographic indices" OR "topographic metric*" OR "topographic position" OR "topographic heterogeneity" OR "land surface parameter*" OR "land-surface parameter*" OR "land surface variable*" OR "land-surface variable*" OR "elevation derivative*" OR "DEM derivative*" OR "topographic derivative*" OR geomorphometr* OR morphometr* OR slope* OR hillslope* OR "topographic gradient*" OR "terrain gradient*" OR "surface gradient*" OR curvature* OR roughness OR rugosity OR ruggedness OR "relative elevation" OR "relative height" OR "local relief" OR "residual relief" OR "wetness index" OR TWI OR "flow accumulation" OR "contributing area" OR "depth-to-water" OR "depth to water" OR "height above" OR TPI

B_hr      = lidar OR "light detection and ranging" OR "laser scan*" OR "laser altimet*" OR "airborne laser" OR "terrestrial laser" OR "point cloud*" OR ALS OR TLS OR ULS OR photogrammetr* OR "structure from motion" OR "structure-from-motion" OR SfM OR UAV OR UAVs OR UAS OR drone* OR "unmanned aerial" OR "uncrewed aerial" OR "remotely piloted" OR ArcticDEM OR "Arctic DEM" OR IfSAR OR "high-resolution topograph*" OR "high resolution topograph*"
```

## A.4 Notes for Stage S1

- Confirm every core seed at full text before testing, and add experts' key studies to the validation set.

- Check whether EBSCOhost and ProQuest accept wildcards inside quoted phrases. If not, expand those phrases to explicit variants and log the change.

- Export full records with abstracts: Web of Science full record (tab-delimited, UTF-8), Scopus CSV with abstracts, EBSCOhost or ProQuest RIS.

- Log the exact string as run, the date, the platform and the hit count in search_log_v0.1.csv.

- Run recall_check.py on each export and on their union; diagnose every missed seed with --diagnose.

## A.5 Novelty search for gate criterion G4 (Stage S6)

Run in Web of Science and Scopus with no area block, so that benchmarks outside the Arctic are found. Screen for studies that benchmark the full chain against known truth.

```
B_hr AND C_generic AND D   (no area block; run at Stage S6)

D = benchmark* OR synthetic OR simulat* OR "virtual laser" OR "laser scanning simulat*" OR "ground truth" OR "known truth" OR analytic* OR intercompar* OR "error propagation" OR "error budget"
```
