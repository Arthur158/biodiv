import random

import random

# Expanded Latin/Greek roots for species names
prefixes = [
    "Aero", "Amph", "Anthro", "Aqua", "Arthro", "Bio", "Cephalo", "Chloro", "Cyto", "Dendro", 
    "Eco", "Entomo", "Hemi", "Hepato", "Hetero", "Homo", "Ichthyo", "Lepido", "Litho", "Mammo", 
    "Morpho", "Necto", "Neuro", "Odon", "Ornitho", "Osteo", "Phyto", "Ptero", "Saur", "Thermo", 
    "Zoo", "Paleo", "Pyro", "Carno", "Herbi", "Fungi", "Phyco", "Proto", "Terra", "Astra", 
    "Galacto", "Helio", "Magna", "Mega", "Micro", "Multi", "Neo", "Pan", "Poly", "Hypo",
    "Hyper", "Endo", "Exo", "Iso", "Macro", "Mono", "Omni", "Para", "Peri", "Poly",
    "Pseudo", "Tele", "Trans", "Ultra", "Uni", "Vice", "Archaeo", "Auto", "Bi", "Circum",
    "Co", "Contra", "Counter", "De", "Di", "Dis", "Epi", "Eu", "Extra", "Inter",
    "Intra", "Mal", "Meso", "Meta", "Non", "Post", "Pre", "Proto", "Re", "Semi",
    "Sub", "Super", "Sym", "Syn", "Tri", "Un", "Ante", "Anti", "Cata", "Cis",
    "En", "Em", "Ex", "Fore", "Holo", "Infra", "Intro", "Kilo", "Maxi", "Mega",
    "Min", "Out", "Over", "Pro", "Retro", "Se", "Sed", "Self", "Sur", "Sus",
    "Twice", "Up", "Vice", "With", "Acro", "Allo", "Alter", "Cata", "Circum", "Com",
    "Cor", "Cryo", "Dactyl", "De", "Demi", "Dys", "Ecto", "End", "Equi", "Exo",
    "Extra", "Hemi", "Hexa", "Homeo", "Iso", "Leuco", "Lipo", "Logy", "Macro", "Medi",
    "Meso", "Meta", "Metri", "Mono", "Muta", "Neo", "Noto", "Octo", "Oligo", "Ortho",
    "Out", "Over", "Penta", "Per", "Peri", "Photo", "Poly", "Quadra", "Retro", "Se",
    "Syl", "Sym", "Tetra", "Tri", "Un", "Under", "Xeno", "Zoo", "Circum", "Com"
]

suffixes = [
    "ceras", "derma", "donta", "fera", "formes", "gryphus", "lith", "mancy", "morph", "nauta", 
    "nympha", "poda", "rhynchus", "soma", "stoma", "therium", "tome", "trope", "viridis", "vore",
    "phyte", "plasm", "gramme", "logue", "neme", "phore", "scope", "trix", "ule", "vent",
    "zoon", "osis", "ation", "ise", "fy", "lyse", "esce", "ify", "ize", "oid",
    "itis", "osis", "ectomy", "otomy", "graphy", "logy", "philia", "phobia", "mania", "ist",
    "ian", "er", "ary", "able", "ible", "hood", "ship", "ment", "ly", "ward",
    "wise", "ful", "less", "ness", "cy", "dom", "ance", "ence", "or", "tion",
    "sion", "ic", "ical", "ish", "ive", "ous", "y", "ate", "en", "ify",
    "fy", "ize", "ise", "al", "ed", "ing", "ly", "ward", "wise", "less",
    "ic", "sion", "tion", "ative", "cide", "ectomy", "ia", "ist", "ity", "ment",
    "ness", "or", "phobia", "phyte", "cy", "ance", "arium", "cracy", "crat", "ology",
    "dom", "esque", "ful", "fy", "hood", "ial", "ian", "ic", "ical", "ish",
    "ism", "ist", "ite", "ity", "ive", "less", "like", "ly", "ment", "ness",
    "or", "ous", "ship", "sion", "tion", "y", "al", "ance", "ence", "dom",
    "er", "ful", "ic", "ish", "ism", "ist", "ity", "ive", "less", "ly",
    "ment", "ness", "or", "ous", "ship", "sion", "tion", "y", "arium", "ary"
]

def get_random_name():
    return random.choice(prefixes) + random.choice(suffixes)



syllables_start = ['Ama', 'Sy', 'Af', 'Terra', 'Hyper', 'Ast', 'Geo', 'Eco', 'Aero', 'Sol',
                    'Luna', 'Iso', 'Poly', 'Mono', 'Giga', 'Tera', 'Mega', 'Thermo', 'Hydro', 'Mar']
                    
syllables_mid = ['ber', 'zon', 'tri', 'ver', 'mal', 'qua', 'ro', 'vi', 'li', 'co', 
                    'tic', 'rex', 'man', 'bel', 'cal', 'dem', 'gon', 'nar', 'pal', 'tor']
                    
syllables_end = ['ia', 'ka', 'ya', 'ra', 'que', 'via', 'nia', 'way', 'os', 'an', 
                    'ium', 'ian', 'us', 'ent', 'ine', 'oid', 'ics', 'ogy', 'ful', 'ish']


def get_random_region_name():
    return random.choice(syllables_start) + random.choice(syllables_mid) + random.choice(syllables_end)
