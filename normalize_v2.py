#!/usr/bin/env python3
"""
normalize_v2.py — Schema canônico revisado pós-auditoria.
Aplica todas as melhorias obrigatórias da SCHEMA_FREEZE_AUDIT.
"""
import json, os, re
from collections import defaultdict

SRC = "/home/claude/mh-cortex-output/sources"
OUT = "/home/claude/mh-cortex-output/normalized_v2"

# ─── Tabelas de coeficientes ─────────────────────────────────────────────────
CLASS_COEFF = {
    "gen1_2":  {"Great Sword":4.8,"Long Sword":4.8,"Sword and Shield":1.4,
                "Dual Blades":1.4,"Hammer":5.2,"Hunting Horn":4.2,
                "Lance":2.3,"Gunlance":2.3,"Bow":1.2,
                "Light Bowgun":1.3,"Heavy Bowgun":1.5,"_elem_div":10},
    "gen3":    {"Great Sword":4.8,"Long Sword":4.8,"Sword and Shield":1.4,
                "Hammer":5.2,"Hunting Horn":4.2,"Lance":2.3,"Gunlance":2.3,
                "Switch Axe":5.4,"Bow":1.2,"Light Bowgun":1.3,"Heavy Bowgun":1.5,
                "_elem_div":10},
    "gen4_gu": {"Great Sword":4.8,"Long Sword":3.3,"Sword and Shield":1.4,
                "Dual Blades":1.4,"Hammer":5.2,"Hunting Horn":4.2,
                "Lance":2.3,"Gunlance":2.3,"Switch Axe":5.4,
                "Charge Blade":3.6,"Insect Glaive":3.1,
                "Bow":1.2,"Light Bowgun":1.3,"Heavy Bowgun":1.5,"_elem_div":10},
    "world":   {"Great Sword":4.8,"Long Sword":3.3,"Sword and Shield":1.4,
                "Dual Blades":1.4,"Hammer":5.2,"Hunting Horn":4.2,
                "Lance":2.3,"Gunlance":2.3,"Switch Axe":3.5,
                "Charge Blade":3.6,"Insect Glaive":3.1,
                "Bow":1.2,"Light Bowgun":1.3,"Heavy Bowgun":1.5,"_elem_div":10},
    "rise":    {"Great Sword":4.8,"Long Sword":3.3,"Sword and Shield":1.4,
                "Dual Blades":1.4,"Hammer":5.2,"Hunting Horn":4.2,
                "Lance":2.3,"Gunlance":2.3,"Switch Axe":3.5,
                "Charge Blade":3.6,"Insect Glaive":3.1,
                "Bow":1.2,"Light Bowgun":1.3,"Heavy Bowgun":1.5,"_elem_div":1},
    "wilds":   {"Great Sword":4.8,"Long Sword":3.3,"Sword and Shield":1.4,
                "Dual Blades":1.4,"Hammer":5.2,"Hunting Horn":4.2,
                "Lance":2.3,"Gunlance":2.3,"Switch Axe":3.5,
                "Charge Blade":3.6,"Insect Glaive":3.1,
                "Bow":1.2,"Light Bowgun":1.3,"Heavy Bowgun":1.5,"_elem_div":1},
}
GAME_COEFF = {
    "mhfu":"gen1_2","mhf2":"gen1_2","mhf1":"gen1_2","mh1":"gen1_2",
    "mh2":"gen1_2","mhdos":"gen1_2","mhg":"gen1_2",
    "mh3tri":"gen3","mh3u":"gen3","mhp3rd":"gen3",
    "mhgu":"gen4_gu","mhgen":"gen4_gu","mh4u":"gen4_gu","mh4":"gen4_gu",
    "world":"world","rise":"rise","wilds":"wilds",
}

SHARPNESS_COLORS = ["red","orange","yellow","green","blue","white","purple"]
SHARPNESS_MULT = {
    "default": {"red":(0.50,0.25),"orange":(0.75,0.50),"yellow":(1.00,0.75),
                "green":(1.05,1.00),"blue":(1.20,1.0625),"white":(1.32,1.15),"purple":(1.45,1.25)},
    "rise":    {"red":(0.50,0.25),"orange":(0.75,0.50),"yellow":(1.00,0.75),
                "green":(1.05,1.00),"blue":(1.20,1.05),"white":(1.32,1.15),"purple":(1.39,1.25)},
    "wilds":   {"red":(0.50,0.25),"orange":(0.75,0.50),"yellow":(1.00,0.75),
                "green":(1.05,1.00),"blue":(1.20,1.05),"white":(1.32,1.15),"purple":(1.39,1.25)},
}

