# MH-CORTEX SCHEMA FREEZE AUDIT — RELATÓRIO FINAL
**Data:** 2026-06-07  
**Método:** Auditoria baseada exclusivamente em dados reais das fontes do acervo  
**Fontes verificadas:** MHGU (gatheringhallstudios), MHWorld (gatheringhallstudios), MH3/Tri (maliciousbanjo/mh3-data), MHP3rd (mikejsavage), MHFU (JS-Jr + Kolyn090)

---

## 1. LACUNAS REAIS IDENTIFICADAS

### 1.1 WEAPON — 6 lacunas reais

| # | Dado Real | Fonte | Campo Ausente | Pode Ser Armazenado Hoje? |
|---|-----------|-------|---------------|--------------------------|
| W1 | Bowgun ammo config (clip, recoil, reload por tipo de ammo) | MHWorld `weapon_ammo` | Ausente — `type_specific` aceita objeto livre, mas nenhum schema definido | Parcialmente — cabe em `type_specific` mas sem estrutura |
| W2 | Bow coatings bitmask (`"1121"` em MHGU, flags `{close,power,poison...}` em World) | MHGU + MHWorld `weapon_bow_ext` | Ausente | Parcialmente — cabe em `type_specific` mas formatos incompatíveis entre jogos |
| W3 | Bow charges (`"Rapid 1|Rapid 1|Rapid 2|Spread 2*"`) | MHGU + MHP3rd | Ausente | Parcialmente — cabe em `type_specific` como string ou array |
| W4 | HH horn notes (`"WBR"` — sequência de notas) e melody data (duração base/ext) | MHGU + MHWorld `weapon_melody_*` | Ausente | Parcialmente — cabe em `type_specific` |
| W5 | Elderseal (low/average/high) | MHWorld `weapon_base.elderseal` | Ausente | Não — `damage` não tem campo para isso |
| W6 | Kinsect bonus (affinity/element/speed/etc) | MHWorld `weapon_base.kinsect_bonus` | Ausente | Parcialmente — cabe em `type_specific` |

**Diagnóstico `type_specific`:** O campo existe mas é `object | null` sem schema. Isso funciona para dados arbitrários mas significa que o normalizador não sabe como tratar cada tipo. A solução não é remover — é definir o schema interno de `type_specific` por `weapon_type`.

### 1.2 ARMOR — 3 lacunas reais

| # | Dado Real | Fonte | Pode Ser Armazenado Hoje? |
|---|-----------|-------|--------------------------|
| A1 | Set bonus (habilidade ativada com N peças do set) | MHWorld `armorset_bonus_base` — ex: "Anjanath Power: Adrenaline com 3 peças" | Não — `armor_piece` não tem referência ao set nem ao bonus |
| A2 | Armor series/set agrupamento (ex: "Leather Set" = 5 peças + nome do set + rank) | MHGU `armor_families` + MHWorld `armorset_base` | Não — `armor_piece` tem `family` int mas não há entidade `armor_set` |
| A3 | Defense augmented max (terceiro valor além de base e max) | MHWorld `armor_base.defense_augment_max` | Não — `defense` tem `{base, max}` mas falta `augmented_max` |

### 1.3 MONSTER — 7 lacunas reais

| # | Dado Real | Fonte | Pode Ser Armazenado Hoje? |
|---|-----------|-------|--------------------------|
| M1 | Hitzones com campo `ko` (KO por impacto na cabeça) | MHGU `mhgu_monster_damage.ko` | Não — schema de hitzone tem `{slash,blunt,shot,fire,water,thunder,ice,dragon}` mas falta `ko` |
| M2 | Status thresholds (initial, increase, max, duration, damage por status) | MHGU `mhgu_monster_status` | Não — `monster` não tem campo para isso |
| M3 | Habitat detalhado (start_area, move_area, rest_area por localização) | MHGU `mhgu_monster_habitat` | Não — `locations` é `array[string]`, não tem estrutura de área |
| M4 | Hunting rewards separados por condição (Body Carve, Tail Carve, Capture, Break: Horns, etc.) | MHGU `mhgu_hunting_rewards.condition` | Não — `monster` não tem rewards; estão num arquivo separado linkado por `monster_id` |
| M5 | Shiny drops por rank (low/high/G) | MHP3rd `monster.shinies[].{low,high}` | Não — `monster` não tem rewards |
| M6 | Base HP por rank | MHGU `mhgu_monsters_full.base_hp` | Parcialmente — `base_hp` existe na fonte mas não está no schema de monster |
| M7 | Estado do monstro para hitzones (Normal vs Enraged vs Part Broken) | MHGU `mhgu_monster_weakness.state` = "Normal" | Parcialmente — hitzones não tem campo `state` |

