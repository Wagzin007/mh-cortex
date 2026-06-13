# MH-CORTEX — CHECKLIST DE FONTES
**Atualizado:** 2026-06-07  
**Status geral:** ~227k registros no acervo

---

## ✅ FONTES ESGOTADAS (feitas pelo agente)

| Fonte | Jogo | O que trouxe |
|-------|------|-------------|
| `TimH96/mhtri-armor-set-searcher` | MH3/Tri | 568 armaduras (enriquecidas: rarity, resistances, skill_points) |
| `TimH96/mhdos-armor-set-searcher` | MH2/Dos | 1.102 armaduras, 198 skill effects, 122 decorações |
| `mikejsavage/MHP3DB` | MHP3rd | 522 weapons, 1.020 armaduras, 813 itens, 60 monstros, 100 skills, 164 decos |
| `Kolyn090/mhfu-db` | MHFU | 2.170 armaduras alt, 1.259 itens alt, 192 decos, 21 mapas, trenya, veggie elder, awards |
| `maliciousbanjo/mh3-data` (npm) | MH3/Tri | 327 weapons reais (era 12 esqueletos), 152 quests, 585 itens, 83 skills |
| `itytophile/monster-hunter-rise-armors` | Rise | 587 armaduras com skills nomeadas e resistências (formato .ron convertido) |
| `ParrotTulips/mhwilds-metadata` (npm+tsc) | Wilds | 427 armaduras, 163 charms, 361 decorações, 30 monstros c/ hitzones, 11 skill groups |
| `gatheringhallstudios/MHGenDatabase` | MHGU | Base completa: 10.877 weapons, 5.637 armaduras, 21.153 itens, 1.355 quests, 175k+ registros |
| `gatheringhallstudios/MHWorldData` | World+IB | 13.442 weapons, 7.168 armaduras, 2.750 itens, 6.629 quests, 774 skills |
| `gatheringhallstudios/MHWorldDatabase` | World+IB | 92 monster icons (IDs numéricos) |
| `JS-Jr/MHFU-Database-Companion` | MHFU | 1.500 weapons, 2.081 armaduras, 919 itens, 214 skills, 408 quests |
| `Badge87/MHRiseScraperData` | Rise | 1.860 weapons, 626 armaduras, 1.000 itens, 111 skills, 101 decos |
| `Neryss/monster_hunter_db` | World/Rise/Wilds | monstros detalhados: 90 (World), 70 (Rise), 19 (Wilds) |
| `CrimsonNynja/monster-hunter-DB` | Multi | 337 monstros cross-game + 854 ícones PNG |

---

## 🔴 PRECISA DA TUA INTERVENÇÃO (scrap manual no browser)

### Alta prioridade — dados que impactam diretamente o MH-Cortex

| Alvo | Jogo | O que buscar | URL |
|------|------|-------------|-----|
| wikiwiki.jp/mhxx | MHGU/XX | **Charms/talismãs** (tabelas de possibilidade por nível) — maior lacuna do acervo | `https://wikiwiki.jp/mhxx/タリスマン` |
| wikiwiki.jp/mhrise | Rise/SB | **Quests completas** (Village + Hub + Sunbreak) — zero quests no acervo | `https://wikiwiki.jp/mhrise/クエスト` |
| wikiwiki.jp/mh2 | MH2/Dos | **Weapons** (todas as árvores) e **itens** — completamente ausentes | `https://wikiwiki.jp/mh2/武器` |
| wikiwiki.jp/mhp3 | MHP3rd | **Bow, LBG, HBG** — os 3 tipos que o mikejsavage não coletou | `https://wikiwiki.jp/mhp3/武器` |

### Média prioridade