WTYPE_SLUG = {
    "great-sword":"Great Sword","great_sword":"Great Sword","greatsword":"Great Sword",
    "long-sword":"Long Sword","long_sword":"Long Sword","longsword":"Long Sword",
    "sword-and-shield":"Sword and Shield","sword_and_shield":"Sword and Shield","sns":"Sword and Shield",
    "dual-blades":"Dual Blades","dual_blades":"Dual Blades","dualblades":"Dual Blades","ds":"Dual Blades",
    "hammer":"Hammer","hm":"Hammer",
    "hunting-horn":"Hunting Horn","hunting_horn":"Hunting Horn","huntinghorn":"Hunting Horn","hh":"Hunting Horn",
    "lance":"Lance","lc":"Lance",
    "gunlance":"Gunlance","gun-lance":"Gunlance","gl":"Gunlance",
    "switch-axe":"Switch Axe","switch_axe":"Switch Axe","switchaxe":"Switch Axe","sa":"Switch Axe",
    "charge-blade":"Charge Blade","charge_blade":"Charge Blade","chargeblade":"Charge Blade","cb":"Charge Blade",
    "insect-glaive":"Insect Glaive","insect_glaive":"Insect Glaive","insectglaive":"Insect Glaive","ig":"Insect Glaive",
    "bow":"Bow",
    "light-bowgun":"Light Bowgun","light_bowgun":"Light Bowgun","lightbowgun":"Light Bowgun","lbg":"Light Bowgun",
    "heavy-bowgun":"Heavy Bowgun","heavy_bowgun":"Heavy Bowgun","heavybowgun":"Heavy Bowgun","hbg":"Heavy Bowgun",
}
WTYPE_INT = {
    0:"Great Sword",1:"Sword and Shield",2:"Dual Blades",3:"Long Sword",
    4:"Hammer",5:"Hunting Horn",6:"Lance",7:"Gunlance",8:"Switch Axe",
    9:"Charge Blade",10:"Insect Glaive",11:"Bow",12:"Light Bowgun",13:"Heavy Bowgun"
}

# ─── Helpers ─────────────────────────────────────────────────────────────────

def coeff(game): return CLASS_COEFF.get(GAME_COEFF.get(game,"gen4_gu"), CLASS_COEFF["gen4_gu"])
def sharp_tbl(game): return SHARPNESS_MULT.get(game if game in SHARPNESS_MULT else "default", SHARPNESS_MULT["default"])

def clean_int(v, d=0):
    if v is None: return d
    if isinstance(v, bool): return int(v)
    if isinstance(v, (int,float)): return int(v)
    if isinstance(v, dict):
        for k in ("base","value","display","raw"):
            if k in v: return clean_int(v[k], d)
        return d
    try: return int(float(str(v).replace("%","").replace("+","").replace(",","")))
    except: return d

def clean_str(v): return str(v).strip() if v else None
def clean_affinity(v):
    if isinstance(v, (int,float)): return int(v)
    try: return int(float(str(v).replace("%","").replace(" ","")))
    except: return 0

def resolve_wtype(v):
    if isinstance(v, int): return WTYPE_INT.get(v, f"Unknown_{v}")
    s = str(v).strip()
    if s in WTYPE_INT.values(): return s
    return WTYPE_SLUG.get(s.lower(), s)

def norm_slots(v):
    if isinstance(v, int): return v
    if isinstance(v, list): return len([x for x in v if x and str(x) not in ("0","","-")])
    if isinstance(v, str): return v.count("O") or v.count("o")
    return 0

def norm_skills(v):
    if not v: return []
    if isinstance(v, dict): return [{"skill_name":str(k),"points":clean_int(p)} for k,p in v.items()]
    if isinstance(v, list):
        out = []
        for s in v:
            if isinstance(s, dict):
                n = s.get("name") or s.get("skill_name") or s.get("skillName","?")
                p = clean_int(s.get("points") or s.get("skillPoints") or s.get("level") or 0)
                out.append({"skill_name":str(n),"points":p})
            elif isinstance(s,(list,tuple)) and len(s)>=2:
                out.append({"skill_name":str(s[0]),"points":clean_int(s[1])})
        return out
    return []

def norm_res(v):
    t = {"fire":0,"water":0,"thunder":0,"ice":0,"dragon":0}
    if not v: return t
    if isinstance(v, list) and len(v)>=5:
        for i,k in enumerate(["fire","water","ice","thunder","dragon"]):
            t[k] = clean_int(v[i])
        return t
    if isinstance(v, dict):
        aliases = {
            "fire":   ["fire","fireRes","fire_res","fireRes_alt"],
            "water":  ["water","waterRes","water_res","waterRes_alt"],
            "thunder":["thunder","thunderRes","thunder_res","thunderRes_alt"],
            "ice":    ["ice","iceRes","ice_res","iceRes_alt"],
            "dragon": ["dragon","dragonRes","dragon_res","dragonRes_alt"],
        }
        for k, alts in aliases.items():
            for a in alts:
                if a in v: t[k] = clean_int(v[a]); break
    return t

def sharpness_dict(arr, game):
    if not arr: return None
    try: arr = [int(x) for x in arr]
    except: return None
    bars = {c:v for c,v in zip(SHARPNESS_COLORS[:len(arr)], arr) if v>0}
    if not bars: return None
    highest = max(bars, key=lambda c: SHARPNESS_COLORS.index(c))
    mult = sharp_tbl(game).get(highest,(1.0,1.0))
    return {"bars":bars,"highest":highest,"raw_multiplier":mult[0],"elem_multiplier":mult[1]}

