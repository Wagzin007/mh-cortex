# MH-Cortex DB

**A free, open-source Monster Hunter franchise database for the community.**

Normalized JSON data covering weapons, armors, monsters, skills, items, quests, decorations, and charms across all mainline Monster Hunter titles — built and maintained by the community, for the community.

> Monster Hunter is a trademark of Capcom Co., Ltd. This project contains fan-curated data derived from public community sources and is not affiliated with or endorsed by Capcom.

---

## Contents

- [Purpose](#purpose)
- [Coverage](#coverage)
- [Repository Structure](#repository-structure)
- [Schema](#schema)
- [How to Use the Data](#how-to-use-the-data)
- [Contributing](#contributing)
- [Data Sources](#data-sources)
- [License](#license)

---

## Purpose

There is no single, reliable, machine-readable Monster Hunter database that covers the full franchise. Existing resources are scattered across wikis, game-specific apps, and community GitHub repos — each with different formats, missing fields, and inconsistent naming.

MH-Cortex DB aims to fix that:

- **Free** — no paywalls, no API keys, no rate limits. Raw JSON files you can download and use directly.
- **Normalized** — every entity follows a consistent schema across all games. A weapon from MHP3rd and a weapon from MH Wilds have the same structure.
- **Cross-game** — covers MH1 through MH Wilds, including portable titles (MHF, MHP3rd, MHGU) and modern entries (World, Rise, Wilds).
- **Community-maintained** — data is curated manually from public sources, corrected, and versioned.

---

## Coverage

| Game | Monsters | Weapons | Armors | Items | Skills | Quests | Extras |
|------|:---:|:---:|:---:|:---:|:---:|:---:|---|
| MH1 / MHG | — | ❌ | ❌ | ❌ | ❌ | ❌ | — |
| MH2 / Dos | — | ❌ | ✅ 1.102 | ❌ | ✅ 198 | ❌ | ✅ 122 decos |
| MH3 / Tri | ✅ 35 | ✅ 327 | ✅ 568 | ✅ 585 | ✅ 83 | ✅ 152 | decos |
| MHP3rd | ✅ 60 | ✅ 522 | ✅ 1.020 | ✅ 813 | ✅ 100 | ❌ | decos |
| MHFU | via cross-game | ✅ 1.500 | ✅ 2.081 | ✅ 919 | ✅ 214 | ✅ 408 | decos, maps, trenya |
| MHGU / XX | ✅ 129 | ✅ 10.877 | ✅ 5.637 | ✅ 21.153 | ✅ 326 | ✅ 1.355 | hitzones, rewards ✅ |
| MH World / IB | ✅ 90 | ✅ 13.442 | ✅ 7.168 | ✅ 2.750 | ✅ 774 | ✅ 6.629 | set bonuses |
| MH Rise / SB | ✅ 70 | ✅ 1.860 | ✅ 1.213 | ✅ 1.000 | ✅ 111 | ❌ | decos |
| MH Wilds | ✅ 49 + hitzones | ❌ | ✅ 427 | ❌ | ✅ partial | ❌ | charms, decos ✅ |
| Cross-game | ✅ 337 + icons | — | — | — | — | — | 854 PNG icons |

**Total: ~227.000+ records across all games.**

❌ = absent or incomplete — contributions welcome.

---

## Repository Structure

```
mh-cortex-db/
│
├── normalized_v2/                  # Main data — all normalized JSON files
│   ├── mhgu/
│   │   ├── weapons/
│   │   │   └── mhgu_weapons_normalized.json
│   │   ├── armors/
│   │   ├── armor_sets/
│   │   ├── monsters/
│   │   ├── items/
│   │   ├── skills/
│   │   ├── quests/
│   │   ├── decorations/
│   │   ├── quest_rewards/
│   │   └── monster_rewards/
│   ├── world/
│   │   ├── weapons/
│   │   ├── armors/
│   │   ├── armor_sets/
│   │   ├── monsters/
│   │   ├── items/
│   │   ├── skills/
│   │   ├── quests/
│   │   └── set_bonuses/
│   ├── rise/
│   ├── wilds/
│   ├── mhp3rd/
│   ├── mh3tri/
│   ├── mhdos/
│   ├── mhfu/
│   └── cross-game/
│       └── monsters/               # Cross-game monster list + icons
│
├── docs/
│   ├── SCHEMA.md                   # Full schema reference (this document)
│   ├── SCHEMA_FREEZE_AUDIT.md      # Audit log of schema decisions
│   └── FONTE_CHECKLIST.md          # Data source checklist and coverage status
│
├── schema_canonical.json           # Machine-readable schema definition
├── normalization_report.json       # Stats from last normalization run
├── LICENSE
└── README.md
```

---

## Schema

All records follow **schema v2**. Every entity has an `id`, `game`, and `source_file` field for traceability.

Full reference: [`docs/SCHEMA.md`](docs/SCHEMA.md)

### Entities

| Entity | File pattern | Description |
|--------|-------------|-------------|
| `weapon` | `*_weapons_normalized.json` | Weapons with damage, sharpness, crafting tree, type-specific data |
| `armor_piece` | `*_armors_normalized.json` | Individual armor pieces with skills, resistances, defense |
| `armor_set` | `*_armor_sets_normalized.json` | Armor set groupings with set bonus reference |
| `set_bonus` | `*_set_bonuses_normalized.json` | Skills activated by equipping N pieces of a set |
| `monster` | `*_monsters_normalized.json` | Monsters with hitzones, weaknesses, locations, base HP |
| `monster_reward` | `*_monster_rewards_normalized.json` | Carve/capture/break reward tables with drop rates |
| `skill` | `*_skills_normalized.json` | Skills with level descriptions and point thresholds |
| `item` | `*_items_normalized.json` | Items with carry limits, buy/sell prices, categories |
| `quest` | `*_quests_normalized.json` | Quests with targets, rewards, subquests, flavor text |
| `quest_reward` | `*_quest_rewards_normalized.json` | Quest reward tables with slot/chance data |
| `decoration` | `*_decorations_normalized.json` | Decorations with slot size and skills |
| `charm` | `*_charms_normalized.json` | Charms/talismans with skills and slots |

### Key field conventions

- **IDs** — `{game}_{entity}_{sequential}`, e.g. `mhgu_weapon_0042`
- **game field** — lowercase short name: `mhgu`, `world`, `rise`, `wilds`, `mhp3rd`, `mh3tri`, `mhdos`, `mhfu`
- **null vs absent** — fields that have no data for a given game are `null`, never omitted
- **name_ja** — Japanese name when available, `null` otherwise
- **source_file** — original filename the record was normalized from

### Weapon damage fields

```json
"damage": {
  "display_raw": 210,
  "true_raw": 140.0,
  "class_coefficient": 4.8,
  "affinity": 15,
  "element_type": "Fire",
  "element_display": 300,
  "element_true": 30.0,
  "element_hidden": false,
  "elderseal": null
}
```

`true_raw = display_raw / class_coefficient`. Use `true_raw` for damage calculations.

### Hitzone fields

```json
{
  "part": "Head",
  "state": "Normal",
  "slash": 65,
  "blunt": 70,
  "shot": 55,
  "fire": 20,
  "water": 0,
  "thunder": 15,
  "ice": 10,
  "dragon": 25,
  "ko": 100
}
```

`state` is `"Normal"`, `"Enraged"`, `"Broken: Part"`, or `null` for games that don't differentiate.

### Type-specific weapon data

The `type_specific` field holds weapon-type data that doesn't apply universally:

| Weapon type | Fields |
|-------------|--------|
| Gunlance | `shelling_type`, `shelling_level` |
| Switch Axe | `phial_type` |
| Charge Blade | `phial_type`, `phial_power` |
| Hunting Horn | `notes` (e.g. `"WBR"`), `melody_ids` |
| Bow | `coatings` (array), `charges` (array of `{type, level, is_arc}`) |
| Light Bowgun | `special_ammo`, `deviation` |
| Heavy Bowgun | `special_ammo`, `deviation` |
| Insect Glaive | `kinsect_bonus` |

---

## How to Use the Data

The files are plain JSON — no dependencies, no build step.

**Load a specific game's weapons:**

```python
import json

with open("normalized_v2/mhgu/weapons/mhgu_weapons_normalized.json") as f:
    weapons = json.load(f)

# Filter by weapon type
greatswords = [w for w in weapons if w["weapon_type"] == "Great Sword"]
```

**Find all monsters weak to fire (hitzone > 20):**

```python
with open("normalized_v2/world/monsters/mhworld_monsters_detailed_normalized.json") as f:
    monsters = json.load(f)

weak_to_fire = [
    m["name"] for m in monsters
    if any(h["fire"] > 20 for h in (m.get("hitzones") or []))
]
```

**Cross-game monster lookup:**

```python
with open("normalized_v2/cross-game/monsters/all_monsters_normalized.json") as f:
    all_monsters = json.load(f)

# Find which games a monster appears in
rathalos = next(m for m in all_monsters if "Rathalos" in m["name"])
print(rathalos["games"])
```

---

## Contributing

### Adding missing data

The priority gaps are documented in [`docs/FONTE_CHECKLIST.md`](docs/FONTE_CHECKLIST.md). The main ones:

1. **MHGU charms** — talismans/charm tables are completely absent
2. **Rise / Sunbreak quests** — zero quests in the dataset
3. **MH2 / Dos weapons and items** — completely absent
4. **MHP3rd Bow, LBG, HBG** — the three ranged types are missing

### Submitting data

1. Fork the repo
2. Add your normalized JSON file(s) following the schema in [`docs/SCHEMA.md`](docs/SCHEMA.md)
3. Place files in the correct `normalized_v2/{game}/{entity}/` folder
4. Open a PR with a description of what was added and the source

### Reporting errors

Open an issue with the file name, the record `id`, and what the correct value should be. Source citations help a lot.

### Schema changes

Schema is currently **not frozen** (v2, under active curation). If you find data that doesn't fit the current schema, open an issue before submitting data — a schema fix may be needed first.

---

## Data Sources

All data is derived from public community sources. Original credits:

| Source | Games covered |
|--------|--------------|
| [gatheringhallstudios/MHGenDatabase](https://github.com/gatheringhallstudios/MHGenDatabase) | MHGU / XX |
| [gatheringhallstudios/MHWorldData](https://github.com/gatheringhallstudios/MHWorldData) | MH World / Iceborne |
| [mikejsavage/MHP3DB](https://github.com/mikejsavage/MHP3DB) | MHP3rd |
| [JS-Jr/MHFU-Database-Companion](https://github.com/JS-Jr/MHFU-Database-Companion) | MHFU |
| [Kolyn090/mhfu-db](https://github.com/Kolyn090/mhfu-db) | MHFU |
| [Badge87/MHRiseScraperData](https://github.com/Badge87/MHRiseScraperData) | MH Rise |
| [itytophile/monster-hunter-rise-armors](https://github.com/itytophile/monster-hunter-rise-armors) | MH Rise |
| [ParrotTulips/mhwilds-metadata](https://github.com/ParrotTulips/mhwilds-metadata) | MH Wilds |
| [CrimsonNynja/monster-hunter-DB](https://github.com/CrimsonNynja/monster-hunter-DB) | Cross-game |
| [Neryss/monster_hunter_db](https://github.com/Neryss/monster_hunter_db) | World / Rise / Wilds |
| [maliciousbanjo/mh3-data](https://github.com/maliciousbanjo/mh3-data) | MH3 / Tri |
| [TimH96/mhtri-armor-set-searcher](https://github.com/TimH96/mhtri-armor-set-searcher) | MH3 / Tri |
| [TimH96/mhdos-armor-set-searcher](https://github.com/TimH96/mhdos-armor-set-searcher) | MH2 / Dos |
| Community wikis (wikiwiki.jp, kiranico.com, fandom) | Various |

---

## License

MIT License — see [LICENSE](LICENSE) for full text.

The normalization pipeline, schema design, and curated corrections are original work released under MIT.  
Monster Hunter game data belongs to Capcom Co., Ltd. and is used here under fair use for non-commercial, community reference purposes.
