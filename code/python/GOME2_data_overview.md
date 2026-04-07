# GOME-2 Satellite Data — Overview for New Team Members

## 1. The GOME-2 Instrument

GOME-2 (Global Ozone Monitoring Experiment-2) is an optical spectrometer mounted on the **Metop** series of polar-orbiting satellites operated by EUMETSAT. It measures sunlight backscattered from Earth's atmosphere in the **ultraviolet and visible spectrum (240–790 nm)** at high spectral resolution (0.26–0.51 nm), producing 4096 spectral points per measurement across four detector channels.

**Key characteristics:**
- Footprint size: 80×40 km per main channel pixel
- Orbit altitude: ~820 km, sun-synchronous
- Equatorial overpass time: ~09:30 local time (descending node)
- Three active instruments: GOME-2A (Metop-A, 2006), GOME-2B (Metop-B, 2012), GOME-2C (Metop-C, 2018)

**What it measures:** By analysing absorption features in the backscattered radiance spectrum using DOAS (Differential Optical Absorption Spectroscopy), GOME-2 can retrieve column concentrations of trace gases including NO₂, O₃, SO₂, BrO, HCHO, H₂O, and CO. It also provides aerosol index and cloud properties.

---

## 2. Satellites and Filename Conventions

GOME-2 files follow the EPS (EUMETSAT Polar System) naming convention:

```
GOME_xxx_1B_M02_20211101073256Z_20211101091456Z_N_O_20211101091214Z
```

| Field | Meaning |
|---|---|
| `GOME` | Instrument name |
| `xxx` | Product type (full-orbit dump — literally `xxx`, not a placeholder) |
| `1B` | Processing level (Level 1B) |
| `M01` | Metop-A |
| `M02` | Metop-B |
| `M03` | Metop-C |
| First timestamp | Sensing start time (UTC) |
| Second timestamp | Sensing end time (UTC) |
| `N` | Orbit direction (N = descending) |
| `O` | Processing mode (O = Operational NRT) |
| Third timestamp | File generation/processing time (UTC) |

Each file covers roughly 100 minutes of orbit data (Svalbard to Svalbard). All three Metop satellites may observe the same area on the same day, providing complementary coverage.

---

## 3. Data Processing Levels

| Level | Description | Format | Who produces it |
|---|---|---|---|
| L0 | Raw instrument counts | Binary | EUMETSAT |
| L1B | Calibrated radiances + geolocation | EPS Native (.nat) | EUMETSAT |
| L2 | Retrieved trace gas columns per orbit pixel | HDF5 | DLR (via AC SAF) |
| L3 | Gridded daily/monthly trace gas maps | NetCDF-4 | AC SAF |

For pollution monitoring, **L2 and L3 are the most directly useful**. L1B requires running your own retrieval algorithm to extract trace gas concentrations.

---

## 4. EPS Native Format (.nat)

The `.nat` file is EUMETSAT's proprietary binary format for L1B data. It is **not directly readable** by standard tools like xarray or numpy. The file structure consists of binary records defined in EUMETSAT's Product Format Specification document.

**To work with .nat files in Python**, the recommended tool chain is:

- **CODA** — low-level C library with Python bindings, from the ESA Atmospheric Toolbox, understands the EPS binary format
- **HARP** — higher-level tool built on CODA, can convert .nat files to NetCDF via `harpconvert`
- **codadef-eps** — format definition files that teach CODA how to parse GOME-2 and IASI records specifically

These tools are maintained by S&T Corporation and distributed via the `stcorp-forge` conda channel.

---

## 5. GOME-2 Data Variables (after conversion to NetCDF)

After converting a L1B .nat file to NetCDF with HARP, the dataset contains:

| Variable | Dimensions | Description |
|---|---|---|
| `datetime` | time | Measurement timestamp |
| `latitude` / `longitude` | time | Pixel centre coordinates |
| `latitude_bounds` / `longitude_bounds` | time × 4 | 4-corner pixel footprint |
| `wavelength` | time × spectral | Wavelength grid per pixel (nm) |
| `wavelength_photon_radiance` | time × spectral | Earth radiance spectra |
| `solar_irradiance` | spectral | Daily solar reference spectrum |
| `cloud_fraction` | time | Cloud cover per pixel (0–1) |
| `cloud_top_pressure` | time | Cloud top pressure |
| `integration_time` | time × spectral | Integration time per spectral point |
| `scan_subindex` | time | Scan position index |
| `scan_direction_type` | time | Forward/backward scan flag |
| `solar_zenith_angle_toa` | time | Sun angle at top of atmosphere |
| `solar_azimuth_angle_toa` | time | Sun azimuth |
| `viewing_zenith_angle_toa` | time | Sensor viewing angle |
| `viewing_azimuth_angle_toa` | time | Sensor azimuth |
| `orbit_index` | scalar | Orbit number |