def parse_mhgu_sharp(s):
    if not s or not isinstance(s,str): return None,None
    parts = s.strip().split()
    def parse(p):
        try: return [int(x) for x in p.split(".")]
        except: return None
    arr = [parse(p) for p in parts[:2]]
    while len(arr)<2: arr.append(None)
    return arr[0], arr[1]

def uid(rec, *fields):
    for f in fields:
        v = rec.get(f)
        if v: return str(v)
    return re.sub(r'\W+','_', str(rec.get("name","?")).lower())

# ─── type_specific builders ───────────────────────────────────────────────────

def build_type_specific(w, wtype, game):
    """Extrai dados específicos por tipo de arma."""
    if wtype == "Gunlance":
        st = w.get("shelling_type") or w.get("shelling") or ""
        sl = w.get("shelling_level") or ""
        if st:
            # "Normal 1" → type=Normal, level=1
            parts = str(st).split()
            stype = parts[0] if parts else str(st)
            slevel = clean_int(parts[1]) if len(parts)>1 else clean_int(sl) or 1
            return {"shelling_type": stype, "shelling_level": slevel}

    elif wtype == "Switch Axe":
        phial = w.get("phial") or w.get("phial_type") or ""
        if phial:
            return {"phial_type": str(phial).strip()}

    elif wtype == "Charge Blade":
        phial = w.get("phial") or w.get("phial_type") or ""
        power = clean_int(w.get("phial_power") or 0) or None
        if phial:
            return {"phial_type": str(phial).strip(), "phial_power": power}

    elif wtype == "Hunting Horn":
        notes = w.get("horn_notes") or w.get("notes") or ""
        if notes:
            return {"notes": str(notes).strip(), "melody_ids": []}

    elif wtype == "Bow":
        # Coatings: bitmask "1121" ou dict flags
        coatings_raw = w.get("coatings") or w.get("coating") or ""
        charges_raw  = w.get("charges") or w.get("bow_charges") or ""
        coatings = []
        COATING_NAMES = ["Close Range","Power","Paralysis","Poison","Sleep","Blast"]
        if isinstance(coatings_raw, str) and coatings_raw.isdigit():
            for i, bit in enumerate(coatings_raw):
                if bit == "1" and i < len(COATING_NAMES):
                    coatings.append(COATING_NAMES[i])
        elif isinstance(coatings_raw, dict):
            for k, v in coatings_raw.items():
                if str(v).upper() in ("TRUE","1","YES"):
                    coatings.append(k.replace("_"," ").title())
        charges = []
        if isinstance(charges_raw, str) and charges_raw:
            for part in charges_raw.split("|"):
                part = part.strip().rstrip("*")
                tokens = part.split()
                if len(tokens) >= 2:
                    charges.append({"type": tokens[0], "level": clean_int(tokens[1])})
        if coatings or charges:
            return {"coatings": coatings, "charges": charges}

    elif wtype in ("Light Bowgun", "Heavy Bowgun"):
        special = w.get("special_ammo") or w.get("wyvernfire") or None
        deviation = w.get("deviation") or w.get("recoil") or None
        ammo_cfg = w.get("ammo_config") or w.get("ammo_config_id") or None
        result = {}
        if deviation: result["deviation"] = str(deviation)
        if special:   result["special_ammo"] = str(special)
        if ammo_cfg:  result["ammo_config_id"] = str(ammo_cfg)
        return result if result else None

    elif wtype == "Insect Glaive":
        bonus = w.get("kinsect_bonus") or w.get("kinsect_bonus_type") or None
        if bonus: return {"kinsect_bonus": str(bonus).strip()}

    return None

# ─── Normalizadores ───────────────────────────────────────────────────────────

