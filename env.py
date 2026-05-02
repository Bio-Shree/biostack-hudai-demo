from hud import Environment

env = Environment("biostack-drug-env")

# ── TOOLS ────────────────────────────────────────────────────────────────────
# These represent BioStack's structured biomedical data pipelines.
# In production: replace with live EHR / assay / CRO data queries.

@env.tool
def get_target_info(target_name: str) -> dict:
    """
    Returns clinical and biological context about a protein target.
    Mirrors BioStack's structured target data pipeline.
    """
    targets = {
        "EGFR": {
            "full_name": "Epidermal Growth Factor Receptor",
            "role": "Tyrosine kinase driving cell proliferation",
            "disease": "Non-small cell lung cancer (NSCLC)",
            "binding_site": "ATP-binding pocket in kinase domain",
            "mutation_relevance": "EGFR exon 19 deletions / L858R point mutation",
        },
        "BRAF": {
            "full_name": "B-Raf proto-oncogene serine/threonine-protein kinase",
            "role": "MAP kinase pathway regulator",
            "disease": "Melanoma (V600E mutation)",
            "binding_site": "Activation loop of kinase domain",
            "mutation_relevance": "V600E substitution drives constitutive activation",
        },
        "VEGFR2": {
            "full_name": "Vascular Endothelial Growth Factor Receptor 2",
            "role": "Key mediator of tumour angiogenesis",
            "disease": "Multiple solid tumours",
            "binding_site": "Extracellular ligand-binding domain",
            "mutation_relevance": "Overexpressed in highly vascularised tumours",
        },
    }
    return targets.get(target_name, {"error": f"Target '{target_name}' not found in BioStack index."})


@env.tool
def get_compound_profile(compound_name: str) -> dict:
    """
    Returns the molecular and clinical profile of a drug candidate.
    Mirrors BioStack's structured compound / CRO data pipeline.
    """
    compounds = {
        "Erlotinib": {
            "type": "Small molecule",
            "mechanism": "Reversible EGFR tyrosine kinase inhibitor",
            "selectivity": "High selectivity for EGFR",
            "clinical_stage": "FDA approved — NSCLC (1st / 2nd line)",
            "key_data": "Blocks ATP binding at EGFR kinase domain",
        },
        "Vemurafenib": {
            "type": "Small molecule",
            "mechanism": "Selective BRAF V600E inhibitor",
            "selectivity": "High selectivity for mutant BRAF V600E",
            "clinical_stage": "FDA approved — unresectable or metastatic melanoma",
            "key_data": "Inactive against wild-type BRAF",
        },
        "Bevacizumab": {
            "type": "Monoclonal antibody",
            "mechanism": "Anti-VEGF — blocks VEGF-A from binding VEGFR2",
            "selectivity": "Targets VEGF ligand, not the receptor directly",
            "clinical_stage": "FDA approved — multiple solid tumours",
            "key_data": "Inhibits tumour angiogenesis",
        },
        "Metformin": {
            "type": "Biguanide",
            "mechanism": "AMPK activator — reduces hepatic gluconeogenesis",
            "selectivity": "Metabolic target, not a kinase inhibitor",
            "clinical_stage": "FDA approved — Type 2 diabetes",
            "key_data": "No established oncology kinase selectivity",
        },
    }
    return compounds.get(compound_name, {"error": f"Compound '{compound_name}' not found in BioStack index."})


# ── SCENARIO ─────────────────────────────────────────────────────────────────
# The agent must use the tools above to reason and pick the correct drug.

@env.scenario("match_drug_to_target")
async def match_drug_to_target(target: str, candidates: list[str], correct: str):
    """
    Drug-target matching scenario.

    The agent receives a protein target and a list of candidate compounds.
    It must call the tools, reason through the biology, and output the
    name of the best therapeutic match — exactly as written in the candidates list.

    Reward:
        1.0  — correct match
        0.0  — incorrect or malformed answer
    """
    prompt = f"""You are a drug discovery reasoning assistant at BioStack.

Your task: Identify which of the following candidate compounds is the
best therapeutic match for the protein target below.

Protein target  : {target}
Candidates      : {candidates}

Tools available:
  - get_target_info(target_name)     → clinical context, binding site, disease area
  - get_compound_profile(compound_name) → mechanism, selectivity, clinical stage

Instructions:
  1. Call get_target_info for the target.
  2. Call get_compound_profile for each candidate.
  3. Reason step by step about which compound best matches the target's mechanism.
  4. Output ONLY the compound name — exactly as it appears in the candidates list.
     Do not add any explanation after your final answer.
"""
    response = yield prompt

    # Evaluate agent's answer
    answer = response.strip()
    reward = 1.0 if correct in answer else 0.0

    yield reward
