"""Organic Farming Knowledge Service: Curated datasets and calculation algorithms for remedies, fertilizers, companions, seed treatment, load limits, schemes, crops, and microclimate."""

from typing import List, Dict, Any, Optional

# ==============================================================================
# 1. ORGANIC REMEDIES DATASET
# ==============================================================================
ORGANIC_REMEDIES: List[Dict[str, Any]] = [
    {
        "id": "neem-oil-emulsion",
        "name": "Cold-Pressed Neem Oil Emulsion (5ml/L)",
        "category": "Botanical Insecticide & Repellent",
        "target_pests": ["Aphids", "Whiteflies", "Thrips", "Spider Mites", "Mealybugs", "Leafminers", "Caterpillars"],
        "active_compound": "Azadirachtin (natural insect growth regulator & antifeedant)",
        "recipe": {
            "ingredients": ["Pure cold-pressed Neem Oil: 5 ml", "Mild liquid castile or coconut soap: 2 ml (or 2-3 drops)", "Lukewarm clean water: 1 Liter"],
            "preparation_steps": [
                "1. Mix 5 ml neem oil with 2 ml liquid soap in a small cup until the oil turns milky and emulsifies.",
                "2. Pour the emulsified mixture into 1 Liter of lukewarm water in a clean spray bottle.",
                "3. Shake vigorously before each spray to ensure thorough mixing.",
            ],
            "application_protocol": "Spray thoroughly on both the upper and undersides of leaves during late evening (after 5 PM) to prevent sun scorch. Repeat every 7 to 10 days for maintenance, or every 4 days during active pest outbreak.",
            "safety_precautions": "Avoid spraying during peak midday sunlight. Harmless to honeybees when sprayed after pollinator activity subsides in the evening.",
        },
    },
    {
        "id": "sour-buttermilk-fungicide",
        "name": "Fermented Sour Buttermilk Bio-Fungicide (1:10)",
        "category": "Microbial / Biological Fungicide",
        "target_pests": ["Powdery Mildew", "Downy Mildew", "Early Blight", "Leaf Spot", "Chilli Leaf Curl Virus Vectors"],
        "active_compound": "Lactic acid bacteria (*Lactobacillus*) & natural antifungal bioactive peptides",
        "recipe": {
            "ingredients": ["Sour whole milk curd or buttermilk: 100 ml", "Clean non-chlorinated water: 1 Liter", "Copper wire/vessel (optional traditional booster): 1 small piece"],
            "preparation_steps": [
                "1. Keep fresh curd or buttermilk in a shaded spot for 3 to 4 days until it turns noticeably sour and tangy.",
                "(Optional: Place a clean copper wire in the fermenting curd for 48 hours to release copper lactate).",
                "2. Dilute 100 ml of this sour buttermilk into 900 ml of clean water (1:10 ratio).",
                "3. Strain through a fine muslin cloth to avoid clogging the spray nozzle.",
            ],
            "application_protocol": "Spray foliar mist over all leaves once every 7 to 10 days. The acidic lactic bacteria alter leaf surface pH and form a protective biological barrier against fungal mycelium.",
            "safety_precautions": "Always strain well. Do not store diluted mixture for more than 24 hours.",
        },
    },
    {
        "id": "garlic-chilli-extract",
        "name": "Garlic-Chilli-Ginger Hot Repellent Spray (Agniastra Blend)",
        "category": "Broad-Spectrum Botanical Pest Deterrent",
        "target_pests": ["Biting Caterpillars", "Pod Borers", "Grasshoppers", "Slugs & Snails", "Beetles"],
        "active_compound": "Allicin (Garlic), Capsaicin (Chilli), and Gingerol (Ginger)",
        "recipe": {
            "ingredients": ["Hot green or red chillies: 50 grams", "Fresh garlic cloves: 50 grams", "Fresh ginger: 20 grams", "Clean water: 1 Liter", "Liquid soap: 2 drops"],
            "preparation_steps": [
                "1. Grind chillies, garlic, and ginger into a fine paste.",
                "2. Boil the paste in 500 ml water for 15 minutes, then cool overnight.",
                "3. Filter through a fine cloth and dilute with another 500 ml water plus 2 drops of soap.",
            ],
            "application_protocol": "Spray on affected vegetable foliage every 5 to 7 days. Causes immediate contact deterrence and stops insect feeding.",
            "safety_precautions": "Wear gloves and eye protection while preparing and spraying. Keep away from children and pets.",
        },
    },
    {
        "id": "trichoderma-biofungicide",
        "name": "Trichoderma Harzianum / Viride Bio-Drench",
        "category": "Beneficial Antagonistic Fungi",
        "target_pests": ["Root Rot", "Damping-Off", "Collar Rot", "Fusarium Wilt", "Rhizoctonia"],
        "active_compound": "Live antagonistic fungus (*Trichoderma harzianum* / *viride*)",
        "recipe": {
            "ingredients": ["Trichoderma powder: 10 grams", "Jaggery / Molasses: 5 grams", "Clean water: 1 Liter"],
            "preparation_steps": [
                "1. Dissolve 5g jaggery in 1L water as a starter food for the beneficial spores.",
                "2. Add 10g of Trichoderma bio-powder and stir gently.",
                "3. Let it rest for 2 to 3 hours in the shade to activate.",
            ],
            "application_protocol": "Drench 200–300 ml of the solution directly around the root zone of each grow bag before transplanting and every 21 days thereafter.",
            "safety_precautions": "Do not mix with chemical fungicides or apply in direct scorching sun. Store bio-powder in a cool, dry place.",
        },
    },
    {
        "id": "wood-ash-potassium-dust",
        "name": "Natural Hardwood Ash Dusting & Soil Sweetener",
        "category": "Mineral Pest Barrier & Potassium Fertilizer",
        "target_pests": ["Flea Beetles", "Aphids", "Slugs", "Cutworms", "Powdery Mildew"],
        "active_compound": "Potassium carbonate, Calcium oxide, and Silica crystals",
        "recipe": {
            "ingredients": ["Clean pure hardwood ash (from unpainted firewood): 1 cup"],
            "preparation_steps": ["1. Sift dry wood ash through a fine kitchen sieve to remove large charcoal chunks."],
            "application_protocol": "Dust lightly over morning-dew damp leaves to deter leaf-chewing beetles. Sprinkle a 1-inch ring around container rims to stop crawling cutworms and snails.",
            "safety_precautions": "Wood ash raises soil pH (alkaline). Use moderately (max 1 tablespoon per 12x12 bag monthly) and avoid on acid-loving crops (blueberries, potatoes).",
        },
    },
    {
        "id": "baking-soda-potassium-bicarbonate",
        "name": "Baking Soda / Potassium Bicarbonate Mildew Cure",
        "category": "Mineral Foliar Spray",
        "target_pests": ["Powdery Mildew", "Black Spot", "Blight spores"],
        "active_compound": "Sodium / Potassium Bicarbonate (pH disruptor)",
        "recipe": {
            "ingredients": ["Baking soda (or Potassium bicarbonate): 1 teaspoon (5g)", "Vegetable cooking oil: 1 teaspoon (5ml)", "Liquid soap: 2 drops", "Water: 1 Liter"],
            "preparation_steps": ["1. Dissolve baking soda in water, then add oil and soap. Shake well to emulsify."],
            "application_protocol": "Spray affected foliage at first sign of white fungal powder. The alkaline pH arrests fungal germination.",
            "safety_precautions": "Do not exceed dosage to prevent sodium build-up in container soil.",
        },
    },
]