### 1.4 QUEST — 4 lacunas reais

| # | Dado Real | Fonte | Pode Ser Armazenado Hoje? |
|---|-----------|-------|--------------------------|
| Q1 | Subquest (sub_goal, sub_reward, sub_hrp separados da main quest) | MHGU `sub_goal`, `sub_reward`, `sub_hrp` | Não — schema não tem subquest |
| Q2 | HRP reward (hunter rank points) separado da zenny reward | MHGU `hrp` e `sub_hrp` | Não — schema tem só `contract_fee`, falta `zenny_reward` e `hrp_reward` |
| Q3 | Flavor text / quest description do cliente | MHGU `flavor`, `goal` text | Não — schema tem `name` mas não `description` nem `goal_text` |
| Q4 | Permit monster (monstro especial liberado pela quest) | MHGU `permit_monster_id` | Não — `targets` cobre inimigos principais, mas permit é diferente |

### 1.5 SKILL — 1 lacuna real

| # | Dado Real | Fonte | Pode Ser Armazenado Hoje? |
|---|-----------|-------|--------------------------|
| S1 | Points required por nível no sistema de skill trees (pre-World) | MHGU `mhgu_skill_trees` — cada skill tree tem threshold de ativação | Parcialmente — `levels[].points_required` existe no schema mas não está sendo populado |

### 1.6 ITEM — 0 lacunas reais

Schema atual suporta todos os campos encontrados nas fontes.

### 1.7 DECORATION — 0 lacunas reais

Schema atual suporta todos os campos encontrados nas fontes.

### 1.8 CHARM — 0 lacunas reais

Schema atual suporta todos os campos encontrados nas fontes.

---

## 2. ENTIDADES FALTANDO NO SCHEMA (não são campos — são entidades novas)

| Entidade | Dados Reais | Fontes |
|----------|-------------|--------|
| `armor_set` | Nome do set, rank, lista de armor_ids, set_bonus_id | MHGU `armor_families`, MHWorld `armorset_base` |
| `set_bonus` | Nome, skill ativada, peças necessárias | MHWorld `armorset_bonus_base` |
| `monster_reward` | monster_id, condition (Body Carve/Tail/Capture/Break), item_id, rank, chance, stack | MHGU `hunting_rewards`, MHP3rd `shinies` |
| `monster_status_threshold` | monster_id, status_type, initial, increase, max, duration, damage | MHGU `monster_status` |
| `quest_reward` | quest_id, item_id, reward_slot (A/B/C), chance, stack | MHGU `quest_rewards` |
| `location` | id, nome, áreas, jogos onde aparece | MHGU `locations` |
| `bowgun_ammo` | weapon_id, ammo_type, clip_size, recoil, reload_speed, rapid | MHWorld `weapon_ammo` |
| `hh_melody` | id, nome, notas, duração base/extension | MHWorld `weapon_melody_base` |

---

## 3. CAMPOS REDUNDANTES OU PROBLEMÁTICOS

| Campo | Entidade | Problema | Decisão |
|-------|----------|---------|---------|
| `weaknesses` em `monster` | monster | Duplica `mhgu_monster_weakness` que é mais completo (tem state, traps, bombs). Array simples de `{element, rating}` perde informação. | MANTER mas reconhecer que é simplificado |
| `hitzones` em `monster` | monster | Sem campo `ko` e sem campo `state`. Dados reais do MHGU têm ambos. | CORRIGIR |
| `locations` em `monster` | monster | `array[string]` simples. Dados reais têm start_area, move_area, rest_area. | MANTER como summary; habitat detalhado vai em `monster_reward` |
| `games` em `monster` | monster | Útil para cross-game. Dados reais têm isso (`all_monsters.json`). | MANTER |
| `element_display` e `element_true` em `damage` | weapon | `element_display` nunca é populado para Rise/Wilds (divisor = 1). Seria o mesmo valor. | MANTER — a semântica muda por jogo, precisa de ambos para clareza |
| `class_coefficient` em `damage` | weapon | Campo derivado (constante por tipo+jogo). Poderia ser lookup externo. | MANTER — facilita cálculos sem lookup |
| `max_level` em `skill` | skill | Derivado de `len(levels)`. | MANTER — útil quando `levels` está vazio |
| `sell_price` em `item` | item | Raramente presente nas fontes. | MANTER — será null na maioria |
| `games` em `monster` | monster | Duplica informação que está em `mhgu/world/rise` monsters separados. | MANTER para cross-game search |