| Alvo | Jogo | O que buscar | URL |
|------|------|-------------|-----|
| wikiwiki.jp/mh3 | MH3/Tri | **Bow, LBG, HBG + quests completas** (temos 152, jogo tem ~300+) | `https://wikiwiki.jp/mh3/武器` |
| wikiwiki.jp/mhxx | MHGU | **name_ja de monstros/skills/itens** — campos `_ja` todos vazios no acervo | `https://wikiwiki.jp/mhxx/モンスター` |
| kiranico.com/mhrise | Rise/SB | Quests, se wikiwiki falhar. EN, mais fácil de processar | `https://mhrise.kiranico.com/data/quests` |
| monsterhunter.fandom.com | MH1/MHG | Únicos dados estruturados disponíveis para esses dois jogos | `https://monsterhunter.fandom.com/wiki/MH1:_Weapons` |

### Baixa prioridade (jogos antigos, cobertura mínima esperada)

| Alvo | Jogo | O que buscar |
|------|------|-------------|
| wikiwiki.jp/mhf | MHF1 | Weapons, armaduras básicas |
| wikiwiki.jp/mhf2 | MHF2 | Weapons, armaduras |
| gamefaqs.gamespot.com | MH1/MHDos | FAQs com dados tabulados de weapons/armors |

---

## ⚙️ COMO USAR O SCRAPER NAS URLS ACIMA

```bash
# Exemplo para MHGU charms (alta prioridade)
python scraper.py https://wikiwiki.jp/mhxx/タリスマン --depth 2 --output mhxx_charms

# Exemplo para Rise quests
python scraper.py https://wikiwiki.jp/mhrise/クエスト --filter クエスト --depth 2 --output mhrise_quests

# Exemplo para MH2 weapons
python scraper.py https://wikiwiki.jp/mh2/武器 --filter 武器 --depth 2 --output mh2_weapons

# Depois me passa as pastas geradas — eu processo e integro no acervo
```

**Importante:** usa `--depth 1` primeiro pra testar antes de ampliar.

---

## 📊 ESTADO ATUAL DO ACERVO (pós-expedição)

| Jogo | Monsters | Weapons | Armors | Items | Skills | Quests | Extras |
|------|---------|---------|--------|-------|--------|--------|--------|
| MHFU | via all_monsters | 1.500 | 2.081 | 919 | 214 | 408 | decos, mapas, trenya ✅ |
| MH2/Dos | — | ❌ | 1.102 | ❌ | 198 effects | ❌ | 122 decos |
| MH3/Tri | 35 | 327 (sem bow/bowguns) | 568 | 585 | 83 | 152 | 131 decos |
| MHP3rd | 60 | 522 (sem bow/bowguns) | 1.020 | 813 | 100 | ❌ | 164 decos |
| MHGU | 129 | 10.877 | 5.637 | 21.153 | 326 | 1.355 | hitzones, rewards, gathering ✅ |
| MHWorld+IB | 90 | 13.442 | 7.168 | 2.750 | 774 | 6.629 | — |
| Rise+SB | 70 | 1.860 | 626+587 | 1.000 | 111 | ❌ | 101 decos |
| MHWilds | 19+30 hitzones | ❌ | 427 | ❌ | 11 groups | ❌ | 163 charms, 361 decos ✅ |
| MH1/MHG | — | ❌ | ❌ | ❌ | ❌ | ❌ | — |
| MHStories 1/2 | via all_monsters | ❌ | ❌ | ❌ | ❌ | ❌ | — |

**❌ = ausente | ✅ = cobertura além do básico**

---

## 🔒 FONTES DESCARTADAS (bloqueadas na rede do container)

Todos esses domínios retornam **403** aqui mas devem funcionar no teu browser:

- `wikiwiki.jp` — wiki japonesa principal (todos os jogos)
- `kiranico.com` — base de dados estruturada EN (MHGU, Rise, World)
- `monsterhunter.fandom.com` — wiki EN com dados históricos (MH1, MHG, MHDos)
- `gamefaqs.gamespot.com` — FAQs tabulados de jogos antigos
- `mhrise-db.com` — base de dados Rise
- `gorillawiki.jp` — wikis por jogo (mh2, mh3, mhp3rd)
- `mhgu.kiranico.com` — MHGU completo incluindo charms

---
*Gerado automaticamente pelo MH-CORTEX DB CURATOR PROTOCOL v1.0*
