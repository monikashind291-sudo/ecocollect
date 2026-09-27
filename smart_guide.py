"""
Smart Waste Guide Module
Simple, fast, and 100% reliable rule-based categorization engine.
Categorizes waste items entered by the user into the appropriate recycling stream.
"""

# Knowledge base of items, category classifications, bin instructions, and eco-facts
WASTE_KNOWLEDGE_BASE = {
    # Plastic
    "plastic": "Plastic",
    "plastic bottle": "Plastic",
    "bottle": "Plastic",
    "water bottle": "Plastic",
    "soda bottle": "Plastic",
    "plastic bag": "Plastic",
    "polythene": "Plastic",
    "wrapper": "Plastic",
    "plastic wrapper": "Plastic",
    "plastic container": "Plastic",
    "container": "Plastic",
    "tupperware": "Plastic",
    "shampoo bottle": "Plastic",
    "detergent bottle": "Plastic",
    "milk jug": "Plastic",
    "straw": "Plastic",
    "plastic cup": "Plastic",
    "bubble wrap": "Plastic",
    "yogurt pot": "Plastic",
    "takeout container": "Plastic",
    "pvc": "Plastic",
    "plastic cutlery": "Plastic",
    "cling wrap": "Plastic",

    # Paper
    "paper": "Paper",
    "newspaper": "Paper",
    "news paper": "Paper",
    "magazine": "Paper",
    "book": "Paper",
    "old book": "Paper",
    "cardboard": "Paper",
    "cardboard box": "Paper",
    "carton": "Paper",
    "milk carton": "Paper",
    "egg carton": "Paper",
    "notebook": "Paper",
    "office paper": "Paper",
    "envelope": "Paper",
    "shipping box": "Paper",
    "paper bag": "Paper",
    "flyer": "Paper",
    "brochure": "Paper",
    "cereal box": "Paper",

    # Glass
    "glass": "Glass",
    "glass bottle": "Glass",
    "wine bottle": "Glass",
    "beer bottle": "Glass",
    "glass jar": "Glass",
    "jam jar": "Glass",
    "pickle jar": "Glass",
    "mason jar": "Glass",
    "broken glass": "Glass",
    "glass cup": "Glass",
    "tumbler": "Glass",
    "perfume bottle": "Glass",
    "glassware": "Glass",

    # Metal
    "metal": "Metal",
    "aluminium can": "Metal",
    "aluminum can": "Metal",
    "soda can": "Metal",
    "beer can": "Metal",
    "can": "Metal",
    "tin can": "Metal",
    "tin": "Metal",
    "foil": "Metal",
    "aluminium foil": "Metal",
    "steel": "Metal",
    "iron": "Metal",
    "copper": "Metal",
    "wire": "Metal",
    "copper wire": "Metal",
    "nail": "Metal",
    "screw": "Metal",
    "pot": "Metal",
    "pan": "Metal",
    "metal cutlery": "Metal",
    "bottle cap": "Metal",

    # E-Waste
    "e-waste": "E-Waste",
    "ewaste": "E-Waste",
    "mobile": "E-Waste",
    "phone": "E-Waste",
    "old mobile phone": "E-Waste",
    "smartphone": "E-Waste",
    "cell phone": "E-Waste",
    "laptop": "E-Waste",
    "computer": "E-Waste",
    "pc": "E-Waste",
    "battery": "E-Waste",
    "lithium battery": "E-Waste",
    "charger": "E-Waste",
    "laptop charger": "E-Waste",
    "phone charger": "E-Waste",
    "cable": "E-Waste",
    "usb cable": "E-Waste",
    "wire cord": "E-Waste",
    "headphone": "E-Waste",
    "earphones": "E-Waste",
    "airpods": "E-Waste",
    "tablet": "E-Waste",
    "ipad": "E-Waste",
    "tv": "E-Waste",
    "television": "E-Waste",
    "monitor": "E-Waste",
    "keyboard": "E-Waste",
    "mouse": "E-Waste",
    "printer": "E-Waste",
    "scanner": "E-Waste",
    "motherboard": "E-Waste",
    "circuit": "E-Waste",
    "smartwatch": "E-Waste",
    "hard drive": "E-Waste",
    "router": "E-Waste",
    "microwave": "E-Waste",
    "toaster": "E-Waste",

    # Organic Waste
    "food": "Organic Waste",
    "food waste": "Organic Waste",
    "vegetable": "Organic Waste",
    "vegetable peel": "Organic Waste",
    "vegetable peels": "Organic Waste",
    "fruit": "Organic Waste",
    "fruit peel": "Organic Waste",
    "apple core": "Organic Waste",
    "banana peel": "Organic Waste",
    "leftovers": "Organic Waste",
    "coffee grounds": "Organic Waste",
    "tea bag": "Organic Waste",
    "tea leaves": "Organic Waste",
    "egg shell": "Organic Waste",
    "eggshells": "Organic Waste",
    "bread": "Organic Waste",
    "leaves": "Organic Waste",
    "garden waste": "Organic Waste",
    "grass": "Organic Waste",
    "dry leaves": "Organic Waste",
    "meat scraps": "Organic Waste",
    "fish bones": "Organic Waste",
    "flowers": "Organic Waste",

    # Other
    "clothes": "Other",
    "fabric": "Other",
    "cloth": "Other",
    "textile": "Other",
    "shoe": "Other",
    "shoes": "Other",
    "ceramic": "Other",
    "ceramic mug": "Other",
    "plate": "Other",
    "mirror": "Other",
    "light bulb": "Other",
    "tube light": "Other",
    "paint": "Other",
    "paint can": "Other",
    "chemical": "Other",
    "medicine": "Other",
    "pill": "Other",
    "tyre": "Other",
    "tire": "Other",
    "rubber": "Other",
    "furniture": "Other",
    "mattress": "Other",
    "styrofoam": "Other",
}

