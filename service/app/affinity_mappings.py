"""
Populate biorhythm_affinity rows for the 100 pilot nodes.

Mapping logic derived from content analysis of the three bucket types:
- bio_field_charts (35 nodes): Pranamaya primary, Enneagram 5+9
- interpretation_maps (35 nodes): Manomaya primary, Enneagram 4+6
- cross_integration_histories (30 nodes): Vijnanamaya primary, Enneagram 8+4

Each node gets multiple affinity rows to enable cross-resonance retrieval.
"""
from __future__ import annotations

BUCKET_AFFINITIES = {
    "bio_field_charts": [
        {"enneagram_type": 5, "kosha_layer": "pranamaya", "resonance_weight": 0.95},
        {"enneagram_type": 9, "kosha_layer": "pranamaya", "resonance_weight": 0.90},
        {"enneagram_type": 5, "kosha_layer": "annamaya", "resonance_weight": 0.70},
        {"enneagram_type": 9, "kosha_layer": "annamaya", "resonance_weight": 0.65},
        {"enneagram_type": 5, "kosha_layer": "manomaya", "resonance_weight": 0.55},
        {"enneagram_type": 6, "kosha_layer": "pranamaya", "resonance_weight": 0.50},
        {"enneagram_type": 1, "kosha_layer": "annamaya", "resonance_weight": 0.45},
    ],
    "interpretation_maps": [
        {"enneagram_type": 4, "kosha_layer": "manomaya", "resonance_weight": 0.92},
        {"enneagram_type": 6, "kosha_layer": "manomaya", "resonance_weight": 0.85},
        {"enneagram_type": 4, "kosha_layer": "vijnanamaya", "resonance_weight": 0.75},
        {"enneagram_type": 6, "kosha_layer": "vijnanamaya", "resonance_weight": 0.68},
        {"enneagram_type": 5, "kosha_layer": "manomaya", "resonance_weight": 0.60},
        {"enneagram_type": 7, "kosha_layer": "manomaya", "resonance_weight": 0.50},
        {"enneagram_type": 4, "kosha_layer": "anandamaya", "resonance_weight": 0.45},
    ],
    "cross_integration_histories": [
        {"enneagram_type": 8, "kosha_layer": "vijnanamaya", "resonance_weight": 0.94},
        {"enneagram_type": 4, "kosha_layer": "vijnanamaya", "resonance_weight": 0.85},
        {"enneagram_type": 8, "kosha_layer": "anandamaya", "resonance_weight": 0.78},
        {"enneagram_type": 4, "kosha_layer": "anandamaya", "resonance_weight": 0.72},
        {"enneagram_type": 1, "kosha_layer": "vijnanamaya", "resonance_weight": 0.65},
        {"enneagram_type": 5, "kosha_layer": "vijnanamaya", "resonance_weight": 0.60},
        {"enneagram_type": 8, "kosha_layer": "manomaya", "resonance_weight": 0.50},
        {"enneagram_type": 2, "kosha_layer": "anandamaya", "resonance_weight": 0.42},
    ],
}

AFFINITIES_SQL = []
for bucket, affinities in BUCKET_AFFINITIES.items():
    for aff in affinities:
        AFFINITIES_SQL.append((bucket, aff["enneagram_type"], None, aff["kosha_layer"], aff["resonance_weight"]))

ENNEAGRAM_HORMONE_MAP = {
    1: "cortisol_discipline",
    2: "oxytocin_attunement",
    3: "dopamine_achievement",
    4: "serotonin_depth",
    5: "acetylcholine_investigation",
    6: "adrenaline_vigilance",
    7: "dopamine_exploration",
    8: "testosterone_confrontation",
    9: "gaba_harmonization",
}

KOSHA_DESCRIPTION = {
    "annamaya": "physical_nourishment",
    "pranamaya": "vital_breath",
    "manomaya": "emotional_mind",
    "vijnanamaya": "discerning_wisdom",
    "anandamaya": "bliss_integration",
}