A typical L1B file contains ~19,000 time steps and 4096 spectral points, resulting in a ~2 GB dataset in memory.

---

## 6. Where to Get GOME-2 Data

### EUMETSAT Data Store (via eumdac)

The official EUMETSAT data access client. Accessible via Python API or command line. Hosts:

- `EO:EUM:DAT:METOP:GOMEL1` — GOME-2 L1B operational NRT (all three Metops)
- `EO:EUM:DAT:0533` — GOME-2 L1B Fundamental Data Record R3 (reprocessed, Metop-A and B)
- Various IASI and TROPOMI products

**GOME-2 L2 and L3 products are NOT available here.** Only L1B is in the Data Store.

### AC SAF (Atmospheric Composition SAF)

A EUMETSAT service facility coordinated by the Finnish Meteorological Institute (FMI), with processing done by DLR (German Aerospace Center). This is where all **processed trace gas products** live.

Access: register at **acsaf.org**, then connect via FTP to `acsaf.eoc.dlr.de`

FTP server structure:
```
/gome2a/          — Metop-A products
/gome2b/          — Metop-B products
/gome2c/          — Metop-C products
/GOME2_L2_Reproc/ — Reprocessed data records
```

Products available:
- **L2 offline** — per-orbit HDF5 files, available 1–3 days after sensing
- **L2 NRT** — per-orbit files, available within 3 hours of sensing
- **L3 daily/monthly** — gridded NetCDF-4 at 0.25°×0.25° resolution, 2007–present
- Species: O₃, NO₂, tropospheric NO₂, SO₂, BrO, HCHO, H₂O, aerosol index, UV index

**AC SAF registration is separate from EUMETSAT registration.** The two systems are independent.

### Sentinel-5P / TROPOMI (also via eumdac)

Available directly in the EUMETSAT Data Store. Best spatial resolution (~3.5×5.5 km), ready-to-use L2 NetCDF. Collection IDs in eumdac: `EO:EUM:DAT:0076` (NO₂), `EO:EUM:DAT:0078` (SO₂), `EO:EUM:DAT:0073` (CO), etc.

---

## 7. IASI — The Other Key Instrument on Metop

IASI (Infrared Atmospheric Sounding Interferometer) is also on all three Metop satellites. Unlike GOME-2 which works in UV/visible, IASI works in the **thermal infrared**, giving it access to different gases and the ability to retrieve **vertical profiles** rather than just total columns.

Key pollutants: CO, O₃, SO₂, NH₃, CH₄, CO₂

Some IASI products (e.g. SO₂ Climate Data Record `EO:EUM:DAT:0960`) are available directly in the EUMETSAT Data Store via eumdac, unlike GOME-2 L2 which requires AC SAF.

---

## 8. Summary: Data Access Decision Tree

```
Need GOME-2 raw spectra (L1B)?
  → EUMETSAT Data Store via eumdac
  → Files are .nat format, need harpconvert to read

Need GOME-2 trace gas columns (L2/L3)?
  → AC SAF via FTP (acsaf.eoc.dlr.de)
  → Register separately at acsaf.org
  → L3 files are ready-to-use NetCDF-4

Need TROPOMI data?
  → EUMETSAT Data Store via eumdac
  → Already L2 NetCDF, no conversion needed

Need IASI data?
  → Some products in EUMETSAT Data Store (eumdac)
  → Some products also via AC SAF FTP
```

---

## 9. Key Organisations

| Organisation | Role |
|---|---|
| EUMETSAT | Operates Metop satellites, produces L1B, runs Data Store |
| DLR (German Aerospace Center) | Produces GOME-2 L2 trace gas products, runs AC SAF FTP archive |
| FMI (Finnish Meteorological Institute) | Coordinates AC SAF, produces aerosol and UV products |
| ESA / S&T Corporation | Maintain CODA/HARP software tools for reading EPS native files |

---

*Document prepared with assistance from Claude Sonnet 4.6 (Anthropic)*  
*Date: 2026-04-01*