# ==============================================================================
# 2. ORGANIC BIO-FERTILIZERS & NPK DATASET
# ==============================================================================
ORGANIC_FERTILIZERS: List[Dict[str, Any]] = [
    {
        "id": "liquid-jeevamrut",
        "name": "Liquid Jeevamrut (Fermented Microbial Biostimulant)",
        "category": "Liquid Bio-Fertilizer & Soil Probiotic",
        "npk_profile": "Rich in microbial biomass, auxins, cytokinins, and micro-nutrients (N: 1.5%, P: 0.4%, K: 1.2%)",
        "shelf_life": "Use within 7 to 10 days of preparation",
        "recipe": {
            "batch_size": "20 Liters Home Terrace Batch",
            "ingredients": [
                "Fresh Cow Dung: 1 kg",
                "Cow Urine (Gomutra): 1 Liter",
                "Organic Jaggery / Molasses: 100 grams",
                "Pulse Flour (Besan / Chickpea / Gram flour): 100 grams",
                "Virgin Living Soil (Rhizosphere soil under a banyan/neem tree): 1 handful (50g)",
                "Water: 18 Liters",
            ],
            "preparation_steps": [
                "1. In a clean 25L plastic drum, mix 18L clean water with cow dung and cow urine.",
                "2. Dissolve jaggery and pulse flour in a small bucket of water, then stir into the drum.",
                "3. Add the handful of virgin fertile soil containing billions of native soil microbes.",
                "4. Stir the barrel clockwise for 2 minutes with a wooden stick.",
                "5. Cover with a breathable burlap/jute sack and keep in shaded terrace area for 4 to 5 days, stirring twice daily.",
            ],
            "dosage_and_application": "Dilute 100 ml of fermented Jeevamrut in 1 Liter of clean water (1:10 ratio). Pour 250–500 ml per grow bag at root zone every 14 days, or spray as a 5% foliar mist.",
        },
    },
    {
        "id": "panchagavya",
        "name": "Panchagavya Master Tonic",
        "category": "Immunity Booster & Growth Hormone Tonic",
        "npk_profile": "Macro & Micro nutrients with gibberellins, auxins, and Lactobacillus (N: 1.8%, P: 0.8%, K: 1.5%)",
        "shelf_life": "Up to 6 months in shade",
        "recipe": {
            "batch_size": "10 Liters Batch",
            "ingredients": [
                "Cow dung: 1 kg",
                "Cow ghee: 100 grams",
                "Cow urine: 1 Liter",
                "Cow milk: 500 ml",
                "Cow curd: 500 ml",
                "Tender coconut water: 500 ml",
                "Sugarcane juice or jaggery water: 500 ml",
                "Ripened bananas: 2 mashed",
            ],
            "preparation_steps": [
                "1. Blend cow dung and ghee, keep in pot for 3 days.",
                "2. On day 4, add urine and water, stir daily for 10 days.",
                "3. On day 15, add milk, curd, coconut water, jaggery water, and mashed bananas.",
                "4. Stir twice daily for another 15 days in shade.",
            ],
            "dosage_and_application": "Dilute 30 ml Panchagavya in 1 Liter water (3% solution). Spray on foliage during flowering and fruit setting to double fruit size and prevent blossom drop.",
        },
    },
    {
        "id": "vermicompost-gold",
        "name": "Enriched Vermicompost (Black Gold)",
        "category": "Solid Humus & Slow-Release Nutrition",
        "npk_profile": "N: 2.5% - 3.0%, P: 1.5% - 2.0%, K: 1.5% - 2.0% + Humic & Fulvic acids",
        "shelf_life": "12 months in moisture-sealed bag",
        "recipe": {
            "ingredients": ["Pure earthworm castings (*Eisenia foetida*)", "Enriched with 5% Neem cake and 1% *Trichoderma*"],
            "dosage_and_application": "Mix 1 to 2 handfuls (100–200 grams) into the top 2 inches of container soil per plant every 25 to 30 days. Water immediately after application.",
        },
    },
    {
        "id": "banana-peel-potassium-tea",
        "name": "Fermented Banana Peel Potassium Tea",
        "category": "Organic Potassium & Flower Booster",
        "npk_profile": "Rich in bioavailable Potassium (K: 3.5%), Magnesium, and Calcium",
        "shelf_life": "Use within 5 days",
        "recipe": {
            "ingredients": ["Chopped ripe banana peels: 4-5 peels", "Clean water: 2 Liters", "Jaggery: 1 teaspoon"],
            "preparation_steps": [
                "1. Chop banana peels into small pieces.",
                "2. Place in a sealed mason jar with 2L water and 1 tsp jaggery.",
                "3. Let ferment for 48 to 72 hours in a dark cupboard.",
                "4. Strain the amber liquid.",
            ],
            "dosage_and_application": "Dilute 1:1 with water and feed 300 ml per flowering tomato/chilli/brinjal plant every 10 days for abundant, firm fruit setting.",
        },
    },
    {
        "id": "eggshell-calcium-tea",
        "name": "Water-Soluble Eggshell Calcium Tea",
        "category": "Calcium Booster (Anti-Blossom End Rot)",
        "npk_profile": "Bio-available Calcium (Ca: 95% Calcium carbonate) and trace minerals",
        "shelf_life": "6 months",
        "recipe": {
            "ingredients": ["Clean crushed eggshells: 100 grams", "Natural apple cider or sugarcane vinegar: 500 ml"],
            "preparation_steps": [
                "1. Toast clean eggshells in a pan on low flame for 5 minutes (do not burn).",
                "2. Crush into coarse grit and drop into a glass jar.",
                "3. Pour 500ml vinegar over shells (it will fizz vigorously releasing calcium acetate).",
                "4. Seal loosely and let sit for 7 days until fizzing stops completely. Strain liquid.",
            ],
            "dosage_and_application": "Dilute 5 ml of calcium extract in 1 Liter of water (1:200 ratio). Spray directly on foliage to cure and prevent blossom end rot in tomatoes and capsicums.",
        },
    },
]