---

## 4. AUDITORIA POR CHECKLIST

### MONSTER

| Dado | Status | Observação |
|------|--------|-----------|
| hitzones | ⚠️ PARCIAL | Falta campo `ko` e campo `state` (Normal/Enraged/Broken) |
| break rewards | ❌ NÃO SUPORTADO | `monster_reward` não existe no schema. Dado real em MHGU `hunting_rewards.condition = "Break: Horns"` |
| carve rewards | ❌ NÃO SUPORTADO | Idem — condition = "Body Carve" |
| capture rewards | ❌ NÃO SUPORTADO | Idem — condition = "Capture" |
| shiny drops | ❌ NÃO SUPORTADO | Dado real em MHP3rd `monster.shinies` |
| habitats | ⚠️ PARCIAL | `locations: array[string]` existe. start/move/rest_area não suportados |
| ecology | ❌ NÃO SUPORTADO | Nenhuma fonte tem isso estruturado |
| crown sizes | ❌ NÃO SUPORTADO | Nenhuma fonte tem isso estruturado |
| size data | ❌ NÃO SUPORTADO | Nenhuma fonte tem isso estruturado |
| body part HP | ❌ NÃO SUPORTADO | Nenhuma fonte tem isso estruturado (cálculo derivado de base_hp) |
| weak points | ✅ SUPORTADO | via `weaknesses` (simplificado) + `hitzones` |
| status weaknesses | ❌ NÃO SUPORTADO | `mhgu_monster_weakness` tem poison/paralysis/sleep/pitfall/shock/flash/sonic/dung — nenhum campo no schema |
| variant relationships | ❌ NÃO SUPORTADO | Nenhuma fonte tem campo `variant_of` estruturado |
| subspecies relationships | ❌ NÃO SUPORTADO | Idem |
| deviant relationships | ❌ NÃO SUPORTADO | Idem |
| rare species relationships | ❌ NÃO SUPORTADO | Idem |
| base_hp | ⚠️ PARCIAL | Existe em MHGU source mas não no schema |
| state-based hitzones | ⚠️ PARCIAL | MHGU weakness tem campo `state` = Normal/Enraged, hitzone não tem |

**Nota importante:** ecology, crown sizes, size data, body part HP, variant/subspecies/deviant relationships — **nenhuma fonte atual tem esses dados estruturados**. Não são lacunas do schema; são lacunas das fontes. O schema não precisa deles agora.

### WEAPON

| Dado | Status | Observação |
|------|--------|-----------|
| weapon trees | ✅ SUPORTADO | `craft.upgrade_from` (parent_id) define a árvore |
| upgrade paths | ✅ SUPORTADO | `craft.upgrade_from` + `craft.upgrade_materials` |
| creation paths | ✅ SUPORTADO | `craft.create_materials` |
| bow coatings | ⚠️ PARCIAL | Cabe em `type_specific` mas sem schema definido. Formatos: bitmask MHGU vs flags booleanas World |
| shelling data | ⚠️ PARCIAL | `type_specific` aceita, mas `"Normal 1"` (MHGU) vs `{type, level}` (World) são formatos diferentes |
| phial data | ⚠️ PARCIAL | Idem — `"Power"` (MHGU SA) vs `{type, power}` (CB World) |
| hunting horn notes | ⚠️ PARCIAL | `type_specific` aceita string `"WBR"` mas melody completa (duração) é entidade separada |
| kinsect bonuses | ⚠️ PARCIAL | MHWorld `kinsect_bonus` string — cabe em `type_specific` |
| rampage skills | ⚠️ PARCIAL | Rise `rampage_skills` array — cabe em `type_specific` |
| augment data | ❌ NÃO SUPORTADO | Nenhuma fonte atual tem augment data estruturado |
| layered weapon data | ❌ NÃO SUPORTADO | Nenhuma fonte atual tem isso estruturado |
| elderseal | ❌ NÃO SUPORTADO | Campo real em MHWorld — não tem lugar no schema atual |
| bowgun ammo | ❌ NÃO SUPORTADO | 50+ campos por arma (clip/recoil/reload por tipo de ammo). Entidade separada necessária |