def norm_weapon(w, game, src):
    wtype = resolve_wtype(
        w.get("weapon_type_name") or w.get("weapon_type") or
        w.get("wtype") or w.get("type") or "Unknown")

    disp_raw = clean_int(w.get("attack") or w.get("display_raw") or
                          w.get("baseVal") or w.get("baseAttack") or 0)
    ct   = coeff(game)
    coef = ct.get(wtype, 1.0)
    true_raw = round(disp_raw / coef, 2) if coef and disp_raw else 0.0

    elem_type = w.get("element_type") or w.get("element") or w.get("secondaryDamageType") or None
    if elem_type: elem_type = re.sub(r'.*\.','', str(elem_type)).lower().strip() or None
    # MHWorld element1 field
    if not elem_type: elem_type = clean_str(w.get("element1")) or None
    if elem_type and elem_type.lower() in ("","none","null","—","-"): elem_type = None

    elem_disp = clean_int(w.get("element_display") or w.get("element_damage") or
                           w.get("secondaryAttack") or w.get("element1_attack") or 0)
    elem_div  = ct.get("_elem_div", 10)
    elem_true = round(elem_disp / elem_div, 2) if elem_disp else None
    elem_hidn = bool(w.get("element_hidden") or w.get("awaken") or
                     str(w.get("element_hidden","")).upper() == "TRUE")

    elderseal = clean_str(w.get("elderseal")) or None

    # Sharpness — MHGU usa string dot-separated, outros usam arrays
    sharp_raw = w.get("_sharpness_parsed") or w.get("sharpness") or w.get("sharpness_levels")
    sharp_max = w.get("_sharpness_hc_parsed") or w.get("sharpnessUp") or w.get("sharpness_handicraft")
    if isinstance(sharp_raw, str):
        sharp_raw, sharp_max = parse_mhgu_sharp(sharp_raw)
    if isinstance(sharp_raw, list):
        try: sharp_raw = [int(x) for x in sharp_raw]
        except: sharp_raw = None
    if isinstance(sharp_max, list):
        try: sharp_max = [int(x) for x in sharp_max]
        except: sharp_max = None
    sharp    = sharpness_dict(sharp_raw, game)
    sharp_hc = sharpness_dict(sharp_max, game)

    # Nome — MHGU precisa de join externo (feito no pré-processador)
    name = str(w.get("name") or w.get("weapon_name") or "?")

    create_mats  = w.get("create") or w.get("create_mats") or w.get("create_materials") or []
    if isinstance(create_mats, dict): create_mats = []
    upgrade_mats = w.get("upgrade") or w.get("improve") or w.get("upgrade_materials") or []
    if isinstance(upgrade_mats, dict): upgrade_mats = []

    ts = build_type_specific(w, wtype, game)

    return {
        "id":          f"{game}_{uid(w,'_id','id','sortId')}",
        "game":        game,
        "name":        name,
        "name_ja":     clean_str(w.get("name_ja") or w.get("jp_name")),
        "weapon_type": wtype,
        "rarity":      clean_int(w.get("rarity") or w.get("rare") or w.get("rareType") or 0) or None,
        "slots":       norm_slots(w.get("slots") or w.get("num_slots") or w.get("slot") or 0),
        "damage": {
            "display_raw":       disp_raw,
            "true_raw":          true_raw,
            "class_coefficient": coef,
            "affinity":          clean_affinity(w.get("affinity") or 0),
            "element_type":      elem_type,
            "element_display":   elem_disp or None,
            "element_true":      elem_true,
            "element_hidden":    elem_hidn,
            "elderseal":         elderseal,
        },
        "sharpness":   {"levels": sharp, "max_levels": sharp_hc},
        "craft": {
            "buy_price":         clean_int(w.get("price") or w.get("buy_price") or w.get("buyVal") or 0) or None,
            "create_materials":  create_mats,
            "upgrade_from":      clean_str(str(w.get("parent_id") or w.get("improve_from") or w.get("upgrade_from") or "")),
            "upgrade_materials": upgrade_mats,
        },
        "type_specific": ts,
        "source_file":   src,
    }


def norm_armor(a, game, src):
    part_map = {
        "hlm":"head","head":"head","helm":"head","helmet":"head",
        "plt":"chest","chest":"chest","body":"chest","torso":"chest",
        "arm":"arms","arms":"arms","gloves":"arms",
        "wst":"waist","waist":"waist","coil":"waist",
        "leg":"legs","legs":"legs","boots":"legs","greaves":"legs",
    }
    part = part_map.get(str(a.get("part") or a.get("armor_type") or a.get("slot") or "?").lower(), "?")

    def_raw = a.get("defense")
    if isinstance(def_raw, dict):
        def_base   = clean_int(def_raw.get("base") or def_raw.get("min") or 0)
        def_max    = clean_int(def_raw.get("max") or 0) or None
        def_aug    = clean_int(def_raw.get("augmented") or def_raw.get("augmented_max") or 0) or None
    else:
        def_base   = clean_int(def_raw or 0)
        def_max    = clean_int(a.get("max_defense") or a.get("defense_max") or 0) or None
        def_aug    = clean_int(a.get("defense_augment_max") or 0) or None

    gender_map = {"male":"male","female":"female","both":"both",
                  "none":"both",None:"both","0":"both","1":"male","2":"female"}
    gender = gender_map.get(str(a.get("gender") or a.get("sex") or "both").lower(), "both")

    armor_type = "both"
    cat = a.get("hunter_type") or a.get("category")
    if cat is not None:
        armor_type = {0:"both",1:"blademaster",2:"gunner"}.get(clean_int(cat), "both")

    slots_raw = a.get("slots") or a.get("slot") or a.get("num_slots") or []
    if isinstance(slots_raw, int): slots_raw = [1]*slots_raw if slots_raw else []
    elif isinstance(slots_raw, str):
        slots_raw = [int(c) for c in slots_raw if c.isdigit()] if slots_raw.isdigit() else []

    # family/set_id
    family = a.get("family") or a.get("set_id") or None
    set_id = f"{game}_set_{family}" if family else None

    res_raw = (a.get("resistance") or a.get("resistances") or
               {k:a.get(k) for k in ["fire_res","water_res","thunder_res","ice_res","dragon_res"] if a.get(k) is not None} or
               a)

    return {
        "id":          f"{game}_{uid(a,'_id','id')}",
        "game":        game,
        "name":        str(a.get("name") or "?"),
        "name_ja":     clean_str(a.get("name_ja")),
        "part":        part,
        "type":        armor_type,
        "rarity":      clean_int(a.get("rarity") or a.get("rare") or 0) or None,
        "gender":      gender,
        "set_id":      set_id,
        "defense": {
            "base":          def_base,
            "max":           def_max,
            "augmented_max": def_aug,
        },
        "resistances": norm_res(res_raw),
        "slots":       slots_raw if isinstance(slots_raw,list) else [],
        "skills":      norm_skills(a.get("skills") or a.get("skill_points") or
                                    a.get("skills_points") or a.get("skillPoints") or []),
        "craft": {
            "buy_price":        clean_int(a.get("price") or a.get("buy_price") or 0) or None,
            "create_materials": a.get("create_materials") or a.get("materials") or [],
        },
        "source_file": src,
    }


