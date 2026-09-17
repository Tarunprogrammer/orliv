"""Real-time Agronomy Lifecycle Engine: Calculates crop age, stages, water, nutrients, and daily care tasks."""

from datetime import date, datetime
from typing import Dict, Any, List, Optional

# Curated Rooftop Organic Crop Knowledge Templates
CROP_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "tomato": {
        "name": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "icon": "🍅",
        "default_variety": "Arka Rakshak / Pusa Ruby",
        "total_days": 85,
        "recommended_pot": "12x12 or 15x15 inch HDPE Grow Bag (1 plant per bag)",
        "sunlight_req": "6 to 8 hours direct sunlight",
        "stages": [
            {
                "name": "Sowing & Germination",
                "days": (1, 7),
                "summary": "Keep seedling tray in warm shaded area. Keep soil moist like a squeezed sponge.",
                "water_ml": 150,
                "water_tip": "Gentle mist spray in the morning. Avoid water logging.",
                "feed_tip": "No fertilizer needed yet; seedling feeds on seed reserves.",
                "roof_tip": "Protect tray from strong terrace winds and direct burning sun.",
            },
            {
                "name": "Seedling Hardening & Transplanting",
                "days": (8, 25),
                "summary": "True leaves appear. Transplant strong seedling into final 12x12 grow bag with 3:1:1 mix.",
                "water_ml": 350,
                "water_tip": "Water early in the morning around the base, not on leaves.",
                "feed_tip": "Mix 2 tablespoons of Neem cake into potting mix to prevent root nematodes.",
                "roof_tip": "Place grow bag near a perimeter beam or east-facing wall for stable support.",
            },
            {
                "name": "Vegetative Growth & Staking",
                "days": (26, 45),
                "summary": "Rapid vertical growth. Install sturdy bamboo stake or trellis string. Prune lower suckers.",
                "water_ml": 600,
                "water_tip": "Increase watering to 600ml daily. Mulch topsoil with 2 inches of dried leaves.",
                "feed_tip": "Drench roots with 1:10 diluted liquid Jeevamrut every 14 days.",
                "roof_tip": "Tie main stem loosely with soft jute twine to withstand rooftop winds.",
            },
            {
                "name": "Flowering & Pollination",
                "days": (46, 65),
                "summary": "Bright yellow flowers bloom. Gently tap stakes at noon to assist self-pollination.",
                "water_ml": 800,
                "water_tip": "Maintain steady moisture. Dry soil followed by heavy watering causes blossom drop.",
                "feed_tip": "Top-dress with 1 cup vermicompost mixed with 1 tablespoon wood ash (for potassium).",
                "roof_tip": "Deploy 50% green agro-shade net if rooftop temperature exceeds 35°C.",
            },
            {
                "name": "Fruit Setting & Ripening",
                "days": (66, 85),
                "summary": "Green fruit clusters swell and turn deep red. Keep regular watering to prevent split skin.",
                "water_ml": 900,
                "water_tip": "Consistent morning watering (800–1000 ml). Ensure bottom drainage holes flow freely.",
                "feed_tip": "Spray sour buttermilk solution (1:10 dilution) every 10 days to prevent powdery mildew.",
                "roof_tip": "Inspect drainage trays under bags to prevent rooftop water pooling.",
            },
            {
                "name": "Harvesting & Rejuvenation",
                "days": (86, 120),
                "summary": "Harvest firm red tomatoes with shears. After harvest, revitalize soil with fresh compost.",
                "water_ml": 600,
                "water_tip": "Moderate watering to maintain continued harvesting.",
                "feed_tip": "Add a handful of bone meal / rock phosphate for secondary fruit flushes.",
                "roof_tip": "Compost spent vines in your terrace aerobic bin; never burn on roof.",
            },
        ],
        "preset_tasks": [
            {"day": 1, "stage": "Sowing", "title": "Sow Tomato Seeds", "desc": "Sow 2-3 seeds 0.5 cm deep in seedling cup or tray. Mist with water.", "cat": "water"},
            {"day": 5, "stage": "Germination", "title": "Check Seedling Sprouting", "desc": "Move sprouted seeds into bright indirect sunlight.", "cat": "sun_safety"},
            {"day": 20, "stage": "Transplanting", "title": "Transplant to 12x12 Grow Bag", "desc": "Fill grow bag with 3:1:1 cocopeat mix + 200g neem cake. Plant the healthiest seedling deep up to its first leaves.", "cat": "nutrient"},
            {"day": 28, "stage": "Vegetative", "title": "First Jeevamrut Drench", "desc": "Mix 100ml liquid Jeevamrut in 1 liter water and pour around root zone.", "cat": "nutrient"},
            {"day": 35, "stage": "Vegetative", "title": "Stake & Prune Suckers", "desc": "Insert 5-foot bamboo stake. Pinch out small diagonal suckers growing in leaf armpits.", "cat": "pruning"},
            {"day": 42, "stage": "Vegetative", "title": "Apply Organic Leaf Mulch", "desc": "Spread 2 inches of dried leaves or straw over bag topsoil to lock moisture.", "cat": "water"},
            {"day": 50, "stage": "Flowering", "title": "Flower Bloom & Tap Pollination", "desc": "Gently shake plant stem at noon to aid pollination. Add 1 cup vermicompost.", "cat": "nutrient"},
            {"day": 60, "stage": "Flowering", "title": "Preventive Neem Oil Spray", "desc": "Mix 5ml pure neem oil + 2 drops liquid soap in 1L water. Spray under leaves in evening.", "cat": "pest"},
            {"day": 72, "stage": "Fruit Setting", "title": "Calcium & Potassium Boost", "desc": "Add eggshell tea or a sprinkle of wood ash to prevent blossom end rot.", "cat": "nutrient"},
            {"day": 85, "stage": "Harvest", "title": "First Tomato Harvest!", "desc": "Pick ripe red tomatoes. Twist gently or snip with clean garden shears.", "cat": "general"},
        ],
    },
    "chilli": {
        "name": "Chilli Pepper",
        "scientific_name": "Capsicum annuum",
        "icon": "🌶️",
        "default_variety": "Pusa Jwala / Bird's Eye",
        "total_days": 90,
        "recommended_pot": "10x10 or 12x12 inch HDPE Grow Bag",
        "sunlight_req": "6 to 8 hours bright sunlight",
        "stages": [
            {"name": "Sowing & Germination", "days": (1, 10), "summary": "Chilli seeds take 7-10 days to sprout at warm temperatures (25-30°C).", "water_ml": 150, "water_tip": "Keep top layer moist with fine mister.", "feed_tip": "None needed yet.", "roof_tip": "Keep in warm sheltered spot."},
            {"name": "Seedling & Hardening", "days": (11, 30), "summary": "Grow to 4-5 true leaves before transplanting into final bag.", "water_ml": 300, "water_tip": "Water every 2 days once top inch is dry.", "feed_tip": "Incorporate vermicompost & neem cake in grow bag.", "roof_tip": "Place near south/east rooftop wall."},
            {"name": "Vegetative & Branching", "days": (31, 50), "summary": "Pinch the main growing tip at Day 35 to encourage bushy lateral branches.", "water_ml": 500, "water_tip": "Water thoroughly in early morning.", "feed_tip": "Apply Jeevamrut drench every 14 days.", "roof_tip": "Light windbreak against fierce gusts."},
            {"name": "Flowering & Fruit Set", "days": (51, 75), "summary": "Small white flowers bloom and transform into green chillies.", "water_ml": 600, "water_tip": "Do not overwater; mild stress enhances chilli pungency.", "feed_tip": "Spray sour buttermilk (1:10) to repel mites & curl virus.", "roof_tip": "Shade net during peak heat waves."},
            {"name": "Harvesting", "days": (76, 120), "summary": "Continuous harvest of green or fiery red chillies every week.", "water_ml": 500, "water_tip": "Regular moderate watering.", "feed_tip": "Top-dress with vermicompost monthly.", "roof_tip": "Harvest with scissors to protect branch stems."},
        ],
        "preset_tasks": [
            {"day": 1, "stage": "Sowing", "title": "Sow Chilli Seeds", "desc": "Sow seeds 0.5cm deep in warm seed tray. Keep moist.", "cat": "water"},
            {"day": 25, "stage": "Transplanting", "title": "Transplant Chilli to 12x12 Bag", "desc": "Transplant into 3:1:1 mix with a handful of vermicompost.", "cat": "nutrient"},
            {"day": 35, "stage": "Vegetative", "title": "Pinch Main Tip for Bushy Growth", "desc": "Snip the top 1 cm of main stem to trigger multiple side branches.", "cat": "pruning"},
            {"day": 45, "stage": "Vegetative", "title": "Sour Buttermilk Mist", "desc": "Spray 100ml fermented buttermilk in 1L water to keep leaves glossy and curl-free.", "cat": "pest"},
            {"day": 65, "stage": "Flowering", "title": "Potassium & Compost Feed", "desc": "Add 2 tablespoons wood ash around edges to support heavy pod bearing.", "cat": "nutrient"},
            {"day": 85, "stage": "Harvest", "title": "Harvest Green Chillies", "desc": "Snip fresh green chillies for your kitchen!", "cat": "general"},
        ],
    },
    "eggplant": {
        "name": "Eggplant (Brinjal)",
        "scientific_name": "Solanum melongena",
        "icon": "🍆",
        "default_variety": "Pusa Purple / Round Black",
        "total_days": 80,
        "recommended_pot": "12x12 or 15x15 inch Grow Bag",
        "sunlight_req": "6 hours sunlight",
        "stages": [
            {"name": "Sowing", "days": (1, 8), "summary": "Seeds sprout in 5-8 days.", "water_ml": 150, "water_tip": "Gentle misting.", "feed_tip": "None.", "roof_tip": "Warm, sunny nursery."},
            {"name": "Seedling", "days": (9, 25), "summary": "Transplant strong seedling with sturdy stem.", "water_ml": 400, "water_tip": "Morning watering.", "feed_tip": "Neem cake 200g in pot.", "roof_tip": "Place near structural columns."},
            {"name": "Vegetative", "days": (26, 45), "summary": "Large broad velvet leaves develop. Stake plant.", "water_ml": 700, "water_tip": "Heavy water feeder.", "feed_tip": "Jeevamrut / Panchagavya drench.", "roof_tip": "Stake firmly against winds."},
            {"name": "Flowering & Fruit", "days": (46, 75), "summary": "Purple flowers produce glossy brinjals.", "water_ml": 900, "water_tip": "Daily 800-1000ml in warm weather.", "feed_tip": "Top-dress with vermicompost.", "roof_tip": "Check drainage."},
            {"name": "Harvest", "days": (76, 110), "summary": "Pick glossy brinjals before seeds harden inside.", "water_ml": 700, "water_tip": "Steady watering.", "feed_tip": "Bi-weekly liquid compost tea.", "roof_tip": "Snip with clean pruners."},
        ],
        "preset_tasks": [
            {"day": 1, "stage": "Sowing", "title": "Sow Brinjal Seeds", "desc": "Sow in seed cups 0.5cm deep.", "cat": "water"},
            {"day": 22, "stage": "Transplanting", "title": "Transplant to 14-inch Bag", "desc": "Plant in 3:1:1 cocopeat mix with 1 cup compost.", "cat": "nutrient"},
            {"day": 35, "stage": "Vegetative", "title": "Install Bamboo Support", "desc": "Tie main stem to stake to support heavy future fruits.", "cat": "pruning"},
            {"day": 50, "stage": "Flowering", "title": "Inspect for Shoot Borer", "desc": "Examine top growing shoots; prune any wilted tips.", "cat": "pest"},
            {"day": 75, "stage": "Harvest", "title": "Harvest Glossy Brinjals", "desc": "Cut fruits while skin is bright and glossy.", "cat": "general"},
        ],
    },
    "spinach": {
        "name": "Spinach (Palak)",
        "scientific_name": "Spinacia oleracea",
        "icon": "🥬",
        "default_variety": "All Green / Pusa Bharati",
        "total_days": 40,
        "recommended_pot": "6 to 8-inch deep wide rectangle planter tray",
        "sunlight_req": "4 to 5 hours direct or partial sunlight",
        "stages": [
            {"name": "Sowing & Sprouting", "days": (1, 5), "summary": "Fast-sprouting seeds. Soak seeds for 8 hours before sowing for 100% germination.", "water_ml": 200, "water_tip": "Keep surface consistently moist.", "feed_tip": "None.", "roof_tip": "Shallow trays are super lightweight on roof slabs."},
            {"name": "Early Growth & Thinning", "days": (6, 18), "summary": "Thin seedlings to 3 inches apart to give room for lush broad leaves.", "water_ml": 350, "water_tip": "Gentle shower watering in morning.", "feed_tip": "Spray mild liquid Jeevamrut (1:20).", "roof_tip": "Partial shade prevents leaf bitterness."},
            {"name": "Lush Vegetative & Cut-and-Come-Again", "days": (19, 45), "summary": "Harvest outer large leaves. The center core will continue producing new greens for 4-5 harvests!", "water_ml": 500, "water_tip": "Daily morning watering.", "feed_tip": "Top-dress with a thin layer of vermicompost after each cutting.", "roof_tip": "Coolest corner of the rooftop."},
        ],
        "preset_tasks": [
            {"day": 1, "stage": "Sowing", "title": "Pre-soak & Sow Spinach", "desc": "Soak seeds in water for 8 hours, then broadcast in wide shallow tray and cover with 1cm cocopeat.", "cat": "water"},
            {"day": 10, "stage": "Thinning", "title": "Thin Dense Seedlings", "desc": "Pluck excess crowded baby greens (eat them as delicious microgreens!).", "cat": "pruning"},
            {"day": 20, "stage": "Growth", "title": "Foliar Nitrogen Boost", "desc": "Spray diluted vermicompost tea or 5% Jeevamrut for vibrant green chlorophyll.", "cat": "nutrient"},
            {"day": 32, "stage": "Harvest", "title": "First Cut & Come Harvest", "desc": "Snip outer leaves 1 inch above soil level. Enjoy fresh organic palak!", "cat": "general"},
        ],
    },
    "cucumber": {
        "name": "Cucumber",
        "scientific_name": "Cucumis sativus",
        "icon": "🥒",
        "default_variety": "Japanese Long / Pusa Uday",
        "total_days": 60,
        "recommended_pot": "15x15 inch Grow Bag with trellis net",
        "sunlight_req": "6 hours sunlight",
        "stages": [
            {"name": "Direct Sowing", "days": (1, 6), "summary": "Fast-growing vine. Best sown directly into the final grow bag.", "water_ml": 250, "water_tip": "Keep moist.", "feed_tip": "Add 2 cups compost in mix.", "roof_tip": "Place bag against terrace parapet trellis."},
            {"name": "Vine Trellising", "days": (7, 25), "summary": "Tendrils reach for support. Train main vine up plastic or nylon trellis netting.", "water_ml": 600, "water_tip": "Deep watering.", "feed_tip": "Weekly Jeevamrut drench.", "roof_tip": "Secure trellis against wind drag."},
            {"name": "Flowering & Fruit", "days": (26, 50), "summary": "Yellow male and female flowers appear. Rapid fruit lengthening.", "water_ml": 1200, "water_tip": "High water requirement during fruiting (1-1.5L daily).", "feed_tip": "Wood ash + vermicompost top-dress.", "roof_tip": "Shade net during hot afternoons."},
            {"name": "Crisp Harvest", "days": (51, 75), "summary": "Pick crunchy green cucumbers before they turn yellow and seed-heavy.", "water_ml": 1000, "water_tip": "Consistent daily watering.", "feed_tip": "Compost tea.", "roof_tip": "Harvest every 2-3 days."},
        ],
        "preset_tasks": [
            {"day": 1, "stage": "Sowing", "title": "Direct Sow 2 Cucumber Seeds", "desc": "Plant 1 inch deep in 15x15 grow bag.", "cat": "water"},
            {"day": 14, "stage": "Trellising", "title": "Guide Tendrils to Trellis", "desc": "Gently tie young vine to vertical nylon netting.", "cat": "pruning"},
            {"day": 30, "stage": "Flowering", "title": "Sour Buttermilk Spray for Mildew", "desc": "Spray 1:10 sour buttermilk under leaves to prevent powdery mildew.", "cat": "pest"},
            {"day": 50, "stage": "Harvest", "title": "Harvest Crisp Cucumbers", "desc": "Cut crisp 6-8 inch green cucumbers with garden shears.", "cat": "general"},
        ],
    },
    "coriander": {
        "name": "Coriander (Dhaniya)",
        "scientific_name": "Coriandrum sativum",
        "icon": "🌿",
        "default_variety": "Pant Haritima / Multi-Cut",
        "total_days": 38,
        "recommended_pot": "6-inch deep wide planter box or tray",
        "sunlight_req": "3 to 5 hours morning sun (Partial Shade)",
        "stages": [
            {"name": "Cracking & Sowing", "days": (1, 6), "summary": "Gently crush whole round coriander seeds into two halves before sowing.", "water_ml": 200, "water_tip": "Gentle spray misting.", "feed_tip": "None.", "roof_tip": "Keep in shaded corner of terrace."},
            {"name": "Bushy Leaf Growth", "days": (7, 24), "summary": "Aromatic lacy leaves spread rapidly.", "water_ml": 350, "water_tip": "Moist soil; do not let dry out.", "feed_tip": "Mild Jeevamrut mist.", "roof_tip": "50% shade net prevents premature flowering/bolting."},
            {"name": "Fragrant Harvest", "days": (25, 45), "summary": "Snip fragrant green stems for fresh daily kitchen use.", "water_ml": 400, "water_tip": "Regular morning mist.", "feed_tip": "Thin vermicompost top-dress.", "roof_tip": "Snip outer stalks."},
        ],
        "preset_tasks": [
            {"day": 1, "stage": "Sowing", "title": "Split Seeds & Sow", "desc": "Gently roll whole seeds under a wooden block to split into halves. Broadcast evenly and cover lightly.", "cat": "water"},
            {"day": 15, "stage": "Growth", "title": "Morning Mist & Shade Check", "desc": "Ensure partial afternoon shade so coriander does not bolt into seed.", "cat": "sun_safety"},
            {"day": 30, "stage": "Harvest", "title": "Snip Fragrant Leaves", "desc": "Snip fresh aromatic coriander sprigs from the base.", "cat": "general"},
        ],
    },
}