# ==============================================================================
# 3. COMPANION PLANTING & GUILD MATRIX
# ==============================================================================
COMPANION_MATRIX: Dict[str, Dict[str, Any]] = {
    "tomato": {
        "crop": "Tomato",
        "icon": "🍅",
        "best_companions": [
            {"name": "French Marigold", "role": "Exudes alpha-terthienyl from roots to kill root-knot nematodes and repels whiteflies."},
            {"name": "Sweet Basil", "role": "Repels tomato hornworms, thrips, and aphids while enhancing tomato sweetness."},
            {"name": "Garlic / Onion", "role": "Pungent sulphur aroma repels red spider mites and deter aphids."},
            {"name": "Carrot", "role": "Breaks lower soil and does not compete with tomato for upper sunlight."},
        ],
        "antagonists": [
            {"name": "Potato", "reason": "Shares identical fungal blight (*Phytophthora*) and potato beetles."},
            {"name": "Fennel", "reason": "Secretes growth-inhibiting allelopathic compounds that stunt tomato stems."},
            {"name": "Brassicas (Cabbage/Broccoli)", "reason": "High calcium/nitrogen competition in small containers."},
        ],
        "guild_tip": "The 'Trio Guild' of 1 Tomato + 1 Basil + 1 Dwarf Marigold in a 15x15 grow bag provides 100% natural pest shield with zero chemicals.",
    },
    "chilli": {
        "crop": "Chilli Pepper",
        "icon": "🌶️",
        "best_companions": [
            {"name": "Sweet Basil", "role": "Masks chilli aroma against thrips and aphids."},
            {"name": "Onion / Shallots", "role": "Repels mites and fungal leaf spot vectors."},
            {"name": "Coriander", "role": "Attracts beneficial hoverflies whose larvae devour green aphids."},
        ],
        "antagonists": [
            {"name": "Fennel", "reason": "Attracts swallowtail caterpillars and stunts pepper growth."},
            {"name": "Beans (Climbing)", "reason": "Aggressive climbing beans can strangle and shade pepper bush."},
        ],
        "guild_tip": "Plant Coriander in a shallow ring around your Chilli grow bag to attract predatory beneficial wasps.",
    },
    "cucumber": {
        "crop": "Cucumber",
        "icon": "🥒",
        "best_companions": [
            {"name": "Sunflower / Corn", "role": "Acts as a living vertical trellis and windbreak on rooftops."},
            {"name": "Dill", "role": "Attracts ladybird beetles and parasitic wasps."},
            {"name": "Radish", "role": "Repels cucumber beetles and flea beetles."},
        ],
        "antagonists": [
            {"name": "Aromatic Sage", "reason": "Stunts cucumber vine vigor."},
            {"name": "Potato", "reason": "Increases susceptibility to early blight spores."},
        ],
        "guild_tip": "Train cucumbers vertically up a nylon trellis and plant fast radishes around the bag base for pest deterrence.",
    },
    "spinach": {
        "crop": "Spinach (Palak)",
        "icon": "🥬",
        "best_companions": [
            {"name": "Strawberries", "role": "Complementary root depth and moisture retention."},
            {"name": "Radish", "role": "Fast harvest frees root space for broad spinach leaves."},
            {"name": "Peas / Beans", "role": "Fix atmospheric nitrogen directly to feed nitrogen-hungry spinach."},
        ],
        "antagonists": [
            {"name": "Fennel", "reason": "Allelopathic suppression of seedling emergence."},
        ],
        "guild_tip": "Intercrop Spinach with bush peas in rectangular trays for continuous natural nitrogen supply.",
    },
}