def norm_skill(s, game, src):
    levels = s.get("levels") or s.get("skill_levels") or []
    return {
        "id":          f"{game}_{uid(s,'_id','id','skill_id')}",
        "game":        game,
        "name":        str(s.get("name") or s.get("skill_name") or "?"),
        "name_ja":     clean_str(s.get("name_ja")),
        "tree_id":     clean_str(str(s.get("tree_id") or s.get("skill_tree_id") or "")),
        "tree_name":   clean_str(s.get("tree_name") or s.get("group")),
        "levels":      levels,
        "max_level":   len(levels) if levels else clean_int(s.get("max_level") or 1),
        "source_file": src,
    }


def norm_monster(m, game, src):
    return {
        "id":       f"{game}_{uid(m,'_id','id')}",
        "game":     game,
        "name":     str(m.get("name") or "?"),
        "name_ja":  clean_str(m.get("name_ja") or m.get("name_ja")),
        "species":  str(m.get("species") or m.get("type") or m.get("class") or "?"),
        "is_large": bool(m.get("isLarge") or m.get("is_large") or False),
        "base_hp":  clean_int(m.get("base_hp") or 0) or None,
        "elements": m.get("elements") or [],
        "ailments": m.get("ailments") or [],
        "weaknesses": m.get("weaknesses") or m.get("weakness") or [],
        "hitzones": m.get("hitzones") or None,
        "locations": m.get("locations") or m.get("habitats") or [],
        "games":    m.get("games") or [game],
        "source_file": src,
    }


def norm_item(it, game, src):
    return {
        "id":          f"{game}_{uid(it,'_id','id')}",
        "game":        game,
        "name":        str(it.get("name") or "?"),
        "name_ja":     clean_str(it.get("name_ja")),
        "description": clean_str(it.get("description")),
        "category":    clean_str(it.get("category") or it.get("type")),
        "rarity":      clean_int(it.get("rarity") or it.get("rare") or 0) or None,
        "carry_max":   clean_int(it.get("carry_max") or it.get("carryMax") or it.get("carry-max") or 0) or None,
        "buy_price":   clean_int(it.get("buy_price") or it.get("buy") or it.get("price") or 0) or None,
        "sell_price":  clean_int(it.get("sell_price") or it.get("sell") or 0) or None,
        "source_file": src,
    }


def norm_quest(q, game, src):
    hub   = str(q.get("region") or q.get("hub") or q.get("hub_type") or q.get("category") or "?").lower()
    rank  = str(q.get("rank") or q.get("difficulty") or "LR")
    stars = str(q.get("starLevel") or q.get("stars") or q.get("star_level") or "?")
    obj   = str(q.get("type") or q.get("objective_type") or q.get("goal_type") or "hunt").lower()

    # Subquest
    sub_goal   = clean_str(q.get("sub_goal"))
    sub_zenny  = clean_int(q.get("sub_reward") or 0) or None
    sub_hrp    = clean_int(q.get("sub_hrp") or 0) or None
    subquest   = {"goal_text": sub_goal, "zenny_reward": sub_zenny, "hrp_reward": sub_hrp} \
                 if any([sub_goal, sub_zenny, sub_hrp]) else None

    return {
        "id":             f"{game}_{uid(q,'_id','id','quest_id')}",
        "game":           game,
        "name":           str(q.get("name") or q.get("quest_name") or "?"),
        "name_ja":        clean_str(q.get("name_ja")),
        "hub":            hub,
        "rank":           rank,
        "stars":          stars,
        "objective_type": obj,
        "goal_text":      clean_str(q.get("goal") or q.get("goal_condition") or q.get("goal_text")),
        "flavor_text":    clean_str(q.get("flavor") or q.get("quest-details") or q.get("flavor_text")),
        "location_id":    clean_str(str(q.get("location_id") or q.get("location") or "")),
        "targets":        q.get("targets") or q.get("main-monsters") or [],
        "contract_fee":   clean_int(q.get("contract") or q.get("fee") or q.get("contract_fee") or q.get("contract-fee") or 0) or None,
        "time_limit":     clean_int(q.get("time") or q.get("time_limit") or q.get("time-limit") or 0) or None,
        "zenny_reward":   clean_int(q.get("reward") or q.get("zenny_reward") or 0) or None,
        "hrp_reward":     clean_int(q.get("hrp") or q.get("hrp_reward") or 0) or None,
        "subquest":       subquest,
        "source_file":    src,
    }


