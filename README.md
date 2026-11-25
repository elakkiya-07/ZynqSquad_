# Real-Time On-Board Cloud/Ocean Filtering on a Low-Cost FPGA

**Team ZynqSquad · VConnecTech Engineering Marathon 2026 · Track: FPGA Design**
Elakkiya K (Lead), M Mohith Chander, Aruna Devi K, Aishwwarya G, Sai Aditiyaa R S — R.M.K. Engineering College

An on-board filter for Earth-observation satellites. Every pixel of a 256 × 256 multispectral tile is labelled
**cloud**, **water** or **land** from its 12 Sentinel-2 bands, the labels are counted in hardware, and the tile is
dropped before it is stored when cloud + water cover at least 70% of it. Target platform: **PYNQ-Z2 (Zynq-7020)**.

## Status

| Stage | Status |
|---|---|
| Data-level study on real CloudSEN12 tiles (this repo) | **Done** |
| Golden reference for hardware verification (200 tiles) | **Done** |
| System architecture and per-tile flow | **Done** (see `figures/`) |
| Classifier training, Brevitas QAT, FINN accelerator | Planned (implementation phase) |
| Tile decision unit RTL, Vivado integration, board run | Planned (implementation phase) |

## Key result (reference labels, i.e. an ideal classifier)

200 tiles (13,107,200 pixels) from 50 CloudSEN12 high-quality patches, 47 distinct locations:

| Threshold | Cloud-only rule | Cloud + water rule |
|---|---|---|
| 60% | 34.5% | 38.5% |
| **70%** | **27.5%** (55 tiles) | **33.0%** (66 tiles) |
| 80% | 22.5% | 27.5% |

Only 15 of the 200 tiles lie between 65% and 75%, where a classifier error could change the decision.

![Distribution](figures/hist.png)
![Example tiles](figures/demo_tiles.png)

## Architecture

![Architecture](figures/fig1a_architecture.png)

Per-tile flow: `figures/fig1b_flowchart.png`.

## Repository layout

```
notebooks/cloudsen12_tile_discard.ipynb   data pipeline: load labels, build 3-class maps, tile, decide, export
results/tiles.csv                         per tile: patch ID, quadrant, cloud/water/land counts, decisions
results/golden_decisions.txt              one bit per tile (1 = discard), cloud + water rule, θ = 70%
results/labels_hex.zip                    200 files tile_XXX.hex: 65,536 labels each, raster order,
                                          one hex digit per line (0 land, 1 water, 2 cloud) for $readmemh
results/used_ids.csv                      the 50 CloudSEN12 patch IDs used (seed 42)
results/summary.txt                       summary printed by the notebook
scripts/threshold_table.py                recomputes the table above from tiles.csv
figures/                                  architecture, flowchart and result figures
```

## How to reproduce

1. Open `notebooks/cloudsen12_tile_discard.ipynb` in Google Colab (File → Upload notebook).
2. Run the cells in order. Cell 0 installs the dependencies (`requirements.txt`).
   Data is read remotely from Hugging Face with `tacoreader`; only label layers are downloaded.
3. Outputs are written to `/content/out/` and zipped as `out.zip`.
4. Locally: `python scripts/threshold_table.py results/tiles.csv`

## Label rules

- **Cloud (2):** CloudSEN12 thick or thin cloud (expert annotations).
- **Water (1):** ESA WorldCover 2020 class 80 (permanent water bodies), only where the pixel is not cloud.
- **Land (0):** everything else, including cloud shadow. Patch padding (509 → 512) is counted as land.
- **Decision:** discard if `cloud + water ≥ 45,876` (= ⌈0.70 × 65,536⌉).

## Data sources and licences

- CloudSEN12 (Aybar et al., Sci. Data 2022), released under CC BY-NC-SA 4.0. The label files in `results/`
  are derived from it and are shared under the same licence, for non-commercial research use.
- ESA WorldCover 10 m 2020 v100 (Zanaga et al., 2021).