# ==============================================================================
# 4. THERMAL HOT WATER SEED TREATMENT CHART
# ==============================================================================
SEED_TREATMENTS: List[Dict[str, Any]] = [
    {
        "crop_group": "Potato Tubers & Banana Suckers",
        "crops": ["Potato", "Banana"],
        "temp_celsius": 55,
        "temp_fahrenheit": 131,
        "immersion_minutes": 10,
        "target_pathogens": ["Blackleg infection (*Erwinia*)", "Powdery scab", "Black scurf (*Rhizoctonia*)", "Nematodes & banana weevils"],
    },
    {
        "crop_group": "Solanaceous & Leafy Vegetables",
        "crops": ["Tomato", "Pepper / Chilli", "Eggplant (Brinjal)", "Spinach", "Brussels Sprouts", "Cabbage"],
        "temp_celsius": 50,
        "temp_fahrenheit": 122,
        "immersion_minutes": 30,
        "target_pathogens": ["Black rot (*Xanthomonas*)", "Bacterial canker", "*Alternaria* blight", "*Septoria* leaf spot", "*Phoma*"],
    },
    {
        "crop_group": "Crucifers & Root Crops",
        "crops": ["Broccoli", "Cauliflower", "Carrot", "Collard", "Kale", "Kohlrabi", "Turnip"],
        "temp_celsius": 50,
        "temp_fahrenheit": 122,
        "immersion_minutes": 20,
        "target_pathogens": ["Black rot (*Xanthomonas campestris*)", "Bacterial leaf blight", "Downy mildew seed spores"],
    },
    {
        "crop_group": "Fast Greens & Small Seeds",
        "crops": ["Mustard", "Cress", "Radish"],
        "temp_celsius": 50,
        "temp_fahrenheit": 122,
        "immersion_minutes": 15,
        "target_pathogens": ["Damping-off fungal spores", "Bacterial leaf spot"],
    },
    {
        "crop_group": "Salad Greens & Apiaceae",
        "crops": ["Lettuce", "Celery", "Celeriac"],
        "temp_celsius": 47,
        "temp_fahrenheit": 116.6,
        "immersion_minutes": 30,
        "target_pathogens": ["Bacterial leaf spot", "Septoria celery blight", "Internal fungal mycelium"],
    },
]