def get_crop_realtime_status(crop_type: str, planted_date: date) -> Dict[str, Any]:
    """Calculate real-time crop age, active stage, and today's dynamic care instructions."""
    template = CROP_TEMPLATES.get(crop_type.lower(), CROP_TEMPLATES["tomato"])
    today = date.today()
    days_old = max(1, (today - planted_date).days + 1)
    total_days = template["total_days"]
    progress_pct = min(100, int((days_old / total_days) * 100))

    # Determine current stage
    current_stage_info = template["stages"][-1]
    for stage in template["stages"]:
        start_d, end_d = stage["days"]
        if start_d <= days_old <= end_d:
            current_stage_info = stage
            break

    days_to_harvest = max(0, total_days - days_old)

    return {
        "crop_type": crop_type.lower(),
        "crop_name": template["name"],
        "icon": template["icon"],
        "variety_default": template["default_variety"],
        "recommended_pot": template["recommended_pot"],
        "sunlight_req": template["sunlight_req"],
        "crop_age_days": days_old,
        "total_days": total_days,
        "days_to_harvest": days_to_harvest,
        "progress_percentage": progress_pct,
        "current_stage": current_stage_info["name"],
        "stage_summary": current_stage_info["summary"],
        "today_water_ml": current_stage_info["water_ml"],
        "water_tip": current_stage_info["water_tip"],
        "feed_tip": current_stage_info["feed_tip"],
        "roof_tip": current_stage_info["roof_tip"],
        "all_stages": template["stages"],
    }