CATEGORY_METADATA = {
    "Plastic": {
        "badge_class": "badge-plastic",
        "icon": "fa-recycle",
        "bin": "Blue Bin / Dry Recyclables",
        "color": "#0ea5e9",
        "tip": "Empty and rinse liquids. Remove caps if composed of mixed plastics and flatten bottles to save volume.",
        "fact": "A plastic bottle takes up to 450 years to decompose in a landfill, but can be recycled into clothing and carpets!"
    },
    "Paper": {
        "badge_class": "badge-paper",
        "icon": "fa-newspaper",
        "bin": "Blue / Paper Bin",
        "color": "#3b82f6",
        "tip": "Keep dry and flatten cardboard boxes. Soiled paper (like greasy pizza boxes) should go to organic composting.",
        "fact": "Recycling 1 ton of paper saves 17 trees, 7,000 gallons of water, and 4,000 kilowatts of energy."
    },
    "Glass": {
        "badge_class": "badge-glass",
        "icon": "fa-wine-bottle",
        "bin": "Green / Glass Bin",
        "color": "#10b981",
        "tip": "Rinse containers clean. Separate metal lids. Wrap broken shards carefully in paper to protect collection workers.",
        "fact": "Glass is 100% recyclable and can be recycled indefinitely without losing quality or purity."
    },
    "Metal": {
        "badge_class": "badge-metal",
        "icon": "fa-box-archive",
        "bin": "Yellow / Metal Bin",
        "color": "#f59e0b",
        "tip": "Rinse food residue. Crush aluminium beverage cans to optimize space in the collection truck.",
        "fact": "Recycling aluminium cans uses 95% less energy than producing new cans from raw bauxite ore."
    },
    "E-Waste": {
        "badge_class": "badge-ewaste",
        "icon": "fa-laptop-code",
        "bin": "Designated E-Waste Drop Box",
        "color": "#8b5cf6",
        "tip": "Do not throw in normal household trash. Back up and erase data from devices. Keep batteries insulated.",
        "fact": "E-waste contains valuable recoverable precious metals like gold, silver, and copper, as well as toxic heavy metals."
    },
    "Organic Waste": {
        "badge_class": "badge-organic",
        "icon": "fa-seedling",
        "bin": "Green Bin / Wet Compost",
        "color": "#16a34a",
        "tip": "Compost at home or pack in biodegradable bags. Avoid mixing plastics, wrappers, or treated woods.",
        "fact": "Organic waste in landfills generates methane, a greenhouse gas 28 times more potent than carbon dioxide."
    },
    "Other": {
        "badge_class": "badge-other",
        "icon": "fa-layer-group",
        "bin": "Specialized / Hazardous Drop-Off",
        "color": "#64748b",
        "tip": "Requires specialized handling. Check local municipal hazardous waste collection rules or textile donation hubs.",
        "fact": "Proper sorting keeps non-recyclable materials from contaminating standard recycling batches."
    }
}

POPULAR_SUGGESTIONS = [
    {"label": "Old Mobile Phone", "query": "old mobile phone", "category": "E-Waste"},
    {"label": "Plastic Bottle", "query": "plastic bottle", "category": "Plastic"},
    {"label": "Newspaper", "query": "newspaper", "category": "Paper"},
    {"label": "Glass Bottle", "query": "glass bottle", "category": "Glass"},
    {"label": "Aluminium Can", "query": "aluminium can", "category": "Metal"},
    {"label": "Food Waste", "query": "food waste", "category": "Organic Waste"},
    {"label": "Laptop Charger", "query": "laptop charger", "category": "E-Waste"},
    {"label": "Cardboard Box", "query": "cardboard box", "category": "Paper"},
]

def classify_waste_item(query):
    """
    Given a user input string (e.g. 'old mobile phone', 'plastic bottle'),
    returns the predicted waste category and full disposal guidance.
    """
    if not query:
        return None
        
    cleaned = query.strip().lower()
    
    # 1. Exact match check
    if cleaned in WASTE_KNOWLEDGE_BASE:
        category = WASTE_KNOWLEDGE_BASE[cleaned]
        meta = CATEGORY_METADATA[category]
        return {
            "query": query,
            "category": category,
            "matched": True,
            **meta
        }
        
    # 2. Key phrase containment check (longer phrases first)
    sorted_phrases = sorted(WASTE_KNOWLEDGE_BASE.keys(), key=lambda x: len(x), reverse=True)
    for phrase in sorted_phrases:
        if phrase in cleaned:
            category = WASTE_KNOWLEDGE_BASE[phrase]
            meta = CATEGORY_METADATA[category]
            return {
                "query": query,
                "category": category,
                "matched": True,
                **meta
            }
            
    # 3. Word token matching
    words = cleaned.replace('-', ' ').replace('/', ' ').split()
    for word in words:
        if word in WASTE_KNOWLEDGE_BASE:
            category = WASTE_KNOWLEDGE_BASE[word]
            meta = CATEGORY_METADATA[category]
            return {
                "query": query,
                "category": category,
                "matched": True,
                **meta
            }
            
    # 4. Fallback to 'Other' with helpful guidance
    meta = CATEGORY_METADATA["Other"]
    return {
        "query": query,
        "category": "Other",
        "matched": False,
        **meta,
        "tip": "We couldn't pinpoint the exact material. Please classify under 'Other' or check if it contains mixed components like electronics, metals, or hazardous chemicals."
    }