### ARMOR

| Dado | Status | Observação |
|------|--------|-----------|
| armor sets | ❌ NÃO SUPORTADO | Entidade `armor_set` não existe. `armor_piece.family` é só um int |
| set bonuses | ❌ NÃO SUPORTADO | Entidade `set_bonus` não existe |
| layered armor | ❌ NÃO SUPORTADO | Nenhuma fonte tem isso estruturado |
| armor upgrades | ⚠️ PARCIAL | `defense.max` cobre upgrade max. `defense_augment_max` (World) não suportado |
| armor series | ❌ NÃO SUPORTADO | Entidade `armor_set` cobre isso |
| transmog systems | ❌ NÃO SUPORTADO | Nenhuma fonte tem isso estruturado |

### QUEST

| Dado | Status | Observação |
|------|--------|-----------|
| village quests | ✅ SUPORTADO | `hub = "village"` |
| guild quests | ✅ SUPORTADO | `hub = "city"/"guild"` |
| event quests | ✅ SUPORTADO | `hub = "event"` (MHGU tem) |
| DLC quests | ✅ SUPORTADO | `hub = "event"` ou flag |
| challenge quests | ⚠️ PARCIAL | `hub = "arena"` cobre parcialmente |
| arena quests | ✅ SUPORTADO | `hub = "arena"` |
| subquests | ❌ NÃO SUPORTADO | MHGU tem `sub_goal`, `sub_reward`, `sub_hrp` — não há campo no schema |
| locales | ⚠️ PARCIAL | `targets` tem monstros mas location está faltando no schema de quest |
| reward tables | ❌ NÃO SUPORTADO | Entidade `quest_reward` necessária |
| unlock chains | ❌ NÃO SUPORTADO | Nenhuma fonte tem isso estruturado |
| zenny reward | ❌ NÃO SUPORTADO | MHGU `reward` (zenny) + `sub_reward` — não há campo |
| hrp reward | ❌ NÃO SUPORTADO | MHGU `hrp` + `sub_hrp` — não há campo |
| flavor text | ❌ NÃO SUPORTADO | MHGU `flavor` — não há campo no schema |
| goal text | ❌ NÃO SUPORTADO | MHGU `goal` (texto descritivo) — não há campo |

### SKILL — Compatibilidade por sistema

| Jogo | Sistema | Status | Problema |
|------|---------|--------|---------|
| MH1–MHGU | Skill trees com threshold de pontos | ⚠️ PARCIAL | `skill.levels[].points_required` existe mas não está sendo populado |
| World/IB | Skill com níveis 1–N, sem tree | ✅ SUPORTADO | `levels[]` cobre perfeitamente |
| Rise/SB | Skill com níveis 1–N + Rampage skills (tipo diferente) | ⚠️ PARCIAL | Rampage skills são entidade diferente, não seriam skill regular |
| Wilds | Skills com GroupSkill + SeriesSkill (ativadas por set, não por peça) | ⚠️ PARCIAL | GroupSkill/SeriesSkill são análogos a set_bonus — não suportados |
| MHGU | Deviant skills (Striker/Aerial/etc por Hunter Style) | ⚠️ PARCIAL | Nenhuma fonte atual tem isso estruturado |

---

## 5. FUTURE SCRAPING TEST

**Se amanhã fossem raspados 100% do wikiwiki.jp, Kiranico, Fandom e GitHub restante:**

O que **quebraria** ou **não poderia ser armazenado** com o schema atual:

| Dado Raspado | Problema |
|--------------|---------|
| Kiranico MHGU — carve tables completas | `monster_reward` não existe |
| Kiranico MHGU — status thresholds (Poison: 180→580) | `monster_status_threshold` não existe |
| Fandom MH Wiki — set bonuses | `set_bonus` não existe |
| Fandom MH Wiki — armor sets | `armor_set` não existe |
| wikiwiki.jp/mhrise — quest rewards completos | `quest_reward` não existe |
| wikiwiki.jp/mhrise — subquests | campo `subquest` não existe em `quest` |
| Kiranico MHWorld — bowgun ammo config completa | `bowgun_ammo` não existe |
| Fandom — elderseal ratings | campo `elderseal` não existe em `damage` |
| wikiwiki.jp — state-based hitzones | campo `state` não existe em hitzone |
| wikiwiki.jp — habitat areas (start/move/rest) | estrutura de habitat não suporta isso |