# ==============================================================================
# 5. ROOFTOP STRUCTURAL LOAD & POTTING MIX CALCULATOR
# ==============================================================================
def calculate_rooftop_load(
    container_count: int,
    container_size_liters: float,
    terrace_area_sqm: float,
    soil_type: str = "3:1:1_cocopeat_mix",
) -> Dict[str, Any]:
    """Calculate rooftop live load in kg/m², safety compliance, and potting mix recipe volume in liters."""
    # Saturated wet densities (kg/liter)
    densities = {
        "3:1:1_cocopeat_mix": 0.45,   # Lightweight 3:1:1 cocopeat + vermicompost + perlite
        "cocopeat_vermicompost": 0.50, # 50:50 cocopeat + compost
        "traditional_topsoil": 1.60,   # Red soil / garden mud (DANGEROUS)
    }

    selected_density = densities.get(soil_type, 0.45)
    total_volume_liters = container_count * container_size_liters
    total_soil_weight_kg = total_volume_liters * selected_density
    
    # Plant biomass + container bag + drainage tray weight allowance (10%)
    total_wet_load_kg = total_soil_weight_kg * 1.10
    
    # Effective load per square meter
    load_per_sqm = total_wet_load_kg / max(1.0, terrace_area_sqm)
    
    # Standard residential roof limit: 150 kg/m² to 200 kg/m²
    safe_limit = 150.0
    is_safe = load_per_sqm <= safe_limit
    safety_ratio = round((load_per_sqm / safe_limit) * 100, 1)

    # 3:1:1 Recipe Formulation Volumes (Liters)
    cocopeat_liters = round(total_volume_liters * (3 / 5), 1)
    vermicompost_liters = round(total_volume_liters * (1 / 5), 1)
    perlite_liters = round(total_volume_liters * (1 / 5), 1)
    neem_cake_kg = round(container_count * 0.15, 2)  # 150g per container

    status_verdict = "SAFE" if is_safe else "EXCEEDS_SAFE_LIMIT"
    recommendation = (
        f"Your proposed setup generates {load_per_sqm:.1f} kg/m², which is within the safe residential roof live-load limit (150 kg/m²). "
        "Place containers along structural perimeter beams or over load-bearing pillars."
        if is_safe else
        f"WARNING: Your proposed setup generates {load_per_sqm:.1f} kg/m², which EXCEEDS safe roof live-load limits (150 kg/m²). "
        "Switch from heavy topsoil to lightweight 3:1:1 cocopeat mix or distribute containers over a larger terrace area."
    )

    return {
        "status": status_verdict,
        "is_safe": is_safe,
        "total_containers": container_count,
        "container_size_liters": container_size_liters,
        "total_mix_volume_liters": round(total_volume_liters, 1),
        "soil_type": soil_type,
        "total_wet_weight_kg": round(total_wet_load_kg, 1),
        "terrace_area_sqm": terrace_area_sqm,
        "load_kg_per_sqm": round(load_per_sqm, 2),
        "safe_limit_kg_per_sqm": safe_limit,
        "safety_capacity_used_pct": safety_ratio,
        "structural_recommendation": recommendation,
        "potting_mix_breakdown_liters": {
            "cocopeat": cocopeat_liters,
            "vermicompost": vermicompost_liters,
            "perlite_or_pumice": perlite_liters,
            "recommended_neem_cake_kg": neem_cake_kg,
        },
    }