def norm_decoration(d, game, src):
    slot = d.get("slots") or d.get("slot_size") or d.get("slotUsage") or d.get("requiredSlots") or d.get("level") or 1
    slot = slot[0] if isinstance(slot, list) and slot else clean_int(slot)
    return {
        "id":          f"{game}_{uid(d,'_id','id')}",
        "game":        game,
        "name":        str(d.get("name") or "?"),
        "name_ja":     clean_str(d.get("name_ja")),
        "slot_size":   clean_int(slot),
        "skills":      norm_skills(d.get("skills") or d.get("skill-points") or d.get("skillPoints") or []),
        "craft":       {"materials": d.get("materials") or []},
        "source_file": src,
    }


def norm_charm(c, game, src):
    return {
        "id":          f"{game}_{uid(c,'_id','id')}",
        "game":        game,
        "name":        clean_str(c.get("name")),
        "skills":      norm_skills(c.get("skills") or []),
        "slots":       clean_int(c.get("slots") or c.get("slot") or 0),
        "source_file": src,
    }

# ─── Entidades novas ──────────────────────────────────────────────────────────

def build_armor_sets_mhgu():
    """Constrói armor_set e set_bonus do MHGU a partir de armor_families.json."""
    fam_path = f"{SRC}/mhgu/armors/mhgu_armor_families.json"
    if not os.path.exists(fam_path): return [], []
    with open(fam_path) as f:
        families = json.load(f)

    sets, bonuses = [], []
    for fam in families:
        fid  = fam.get("_id") or fam.get("id")
        name = fam.get("name","?")
        sets.append({
            "id":           f"mhgu_set_{fid}",
            "game":         "mhgu",
            "name":         name,
            "name_ja":      None,
            "rank":         "?",
            "type":         {0:"both",1:"blademaster",2:"gunner"}.get(
                             clean_int(fam.get("hunter_type") or 0), "both"),
            "piece_ids":    [str(fam.get(k)) for k in
                             ["head_id","body_id","arms_id","waist_id","legs_id"] if fam.get(k)],
            "set_bonus_id": None,
            "source_file":  "mhgu_armor_families.json",
        })
    return sets, bonuses


def build_armor_sets_world():
    """Constrói armor_set e set_bonus do MHWorld."""
    world_path = f"{SRC}/world/armors/mhworld_armors.json"
    if not os.path.exists(world_path): return [], []
    with open(world_path) as f:
        data = json.load(f)

    sets_raw   = data.get("armorset_base", [])
    bonus_raw  = data.get("armorset_bonus_base", [])
    bonus_tr   = {b["name_en"]: b for b in data.get("armorset_bonus_base_translations", [])}

    sets, bonuses = [], []
    for s in sets_raw:
        name = s.get("name_en","?")
        sets.append({
            "id":           f"world_set_{re.sub(r'\W+','_',name.lower())}",
            "game":         "world",
            "name":         name,
            "name_ja":      None,
            "rank":         s.get("rank","?"),
            "type":         "both",
            "piece_ids":    [],
            "set_bonus_id": f"world_bonus_{re.sub(r'\W+','_',(s.get('bonus') or '').lower())}" if s.get("bonus") else None,
            "source_file":  "mhworld_armors.json",
        })

    for b in bonus_raw:
        bname = b.get("name_en","?")
        thresholds = []
        for i in ("","2"):
            sn = b.get(f"skill{i}_name" if i else "skill1_name")
            sr = b.get(f"skill{i}_required" if i else "skill1_required")
            if sn and sr:
                thresholds.append({"pieces_required": clean_int(sr), "skill_name": sn, "skill_id": None})
        bonuses.append({
            "id":          f"world_bonus_{re.sub(r'\W+','_',bname.lower())}",
            "game":        "world",
            "name":        bname,
            "name_ja":     None,
            "thresholds":  thresholds,
            "source_file": "mhworld_armors.json",
        })

    return sets, bonuses


def build_monster_rewards_mhgu():
    """Constrói monster_reward do MHGU a partir de hunting_rewards.json."""
    path = f"{SRC}/mhgu/extras/mhgu_hunting_rewards.json"
    if not os.path.exists(path): return []
    with open(path) as f:
        raw = json.load(f)

    # Construir item name lookup
    items_path = f"{SRC}/mhgu/items/mhgu_items.json"
    item_names = {}
    if os.path.exists(items_path):
        with open(items_path) as f:
            items = json.load(f)
        item_names = {i["_id"]: i.get("name","?") for i in items if "_id" in i}

    rewards = []
    for r in raw:
        rid = r.get("_id","?")
        rewards.append({
            "id":          f"mhgu_reward_{rid}",
            "game":        "mhgu",
            "monster_id":  f"mhgu_{r.get('monster_id','?')}",
            "condition":   str(r.get("condition","?")),
            "rank":        str(r.get("rank","?")),
            "item_id":     f"mhgu_{r.get('item_id','?')}",
            "item_name":   item_names.get(r.get("item_id"), "?"),
            "stack":       clean_int(r.get("stack_size") or 1),
            "chance":      float(r.get("percentage") or 0),
            "source_file": "mhgu_hunting_rewards.json",
        })
    return rewards