**O que funcionaria sem alteração:**
- Nomes em japonês (name_ja) — suportado
- Weapons adicionais de qualquer tipo existente — suportado
- Armors adicionais — suportado
- Itens — suportado
- Skills individuais — suportado
- Monstros adicionais (sem rewards) — suportado
- Quests básicas (sem subquests, sem rewards) — suportado
- Decorations e charms — suportado

---

## 6. LISTA DE MELHORIAS

### 6.1 OBRIGATÓRIAS (dado real que não pode ser armazenado)

**Campos a adicionar em entidades existentes:**

```
weapon.damage.elderseal          string | null    — "low"|"average"|"high"|null
weapon.type_specific             Definir schema interno por weapon_type (ver abaixo)
monster.base_hp                  int | null
monster.hitzones[].ko            int              — KO damage rating
monster.hitzones[].state         string | null    — "Normal"|"Enraged"|"Broken: Part"
monster.status_thresholds        array | null     — LINK para monster_status_threshold
quest.subquest                   object | null    — {goal_text, reward_zenny, hrp}
quest.zenny_reward               int | null
quest.hrp_reward                 int | null
quest.goal_text                  string | null
quest.flavor_text                string | null
quest.location_id                string | null
armor_piece.defense.augmented_max  int | null
armor_piece.set_id               string | null    — FK para armor_set
```

**Novas entidades obrigatórias:**

```
armor_set         — nome, rank, peças, set_bonus_id
set_bonus         — nome, skills ativadas por N peças
monster_reward    — monster_id, condition, rank, item_id, chance, stack
quest_reward      — quest_id, item_id, slot, chance, stack
```

**Schema interno de `type_specific` por weapon_type:**

```json
{
  "Gunlance":      {"shelling_type": "string", "shelling_level": "int"},
  "Switch Axe":    {"phial_type": "string"},
  "Charge Blade":  {"phial_type": "string", "phial_power": "int | null"},
  "Hunting Horn":  {"notes": "string", "melody_ids": "array[string]"},
  "Bow":           {"coatings": "array[string]", "charges": "array[{type, level, is_arc}]"},
  "Light Bowgun":  {"ammo_config_id": "string | null", "special_ammo": "string | null", "deviation": "string"},
  "Heavy Bowgun":  {"ammo_config_id": "string | null", "special_ammo": "string | null", "deviation": "string"},
  "Insect Glaive": {"kinsect_bonus": "string | null"}
}
```

**Novas entidades para bowgun e HH:**

```
bowgun_ammo_config  — weapon_id, 50+ campos de ammo (clip/recoil/reload por tipo)
hh_melody           — id, nome, notas, duração_base, duração_ext
```

### 6.2 OPCIONAIS (dado real existe mas schema atual cobre parcialmente)

```
monster.habitat_details    — start_area, move_area, rest_area por localização
monster.variant_of         — id do monstro base (Subspecies/Deviant/Rare)
skill.points_required      — garantir que está sendo populado no normalizador
monster_status_threshold   — entidade separada (monster_id, status, initial, max, duration)
```

### 6.3 REJEITADAS

| Campo/Entidade | Motivo da Rejeição |
|----------------|-------------------|
| ecology | Nenhuma fonte atual tem isso estruturado |
| crown sizes / size multipliers | Nenhuma fonte atual tem isso estruturado |
| body part HP | Dado derivado de base_hp + fórmulas não documentadas — nenhuma fonte tem |
| layered armor / transmog | Nenhuma fonte atual tem isso estruturado |
| augment data (weapon/armor upgrades World) | Nenhuma fonte atual tem isso estruturado |
| unlock chains | Nenhuma fonte atual tem isso estruturado |
| variant/subspecies/deviant/rare relationships | Nenhuma fonte atual tem isso estruturado |

---

## 7. SCHEMA REVISADO