# ==============================================================================
# 6. GOVERNMENT ORGANIC SCHEMES & CERTIFICATIONS
# ==============================================================================
GOVERNMENT_SCHEMES: List[Dict[str, Any]] = [
    {
        "id": "pkvy",
        "name": "Paramparagat Krishi Vikas Yojana (PKVY)",
        "ministry": "Ministry of Agriculture & Farmers Welfare, Govt of India",
        "financial_assistance": "Rs. 50,000 per hectare for 3 years",
        "subsidy_details": "62% of assistance (Rs. 31,000/ha) is provided directly as financial incentive for organic inputs (bio-fertilizers, vermicompost, botanical extracts).",
        "certification_type": "PGS-India (Participatory Guarantee System)",
        "eligibility": "Cluster-based farming groups (minimum 20 hectares / 50 farmers per cluster) adopting organic practices.",
    },
    {
        "id": "movcdner",
        "name": "Mission Organic Value Chain Development for North Eastern Region (MOVCDNER)",
        "ministry": "Ministry of Agriculture, Govt of India",
        "financial_assistance": "Rs. 25,000 per hectare for 3 years + Up to Rs. 2 Crore per FPO",
        "subsidy_details": "Support for organic inputs, Farmer Producer Organizations (FPOs), capacity building, and cold-chain post-harvest infrastructure.",
        "certification_type": "Third-Party NPOP Export Certification",
        "eligibility": "Farmers and FPOs across 8 North-Eastern states focusing on organic niche crops.",
    },
    {
        "id": "ciss-soil-health",
        "name": "Capital Investment Subsidy Scheme (CISS) for Waste Compost Units",
        "ministry": "National Centre for Organic and Natural Farming (NCONF)",
        "financial_assistance": "100% assistance up to Rs. 190 Lakh for Government units; Up to 33% (Rs. 63 Lakh) for Private entrepreneurs",
        "subsidy_details": "Capital grant for setting up mechanized fruit/vegetable and agro-waste compost production units (3,000 TPA capacity).",
        "certification_type": "FCO (Fertilizer Control Order) Organic Standards",
        "eligibility": "Individuals, APMCs, Cooperatives, and State Government Agencies.",
    },
    {
        "id": "npop-tracenet",
        "name": "APEDA Tracenet & National Programme for Organic Production (NPOP)",
        "ministry": "Ministry of Commerce & Industry, Govt of India",
        "financial_assistance": "Global Export Market Accreditation",
        "subsidy_details": "Equivalence recognition with European Union, Switzerland, and USA for certified unprocessed plant products.",
        "certification_type": "NPOP 3-Year Renewable Organic Certificate",
        "eligibility": "Grower groups (25 to 500 smallholder farmers) with Internal Control Systems (ICS) or commercial farms.",
    },
]