def build_quest_rewards_mhgu():
    """Constrói quest_reward do MHGU a partir de quest_rewards.json."""
    path = f"{SRC}/mhgu/extras/mhgu_quest_rewards.json"
    if not os.path.exists(path): return []
    with open(path) as f:
        raw = json.load(f)

    items_path = f"{SRC}/mhgu/items/mhgu_items.json"
    item_names = {}
    if os.path.exists(items_path):
        with open(items_path) as f:
            items = json.load(f)
        item_names = {i["_id"]: i.get("name","?") for i in items if "_id" in i}

    rewards = []
    for r in raw:
        rid = r.get("_id","?")
        rewards.append({
            "id":          f"mhgu_qreward_{rid}",
            "game":        "mhgu",
            "quest_id":    f"mhgu_{r.get('quest_id','?')}",
            "item_id":     f"mhgu_{r.get('item_id','?')}",
            "item_name":   item_names.get(r.get("item_id"), "?"),
            "slot":        str(r.get("reward_slot","?")),
            "stack":       clean_int(r.get("stack_size") or 1),
            "chance":      float(r.get("percentage") or 0),
            "source_file": "mhgu_quest_rewards.json",
        })
    return rewards


def build_mhgu_hitzones():
    """Constrói hitzones do MHGU a partir de monster_damage.json."""
    path = f"{SRC}/mhgu/extras/mhgu_monster_damage.json"
    if not os.path.exists(path): return {}
    with open(path) as f:
        raw = json.load(f)

    by_monster = defaultdict(list)
    for r in raw:
        mid = r.get("monster_id")
        by_monster[mid].append({
            "part":   str(r.get("body_part","?")),
            "state":  None,
            "slash":  clean_int(r.get("cut") or 0),
            "blunt":  clean_int(r.get("impact") or 0),
            "shot":   clean_int(r.get("shot") or 0),
            "fire":   clean_int(r.get("fire") or 0),
            "water":  clean_int(r.get("water") or 0),
            "thunder":clean_int(r.get("thunder") or 0),
            "ice":    clean_int(r.get("ice") or 0),
            "dragon": clean_int(r.get("dragon") or 0),
            "ko":     clean_int(r.get("ko") or 0),
        })
    return dict(by_monster)


def build_mhgu_status_thresholds():
    """Status thresholds do MHGU."""
    path = f"{SRC}/mhgu/extras/mhgu_monster_status.json"
    if not os.path.exists(path): return {}
    with open(path) as f:
        raw = json.load(f)
    by_monster = defaultdict(list)
    for r in raw:
        mid = r.get("monster_id")
        by_monster[mid].append({
            "status":   str(r.get("status","?")),
            "initial":  clean_int(r.get("initial") or 0),
            "increase": clean_int(r.get("increase") or 0),
            "max":      clean_int(r.get("max") or 0),
            "duration": clean_int(r.get("duration") or 0),
            "damage":   clean_int(r.get("damage") or 0),
        })
    return dict(by_monster)


# ─── Runner ───────────────────────────────────────────────────────────────────

SKIP = [
    "kolyn090","itytophile","maliciousbanjo","_normalized","metadata",
    "mapping","family","gen1","skill_categories","skill_effects",
    "armor_families","crafting_components","combining_recipes",
    "hunting_rewards","quest_rewards","monster_damage","monster_weakness",
    "monster_status","monster_ailment","monster_habitat","gathering",
    "locations","maps","awards","trenya","veggie","item_notes",
    "npc","hitzones","armor_alt","_full",
]

FILE_NORM = {
    "weapons":     (norm_weapon,     "weapons"),
    "armors":      (norm_armor,      "armors"),
    "skills":      (norm_skill,      "skills"),
    "monsters":    (norm_monster,    "monsters"),
    "items":       (norm_item,       "items"),
    "quests":      (norm_quest,      "quests"),
    "decorations": (norm_decoration, "decorations"),
    "charms":      (norm_charm,      "charms"),
}

def infer_cat(fname):
    fn = fname.lower()
    for key in ["decorations","charms","quests","monsters","weapons","armors","skills","items"]:
        if key in fn: return key
    return None

def load_arr(path):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    if isinstance(d, list): return d
    for k in ["weapon_base","armor_base","item_base","skill_base","quest_base","skill_levels"]:
        if k in d and isinstance(d[k], list): return d[k]
    if isinstance(d, dict):
        best = max(((k,v) for k,v in d.items() if isinstance(v,list)),
                   key=lambda x: len(x[1]), default=(None,[]))
        if best[1]: return best[1]
    return []

# Pré-computar dados auxiliares MHGU
mhgu_hitzones    = build_mhgu_hitzones()
mhgu_status_thr  = build_mhgu_status_thresholds()