```json
{
  "weapon": {
    "id":           "string",
    "game":         "string",
    "name":         "string",
    "name_ja":      "string | null",
    "weapon_type":  "string",
    "rarity":       "int | null",
    "slots":        "int",
    "damage": {
      "display_raw":        "int",
      "true_raw":           "float",
      "class_coefficient":  "float",
      "affinity":           "int",
      "element_type":       "string | null",
      "element_display":    "int | null",
      "element_true":       "float | null",
      "element_hidden":     "bool",
      "elderseal":          "string | null  ← NOVO"
    },
    "sharpness": {
      "levels":     "{bars:{color:int}, highest:string, raw_multiplier:float, elem_multiplier:float} | null",
      "max_levels": "idem | null"
    },
    "craft": {
      "buy_price":          "int | null",
      "create_materials":   "array[{item_id, item_name, amount}]",
      "upgrade_from":       "string | null",
      "upgrade_materials":  "array[{item_id, item_name, amount}]"
    },
    "type_specific": "object com schema por weapon_type (ver acima)  ← DEFINIR SCHEMA",
    "source_file":  "string"
  },

  "armor_piece": {
    "id":       "string",
    "game":     "string",
    "name":     "string",
    "name_ja":  "string | null",
    "part":     "string",
    "type":     "string",
    "rarity":   "int | null",
    "gender":   "string | null",
    "set_id":   "string | null  ← NOVO",
    "defense": {
      "base":           "int",
      "max":            "int | null",
      "augmented_max":  "int | null  ← NOVO"
    },
    "resistances":  "{fire,water,thunder,ice,dragon: int}",
    "slots":        "array[int]",
    "skills":       "array[{skill_name, points}]",
    "craft": {
      "buy_price":        "int | null",
      "create_materials": "array[{item_id, item_name, amount}]"
    },
    "source_file": "string"
  },

  "armor_set": {
    "id":           "string  ← NOVA ENTIDADE",
    "game":         "string",
    "name":         "string",
    "name_ja":      "string | null",
    "rank":         "string",
    "type":         "string",
    "piece_ids":    "array[string]",
    "set_bonus_id": "string | null",
    "source_file":  "string"
  },

  "set_bonus": {
    "id":       "string  ← NOVA ENTIDADE",
    "game":     "string",
    "name":     "string",
    "name_ja":  "string | null",
    "thresholds": "array[{pieces_required: int, skill_name: string, skill_id: string | null}]",
    "source_file": "string"
  },

  "monster": {
    "id":        "string",
    "game":      "string",
    "name":      "string",
    "name_ja":   "string | null",
    "species":   "string",
    "is_large":  "bool",
    "base_hp":   "int | null  ← NOVO",
    "elements":  "array[string]",
    "ailments":  "array[string]",
    "weaknesses": "array[{element, rating}]",
    "hitzones": "array[{part, state, slash, blunt, shot, fire, water, thunder, ice, dragon, ko}]  ← state e ko NOVOS",
    "locations": "array[string]",
    "games":     "array[string]",
    "source_file": "string"
  },

  "monster_reward": {
    "id":          "string  ← NOVA ENTIDADE",
    "game":        "string",
    "monster_id":  "string",
    "condition":   "string  — 'Body Carve'|'Head Carve'|'Tail Carve'|'Capture'|'Break: Horns'|'Shiny'|...",
    "rank":        "string  — 'LR'|'HR'|'G'",
    "item_id":     "string",
    "item_name":   "string",
    "stack":       "int",
    "chance":      "float  — 0-100",
    "source_file": "string"
  },

  "skill": {
    "id":         "string",
    "game":       "string",
    "name":       "string",
    "name_ja":    "string | null",
    "tree_id":    "string | null",
    "tree_name":  "string | null",
    "levels":     "array[{level, name, description, points_required}]",
    "max_level":  "int",
    "source_file": "string"
  },

  "item": {
    "id":           "string",
    "game":         "string",
    "name":         "string",
    "name_ja":      "string | null",
    "description":  "string | null",
    "category":     "string | null",
    "rarity":       "int | null",
    "carry_max":    "int | null",
    "buy_price":    "int | null",
    "sell_price":   "int | null",
    "source_file":  "string"
  },

  "quest": {
    "id":             "string",
    "game":           "string",
    "name":           "string",
    "name_ja":        "string | null",
    "hub":            "string",
    "rank":           "string",
    "stars":          "string",
    "objective_type": "string",
    "goal_text":      "string | null  ← NOVO",
    "flavor_text":    "string | null  ← NOVO",
    "location_id":    "string | null  ← NOVO",
    "targets":        "array[{monster_id, monster_name, count}]",
    "contract_fee":   "int | null",
    "time_limit":     "int | null",
    "zenny_reward":   "int | null  ← NOVO",
    "hrp_reward":     "int | null  ← NOVO",
    "subquest": {
      "goal_text":    "string | null",
      "zenny_reward": "int | null",
      "hrp_reward":   "int | null"
    },
    "source_file": "string"
  },

  "quest_reward": {
    "id":         "string  ← NOVA ENTIDADE",
    "game":       "string",
    "quest_id":   "string",
    "item_id":    "string",
    "item_name":  "string",
    "slot":       "string  — 'A'|'B'|'C'|'D'",
    "stack":      "int",
    "chance":     "float",
    "source_file": "string"
  },

  "decoration": {
    "id":          "string",
    "game":        "string",
    "name":        "string",
    "name_ja":     "string | null",
    "slot_size":   "int",
    "skills":      "array[{skill_name, points}]",
    "craft":       "{materials: array[{item_id, item_name, amount}]}",
    "source_file": "string"
  },

  "charm": {
    "id":          "string",
    "game":        "string",
    "name":        "string | null",
    "skills":      "array[{skill_name, points}]",
    "slots":       "int",
    "source_file": "string"
  }
}
```