# ==============================================================================
# 7. ROOFTOP CROP CATALOG
# ==============================================================================
ROOFTOP_CROPS: List[Dict[str, Any]] = [
    {"id": "tomato", "name": "Tomato", "icon": "🍅", "season": "Kharif / Rabi (Aug-Nov & Jan-Feb)", "container_depth_inches": 12, "germination_days": 6, "harvest_days": 85, "sunlight_hours": "6-8 hrs", "water_ml_day": 800, "ph_range": "6.0 - 6.8"},
    {"id": "chilli", "name": "Chilli Pepper", "icon": "🌶️", "season": "All Year (Warm climate)", "container_depth_inches": 10, "germination_days": 8, "harvest_days": 90, "sunlight_hours": "6-8 hrs", "water_ml_day": 600, "ph_range": "6.0 - 6.5"},
    {"id": "eggplant", "name": "Eggplant (Brinjal)", "icon": "🍆", "season": "Kharif / Summer (Feb-Mar & Jun-Jul)", "container_depth_inches": 12, "germination_days": 7, "harvest_days": 80, "sunlight_hours": "6 hrs", "water_ml_day": 900, "ph_range": "5.5 - 6.5"},
    {"id": "spinach", "name": "Spinach (Palak)", "icon": "🥬", "season": "Rabi / Winter (Sep-Dec)", "container_depth_inches": 6, "germination_days": 4, "harvest_days": 40, "sunlight_hours": "4-5 hrs", "water_ml_day": 400, "ph_range": "6.5 - 7.0"},
    {"id": "coriander", "name": "Coriander (Dhaniya)", "icon": "🌿", "season": "All Year (Oct-Feb optimal)", "container_depth_inches": 6, "germination_days": 6, "harvest_days": 38, "sunlight_hours": "3-5 hrs (Partial shade)", "water_ml_day": 350, "ph_range": "6.2 - 6.8"},
    {"id": "cucumber", "name": "Cucumber", "icon": "🥒", "season": "Summer / Zaid (Feb-Mar & Jun-Jul)", "container_depth_inches": 15, "germination_days": 5, "harvest_days": 60, "sunlight_hours": "6 hrs", "water_ml_day": 1200, "ph_range": "6.0 - 7.0"},
    {"id": "okra", "name": "Okra (Bhindi)", "icon": "🫑", "season": "Summer / Rainy (Feb-Apr & Jun-Jul)", "container_depth_inches": 12, "germination_days": 5, "harvest_days": 60, "sunlight_hours": "6-8 hrs", "water_ml_day": 700, "ph_range": "6.0 - 6.8"},
    {"id": "mint", "name": "Mint (Pudina)", "icon": "🌱", "season": "All Year (Summer vigorous)", "container_depth_inches": 6, "germination_days": 7, "harvest_days": 35, "sunlight_hours": "4-5 hrs", "water_ml_day": 400, "ph_range": "6.0 - 7.0"},
]