# Lookup de nomes MHGU (weapons + armors precisam de join)
mhgu_item_names = {}
mhgu_items_path = f"{SRC}/mhgu/items/mhgu_items.json"
if os.path.exists(mhgu_items_path):
    with open(mhgu_items_path) as f:
        _items = json.load(f)
    mhgu_item_names = {i["_id"]: i.get("name","?") for i in _items if "_id" in i}

stats  = defaultdict(lambda: defaultdict(int))
errors = []

for game in sorted(os.listdir(SRC)):
    gpath = f"{SRC}/{game}"
    if not os.path.isdir(gpath): continue

    for root, dirs, files in os.walk(gpath):
        for fname in sorted(files):
            if not fname.endswith(".json"): continue
            if any(p in fname.lower() for p in SKIP): continue
            cat = infer_cat(fname)
            if cat not in FILE_NORM: continue
            norm_fn, out_cat = FILE_NORM[cat]

            fpath = os.path.join(root, fname)
            try:    records = load_arr(fpath)
            except Exception as e:
                errors.append(f"LOAD {fname}: {e}"); continue
            if not records: continue

            normalized = []
            for rec in records:
                try:
                    # MHGU weapons: injetar nome e sharpness pré-processados
                    if game == "mhgu" and cat == "weapons":
                        wid = rec.get("_id")
                        rec["name"] = mhgu_item_names.get(wid, f"weapon_{wid}")
                        s, shc = parse_mhgu_sharp(rec.get("sharpness",""))
                        rec["_sharpness_parsed"]    = s
                        rec["_sharpness_hc_parsed"] = shc
                        rec["_elem_type"]   = rec.get("element") or rec.get("awaken") or None
                        rec["_elem_attack"] = rec.get("element_attack") or rec.get("awaken_attack") or 0
                        rec["element"]      = rec.get("_elem_type")
                        rec["element_display"] = rec.get("_elem_attack")

                    # MHGU monsters: injetar hitzones e name_ja
                    if game == "mhgu" and cat == "monsters":
                        mid = rec.get("_id")
                        rec["name_ja"]  = rec.get("name_ja") or ""
                        rec["base_hp"]  = rec.get("base_hp")
                        rec["hitzones"] = mhgu_hitzones.get(mid)
                        rec["status_thresholds"] = mhgu_status_thr.get(mid)

                    normalized.append(norm_fn(rec, game, fname))
                except Exception as e:
                    errors.append(f"NORM {fname}[{rec.get('name','?')}]: {e}")

            if not normalized: continue
            out_dir = f"{OUT}/{game}/{out_cat}"
            os.makedirs(out_dir, exist_ok=True)
            out_path = f"{out_dir}/{fname.replace('.json','_normalized.json')}"
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(normalized, f, indent=2, ensure_ascii=False)
            stats[game][out_cat] += len(normalized)
            print(f"  ✅ {game:10s} {out_cat:13s} {len(normalized):>7,}  ← {fname}")

# ─── Novas entidades ──────────────────────────────────────────────────────────
print("\n── NOVAS ENTIDADES ──")

def save(data, game, entity, fname):
    if not data: return
    d = f"{OUT}/{game}/{entity}"
    os.makedirs(d, exist_ok=True)
    with open(f"{d}/{fname}", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  ✅ {game:10s} {entity:13s} {len(data):>7,}  ← {fname}")
    stats[game][entity] += len(data)

mhgu_sets, _ = build_armor_sets_mhgu()
save(mhgu_sets, "mhgu", "armor_sets", "mhgu_armor_sets_normalized.json")

world_sets, world_bonuses = build_armor_sets_world()
save(world_sets,   "world", "armor_sets",  "world_armor_sets_normalized.json")
save(world_bonuses,"world", "set_bonuses", "world_set_bonuses_normalized.json")

monster_rewards = build_monster_rewards_mhgu()
save(monster_rewards, "mhgu", "monster_rewards", "mhgu_monster_rewards_normalized.json")

quest_rewards = build_quest_rewards_mhgu()
save(quest_rewards, "mhgu", "quest_rewards", "mhgu_quest_rewards_normalized.json")

# ─── Relatório final ──────────────────────────────────────────────────────────
print("\n" + "="*65)
grand = sum(n for cats in stats.values() for n in cats.values())
for game, cats in sorted(stats.items()):
    t = sum(cats.values())
    print(f"\n  [{game.upper():12s}] {t:>8,}")
    for cat, n in sorted(cats.items()):
        print(f"    {cat:17s}: {n:>7,}")
print(f"\n  TOTAL: {grand:,}")
if errors:
    print(f"\n  ⚠️  {len(errors)} erros:")
    for e in errors[:15]: print(f"    {e}")

os.makedirs(OUT, exist_ok=True)
with open(f"{OUT}/normalization_report.json","w") as f:
    json.dump({"schema_version":"2.0.0","total":grand,
               "by_game":{g:dict(c) for g,c in stats.items()},
               "errors":errors}, f, indent=2, ensure_ascii=False)