---

## 8. RISCO DE MUDANÇA

| Alteração | Risco | Compatibilidade Retroativa |
|-----------|-------|--------------------------|
| Adicionar `elderseal` em `damage` | Baixo | Sim — campo opcional, null por default |
| Adicionar `base_hp` em `monster` | Baixo | Sim — campo opcional, null por default |
| Adicionar `ko` e `state` em hitzones | Médio | Sim — campos opcionais |
| Adicionar `goal_text`, `flavor_text`, `location_id` em `quest` | Baixo | Sim — campos opcionais |
| Adicionar `zenny_reward`, `hrp_reward` em `quest` | Baixo | Sim — campos opcionais |
| Adicionar `subquest` object em `quest` | Baixo | Sim — objeto opcional, null por default |
| Adicionar `set_id` em `armor_piece` | Baixo | Sim — campo opcional, null por default |
| Adicionar `augmented_max` em `defense` | Baixo | Sim — campo opcional |
| Definir schema interno de `type_specific` | Baixo | Sim — só documenta o que já existe |
| Criar entidades `armor_set` e `set_bonus` | Zero | Sim — novas entidades não afetam existentes |
| Criar entidade `monster_reward` | Zero | Sim — nova entidade |
| Criar entidade `quest_reward` | Zero | Sim — nova entidade |

**Nenhuma alteração quebra dados já normalizados.** Todos os campos novos são opcionais.

---

## 9. COMPATIBILIDADE RETROATIVA

**100% retrocompatível.** Nenhum campo existente é removido ou renomeado.  
Os arquivos `_normalized.json` gerados até agora permanecem válidos.  
As novas entidades (`armor_set`, `set_bonus`, `monster_reward`, `quest_reward`) são arquivos separados.

---

## 10. NOTA FINAL DE COMPLETUDE

| Entidade | Completude Atual | Pós-Revisão |
|----------|-----------------|-------------|
| weapon | 88% | 95% |
| armor_piece | 82% | 92% |
| armor_set | 0% | 90% (nova entidade) |
| set_bonus | 0% | 90% (nova entidade) |
| skill | 90% | 95% |
| monster | 65% | 80% |
| monster_reward | 0% | 90% (nova entidade) |
| item | 98% | 98% |
| quest | 70% | 88% |
| quest_reward | 0% | 90% (nova entidade) |
| decoration | 98% | 98% |
| charm | 98% | 98% |
| **GERAL** | **~78%** | **~92%** |

---

## VEREDICTO

**O schema NÃO pode ser congelado ainda.**  
Há **14 campos** faltando em entidades existentes e **4 entidades** ausentes que têm dados reais nas fontes atuais.

**O schema PODE ser congelado após aplicar as melhorias obrigatórias da seção 6.1.**  
Todas as alterações são retrocompatíveis e de baixo risco.

**Estimativa:** aplicar as correções e rerodar o normalizador completo é um único ciclo de trabalho. Após isso, o schema estará em ~92% de completude e pronto para ser congelado — qualquer dado que chegar do scraping manual entra sem alterar o schema.