# ==============================================================================
# 8. ROOFTOP MICROCLIMATE & WEATHER ADVISOR
# ==============================================================================
def get_weather_microclimate_advice(
    temp_celsius: float,
    humidity_pct: float = 60.0,
    wind_kmh: float = 12.0,
    uv_index: float = 6.0,
) -> Dict[str, Any]:
    """Generate dynamic rooftop care and plant protection advisories based on weather conditions."""
    alerts = []
    actions = []

    # Temperature Alerts
    if temp_celsius >= 35.0:
        alerts.append("🔥 High Heatwave Alert on Rooftop")
        actions.append("Deploy 50% Green Agro-Shade Net over sensitive crops (Tomatoes, Capsicum, Coriander).")
        actions.append("Water containers twice daily (early morning before 7 AM and evening after 5:30 PM).")
        actions.append("Replenish topsoil mulch with 2 inches of dried leaves to prevent root zone baking.")
    elif temp_celsius <= 12.0:
        alerts.append("❄️ Cold Stress & Frost Risk")
        actions.append("Cover night crops with breathable non-woven fleece or move small bags near heat-radiating walls.")
        actions.append("Reduce watering frequency to prevent root chills and fungal root rot.")
    else:
        alerts.append("🌱 Optimal Rooftop Growing Temperature (20°C - 30°C)")
        actions.append("Ideal conditions for foliar bio-fertilizer spraying (Jeevamrut / Panchagavya).")

    # Wind Alerts
    if wind_kmh >= 25.0:
        alerts.append("💨 Fierce Terrace Wind Alert")
        actions.append("Inspect and reinforce bamboo stakes on tall fruiting plants (Tomatoes, Brinjal, Okra).")
        actions.append("Move lighter pots closer to parapet wall barriers.")

    # Humidity & Fungal Alerts
    if humidity_pct >= 80.0:
        alerts.append("🌧️ High Humidity & Fungal Risk Alert")
        actions.append("Avoid watering leaves directly; water strictly at soil base to prevent fungal spores.")
        actions.append("Proactively spray sour buttermilk (1:10) or Trichoderma to prevent powdery mildew and blight.")

    return {
        "temperature_celsius": temp_celsius,
        "humidity_percentage": humidity_pct,
        "wind_speed_kmh": wind_kmh,
        "uv_index": uv_index,
        "alerts": alerts,
        "actionable_care_steps": actions,
    }
