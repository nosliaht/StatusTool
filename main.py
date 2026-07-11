from __future__ import annotations

import re
import tkinter as tk
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation, ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_UP
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Callable

# =============================================================================
# CORES (Tema Escuro Profissional)
# =============================================================================
COLORS = {
    "background": "#0D1117",
    "header": "#161B22",
    "card": "#111820",
    "highlight": "#2FBC72",
    "text": "#F0F6FC",
    "text_muted": "#8B949E",
    "button": "#21262D",
    "button_text": "#F0F6FC",
    "button_active": "#2FBC72",
    "button_active_text": "#07130C",
    "frame_selected": "#2FBC72",
    "frame_normal": "#151B23",
    "border": "#30363D",
}

# =============================================================================
# ITEM INDEX (|V.6|194|)
# =============================================================================
FIELD_INDEX = {
    "Id": 0,
    "IconFilename": 1,
    "ModelId": 2,
    "ModelFilename": 3,
    "WeaponEffectId": 4,
    "FlyEffectId": 5,
    "UsedEffectId": 6,
    "UsedSoundName": 7,
    "EnhanceEffectId": 8,
    "Name": 9,
    "ItemType": 10,
    "EquipType": 11,
    "OpFlags": 12,
    "OpFlagsPlus": 13,
    "Target": 14,
    "RestrictGender": 15,
    "RestrictLevel": 16,
    "RestrictMaxLevel": 17,
    "RebirthCount": 18,
    "RebirthScore": 19,
    "RebirthMaxScore": 20,
    "RestrictAlign": 21,
    "RestrictPrestige": 22,
    "RestrictClass": 23,
    "ItemQuality": 24,
    "ItemGroup": 25,
    "CastingTime": 26,
    "CoolDownTime": 27,
    "CoolDownGroup": 28,
    "MaxHp": 29,
    "MaxMp": 30,
    "Str": 31,
    "Con": 32,
    "Int": 33,
    "Vol": 34,
    "Dex": 35,
    "AvgPhysicoDamage": 36,
    "RandPhysicoDamage": 37,
    "AttackRange": 38,
    "AttackSpeed": 39,
    "Attack": 40,
    "RangeAttack": 41,
    "PhysicoDefence": 42,
    "MagicDamage": 43,
    "MagicDefence": 44,
    "HitRate": 45,
    "DodgeRate": 46,
    "PhysicoCriticalRate": 47,
    "PhysicoCriticalDamage": 48,
    "MagicCriticalRate": 49,
    "MagicCriticalDamage": 50,
    "PhysicalPenetration": 51,
    "MagicalPenetration": 52,
    "PhysicalPenetrationDefence": 53,
    "MagicalPenetrationDefence": 54,
    "Attribute": 55,
    "AttributeRate": 56,
    "AttributeDamage": 57,
    "AttributeResist": 58,
    "SpecialType": 59,
    "SpecialRate": 60,
    "SpecialDamage": 61,
    "DropRate": 62,
    "DropIndex": 63,
    "TreasureBuffs0": 64,
    "TreasureBuffs1": 65,
    "TreasureBuffs2": 66,
    "TreasureBuffs3": 67,
    "EnchantType": 68,
    "EnchantId": 69,
    "ExpertLevel": 70,
    "ExpertEnchantId": 71,
    "ElfSkillId": 72,
    "EnchantTimeType": 73,
    "EnchantDuration": 74,
    "LimitType": 75,
    "DueDateTime": 76,
    "BackpackSize": 77,
    "MaxSocket": 78,
    "SocketRate": 79,
    "MaxDurability": 80,
    "MaxStack": 81,
    "ShopPriceType": 82,
    "SysPrice": 83,
    "RestrictEventPosId": 84,
    "TargetIDs": 85,
    "BlockRate": 86,
    "LogLevel": 87,
    "AuctionType": 88,
    "ExtraData0": 89,
    "ExtraData1": 90,
    "ExtraData2": 91,
    "Tip": 92,
}

# =============================================================================
# SPELL INDEX (|V.10|71|)
# =============================================================================
SPELL_INDEX = {
    "Id": 0,
    "IconFilename": 1,
    "CastingAnimId": 2,
    "ShootAnimId": 3,
    "CastingEffectId": 4,
    "ShootEffectId": 5,
    "FlyEffectId": 6,
    "HitEffectId": 7,
    "HitNode": 8,
    "HitSound": 9,
    "ShowEquip": 10,
    "Name": 11,
    "SpellType": 12,
    "SpellFlag": 13,
    "OpFlag": 14,
    "Target": 15,
    "RestrictEquip": 16,
    "RestrictLeve": 17,
    "RestrictClass": 18,
    "RebirthCount": 19,
    "RebirthScore": 20,
    "RestrictForm": 21,
    "UseItemId": 22,
    "ComboPoint": 23,
    "CastingTime": 24,
    "CoolDownTime": 25,
    "CoolDownGroup": 26,
    "AreaSpellType": 27,
    "Range": 28,
    "Radius": 29,
    "AreaSpellParameter": 30,
    "Mp": 31,
    "Hp": 32,
    "HpRate": 33,
    "KeepingHitPeriod": 34,
    "AvgDamage": 35,
    "RandDamage": 36,
    "DamageRate": 37,
    "ComboPoint1_avgDamage": 38,
    "ComboPoint1_randDamage": 39,
    "ComboPoint1_damageRate": 40,
    "ComboPoint2_avgDamage": 41,
    "ComboPoint2_randDamage": 42,
    "ComboPoint2_damageRate": 43,
    "ComboPoint3_avgDamage": 44,
    "ComboPoint3_randDamage": 45,
    "ComboPoint3_damageRate": 46,
    "ComboPoint4_avgDamage": 47,
    "ComboPoint4_randDamage": 48,
    "ComboPoint4_damageRate": 49,
    "BreakSpellRate": 50,
    "Attribute": 51,
    "AttributeDamage": 52,
    "AttributeRate": 53,
    "SpecialType": 54,
    "SpecialRate": 55,
    "SpecialDamage": 56,
    "EnchantId": 57,
    "EnchantRate": 58,
    "EnchantDuration": 59,
    "ComboPoint1_duration": 60,
    "ComboPoint2_duration": 61,
    "ComboPoint3_duration": 62,
    "ComboPoint4_duration": 63,
    "SelfEnchantId": 64,
    "SelfEnchantRate": 65,
    "SelfEnchantDuration": 66,
    "LearnPrice": 67,
    "LearnDependentSpellId": 68,
    "SpellSet": 69,
    "Tip": 70,
}

# =============================================================================
# ENCHANT INDEX (|V.10|63|)
# =============================================================================
ENCHANT_INDEX = {
    "Id": 0,
    "IconFilename": 1,
    "AnimId": 2,
    "EffectId": 3,
    "EffectNode": 4,
    "Name": 5,
    "EnchantType": 6,
    "EnchantFlag": 7,
    "EnchantCategory": 8,
    "ImmuneMonsterType": 9,
    "Cmd1_Id": 10,
    "Cmd1_Param1": 11,
    "Cmd1_Param2": 12,
    "Cmd1_Param3": 13,
    "Cmd1_Param4": 14,
    "Cmd1_Param5": 15,
    "Cmd1_Param6": 16,
    "Cmd2_Id": 17,
    "Cmd2_Param1": 18,
    "Cmd2_Param2": 19,
    "Cmd2_Param3": 20,
    "Cmd2_Param4": 21,
    "Cmd2_Param5": 22,
    "Cmd2_Param6": 23,
    "Cmd3_Id": 24,
    "Cmd3_Param1": 25,
    "Cmd3_Param2": 26,
    "Cmd3_Param3": 27,
    "Cmd3_Param4": 28,
    "Cmd3_Param5": 29,
    "Cmd3_Param6": 30,
    "Cmd4_Id": 31,
    "Cmd4_Param1": 32,
    "Cmd4_Param2": 33,
    "Cmd4_Param3": 34,
    "Cmd4_Param4": 35,
    "Cmd4_Param5": 36,
    "Cmd4_Param6": 37,
    "Period": 38,
    "Hiword": 39,
    "Lowword": 40,
    "TransitionCmd": 41,
    "EnchantTransition": 42,
    "TransitionRate": 43,
    "TransitionDuration": 44,
    "TransitionPeriod": 45,
    "TransitionIconFilename": 46,
    "TransitionEnchantType": 47,
    "TransitionEnchantFlag": 48,
    "TransitionEnchantCategory": 49,
    "TransitionAnimId": 50,
    "TransitionEffectId": 51,
    "TransitionEffectNode": 52,
    "TransitionEffectDuration": 53,
    "TransitionEffectDurationNode": 54,
    "TransitionCooldownTime": 55,
    "WeaponFlag": 56,
    "TransitionEnchantHiword": 57,
    "TransitionEnchantLowword": 58,
    "Tip": 59,
    "TransitionTip": 60,
    "TransitionName": 61,
    "MaxStack": 62,
}

# =============================================================================
# CLASS DEFINITIONS WITH SUBGROUPS
# =============================================================================
CLASS_GROUPS = [
    ("Fighter", [
        ("Ocupações Básicas", [
            ("Fighter", 0x0002),
            ("Warrior", 0x0004),
        ]),
        ("Defesa", [
            ("Paladin", 0x0010),
            ("Templar", 0x40000),
            ("Royal Knight", 0x200000000),
            ("Sacred Knight", 0x20000000000),
        ]),
        ("Ataque", [
            ("Berserker", 0x0008),
            ("Titan", 0x20000),
            ("Death Knight", 0x100000000),
            ("Destroyer", 0x10000000000),
        ]),
    ]),
    ("Hunter", [
        ("Ocupações Básicas", [
            ("Hunter", 0x0020),
            ("Archer", 0x0040),
        ]),
        ("Longo Alcance", [
            ("Ranger", 0x0080),
            ("Sniper", 0x80000),
            ("Mercenary", 0x400000000),
            ("Predator", 0x40000000000),
        ]),
        ("Assassino", [
            ("Assassin", 0x0100),
            ("Shadow Sicarius", 0x100000),
            ("Ninja", 0x800000000),
            ("Shinobi", 0x80000000000),
        ]),
    ]),
    ("Acolyte", [
        ("Ocupações Básicas", [
            ("Acolyte", 0x0200),
            ("Priest", 0x0400),
        ]),
        ("Curativo", [
            ("Cleric", 0x0800),
            ("Prophet", 0x200000),
            ("Divine Master", 0x1000000000),
            ("Archangel", 0x100000000000),
        ]),
        ("Transformação", [
            ("Sage", 0x1000),
            ("Mystic", 0x400000),
            ("Shaman", 0x2000000000),
            ("Druid", 0x200000000000),
        ]),
    ]),
    ("Warlock", [
        ("Ocupações Básicas", [
            ("Warlock (0x2000)", 0x2000),
            ("Magician", 0x4000),
        ]),
        ("Mágica", [
            ("Sorcerer", 0x8000),
            ("Archmage", 0x800000),
            ("Arcane", 0x4000000000),
            ("Warlock (0x400000000000)", 0x400000000000),
        ]),
        ("Inovação", [
            ("Necromancer", 0x10000),
            ("Demonologist", 0x1000000),
            ("Lord of the Dead", 0x8000000000),
            ("Shinigami", 0x800000000000),
        ]),
    ]),
    ("Machinist", [
        ("Ocupações Básicas", [
            ("Apprentice", 0x2000000),
            ("Machinist", 0x4000000),
        ]),
        ("Armadura Pesada", [
            ("Aggressor", 0x8000000),
            ("Prime", 0x20000000),
            ("Megatron", 0x1000000000000),
            ("Omega", 0x4000000000000),
        ]),
        ("Armadura Leve", [
            ("Demolisher", 0x10000000),
            ("Optimus", 0x40000000),
            ("Galvatron", 0x2000000000000),
            ("Celestial Titan", 0x8000000000000),
        ]),
    ]),
    ("Traveler", [
        ("Ocupações Básicas", [
            ("Traveler", 0x10000000000000),
            ("Nomad", 0x20000000000000),
        ]),
        ("Classe Espacial", [
            ("Swordsman", 0x40000000000000),
            ("Samurai", 0x100000000000000),
            ("Ronin", 0x400000000000000),
            ("Dimensional Master", 0x1000000000000000),
        ]),
        ("Classe do Tempo", [
            ("Illusionist", 0x80000000000000),
            ("Augur", 0x200000000000000),
            ("Oracle", 0x800000000000000),
            ("Chronos", 0x2000000000000000),
        ]),
    ]),
]

# =============================================================================
# COMMON HELPERS
# =============================================================================
ITEM_TYPE_BATTLE_AXE = "12"
ITEM_TYPE_CRYSTAL_KATANA = "59"
ITEM_TYPE_CRYSTAL_KEY = "60"
EQUIP_TYPE_HEAD = "1"
ARMOR_EQUIP_TYPES = {"1", "2", "3", "4", "5", "6"}
ENCHANT_FIELD_NAMES = (
    "EnchantType",
    "EnchantId",
    "ExpertLevel",
    "ExpertEnchantId",
    "ElfSkillId",
    "EnchantTimeType",
    "EnchantDuration",
)
TRAVELER_CLASS_FLAGS = {
    "10000000000000": "Traveler",
    "20000000000000": "Nomad",
    "40000000000000": "Swordsman",
    "80000000000000": "Illusionist",
    "100000000000000": "Samurai",
    "200000000000000": "Augur",
    "400000000000000": "Ronin",
    "800000000000000": "Oracle",
    "1000000000000000": "Dimensional Master",
    "2000000000000000": "Chronos",
}
TRAVELER_CLASS_MASKS = [int(value, 16) for value in TRAVELER_CLASS_FLAGS]
HEADER_PATTERN = re.compile(r"^\|V\.([^|]+)\|(\d+)\|$")
INTEGER_PATTERN = re.compile(r"^[+-]?\d+$")
HEX_PATTERN = re.compile(r"^[0-9A-Fa-f]+$")
COOLDOWN_SPLIT_PATTERN = re.compile(r"[\s,;|/]+")

DEFAULT_CLASS_MASKS = {
    0x0002, 0x0004, 0x0008, 0x0010, 0x20000, 0x40000, 0x100000000, 0x200000000,
    0x10000000000, 0x20000000000,
    0x0020, 0x0040, 0x0080, 0x0100, 0x80000, 0x100000, 0x400000000, 0x800000000,
    0x40000000000, 0x80000000000,
    0x0200, 0x0400, 0x0800, 0x1000, 0x200000, 0x400000, 0x1000000000, 0x2000000000,
    0x100000000000, 0x200000000000,
    0x2000, 0x4000, 0x8000, 0x10000, 0x800000, 0x1000000, 0x4000000000, 0x8000000000,
    0x400000000000, 0x800000000000,
    0x2000000, 0x4000000, 0x8000000, 0x10000000, 0x20000000, 0x40000000,
    0x1000000000000, 0x2000000000000, 0x4000000000000, 0x8000000000000,
    0x10000000000000, 0x20000000000000, 0x40000000000000, 0x80000000000000,
    0x100000000000000, 0x200000000000000, 0x400000000000000, 0x800000000000000,
    0x1000000000000000, 0x2000000000000000,
}

SPELL_COMMANDS = {"1999", "2064", "2065", "2066", "6002", "6003", "2139", "2142"}

# =============================================================================
# DATA CLASSES
# =============================================================================
@dataclass
class ProcessingOptions:
    apply_battleaxe_defence: bool
    defence_percent: Decimal
    defence_round_mode: str
    apply_katana_str_to_con: bool
    apply_key_dex_to_con: bool
    apply_head_level_41_to_40: bool
    apply_traveler_equipment_to_con: bool
    add_to_existing_con: bool
    apply_cooldown_enchant_replace: bool
    cooldown_groups: set[str]
    enchant_copy_mode: str
    apply_clear_rebirth_count: bool

@dataclass
class ItemRecord:
    fields: list[str]
    line_ending: str
    physical_start_line: int

@dataclass
class ParsedIni:
    codec: str
    encoding_label: str
    version: str
    pipes_per_record: int
    header_line: str
    records: list[ItemRecord]

@dataclass
class EnchantLookup:
    by_id: dict[str, dict[str, str]] = field(default_factory=dict)
    cooldown_by_id: dict[str, str] = field(default_factory=dict)
    duplicate_ids: int = 0
    records_read: int = 0

@dataclass
class ProcessingReport:
    version: str
    pipes_per_record: int
    total_records: int
    detected_encoding: str
    base_version: str = ""
    base_pipes_per_record: int = 0
    base_total_records: int = 0
    base_detected_encoding: str = ""
    base_duplicate_ids: int = 0
    battle_axes_found: int = 0
    battle_axes_updated: int = 0
    battle_axes_invalid_attack: int = 0
    battle_axes_overwritten_defence: int = 0
    katanas_found: int = 0
    katanas_updated: int = 0
    katanas_invalid_str: int = 0
    katanas_invalid_con: int = 0
    katanas_overwritten_con: int = 0
    keys_found: int = 0
    keys_updated: int = 0
    keys_invalid_dex: int = 0
    keys_invalid_con: int = 0
    keys_overwritten_con: int = 0
    heads_found: int = 0
    heads_level_41_found: int = 0
    heads_level_updated: int = 0
    traveler_equipment_found: int = 0
    traveler_equipment_updated: int = 0
    traveler_str_moved: int = 0
    traveler_dex_moved: int = 0
    traveler_invalid_str: int = 0
    traveler_invalid_dex: int = 0
    traveler_invalid_con: int = 0
    traveler_overwritten_con: int = 0
    traveler_invalid_class_mask: int = 0
    cooldown_items_found: int = 0
    cooldown_enchant_updated: int = 0
    cooldown_enchant_no_change: int = 0
    cooldown_enchant_missing_base_id: int = 0
    cooldown_enchant_empty_id: int = 0
    cooldown_enchant_fields_changed: int = 0
    rebirth_count_found: int = 0
    rebirth_count_cleared: int = 0

    @property
    def total_updated(self) -> int:
        return (
            self.battle_axes_updated + self.katanas_updated + self.keys_updated +
            self.heads_level_updated + self.traveler_equipment_updated +
            self.cooldown_enchant_updated + self.rebirth_count_cleared
        )

@dataclass
class RemovalReport:
    item_files_processed: list[Path] = field(default_factory=list)
    items_found_total: int = 0
    items_removed_total: int = 0
    removed_ids: list[str] = field(default_factory=list)
    store_files_processed: list[Path] = field(default_factory=list)
    store_refs_removed: int = 0
    drop_files_processed: list[Path] = field(default_factory=list)
    drop_refs_removed: int = 0
    item_file_counts: dict[str, int] = field(default_factory=dict)

@dataclass
class SpellRemovalReport:
    spell_files_processed: list[Path] = field(default_factory=list)
    spells_removed: int = 0
    spells_removed_ids: list[str] = field(default_factory=list)
    enchant_files_processed: list[Path] = field(default_factory=list)
    enchants_removed: int = 0
    enchants_removed_ids: list[str] = field(default_factory=list)
    spells_removed_by_enchant_ref: int = 0
    spells_removed_by_enchant_ref_ids: list[str] = field(default_factory=list)
    items_removed_by_enchant_ref: int = 0
    items_removed_by_enchant_ref_ids: list[str] = field(default_factory=list)
    item_store_refs_removed: int = 0
    item_drop_refs_removed: int = 0

# =============================================================================
# PARSING / ENCODING HELPERS
# =============================================================================
class ItemIniError(ValueError):
    pass

def detect_encoding(data: bytes) -> tuple[str, str]:
    candidates = (
        ("utf-8-sig", "UTF-8 com BOM"),
        ("utf-8", "UTF-8"),
        ("cp950", "CP950 / Big5"),
        ("big5hkscs", "Big5-HKSCS"),
        ("big5", "Big5"),
    )
    if not data.startswith(b"\xef\xbb\xbf"):
        candidates = candidates[1:]
    for codec, label in candidates:
        try:
            decoded = data.decode(codec)
            decoded.encode(codec)
            return codec, label
        except (UnicodeDecodeError, UnicodeEncodeError):
            continue
    raise ItemIniError("Não foi possível identificar uma codificação compatível com Big5/CP950 ou UTF-8.")

def split_final_line_ending(record: str) -> tuple[str, str]:
    if record.endswith("\r\n"):
        return record[:-2], "\r\n"
    if record.endswith("\n"):
        return record[:-1], "\n"
    if record.endswith("\r"):
        return record[:-1], "\r"
    return record, ""

def parse_header(header_line: str) -> tuple[str, int]:
    header_without_eol = header_line.rstrip("\r\n")
    match = HEADER_PATTERN.fullmatch(header_without_eol)
    if not match:
        raise ItemIniError("Cabeçalho inválido. Era esperado algo como: |V.6|194|")
    version = match.group(1)
    pipes_per_record = int(match.group(2))
    return version, pipes_per_record

def parse_ini(data: bytes, index: dict, *, source_label: str) -> ParsedIni:
    codec, encoding_label = detect_encoding(data)
    text = data.decode(codec)
    physical_lines = text.splitlines(keepends=True)
    if not physical_lines:
        raise ItemIniError(f"O arquivo {source_label} está vazio.")
    version, pipes_per_record = parse_header(physical_lines[0])
    records: list[ItemRecord] = []
    record_parts: list[str] = []
    current_pipe_count = 0
    record_start_line = 2
    max_index = max(index.values())
    if pipes_per_record <= max_index:
        raise ItemIniError(
            f"A quantidade de pipes declarada no cabeçalho é insuficiente para localizar os campos necessários."
        )
    for physical_line_number, line in enumerate(physical_lines[1:], start=2):
        if not record_parts:
            record_start_line = physical_line_number
        record_parts.append(line)
        current_pipe_count += line.count("|")
        if current_pipe_count > pipes_per_record:
            raise ItemIniError(
                f"Registro inválido no arquivo {source_label}, próximo à linha física {physical_line_number}: "
                f"foram encontrados mais de {pipes_per_record} pipes."
            )
        if current_pipe_count != pipes_per_record:
            continue
        record = "".join(record_parts)
        core, line_ending = split_final_line_ending(record)
        fields = core.split("|")
        expected_parts = pipes_per_record + 1
        if len(fields) != expected_parts:
            raise ItemIniError(
                f"Registro {len(records) + 1} do arquivo {source_label} possui {len(fields)} partes; "
                f"eram esperadas {expected_parts}."
            )
        records.append(ItemRecord(fields=fields, line_ending=line_ending, physical_start_line=record_start_line))
        record_parts.clear()
        current_pipe_count = 0
    if record_parts:
        raise ItemIniError(
            f"O último registro do arquivo {source_label} está incompleto: "
            "a quantidade de pipes não corresponde ao cabeçalho."
        )
    return ParsedIni(
        codec=codec,
        encoding_label=encoding_label,
        version=version,
        pipes_per_record=pipes_per_record,
        header_line=physical_lines[0],
        records=records,
    )

def encode_parsed_ini(parsed: ParsedIni) -> bytes:
    output_text = parsed.header_line + "".join(
        "|".join(record.fields) + record.line_ending for record in parsed.records
    )
    return output_text.encode(parsed.codec)

def parse_int_field(value: str) -> int | None:
    value = value.strip()
    if not value:
        return None
    if not INTEGER_PATTERN.fullmatch(value):
        return None
    return int(value)

def parse_class_mask(value: str) -> int | None:
    cleaned = value.strip()
    if not cleaned:
        return None
    if not HEX_PATTERN.fullmatch(cleaned):
        return None
    return int(cleaned, 16)

def is_traveler_class_mask(value: str) -> tuple[bool, bool]:
    mask = parse_class_mask(value)
    if mask is None:
        return False, bool(value.strip())
    return any(mask & traveler_mask for traveler_mask in TRAVELER_CLASS_MASKS), False

def calculate_defence_value(attack: int, percent: Decimal, round_mode: str) -> int:
    raw = Decimal(attack) * percent / Decimal(100)
    if round_mode == "nearest":
        return int(raw.to_integral_value(rounding=ROUND_HALF_UP))
    if round_mode == "ceil":
        return int(raw.to_integral_value(rounding=ROUND_CEILING))
    return int(raw.to_integral_value(rounding=ROUND_FLOOR))

def move_attribute_to_con(
    fields: list[str],
    source_index: int,
    *,
    add_to_existing_con: bool,
) -> tuple[bool, bool, bool, bool]:
    source_value = parse_int_field(fields[source_index])
    if source_value is None:
        if fields[source_index].strip():
            return False, True, False, False
        return False, False, False, False
    con_index = FIELD_INDEX["Con"]
    con_text = fields[con_index].strip()
    con_was_filled = bool(con_text)
    if add_to_existing_con and con_text:
        con_value = parse_int_field(fields[con_index])
        if con_value is None:
            return False, False, True, con_was_filled
        new_con = con_value + source_value
    else:
        new_con = source_value
    fields[source_index] = ""
    fields[con_index] = str(new_con)
    return True, False, False, con_was_filled

def move_str_and_dex_to_con(
    fields: list[str],
    *,
    add_to_existing_con: bool,
) -> dict[str, int | bool]:
    result: dict[str, int | bool] = {
        "updated": False,
        "str_moved": 0,
        "dex_moved": 0,
        "invalid_str": 0,
        "invalid_dex": 0,
        "invalid_con": 0,
        "con_was_filled": bool(fields[FIELD_INDEX["Con"]].strip()),
    }
    str_text = fields[FIELD_INDEX["Str"]].strip()
    dex_text = fields[FIELD_INDEX["Dex"]].strip()
    con_text = fields[FIELD_INDEX["Con"]].strip()
    str_value = parse_int_field(str_text)
    dex_value = parse_int_field(dex_text)
    if str_text and str_value is None:
        result["invalid_str"] = 1
    if dex_text and dex_value is None:
        result["invalid_dex"] = 1
    values_to_move: list[tuple[str, int]] = []
    if str_value is not None:
        values_to_move.append(("Str", str_value))
    if dex_value is not None:
        values_to_move.append(("Dex", dex_value))
    if not values_to_move:
        return result
    if add_to_existing_con and con_text:
        con_value = parse_int_field(con_text)
        if con_value is None:
            result["invalid_con"] = 1
            return result
        new_con = con_value + sum(value for _, value in values_to_move)
    else:
        new_con = sum(value for _, value in values_to_move)
    for name, _ in values_to_move:
        if name == "Str":
            fields[FIELD_INDEX["Str"]] = ""
            result["str_moved"] = 1
        elif name == "Dex":
            fields[FIELD_INDEX["Dex"]] = ""
            result["dex_moved"] = 1
    fields[FIELD_INDEX["Con"]] = str(new_con)
    result["updated"] = True
    return result

def parse_cooldown_groups_input(value: str) -> set[str]:
    groups = {part.strip() for part in COOLDOWN_SPLIT_PATTERN.split(value.strip()) if part.strip()}
    if not groups:
        raise ItemIniError("Informe pelo menos um CoolDownGroup, por exemplo: 998,999")
    invalid = sorted(group for group in groups if not INTEGER_PATTERN.fullmatch(group))
    if invalid:
        raise ItemIniError(f"CoolDownGroup inválido: {', '.join(invalid)}")
    return groups

def enchant_fields_for_mode(mode: str) -> tuple[str, ...]:
    if mode == "id":
        return ("EnchantId",)
    if mode == "type_id":
        return ("EnchantType", "EnchantId")
    return ENCHANT_FIELD_NAMES

def build_enchant_lookup(parsed_base: ParsedIni, fields_to_copy: tuple[str, ...]) -> EnchantLookup:
    lookup = EnchantLookup(records_read=len(parsed_base.records))
    for record in parsed_base.records:
        item_id = record.fields[FIELD_INDEX["Id"]].strip()
        if not item_id:
            continue
        if item_id in lookup.by_id:
            lookup.duplicate_ids += 1
        lookup.by_id[item_id] = {
            field_name: record.fields[FIELD_INDEX[field_name]] for field_name in fields_to_copy
        }
        lookup.cooldown_by_id[item_id] = record.fields[FIELD_INDEX["CoolDownGroup"]].strip()
    return lookup

def parse_percent_input(value: str) -> Decimal:
    cleaned = value.strip().replace("%", "").replace(",", ".")
    if not cleaned:
        raise ItemIniError("Informe uma porcentagem de defesa.")
    try:
        percent = Decimal(cleaned)
    except InvalidOperation as exc:
        raise ItemIniError("A porcentagem de defesa precisa ser um número válido.") from exc
    if percent < 0:
        raise ItemIniError("A porcentagem de defesa não pode ser negativa.")
    if percent > 1000:
        raise ItemIniError("A porcentagem de defesa está muito alta. Use até 1000%.")
    return percent

def format_decimal_for_filename(value: Decimal) -> str:
    text = format(value.normalize(), "f")
    return text.replace(".", "p").replace("-", "m")

# =============================================================================
# ITEM BALANCE PROCESSING
# =============================================================================
def process_item_file(
    data: bytes,
    options: ProcessingOptions,
    *,
    base_data: bytes | None = None,
) -> tuple[bytes, ProcessingReport]:
    parsed = parse_ini(data, FIELD_INDEX, source_label="principal")
    enchant_lookup: EnchantLookup | None = None
    fields_to_copy: tuple[str, ...] = ()
    base_parsed: ParsedIni | None = None
    if options.apply_cooldown_enchant_replace:
        if base_data is None:
            raise ItemIniError("Selecione o INI base para substituir os enchants por CoolDownGroup.")
        base_parsed = parse_ini(base_data, FIELD_INDEX, source_label="base de enchants")
        fields_to_copy = enchant_fields_for_mode(options.enchant_copy_mode)
        enchant_lookup = build_enchant_lookup(base_parsed, fields_to_copy)

    report = ProcessingReport(
        version=parsed.version,
        pipes_per_record=parsed.pipes_per_record,
        total_records=len(parsed.records),
        detected_encoding=parsed.encoding_label,
    )
    if base_parsed is not None and enchant_lookup is not None:
        report.base_version = base_parsed.version
        report.base_pipes_per_record = base_parsed.pipes_per_record
        report.base_total_records = len(base_parsed.records)
        report.base_detected_encoding = base_parsed.encoding_label
        report.base_duplicate_ids = enchant_lookup.duplicate_ids

    for record in parsed.records:
        fields = record.fields
        item_id = fields[FIELD_INDEX["Id"]].strip()
        item_type = fields[FIELD_INDEX["ItemType"]].strip()
        equip_type = fields[FIELD_INDEX["EquipType"]].strip()

        if options.apply_battleaxe_defence and item_type == ITEM_TYPE_BATTLE_AXE:
            report.battle_axes_found += 1
            attack_value = parse_int_field(fields[FIELD_INDEX["Attack"]])
            if attack_value is None:
                if fields[FIELD_INDEX["Attack"]].strip():
                    report.battle_axes_invalid_attack += 1
            else:
                defence_index = FIELD_INDEX["PhysicoDefence"]
                if fields[defence_index].strip():
                    report.battle_axes_overwritten_defence += 1
                fields[defence_index] = str(
                    calculate_defence_value(
                        attack_value,
                        options.defence_percent,
                        options.defence_round_mode,
                    )
                )
                report.battle_axes_updated += 1

        if options.apply_katana_str_to_con and item_type == ITEM_TYPE_CRYSTAL_KATANA:
            report.katanas_found += 1
            updated, invalid_source, invalid_con, con_was_filled = move_attribute_to_con(
                fields,
                FIELD_INDEX["Str"],
                add_to_existing_con=options.add_to_existing_con,
            )
            if con_was_filled:
                report.katanas_overwritten_con += 1
            if updated:
                report.katanas_updated += 1
            if invalid_source:
                report.katanas_invalid_str += 1
            if invalid_con:
                report.katanas_invalid_con += 1

        if options.apply_key_dex_to_con and item_type == ITEM_TYPE_CRYSTAL_KEY:
            report.keys_found += 1
            updated, invalid_source, invalid_con, con_was_filled = move_attribute_to_con(
                fields,
                FIELD_INDEX["Dex"],
                add_to_existing_con=options.add_to_existing_con,
            )
            if con_was_filled:
                report.keys_overwritten_con += 1
            if updated:
                report.keys_updated += 1
            if invalid_source:
                report.keys_invalid_dex += 1
            if invalid_con:
                report.keys_invalid_con += 1

        if options.apply_head_level_41_to_40 and equip_type == EQUIP_TYPE_HEAD:
            report.heads_found += 1
            level_index = FIELD_INDEX["RestrictLevel"]
            if fields[level_index].strip() == "41":
                report.heads_level_41_found += 1
                fields[level_index] = "40"
                report.heads_level_updated += 1

        if options.apply_traveler_equipment_to_con and equip_type in ARMOR_EQUIP_TYPES:
            is_traveler, invalid_mask = is_traveler_class_mask(fields[FIELD_INDEX["RestrictClass"]])
            if invalid_mask:
                report.traveler_invalid_class_mask += 1
            if is_traveler:
                report.traveler_equipment_found += 1
                move_result = move_str_and_dex_to_con(
                    fields,
                    add_to_existing_con=options.add_to_existing_con,
                )
                if bool(move_result["con_was_filled"]):
                    report.traveler_overwritten_con += 1
                if bool(move_result["updated"]):
                    report.traveler_equipment_updated += 1
                report.traveler_str_moved += int(move_result["str_moved"])
                report.traveler_dex_moved += int(move_result["dex_moved"])
                report.traveler_invalid_str += int(move_result["invalid_str"])
                report.traveler_invalid_dex += int(move_result["invalid_dex"])
                report.traveler_invalid_con += int(move_result["invalid_con"])

        if options.apply_cooldown_enchant_replace and enchant_lookup is not None:
            cooldown_group = fields[FIELD_INDEX["CoolDownGroup"]].strip()
            if cooldown_group in options.cooldown_groups:
                report.cooldown_items_found += 1
                if not item_id:
                    report.cooldown_enchant_empty_id += 1
                elif item_id not in enchant_lookup.by_id:
                    report.cooldown_enchant_missing_base_id += 1
                else:
                    changed = 0
                    base_values = enchant_lookup.by_id[item_id]
                    for field_name in fields_to_copy:
                        field_index = FIELD_INDEX[field_name]
                        new_value = base_values[field_name]
                        if fields[field_index] != new_value:
                            fields[field_index] = new_value
                            changed += 1
                    if changed:
                        report.cooldown_enchant_updated += 1
                        report.cooldown_enchant_fields_changed += changed
                    else:
                        report.cooldown_enchant_no_change += 1

        if options.apply_clear_rebirth_count:
            rebirth_index = FIELD_INDEX["RebirthCount"]
            if fields[rebirth_index].strip():
                report.rebirth_count_found += 1
                fields[rebirth_index] = ""
                report.rebirth_count_cleared += 1

    return encode_parsed_ini(parsed), report

# =============================================================================
# ITEM REMOVAL (C_* files)
# =============================================================================
def icon_filename_between(value: str, lo: int, hi: int) -> bool:
    val = value.strip()
    if not val or len(val) < 2 or val[0].upper() != "I":
        return False
    try:
        num = int(val[1:])
    except ValueError:
        return False
    return lo <= num <= hi

def match_removal_criteria(fields: list[str]) -> bool:
    icon = fields[FIELD_INDEX["IconFilename"]]
    if not icon_filename_between(icon, 595, 609):
        return False
    if fields[FIELD_INDEX["CastingTime"]].strip() != "30":
        return False
    if fields[FIELD_INDEX["CoolDownTime"]].strip() != "10":
        return False
    if fields[FIELD_INDEX["CoolDownGroup"]].strip() != "994":
        return False
    if fields[FIELD_INDEX["AuctionType"]].strip() != "32":
        return False
    return True

def remove_items_from_item_file(data: bytes) -> tuple[bytes, list[str]]:
    parsed = parse_ini(data, FIELD_INDEX, source_label="item file (C_)")
    new_records: list[ItemRecord] = []
    found_ids: list[str] = []
    for record in parsed.records:
        fields = record.fields
        if match_removal_criteria(fields):
            item_id = fields[FIELD_INDEX["Id"]].strip()
            if item_id:
                found_ids.append(item_id)
        else:
            new_records.append(record)
    parsed.records = new_records
    return encode_parsed_ini(parsed), found_ids

def remove_references_from_store(data: bytes, removed_ids: set[str]) -> tuple[bytes, int]:
    parsed = parse_ini(data, FIELD_INDEX, source_label="store file (C_)")
    group_size = 3
    offset = 2
    total_cleared = 0
    for record in parsed.records:
        fields = record.fields
        for i in range(offset, len(fields), group_size):
            if i + group_size > len(fields):
                break
            if fields[i].strip() in removed_ids:
                for j in range(i, i + group_size):
                    fields[j] = ""
                total_cleared += 1
    return encode_parsed_ini(parsed), total_cleared

def remove_references_from_drop(data: bytes, removed_ids: set[str]) -> tuple[bytes, int]:
    parsed = parse_ini(data, FIELD_INDEX, source_label="drop file (C_)")
    group_size = 4
    total_cleared = 0
    for record in parsed.records:
        fields = record.fields
        i = 0
        while i < len(fields):
            if fields[i].strip() in removed_ids:
                for j in range(i, min(i + group_size, len(fields))):
                    fields[j] = ""
                total_cleared += 1
                i += group_size
            else:
                i += 1
    return encode_parsed_ini(parsed), total_cleared

def remove_item_ids_from_file(data: bytes, ids_to_remove: set[str]) -> bytes:
    parsed = parse_ini(data, FIELD_INDEX, source_label="item file (C_)")
    new_records = [r for r in parsed.records if r.fields[FIELD_INDEX["Id"]].strip() not in ids_to_remove]
    parsed.records = new_records
    return encode_parsed_ini(parsed)

def remove_item_ids_from_store_and_drop(
    store_data: bytes | None,
    drop_data: bytes | None,
    ids_to_remove: set[str]
) -> tuple[bytes | None, int, bytes | None, int]:
    store_cleared = 0
    drop_cleared = 0
    new_store_data = None
    new_drop_data = None
    if store_data is not None:
        new_store_data, store_cleared = remove_references_from_store(store_data, ids_to_remove)
    if drop_data is not None:
        new_drop_data, drop_cleared = remove_references_from_drop(drop_data, ids_to_remove)
    return new_store_data, store_cleared, new_drop_data, drop_cleared

def process_removal(
    input_folder: Path,
    output_folder: Path,
    *,
    progress_callback: Callable[[str], None] | None = None,
) -> RemovalReport:
    report = RemovalReport()
    output_folder.mkdir(parents=True, exist_ok=True)
    item_files = [input_folder / "C_Item.ini", input_folder / "C_ItemMall.ini"]
    store_files = [input_folder / "C_Store.ini"]
    drop_files = [input_folder / "C_DropItem.ini"]
    item_files = [f for f in item_files if f.exists()]
    store_files = [f for f in store_files if f.exists()]
    drop_files = [f for f in drop_files if f.exists()]
    if not item_files:
        raise ItemIniError("Nenhum arquivo C_Item ou C_ItemMall encontrado.")
    all_removed_ids: list[str] = []
    for file_path in item_files:
        if progress_callback:
            progress_callback(f"Processando {file_path.name}...")
        try:
            data = file_path.read_bytes()
            new_data, found_ids = remove_items_from_item_file(data)
            out_path = output_folder / file_path.name
            out_path.write_bytes(new_data)
            if found_ids:
                report.item_file_counts[file_path.name] = len(found_ids)
                all_removed_ids.extend(found_ids)
                report.items_found_total += len(found_ids)
                report.items_removed_total += len(found_ids)
            else:
                report.item_file_counts[file_path.name] = 0
            report.item_files_processed.append(file_path)
        except Exception as e:
            if progress_callback:
                progress_callback(f"Erro ao processar {file_path.name}: {e}")
            report.item_files_processed.append(file_path)
            report.item_file_counts[file_path.name] = 0
    removed_set = set(all_removed_ids)
    report.removed_ids = sorted(all_removed_ids) if all_removed_ids else []
    for file_path in store_files:
        if progress_callback:
            progress_callback(f"Limpando referências em {file_path.name}...")
        try:
            data = file_path.read_bytes()
            new_data, cleared = remove_references_from_store(data, removed_set)
            out_path = output_folder / file_path.name
            out_path.write_bytes(new_data)
            report.store_refs_removed += cleared
            report.store_files_processed.append(file_path)
        except Exception as e:
            if progress_callback:
                progress_callback(f"Erro ao processar {file_path.name}: {e}")
            report.store_files_processed.append(file_path)
    for file_path in drop_files:
        if progress_callback:
            progress_callback(f"Limpando referências em {file_path.name}...")
        try:
            data = file_path.read_bytes()
            new_data, cleared = remove_references_from_drop(data, removed_set)
            out_path = output_folder / file_path.name
            out_path.write_bytes(new_data)
            report.drop_refs_removed += cleared
            report.drop_files_processed.append(file_path)
        except Exception as e:
            if progress_callback:
                progress_callback(f"Erro ao processar {file_path.name}: {e}")
            report.drop_files_processed.append(file_path)
    return report

# =============================================================================
# SPELL REMOVAL - AUXILIARY FUNCTIONS
# =============================================================================
def parse_spell_ini(data: bytes, source_label: str) -> ParsedIni:
    return parse_ini(data, SPELL_INDEX, source_label=source_label)

def parse_enchant_ini(data: bytes, source_label: str) -> ParsedIni:
    return parse_ini(data, ENCHANT_INDEX, source_label=source_label)

def encode_spell_ini(parsed: ParsedIni) -> bytes:
    return encode_parsed_ini(parsed)

def encode_enchant_ini(parsed: ParsedIni) -> bytes:
    return encode_parsed_ini(parsed)

def is_root_spell(fields: list[str]) -> bool:
    dep = fields[SPELL_INDEX["LearnDependentSpellId"]].strip()
    return dep == "" or dep == "0"

def spell_meets_criteria(
    fields: list[str], 
    class_masks: set[int] | None = None, 
    absolute_force: bool = False
) -> bool:
    cm = parse_class_mask(fields[SPELL_INDEX["RestrictClass"]])
    if cm is None:
        return False

    if class_masks is not None:
        selected_sum = sum(class_masks)
        if absolute_force:
            # Deve bater exatamente o valor combinado final
            return cm == selected_sum
        else:
            # Deve ser um subconjunto estrito da seleção de classes, e não zero
            return (cm & ~selected_sum) == 0 and cm != 0
    else:
        # Filtro padrão
        level = parse_int_field(fields[SPELL_INDEX["RestrictLeve"]])
        if level is None or level > 30:
            return False
        return any(cm & mask for mask in DEFAULT_CLASS_MASKS)

def collect_spell_ids_to_remove(
    data: bytes,
    force_root_id: str | None = None,
    class_masks: set[int] | None = None,
    absolute_force: bool = False
) -> tuple[set[str], list[str]]:
    parsed = parse_spell_ini(data, "spell file")
    id_to_fields: dict[str, list[str]] = {}
    for record in parsed.records:
        sid = record.fields[SPELL_INDEX["Id"]].strip()
        if sid:
            id_to_fields[sid] = record.fields

    if force_root_id:
        if force_root_id not in id_to_fields:
            raise ItemIniError(f"Spell ID {force_root_id} não encontrado.")
        dep_map: dict[str, list[str]] = {}
        for sid, fields in id_to_fields.items():
            dep = fields[SPELL_INDEX["LearnDependentSpellId"]].strip()
            if dep and dep in id_to_fields:
                dep_map.setdefault(dep, []).append(sid)
        to_remove = set()
        def add_chain(spell_id: str) -> None:
            if spell_id in to_remove:
                return
            to_remove.add(spell_id)
            for child in dep_map.get(spell_id, []):
                add_chain(child)
        add_chain(force_root_id)
        return to_remove, sorted(to_remove)

    candidates = set()
    for sid, fields in id_to_fields.items():
        if spell_meets_criteria(fields, class_masks, absolute_force):
            candidates.add(sid)

    if not candidates:
        return set(), []

    # RECONSTRUÇÃO DA LÓGICA DE HERANÇA:
    # Se o filtro de classe estiver ativo, NÃO subimos para os ancestrais,
    # pois isso removeria habilidades base partilhadas por outras classes (ex: Berserker no exemplo).
    # Caso contrário (filtro padrão de nível), mantemos a subida original de ancestrais.
    if class_masks is not None:
        to_remove = set(candidates)
    else:
        parent_map = {}
        for sid, fields in id_to_fields.items():
            dep = fields[SPELL_INDEX["LearnDependentSpellId"]].strip()
            if dep and dep in id_to_fields:
                parent_map[sid] = dep

        ancestors = set(candidates)
        for cid in list(candidates):
            current = cid
            while current in parent_map:
                parent = parent_map[current]
                ancestors.add(parent)
                current = parent
        to_remove = set(ancestors)

    # A expansão para descendentes (filhos) permanece sempre ativa.
    # Se um elo da corrente é removido, os upgrades seguintes não podem ser aprendidos.
    dep_map: dict[str, list[str]] = {}
    for sid, fields in id_to_fields.items():
        dep = fields[SPELL_INDEX["LearnDependentSpellId"]].strip()
        if dep and dep in id_to_fields:
            dep_map.setdefault(dep, []).append(sid)

    to_process = list(to_remove)
    while to_process:
        current = to_process.pop()
        for child in dep_map.get(current, []):
            if child not in to_remove:
                to_remove.add(child)
                to_process.append(child)

    return to_remove, sorted(to_remove)

def build_dependency_map(data: bytes) -> dict[str, list[str]]:
    parsed = parse_spell_ini(data, "spell file")
    dep_map: dict[str, list[str]] = {}
    id_set = set()
    for record in parsed.records:
        sid = record.fields[SPELL_INDEX["Id"]].strip()
        if sid:
            id_set.add(sid)
    for record in parsed.records:
        sid = record.fields[SPELL_INDEX["Id"]].strip()
        if not sid:
            continue
        dep = record.fields[SPELL_INDEX["LearnDependentSpellId"]].strip()
        if dep and dep in id_set:
            dep_map.setdefault(dep, []).append(sid)
    return dep_map

def expand_chain(ids: set[str], dep_map: dict[str, list[str]]) -> set[str]:
    result = set(ids)
    to_process = list(ids)
    while to_process:
        current = to_process.pop()
        for child in dep_map.get(current, []):
            if child not in result:
                result.add(child)
                to_process.append(child)
    return result

def remove_spells_from_file(data: bytes, ids_to_remove: set[str]) -> bytes:
    parsed = parse_spell_ini(data, "spell file")
    new_records = [r for r in parsed.records if r.fields[SPELL_INDEX["Id"]].strip() not in ids_to_remove]
    parsed.records = new_records
    return encode_spell_ini(parsed)

def get_all_buff_enchants(spell_data: bytes) -> set[str]:
    parsed = parse_spell_ini(spell_data, "spell file")
    buffs = set()
    for record in parsed.records:
        ench = record.fields[SPELL_INDEX["EnchantId"]].strip()
        self_ench = record.fields[SPELL_INDEX["SelfEnchantId"]].strip()
        if ench:
            buffs.add(ench)
        if self_ench:
            buffs.add(self_ench)
    return buffs

def get_protected_enchants_from_spells(
    spell_data: bytes,
    spells_to_remove: set[str]
) -> set[str]:
    parsed = parse_spell_ini(spell_data, "spell file")
    protected: set[str] = set()
    for record in parsed.records:
        sid = record.fields[SPELL_INDEX["Id"]].strip()
        if sid in spells_to_remove:
            continue
        ench_id = record.fields[SPELL_INDEX["EnchantId"]].strip()
        self_ench = record.fields[SPELL_INDEX["SelfEnchantId"]].strip()
        if ench_id:
            protected.add(ench_id)
        if self_ench:
            protected.add(self_ench)
    return protected

def find_enchants_referencing_spells(
    enchant_data: bytes,
    spell_ids: set[str],
    protected_enchants: set[str]
) -> tuple[set[str], list[str]]:
    parsed = parse_enchant_ini(enchant_data, "enchant file")
    enchants_to_remove: set[str] = set()
    id_list: list[str] = []
    for record in parsed.records:
        fields = record.fields
        eid = fields[ENCHANT_INDEX["Id"]].strip()
        if not eid or eid in protected_enchants:
            continue
        for cmd in (1, 2, 3, 4):
            cmd_id = fields[ENCHANT_INDEX[f"Cmd{cmd}_Id"]].strip()
            if cmd_id not in SPELL_COMMANDS:
                continue
            for p in range(1, 7):
                param = fields[ENCHANT_INDEX[f"Cmd{cmd}_Param{p}"]].strip()
                if param in spell_ids:
                    enchants_to_remove.add(eid)
                    id_list.append(eid)
                    break
            if eid in enchants_to_remove:
                break
    return enchants_to_remove, id_list

def find_enchants_referencing_enchants(
    enchant_data: bytes,
    enchant_ids: set[str],
    protected_enchants: set[str]
) -> tuple[set[str], list[str]]:
    parsed = parse_enchant_ini(enchant_data, "enchant file")
    enchants_to_remove: set[str] = set()
    id_list: list[str] = []
    for record in parsed.records:
        fields = record.fields
        eid = fields[ENCHANT_INDEX["Id"]].strip()
        if not eid or eid in protected_enchants or eid in enchant_ids:
            continue
        for cmd in (1, 2, 3, 4):
            cmd_id = fields[ENCHANT_INDEX[f"Cmd{cmd}_Id"]].strip()
            if cmd_id != "7001":
                continue
            ref_ench = fields[ENCHANT_INDEX[f"Cmd{cmd}_Param4"]].strip()
            if ref_ench in enchant_ids:
                enchants_to_remove.add(eid)
                id_list.append(eid)
                break
    return enchants_to_remove, id_list

def remove_enchants_from_file(data: bytes, ids_to_remove: set[str]) -> bytes:
    parsed = parse_enchant_ini(data, "enchant file")
    new_records = [r for r in parsed.records if r.fields[ENCHANT_INDEX["Id"]].strip() not in ids_to_remove]
    parsed.records = new_records
    return encode_enchant_ini(parsed)

def find_spells_referencing_enchants(data: bytes, enchant_ids: set[str]) -> tuple[set[str], list[str]]:
    parsed = parse_spell_ini(data, "spell file")
    spells_to_remove: set[str] = set()
    id_list: list[str] = []
    for record in parsed.records:
        fields = record.fields
        enchant_id = fields[SPELL_INDEX["EnchantId"]].strip()
        self_enchant_id = fields[SPELL_INDEX["SelfEnchantId"]].strip()
        if enchant_id in enchant_ids or self_enchant_id in enchant_ids:
            spell_id = fields[SPELL_INDEX["Id"]].strip()
            if spell_id:
                spells_to_remove.add(spell_id)
                id_list.append(spell_id)
    return spells_to_remove, id_list

def find_items_using_enchants(data: bytes, enchant_ids: set[str]) -> tuple[set[str], list[str]]:
    parsed = parse_ini(data, FIELD_INDEX, source_label="item file (C_)")
    items_to_remove: set[str] = set()
    id_list: list[str] = []
    for record in parsed.records:
        fields = record.fields
        enchant_id = fields[FIELD_INDEX["EnchantId"]].strip()
        expert_enchant = fields[FIELD_INDEX["ExpertEnchantId"]].strip()
        elf_skill = fields[FIELD_INDEX["ElfSkillId"]].strip()
        if (enchant_id in enchant_ids or expert_enchant in enchant_ids or elf_skill in enchant_ids):
            item_id = fields[FIELD_INDEX["Id"]].strip()
            if item_id:
                items_to_remove.add(item_id)
                id_list.append(item_id)
    return items_to_remove, id_list

def refine_enchants_to_remove(
    enchant_data: bytes,
    candidates: set[str],
    protected_enchants: set[str]
) -> set[str]:
    if not candidates:
        return set()

    parsed = parse_enchant_ini(enchant_data, "enchant file")
    ref_map: dict[str, set[str]] = {}
    for record in parsed.records:
        fields = record.fields
        eid = fields[ENCHANT_INDEX["Id"]].strip()
        if not eid:
            continue
        for cmd in (1, 2, 3, 4):
            cmd_id = fields[ENCHANT_INDEX[f"Cmd{cmd}_Id"]].strip()
            if cmd_id != "7001":
                continue
            ref_ench = fields[ENCHANT_INDEX[f"Cmd{cmd}_Param4"]].strip()
            if ref_ench:
                ref_map.setdefault(ref_ench, set()).add(eid)

    to_remove = set(candidates)
    changed = True
    while changed:
        changed = False
        for ench in list(to_remove):
            referencers = ref_map.get(ench, set())
            external_ref = any(ref not in to_remove for ref in referencers)
            if external_ref:
                to_remove.remove(ench)
                changed = True
    return to_remove

# =============================================================================
# PRINCIPAL SPELL REMOVAL PROCESS
# =============================================================================
def process_spell_removal(
    input_folder: Path,
    output_folder: Path,
    *,
    progress_callback: Callable[[str], None] | None = None,
    force_root_id: str | None = None,
    class_masks: set[int] | None = None,
    keep_spells: bool = False,
    absolute_force: bool = False,
) -> SpellRemovalReport:
    report = SpellRemovalReport()
    output_folder.mkdir(parents=True, exist_ok=True)

    spell_file = input_folder / "C_Spell.ini"
    enchant_file = input_folder / "C_Enchant.ini"
    item_files = [input_folder / "C_Item.ini", input_folder / "C_ItemMall.ini"]
    store_file = input_folder / "C_Store.ini"
    drop_file = input_folder / "C_DropItem.ini"

    if not spell_file.exists():
        raise ItemIniError("C_Spell.ini não encontrado.")
    if not enchant_file.exists():
        raise ItemIniError("C_Enchant.ini não encontrado.")

    spell_data = spell_file.read_bytes()
    enchant_data = enchant_file.read_bytes()
    item_data = {}
    for f in item_files:
        if f.exists():
            item_data[f.name] = f.read_bytes()
    store_data = store_file.read_bytes() if store_file.exists() else None
    drop_data = drop_file.read_bytes() if drop_file.exists() else None

    dep_map = build_dependency_map(spell_data)

    if progress_callback:
        if force_root_id:
            progress_callback(f"Coletando cadeia a partir do ID {force_root_id}...")
        else:
            if class_masks:
                mode_str = "Filtro absoluto" if absolute_force else "Filtro subconjunto"
                progress_callback(f"Coletando spells por classe ({mode_str})...")
            else:
                progress_callback("Coletando spells (nível<=30 e classes padrão)...")

    ids_to_remove, id_list = collect_spell_ids_to_remove(
        spell_data, force_root_id, class_masks, absolute_force
    )

    if not ids_to_remove:
        if progress_callback:
            progress_callback("Nenhuma spell alvo encontrada.")
        (output_folder / "C_Spell.ini").write_bytes(spell_data)
        (output_folder / "C_Enchant.ini").write_bytes(enchant_data)
        for name, data in item_data.items():
            (output_folder / name).write_bytes(data)
        if store_data:
            (output_folder / "C_Store.ini").write_bytes(store_data)
        if drop_data:
            (output_folder / "C_DropItem.ini").write_bytes(drop_data)
        report.spell_files_processed.append(spell_file)
        report.enchant_files_processed.append(enchant_file)
        return report

    # Aqui já temos a cadeia expandida corretamente (com ou sem ancestral conforme as novas regras)
    spells_to_remove = ids_to_remove

    if progress_callback:
        progress_callback(f"Spells a remover (cadeia expandida): {len(spells_to_remove)}")

    if keep_spells:
        protected_enchants = get_all_buff_enchants(spell_data)
        if progress_callback:
            progress_callback(f"Modo 'apenas referências': protegendo todos os {len(protected_enchants)} buffs de spells.")
    else:
        protected_enchants = get_protected_enchants_from_spells(spell_data, spells_to_remove)
        if progress_callback:
            progress_callback(f"Enchants protegidos (buffs de spells não removidas): {len(protected_enchants)}")

    candidates, _ = find_enchants_referencing_spells(enchant_data, spells_to_remove, protected_enchants)

    all_candidates = set(candidates)
    while True:
        new_from_ench, _ = find_enchants_referencing_enchants(enchant_data, all_candidates, protected_enchants)
        new_found = new_from_ench - all_candidates
        if not new_found:
            break
        all_candidates.update(new_found)

    if progress_callback:
        progress_callback(f"Candidatos a remoção (incluindo referências encadeadas): {len(all_candidates)}")

    refined = refine_enchants_to_remove(enchant_data, all_candidates, protected_enchants)
    refined -= protected_enchants

    if progress_callback:
        progress_callback(f"Após refinamento: {len(refined)} enchants a remover")

    spells_removed_by_ench_ref = set()
    spells_removed_by_ench_ref_ids = []
    if refined and not keep_spells:
        if progress_callback:
            progress_callback("Procurando spells que referenciam enchants removidos...")
        spells_ref, ids_ref = find_spells_referencing_enchants(spell_data, refined)
        if spells_ref:
            new_spells = spells_ref - spells_to_remove
            if new_spells:
                expanded_new = expand_chain(new_spells, dep_map)
                spells_removed_by_ench_ref = expanded_new - spells_to_remove
                spells_to_remove.update(spells_removed_by_ench_ref)
                spells_removed_by_ench_ref_ids = sorted(spells_removed_by_ench_ref)
                if progress_callback:
                    progress_callback(f"  Adicionadas {len(spells_removed_by_ench_ref)} novas spells por referência a enchants.")

    if keep_spells:
        if progress_callback:
            progress_callback("Modo 'apenas referências': NENHUMA spell será removida.")
        current_spell_data = spell_data
        spells_removed_count = 0
        spells_removed_ids = []
    else:
        if progress_callback:
            progress_callback(f"Removendo {len(spells_to_remove)} spells...")
        current_spell_data = remove_spells_from_file(spell_data, spells_to_remove)
        spells_removed_count = len(spells_to_remove)
        spells_removed_ids = sorted(spells_to_remove)

    if progress_callback:
        progress_callback(f"Removendo {len(refined)} enchants...")
    current_enchant_data = remove_enchants_from_file(enchant_data, refined)

    all_item_ids_to_remove = set()
    item_id_list = []
    if refined and item_data:
        if progress_callback:
            progress_callback("Procurando itens que usam enchants removidos...")
        new_item_data = {}
        for name, data in item_data.items():
            ids, ids_list = find_items_using_enchants(data, refined)
            if ids:
                all_item_ids_to_remove.update(ids)
                item_id_list.extend(ids_list)
                new_data = remove_item_ids_from_file(data, ids)
                new_item_data[name] = new_data
            else:
                new_item_data[name] = data

        if all_item_ids_to_remove:
            if progress_callback:
                progress_callback(f"Removendo {len(all_item_ids_to_remove)} itens...")
            for name, new_data in new_item_data.items():
                (output_folder / name).write_bytes(new_data)
            report.items_removed_by_enchant_ref = len(all_item_ids_to_remove)
            report.items_removed_by_enchant_ref_ids = sorted(item_id_list)

            if store_data or drop_data:
                if progress_callback:
                    progress_callback("Limpando referências em Store e Drop...")
                new_store, store_cleared, new_drop, drop_cleared = remove_item_ids_from_store_and_drop(
                    store_data, drop_data, all_item_ids_to_remove
                )
                if new_store is not None:
                    (output_folder / "C_Store.ini").write_bytes(new_store)
                    report.item_store_refs_removed = store_cleared
                else:
                    if store_data:
                        (output_folder / "C_Store.ini").write_bytes(store_data)
                if new_drop is not None:
                    (output_folder / "C_DropItem.ini").write_bytes(new_drop)
                    report.item_drop_refs_removed = drop_cleared
                else:
                    if drop_data:
                        (output_folder / "C_DropItem.ini").write_bytes(drop_data)
        else:
            for name, data in item_data.items():
                (output_folder / name).write_bytes(data)
    else:
        for name, data in item_data.items():
            (output_folder / name).write_bytes(data)

    out_spell = output_folder / "C_Spell.ini"
    out_spell.write_bytes(current_spell_data)
    report.spell_files_processed.append(spell_file)
    report.spells_removed = spells_removed_count
    report.spells_removed_ids = spells_removed_ids

    out_enchant = output_folder / "C_Enchant.ini"
    out_enchant.write_bytes(current_enchant_data)
    report.enchant_files_processed.append(enchant_file)
    report.enchants_removed = len(refined)
    report.enchants_removed_ids = sorted(refined)

    report.spells_removed_by_enchant_ref = len(spells_removed_by_ench_ref)
    report.spells_removed_by_enchant_ref_ids = spells_removed_by_ench_ref_ids

    if not all_item_ids_to_remove:
        if store_data:
            (output_folder / "C_Store.ini").write_bytes(store_data)
        if drop_data:
            (output_folder / "C_DropItem.ini").write_bytes(drop_data)

    return report

# =============================================================================
# SPELL CHAIN LOOKUP
# =============================================================================
def get_spell_chain(spell_id: str, spell_data: bytes) -> list[dict]:
    parsed = parse_spell_ini(spell_data, "spell file")
    id_to_fields: dict[str, list[str]] = {}
    for record in parsed.records:
        sid = record.fields[SPELL_INDEX["Id"]].strip()
        if sid:
            id_to_fields[sid] = record.fields

    if spell_id not in id_to_fields:
        return []

    parent_map: dict[str, str] = {}
    children_map: dict[str, list[str]] = {}
    for sid, fields in id_to_fields.items():
        dep = fields[SPELL_INDEX["LearnDependentSpellId"]].strip()
        if dep and dep in id_to_fields:
            parent_map[sid] = dep
            children_map.setdefault(dep, []).append(sid)

    root = spell_id
    while root in parent_map:
        root = parent_map[root]

    chain = []
    queue = [root]
    visited = set()
    while queue:
        sid = queue.pop(0)
        if sid in visited:
            continue
        visited.add(sid)
        fields = id_to_fields.get(sid, [])
        chain.append({
            'id': sid,
            'name': fields[SPELL_INDEX["Name"]] if len(fields) > SPELL_INDEX["Name"] else "",
            'level': fields[SPELL_INDEX["RestrictLeve"]] if len(fields) > SPELL_INDEX["RestrictLeve"] else "",
            'class_mask': fields[SPELL_INDEX["RestrictClass"]] if len(fields) > SPELL_INDEX["RestrictClass"] else "",
            'enchant_id': fields[SPELL_INDEX["EnchantId"]] if len(fields) > SPELL_INDEX["EnchantId"] else "",
            'self_enchant_id': fields[SPELL_INDEX["SelfEnchantId"]] if len(fields) > SPELL_INDEX["SelfEnchantId"] else "",
            'dep': fields[SPELL_INDEX["LearnDependentSpellId"]] if len(fields) > SPELL_INDEX["LearnDependentSpellId"] else "",
        })
        for child in children_map.get(sid, []):
            if child not in visited:
                queue.append(child)

    return chain

# =============================================================================
# INTERACTIVE GUI APPLICATION
# =============================================================================
class ItemBalancerApp:
    ROUND_LABELS = {
        "floor": "Arredondar para baixo",
        "nearest": "Arredondar normal",
        "ceil": "Arredondar para cima",
    }
    ROUND_VALUES_BY_LABEL = {label: key for key, label in ROUND_LABELS.items()}
    ENCHANT_MODE_LABELS = {
        "id": "Somente EnchantId",
        "type_id": "EnchantType + EnchantId",
        "all": "Todos os campos de enchant",
    }
    ENCHANT_MODE_BY_LABEL = {label: key for key, label in ENCHANT_MODE_LABELS.items()}

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("INI Toolkit — Balanceador + Gestor de Remoção")
        self.root.geometry("1150x880")
        self.root.configure(bg=COLORS["background"])
        self.root.option_add("*Background", COLORS["background"])
        self.root.option_add("*Foreground", COLORS["text"])

        # Balance variables
        self.input_path: Path | None = None
        self.base_path: Path | None = None

        self.battleaxe_var = tk.BooleanVar(value=True)
        self.katana_var = tk.BooleanVar(value=True)
        self.key_var = tk.BooleanVar(value=True)
        self.head_level_var = tk.BooleanVar(value=True)
        self.traveler_equipment_var = tk.BooleanVar(value=True)
        self.cooldown_enchant_var = tk.BooleanVar(value=True)
        self.clear_rebirth_var = tk.BooleanVar(value=True)
        self.sum_con_var = tk.BooleanVar(value=True)

        self.percent_var = tk.StringVar(value="50")
        self.round_mode_label_var = tk.StringVar(value=self.ROUND_LABELS["floor"])
        self.cooldown_groups_var = tk.StringVar(value="998,999")
        self.enchant_mode_label_var = tk.StringVar(value=self.ENCHANT_MODE_LABELS["all"])

        self.file_var = tk.StringVar(value="INI principal: nenhum arquivo selecionado.")
        self.base_file_var = tk.StringVar(value="INI base de enchants: nenhum arquivo selecionado.")
        self.status_var = tk.StringVar(value="Configure as opções, selecione os arquivos e processe.")

        # Item removal variables
        self.removal_input_folder_var = tk.StringVar(value="")
        self.removal_output_folder_var = tk.StringVar(value="")
        self.removal_status_var = tk.StringVar(value="Nenhuma pasta selecionada.")
        self.removal_progress_var = tk.StringVar(value="Aguardando...")

        # Spell removal variables
        self.spell_input_folder_var = tk.StringVar(value="")
        self.spell_output_folder_var = tk.StringVar(value="")
        self.spell_status_var = tk.StringVar(value="Nenhuma pasta selecionada.")
        self.spell_progress_var = tk.StringVar(value="Aguardando...")
        self.spell_force_id_var = tk.StringVar(value="")
        self.spell_keep_spells_var = tk.BooleanVar(value=False)
        self.spell_absolute_force_var = tk.BooleanVar(value=False)

        # Class variables structure mapping
        self.class_vars_map: dict[str, list[tuple[str, list[tuple[str, tk.BooleanVar, int]]]]] = {}
        self._create_class_vars()

        # Chain visualization variables
        self.chain_spell_id_var = tk.StringVar(value="")
        self.chain_widgets: list[tuple[ttk.Checkbutton, ttk.Label, dict]] = []

        self._setup_styles()
        self._build_interface()

    def _create_class_vars(self) -> None:
        for group_name, subgroups in CLASS_GROUPS:
            group_data = []
            for subgroup_name, classes in subgroups:
                class_list = []
                for class_name, mask in classes:
                    var = tk.BooleanVar(value=False)
                    # Força atualização em tempo real ao alterar valores
                    var.trace_add("write", lambda *args: self._update_flag_display())
                    class_list.append((class_name, var, mask))
                group_data.append((subgroup_name, class_list))
            self.class_vars_map[group_name] = group_data

    def _setup_styles(self) -> None:
        style = ttk.Style(self.root)
        if "clam" in style.theme_names():
            style.theme_use("clam")

        style.configure("TFrame", background=COLORS["background"])
        style.configure("TLabel", background=COLORS["background"], foreground=COLORS["text"])
        style.configure("TLabelframe", background=COLORS["background"], foreground=COLORS["text"], borderwidth=1, relief="solid")
        style.configure("TLabelframe.Label", background=COLORS["background"], foreground=COLORS["highlight"], font=("Segoe UI", 10, "bold"))
        
        # Estilo dos botões padrões
        style.configure("TButton", background=COLORS["button"], foreground=COLORS["button_text"],
                       borderwidth=1, relief="flat", focuscolor="none", font=("Segoe UI", 9))
        style.map("TButton",
                  background=[("active", COLORS["button_active"])],
                  foreground=[("active", COLORS["button_active_text"])])
        
        # Botões de destaque
        style.configure("Accent.TButton", background=COLORS["highlight"], foreground=COLORS["button_active_text"], font=("Segoe UI", 9, "bold"))
        style.map("Accent.TButton", background=[("active", COLORS["button_active"])])
        
        # Botões do menu de grupo (sidebar)
        style.configure("Sidebar.TButton", background=COLORS["card"], foreground=COLORS["text_muted"], borderwidth=0, font=("Segoe UI", 10))
        style.map("Sidebar.TButton",
                  background=[("selected", COLORS["button_active"]), ("active", COLORS["button"])],
                  foreground=[("selected", COLORS["button_active_text"]), ("active", COLORS["text"])])

        style.configure("TNotebook", background=COLORS["background"])
        style.configure("TNotebook.Tab", background=COLORS["header"], foreground=COLORS["text_muted"], font=("Segoe UI", 9, "bold"), padding=[12, 4])
        style.map("TNotebook.Tab",
                  background=[("selected", COLORS["highlight"])],
                  foreground=[("selected", COLORS["button_active_text"])])
        
        style.configure("TCheckbutton", background=COLORS["background"], foreground=COLORS["text"])
        style.configure("TEntry", fieldbackground=COLORS["card"], foreground=COLORS["text"], insertcolor=COLORS["text"], borderwidth=1)
        style.configure("TCombobox", fieldbackground=COLORS["card"], foreground=COLORS["text"])
        style.configure("Treeview", background=COLORS["card"], foreground=COLORS["text"], fieldbackground=COLORS["card"], borderwidth=0)
        style.map("Treeview", background=[("selected", COLORS["highlight"])])

    def _build_interface(self) -> None:
        notebook = ttk.Notebook(self.root, padding=0)
        notebook.pack(fill="both", expand=True, padx=8, pady=8)

        # Tab Balanceamento
        balance_frame = ttk.Frame(notebook, padding=8)
        notebook.add(balance_frame, text="Balanceamento")
        self._build_balance_tab(balance_frame)

        # Tab Remoção de Itens
        removal_frame = ttk.Frame(notebook, padding=8)
        notebook.add(removal_frame, text="Remoção de Itens")
        self._build_removal_tab(removal_frame)

        # Tab Remoção de Spells (Layout Reformulado)
        spell_frame = ttk.Frame(notebook, padding=8)
        notebook.add(spell_frame, text="Remoção de Spells")
        self._build_spell_tab(spell_frame)

        # Tab Visualização de Cadeia
        chain_frame = ttk.Frame(notebook, padding=8)
        notebook.add(chain_frame, text="Visualização de Cadeia")
        self._build_chain_tab(chain_frame)

        # Status Bar inferior
        status_bar = ttk.Frame(self.root, relief="flat", padding=4)
        status_bar.pack(fill="x", side="bottom", padx=8, pady=(0, 8))
        ttk.Label(status_bar, textvariable=self.status_var, wraplength=1100).pack(anchor="w")

    # -------------------------------------------------------------------------
    # Balance Tab
    # -------------------------------------------------------------------------
    def _build_balance_tab(self, parent: ttk.Frame) -> None:
        file_frame = ttk.LabelFrame(parent, text="Arquivos", padding=8)
        file_frame.pack(fill="x", pady=(0, 8))
        ttk.Label(file_frame, textvariable=self.file_var, wraplength=1050).pack(anchor="w")
        ttk.Label(file_frame, textvariable=self.base_file_var, wraplength=1050).pack(anchor="w", pady=(2, 0))
        btn_row = ttk.Frame(file_frame)
        btn_row.pack(fill="x", pady=(6, 0))
        ttk.Button(btn_row, text="Selecionar INI principal", command=self.select_file).pack(side="left")
        ttk.Button(btn_row, text="Selecionar INI base", command=self.select_base_file).pack(side="left", padx=(6, 0))
        ttk.Button(btn_row, text="Processar e salvar", command=self.process_and_save, style="Accent.TButton").pack(side="left", padx=(6, 0))
        ttk.Button(btn_row, text="Processar outro", command=self.select_process_and_save).pack(side="left", padx=(6, 0))

        rules_frame = ttk.LabelFrame(parent, text="Regras", padding=8)
        rules_frame.pack(fill="x", pady=(0, 8))
        ba_row = ttk.Frame(rules_frame)
        ba_row.pack(fill="x", pady=2)
        ttk.Checkbutton(ba_row, variable=self.battleaxe_var, text="BattleAxe (ItemType 12): Defesa = Ataque ×").pack(side="left")
        ttk.Entry(ba_row, textvariable=self.percent_var, width=6).pack(side="left", padx=(4, 4))
        ttk.Label(ba_row, text="%").pack(side="left")
        ttk.Label(ba_row, text="Arredondamento:").pack(side="left", padx=(16, 4))
        ttk.Combobox(ba_row, textvariable=self.round_mode_label_var,
                     values=list(self.ROUND_VALUES_BY_LABEL.keys()), state="readonly", width=18).pack(side="left")

        ttk.Checkbutton(rules_frame, variable=self.katana_var, text="CrystalKatana (ItemType 59): Str → Con").pack(anchor="w", pady=1)
        ttk.Checkbutton(rules_frame, variable=self.key_var, text="CrystalKey (ItemType 60): Dex → Con").pack(anchor="w", pady=1)
        ttk.Checkbutton(rules_frame, variable=self.head_level_var, text="Head (EquipType 1): RestrictLevel 41 → 40").pack(anchor="w", pady=1)
        ttk.Checkbutton(rules_frame, variable=self.traveler_equipment_var,
                        text="Traveler (EquipType 1–6): Str + Dex → Con").pack(anchor="w", pady=1)
        ttk.Checkbutton(rules_frame, variable=self.clear_rebirth_var, text="Limpar RebirthCount").pack(anchor="w", pady=1)
        ttk.Checkbutton(rules_frame, variable=self.sum_con_var,
                        text="Somar no Con existente (senão substitui)").pack(anchor="w", pady=1)

        ench_frame = ttk.LabelFrame(parent, text="Enchants por CoolDownGroup", padding=6)
        ench_frame.pack(fill="x", pady=(0, 8))
        ttk.Checkbutton(ench_frame, variable=self.cooldown_enchant_var,
                        text="Substituir enchants dos itens do principal usando base").pack(anchor="w")
        cd_row = ttk.Frame(ench_frame)
        cd_row.pack(fill="x", pady=2)
        ttk.Label(cd_row, text="CoolDownGroup:").pack(side="left")
        ttk.Entry(cd_row, textvariable=self.cooldown_groups_var, width=20).pack(side="left", padx=(6, 12))
        ttk.Label(cd_row, text="Campos copiados:").pack(side="left")
        ttk.Combobox(cd_row, textvariable=self.enchant_mode_label_var,
                     values=list(self.ENCHANT_MODE_BY_LABEL.keys()), state="readonly", width=24).pack(side="left", padx=(6, 0))

        report_frame = ttk.LabelFrame(parent, text="Relatório", padding=6)
        report_frame.pack(fill="both", expand=True)
        self.report_text = tk.Text(report_frame, height=10, wrap="word", state="disabled",
                                   bg=COLORS["card"], fg=COLORS["text"], font=("Segoe UI", 9),
                                   relief="flat", borderwidth=0)
        self.report_text.pack(side="left", fill="both", expand=True)
        scroll = ttk.Scrollbar(report_frame, orient="vertical", command=self.report_text.yview)
        scroll.pack(side="right", fill="y")
        self.report_text.configure(yscrollcommand=scroll.set)
        self._write_report("Pronto. Selecione os arquivos e regras para começar.")

    # -------------------------------------------------------------------------
    # Item Removal Tab
    # -------------------------------------------------------------------------
    def _build_removal_tab(self, parent: ttk.Frame) -> None:
        folder_frame = ttk.LabelFrame(parent, text="Pastas", padding=8)
        folder_frame.pack(fill="x", pady=(0, 8))
        in_row = ttk.Frame(folder_frame)
        in_row.pack(fill="x", pady=2)
        ttk.Label(in_row, text="Entrada:").pack(side="left")
        ttk.Entry(in_row, textvariable=self.removal_input_folder_var, width=60).pack(side="left", padx=(6, 6))
        ttk.Button(in_row, text="Selecionar", command=self.select_removal_input_folder).pack(side="left")

        out_row = ttk.Frame(folder_frame)
        out_row.pack(fill="x", pady=2)
        ttk.Label(out_row, text="Saída:").pack(side="left")
        ttk.Entry(out_row, textvariable=self.removal_output_folder_var, width=60).pack(side="left", padx=(6, 6))
        ttk.Button(out_row, text="Selecionar", command=self.select_removal_output_folder).pack(side="left")

        ttk.Label(folder_frame, textvariable=self.removal_status_var, wraplength=1050).pack(anchor="w", pady=(4, 0))

        action_frame = ttk.LabelFrame(parent, text="Ações", padding=6)
        action_frame.pack(fill="x", pady=(0, 8))
        btn_row = ttk.Frame(action_frame)
        btn_row.pack(fill="x", pady=2)
        ttk.Button(btn_row, text="▶ Executar remoção", command=self.run_removal, style="Accent.TButton").pack(side="left", padx=(0, 8))
        ttk.Button(btn_row, text="Visualizar relatório", command=self.preview_removal).pack(side="left")

        report_frame = ttk.LabelFrame(parent, text="Relatório", padding=6)
        report_frame.pack(fill="both", expand=True)
        self.removal_report_text = tk.Text(report_frame, height=8, wrap="word", state="disabled",
                                           bg=COLORS["card"], fg=COLORS["text"], font=("Segoe UI", 9),
                                           relief="flat", borderwidth=0)
        self.removal_report_text.pack(side="left", fill="both", expand=True)
        scroll = ttk.Scrollbar(report_frame, orient="vertical", command=self.removal_report_text.yview)
        scroll.pack(side="right", fill="y")
        self.removal_report_text.configure(yscrollcommand=scroll.set)
        self._write_removal_report("Aguardando execução...")

    # -------------------------------------------------------------------------
    # Spell Removal Tab (LAYOUT REFORMULADO)
    # -------------------------------------------------------------------------
    def _build_spell_tab(self, parent: ttk.Frame) -> None:
        # Configurações de pastas e IDs
        top_frame = ttk.LabelFrame(parent, text="Configurações de Arquivos", padding=8)
        top_frame.pack(fill="x", pady=(0, 8))

        row1 = ttk.Frame(top_frame)
        row1.pack(fill="x", pady=2)
        ttk.Label(row1, text="Entrada:").pack(side="left")
        ttk.Entry(row1, textvariable=self.spell_input_folder_var, width=50).pack(side="left", padx=(6, 6))
        ttk.Button(row1, text="Selecionar", command=self.select_spell_input_folder).pack(side="left", padx=2)
        ttk.Label(row1, text="  Saída:").pack(side="left", padx=(10, 0))
        ttk.Entry(row1, textvariable=self.spell_output_folder_var, width=50).pack(side="left", padx=(6, 6))
        ttk.Button(row1, text="Selecionar", command=self.select_spell_output_folder).pack(side="left", padx=2)

        row2 = ttk.Frame(top_frame)
        row2.pack(fill="x", pady=(6, 2))
        ttk.Label(row2, text="ID específico:").pack(side="left")
        ttk.Entry(row2, textvariable=self.spell_force_id_var, width=12).pack(side="left", padx=(6, 6))
        ttk.Label(row2, text="(Deixe vazio para usar filtro de classe)").pack(side="left", padx=(4, 20))
        
        ttk.Checkbutton(row2, variable=self.spell_keep_spells_var,
                        text="Apenas remover referências (Mantém as spells no arquivo)").pack(side="left", padx=(10, 10))
        ttk.Checkbutton(row2, variable=self.spell_absolute_force_var,
                        text="Forçar Absoluto (Máscara idêntica à soma selecionada)").pack(side="left")

        # Painel de Seleção de Classes (Layout Lateral Estilo Tool Profissional)
        class_frame = ttk.LabelFrame(parent, text="Filtro de Classes para Remoção", padding=6)
        class_frame.pack(fill="x", pady=(0, 8))

        # Indicador de flags atuais
        flag_status_frame = ttk.Frame(class_frame)
        flag_status_frame.pack(fill="x", pady=(0, 4))
        ttk.Label(flag_status_frame, text="Valor da flag calculada: ", font=("Segoe UI", 9, "bold")).pack(side="left")
        
        self.flag_global_decimal = tk.StringVar(value="0")
        self.flag_global_hex = tk.StringVar(value="0x0")
        
        ttk.Entry(flag_status_frame, textvariable=self.flag_global_decimal, width=16, state="readonly").pack(side="left", padx=4)
        ttk.Entry(flag_status_frame, textvariable=self.flag_global_hex, width=12, state="readonly").pack(side="left", padx=4)

        # Botões de ação globais
        ttk.Button(flag_status_frame, text="Marcar Todas", command=self._select_all_classes).pack(side="left", padx=(15, 4))
        ttk.Button(flag_status_frame, text="Limpar Todas", command=self._clear_all_classes).pack(side="left", padx=2)
        ttk.Button(flag_status_frame, text="Importar Flag", command=self._check_flag_dialog).pack(side="left", padx=2)

        # Divisor Lateral: Lista de Categorias à Esquerda, Detalhes à Direita
        paned = ttk.Frame(class_frame)
        paned.pack(fill="x", pady=4)

        # Sidebar à esquerda (Grupos principais)
        self.sidebar_frame = ttk.Frame(paned, width=150)
        self.sidebar_frame.pack(side="left", fill="y", padx=(0, 6))

        # Detalhes das subprofissões à direita
        self.subgroup_panel = ttk.Frame(paned, height=180, relief="solid", borderwidth=1)
        self.subgroup_panel.pack(side="left", fill="both", expand=True)

        # Construir botões da barra lateral
        self.sidebar_buttons: dict[str, ttk.Button] = {}
        for group_name in self.class_vars_map.keys():
            btn = ttk.Button(
                self.sidebar_frame, 
                text=group_name, 
                command=lambda g=group_name: self._show_class_group(g)
            )
            btn.pack(fill="x", pady=1, ipady=3)
            self.sidebar_buttons[group_name] = btn

        # Exibe por padrão a primeira categoria
        first_group = list(self.class_vars_map.keys())[0]
        self._show_class_group(first_group)

        # Informação de Status da aba Spell
        ttk.Label(parent, textvariable=self.spell_status_var, font=("Segoe UI", 9, "italic")).pack(anchor="w", pady=2)

        # Seção de Ações
        action_frame = ttk.Frame(parent)
        action_frame.pack(fill="x", pady=(0, 6))
        ttk.Button(action_frame, text="▶ Executar remoção de spells", command=self.run_spell_removal, style="Accent.TButton").pack(side="left", padx=(0, 8))
        ttk.Button(action_frame, text="Visualizar relatório", command=self.preview_spell_removal).pack(side="left")

        # Exibição do Relatório
        report_frame = ttk.LabelFrame(parent, text="Relatório do Processamento", padding=6)
        report_frame.pack(fill="both", expand=True)
        self.spell_report_text = tk.Text(report_frame, height=10, wrap="word", state="disabled",
                                         bg=COLORS["card"], fg=COLORS["text"], font=("Segoe UI", 9),
                                         relief="flat", borderwidth=0)
        self.spell_report_text.pack(side="left", fill="both", expand=True)
        scroll = ttk.Scrollbar(report_frame, orient="vertical", command=self.spell_report_text.yview)
        scroll.pack(side="right", fill="y")
        self.spell_report_text.configure(yscrollcommand=scroll.set)
        self._write_spell_report("Aguardando execução...")

    # ---- MÉTODOS DE CONTROLE DA SELEÇÃO DE CLASSES ----
    def _show_class_group(self, group_name: str) -> None:
        # Destruir widgets anteriores no painel de subgrupos
        for widget in self.subgroup_panel.winfo_children():
            widget.destroy()

        # Atualizar destaque visual dos botões da sidebar
        for name, btn in self.sidebar_buttons.items():
            if name == group_name:
                btn.state(['pressed'])
            else:
                btn.state(['!pressed'])

        # Obter os dados do grupo selecionado
        subgroups = self.class_vars_map[group_name]

        # Layout em grid dinâmico para os subgrupos
        col_idx = 0
        for sub_name, classes in subgroups:
            sub_frame = ttk.Frame(self.subgroup_panel, padding=6)
            sub_frame.grid(row=0, column=col_idx, sticky="nws", padx=10)
            
            # Título do subgrupo
            lbl = ttk.Label(sub_frame, text=sub_name, font=("Segoe UI", 9, "bold"), foreground=COLORS["highlight"])
            lbl.pack(anchor="w", pady=(0, 4))

            # Renderiza as classes deste subgrupo
            for class_name, var, mask in classes:
                cb = ttk.Checkbutton(sub_frame, text=class_name, variable=var)
                cb.pack(anchor="w", pady=1)

            col_idx += 1

    def _update_flag_display(self) -> None:
        total = 0
        for group_name, subgroups in self.class_vars_map.items():
            for sub_name, classes in subgroups:
                for class_name, var, mask in classes:
                    if var.get():
                        total |= mask

        self.flag_global_decimal.set(str(total))
        self.flag_global_hex.set(hex(total))

    def _select_all_classes(self) -> None:
        for group_name, subgroups in self.class_vars_map.items():
            for sub_name, classes in subgroups:
                for class_name, var, mask in classes:
                    var.set(True)
        self._update_flag_display()

    def _clear_all_classes(self) -> None:
        for group_name, subgroups in self.class_vars_map.items():
            for sub_name, classes in subgroups:
                for class_name, var, mask in classes:
                    var.set(False)
        self._update_flag_display()

    def _check_flag_dialog(self) -> None:
        # Diálogo simples para inserção manual da flag
        dialog = tk.Toplevel(self.root)
        dialog.title("Importar Flag de Classe")
        dialog.geometry("350x120")
        dialog.configure(bg=COLORS["background"])
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Digite o valor decimal ou hexadecimal:").pack(pady=8)
        entry_var = tk.StringVar()
        entry = ttk.Entry(dialog, textvariable=entry_var, width=25)
        entry.pack(pady=2)
        entry.focus()

        def apply_flag() -> None:
            raw_val = entry_var.get().strip()
            if not raw_val:
                dialog.destroy()
                return
            try:
                val = int(raw_val, 0)
            except ValueError:
                messagebox.showerror("Erro", "Valor inválido. Digite um número inteiro (ex: 4194304 ou 0x400000).", parent=dialog)
                return
            
            # Define as caixas de seleção correspondentes
            for group_name, subgroups in self.class_vars_map.items():
                for sub_name, classes in subgroups:
                    for class_name, var, mask in classes:
                        var.set((val & mask) != 0)
            self._update_flag_display()
            dialog.destroy()

        btn_row = ttk.Frame(dialog)
        btn_row.pack(pady=8)
        ttk.Button(btn_row, text="Confirmar", command=apply_flag, style="Accent.TButton").pack(side="left", padx=4)
        ttk.Button(btn_row, text="Cancelar", command=dialog.destroy).pack(side="left", padx=4)

    # -------------------------------------------------------------------------
    # Chain Visualization Tab
    # -------------------------------------------------------------------------
    def _build_chain_tab(self, parent: ttk.Frame) -> None:
        top_frame = ttk.Frame(parent)
        top_frame.pack(fill="x", pady=(0, 8))
        ttk.Label(top_frame, text="ID da spell inicial:").pack(side="left")
        ttk.Entry(top_frame, textvariable=self.chain_spell_id_var, width=14).pack(side="left", padx=(6, 6))
        ttk.Button(top_frame, text="Carregar Cadeia", command=self._load_chain, style="Accent.TButton").pack(side="left", padx=(0, 8))
        ttk.Button(top_frame, text="Remover selecionadas da cadeia", command=self._remove_selected_chain).pack(side="left")

        list_frame = ttk.LabelFrame(parent, text="Componentes da Corrente Encontrados", padding=6)
        list_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(list_frame, bg=COLORS["card"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scrollable = ttk.Frame(canvas)

        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.chain_container = scrollable

    def _load_chain(self) -> None:
        for w in self.chain_container.winfo_children():
            w.destroy()
        self.chain_widgets.clear()

        spell_id = self.chain_spell_id_var.get().strip()
        if not spell_id:
            self.status_var.set("Digite um ID de spell para buscar.")
            return

        try:
            spell_file = Path(self.spell_input_folder_var.get().strip()) / "C_Spell.ini"
            if not spell_file.exists():
                self.status_var.set("Erro: C_Spell.ini não encontrado na pasta de entrada configurada.")
                return
            spell_data = spell_file.read_bytes()
            chain = get_spell_chain(spell_id, spell_data)
        except Exception as e:
            self.status_var.set(f"Erro ao processar cadeia: {e}")
            return

        if not chain:
            self.status_var.set(f"Nenhuma spell correspondente ao ID {spell_id} foi localizada.")
            return

        self.status_var.set(f"Cadeia localizada com sucesso. {len(chain)} elos identificados.")

        for item in chain:
            frame = ttk.Frame(self.chain_container)
            frame.pack(fill="x", pady=2)

            var = tk.BooleanVar(value=False)
            cb = ttk.Checkbutton(frame, text=f"ID: {item['id']}", variable=var)
            cb.pack(side="left", padx=4)

            details = f"Nome: {item['name']} | Req. Level: {item['level']} | Classe Mask: {item['class_mask']} | Dep: {item['dep']}"
            lbl = ttk.Label(frame, text=details, font=("Segoe UI", 9))
            lbl.pack(side="left", padx=4)

            self.chain_widgets.append((cb, lbl, item))

    def _remove_selected_chain(self) -> None:
        selected_ids = []
        for cb, _, item in self.chain_widgets:
            # Verifica o estado da checkbox usando a variável associada
            for child in cb.master.winfo_children():
                if isinstance(child, ttk.Checkbutton):
                    var_name = child.cget("variable")
                    if cb.tk.globalgetvar(var_name):
                        selected_ids.append(item['id'])
                        break

        if not selected_ids:
            self.status_var.set("Nenhuma habilidade foi selecionada para exclusão.")
            return

        confirm_msg = f"Deseja deletar {len(selected_ids)} spells e seus vínculos relacionados do arquivo?"
        if not messagebox.askyesno("Confirmar Exclusão", confirm_msg, parent=self.root):
            return

        try:
            input_folder = Path(self.spell_input_folder_var.get().strip())
            output_folder = Path(self.spell_output_folder_var.get().strip())
            if not input_folder.exists():
                raise ItemIniError("A pasta de entrada não está configurada.")
            output_folder.mkdir(parents=True, exist_ok=True)

            keep = self.spell_keep_spells_var.get()
            report = None
            for sid in selected_ids:
                report = process_spell_removal(
                    input_folder, output_folder,
                    progress_callback=lambda msg: self.status_var.set(msg),
                    force_root_id=sid,
                    class_masks=None,
                    keep_spells=keep
                )
            
            self.status_var.set("Processo de exclusão de ramificação concluído.")
            if report:
                messagebox.showinfo("Concluído", f"Spells removidas: {report.spells_removed}\nEnchants removidos: {report.enchants_removed}", parent=self.root)
            self._load_chain()
        except Exception as e:
            self.status_var.set(f"Ocorreu um erro: {e}")
            messagebox.showerror("Erro", str(e), parent=self.root)

    # -------------------------------------------------------------------------
    # COMMON HANDLERS
    # -------------------------------------------------------------------------
    def _write_report(self, text: str) -> None:
        self.report_text.configure(state="normal")
        self.report_text.delete("1.0", "end")
        self.report_text.insert("1.0", text)
        self.report_text.configure(state="disabled")

    def _write_removal_report(self, text: str) -> None:
        self.removal_report_text.configure(state="normal")
        self.removal_report_text.delete("1.0", "end")
        self.removal_report_text.insert("1.0", text)
        self.removal_report_text.configure(state="disabled")

    def _write_spell_report(self, text: str) -> None:
        self.spell_report_text.configure(state="normal")
        self.spell_report_text.delete("1.0", "end")
        self.spell_report_text.insert("1.0", text)
        self.spell_report_text.configure(state="disabled")

    def select_file(self) -> None:
        f = filedialog.askopenfilename(parent=self.root, title="Selecione o INI principal",
                                       filetypes=(("Arquivo INI", "*.ini"), ("Todos", "*.*")))
        if f:
            self.input_path = Path(f)
            self.file_var.set(f"INI principal: {self.input_path}")
            self.status_var.set("INI principal selecionado.")

    def select_base_file(self) -> None:
        f = filedialog.askopenfilename(parent=self.root, title="Selecione o INI base",
                                       filetypes=(("Arquivo INI", "*.ini"), ("Todos", "*.*")))
        if f:
            self.base_path = Path(f)
            self.base_file_var.set(f"INI base de enchants: {self.base_path}")
            self.status_var.set("INI base selecionado.")

    def select_process_and_save(self) -> None:
        self.select_file()
        if self.input_path:
            self.process_and_save()

    def collect_options(self) -> ProcessingOptions:
        any_rule = (self.battleaxe_var.get() or self.katana_var.get() or self.key_var.get() or
                    self.head_level_var.get() or self.traveler_equipment_var.get() or
                    self.cooldown_enchant_var.get() or self.clear_rebirth_var.get())
        if not any_rule:
            raise ItemIniError("Marque pelo menos uma regra.")
        round_label = self.round_mode_label_var.get()
        round_mode = self.ROUND_VALUES_BY_LABEL.get(round_label, "floor")
        enchant_label = self.enchant_mode_label_var.get()
        enchant_mode = self.ENCHANT_MODE_BY_LABEL.get(enchant_label, "all")
        cooldown_groups = set()
        if self.cooldown_enchant_var.get():
            cooldown_groups = parse_cooldown_groups_input(self.cooldown_groups_var.get())
        return ProcessingOptions(
            apply_battleaxe_defence=self.battleaxe_var.get(),
            defence_percent=parse_percent_input(self.percent_var.get()),
            defence_round_mode=round_mode,
            apply_katana_str_to_con=self.katana_var.get(),
            apply_key_dex_to_con=self.key_var.get(),
            apply_head_level_41_to_40=self.head_level_var.get(),
            apply_traveler_equipment_to_con=self.traveler_equipment_var.get(),
            add_to_existing_con=self.sum_con_var.get(),
            apply_cooldown_enchant_replace=self.cooldown_enchant_var.get(),
            cooldown_groups=cooldown_groups,
            enchant_copy_mode=enchant_mode,
            apply_clear_rebirth_count=self.clear_rebirth_var.get(),
        )

    def ensure_base_file_if_needed(self, options: ProcessingOptions) -> bool:
        if not options.apply_cooldown_enchant_replace:
            return True
        if self.base_path:
            return True
        self.select_base_file()
        return self.base_path is not None

    def process_and_save(self) -> None:
        if self.input_path is None:
            self.select_file()
            if self.input_path is None:
                return
        try:
            options = self.collect_options()
            if not self.ensure_base_file_if_needed(options):
                self.status_var.set("Processamento cancelado: INI base não selecionado.")
                return
            self.status_var.set("Processando...")
            self.root.update_idletasks()
            src = self.input_path.read_bytes()
            base = self.base_path.read_bytes() if options.apply_cooldown_enchant_replace and self.base_path else None
            out_data, report = process_item_file(src, options, base_data=base)
            suggested = self.build_suggested_output_name(self.input_path, options)
            out_name = filedialog.asksaveasfilename(parent=self.root, title="Salvar",
                                                    initialdir=str(self.input_path.parent),
                                                    initialfile=suggested, defaultextension=".ini",
                                                    confirmoverwrite=True,
                                                    filetypes=(("Arquivo INI", "*.ini"), ("Todos", "*.*")))
            if not out_name:
                self.status_var.set("Salvamento cancelado.")
                return
            Path(out_name).write_bytes(out_data)
            txt = self.format_report(report, options, Path(out_name))
            self._write_report(txt)
            self.status_var.set(f"Concluído. {report.total_updated} alterações salvas.")
            messagebox.showinfo("Concluído", txt, parent=self.root)
        except Exception as e:
            self.status_var.set("Erro")
            messagebox.showerror("Erro", str(e), parent=self.root)

    @staticmethod
    def build_suggested_output_name(input_path: Path, options: ProcessingOptions) -> str:
        tags = []
        if options.apply_battleaxe_defence:
            tags.append(f"BA_def_{format_decimal_for_filename(options.defence_percent)}pct")
        if options.apply_katana_str_to_con:
            tags.append("Katana_StrToCon")
        if options.apply_key_dex_to_con:
            tags.append("Key_DexToCon")
        if options.apply_head_level_41_to_40:
            tags.append("Head41To40")
        if options.apply_traveler_equipment_to_con:
            tags.append("Traveler_StrDexToCon")
        if options.apply_cooldown_enchant_replace:
            tags.append(f"Enchant_CDG_{'_'.join(sorted(options.cooldown_groups))}")
        if options.apply_clear_rebirth_count:
            tags.append("ClearRebirth")
        return f"{input_path.stem}_{'_'.join(tags)}{input_path.suffix or '.ini'}"

    def format_report(self, report: ProcessingReport, options: ProcessingOptions, out_path: Path) -> str:
        cooldown = ", ".join(sorted(options.cooldown_groups)) if options.cooldown_groups else "nenhum"
        return (
            f"Arquivo salvo: {out_path}\n\n"
            f"Versão: V.{report.version}  |  Pipes: {report.pipes_per_record}  |  Codificação: {report.detected_encoding}\n"
            f"Registros: {report.total_records}\n\n"
            f"BattleAxe: encontrados {report.battle_axes_found}, atualizados {report.battle_axes_updated}\n"
            f"Katana: {report.katanas_found} encontradas, {report.katanas_updated} atualizadas\n"
            f"Chave: {report.keys_found} encontradas, {report.keys_updated} atualizadas\n"
            f"Head: {report.heads_found} encontrados, {report.heads_level_updated} nivelados\n"
            f"Traveler: {report.traveler_equipment_found} equipamentos, {report.traveler_equipment_updated} atualizados\n"
            f"CooldownGroup ({cooldown}): {report.cooldown_items_found} itens, {report.cooldown_enchant_updated} enchants alterados\n"
            f"RebirthCount limpos: {report.rebirth_count_cleared}\n"
            f"Total de ações: {report.total_updated}"
        )

    # -------------------------------------------------------------------------
    # Item Removal Callbacks
    # -------------------------------------------------------------------------
    def select_removal_input_folder(self) -> None:
        f = filedialog.askdirectory(parent=self.root, title="Selecione a pasta com C_*.ini")
        if f:
            self.removal_input_folder_var.set(f)
            self.removal_status_var.set(f"Entrada: {f}")
            self._update_removal_status()

    def select_removal_output_folder(self) -> None:
        f = filedialog.askdirectory(parent=self.root, title="Selecione a pasta de saída")
        if f:
            self.removal_output_folder_var.set(f)
            self.removal_status_var.set(f"Saída: {f}")

    def _update_removal_status(self) -> None:
        folder = self.removal_input_folder_var.get().strip()
        if not folder:
            return
        path = Path(folder)
        files = ["C_Item.ini", "C_ItemMall.ini", "C_Store.ini", "C_DropItem.ini"]
        present = [f for f in files if (path / f).exists()]
        missing = [f for f in files if not (path / f).exists()]
        self.removal_status_var.set(f"Encontrados: {', '.join(present) if present else 'nenhum'} | Ausentes: {', '.join(missing) if missing else 'nenhum'}")

    def _get_removal_files(self) -> tuple[list[Path], list[Path], list[Path], Path]:
        inp = self.removal_input_folder_var.get().strip()
        out = self.removal_output_folder_var.get().strip()
        if not inp or not out:
            raise ItemIniError("Selecione as pastas de entrada e saída.")
        in_path = Path(inp)
        out_path = Path(out)
        item_files = [in_path / f for f in ("C_Item.ini", "C_ItemMall.ini") if (in_path / f).exists()]
        store_files = [in_path / "C_Store.ini"] if (in_path / "C_Store.ini").exists() else []
        drop_files = [in_path / "C_DropItem.ini"] if (in_path / "C_DropItem.ini").exists() else []
        if not item_files:
            raise ItemIniError("Nenhum arquivo C_Item ou C_ItemMall encontrado.")
        return item_files, store_files, drop_files, out_path

    def run_removal(self) -> None:
        try:
            item_files, store_files, drop_files, out_path = self._get_removal_files()
            if not messagebox.askyesno("Confirmar", f"Remover itens e limpar referências? (saída: {out_path})", parent=self.root):
                return
            self.removal_progress_var.set("Processando...")
            self.root.update_idletasks()

            def progress_callback(msg: str) -> None:
                self.removal_progress_var.set(msg)

            report = process_removal(
                Path(self.removal_input_folder_var.get()),
                out_path,
                progress_callback=progress_callback
            )
            self.removal_progress_var.set("Concluído!")
            self._write_removal_report(self._format_removal_report(report))
            messagebox.showinfo("Concluído", f"Itens removidos: {report.items_removed_total}\nRefs loja: {report.store_refs_removed}\nRefs drop: {report.drop_refs_removed}", parent=self.root)
        except Exception as e:
            self.removal_progress_var.set("Erro")
            messagebox.showerror("Erro", str(e), parent=self.root)

    def preview_removal(self) -> None:
        try:
            item_files, store_files, drop_files, _ = self._get_removal_files()
            all_ids = []
            counts = {}
            for f in item_files:
                try:
                    data = f.read_bytes()
                    parsed = parse_ini(data, FIELD_INDEX, source_label=f.name)
                    cnt = 0
                    for rec in parsed.records:
                        if match_removal_criteria(rec.fields):
                            sid = rec.fields[FIELD_INDEX["Id"]].strip()
                            if sid:
                                all_ids.append(sid)
                                cnt += 1
                    counts[f.name] = cnt
                except Exception:
                    counts[f.name] = -1
            store_refs = drop_refs = 0
            removed = set(all_ids)
            if removed:
                for f in store_files:
                    try:
                        data = f.read_bytes()
                        parsed = parse_ini(data, FIELD_INDEX, source_label=f.name)
                        group_size, offset = 3, 2
                        for rec in parsed.records:
                            fields = rec.fields
                            for i in range(offset, len(fields), group_size):
                                if i + group_size > len(fields):
                                    break
                                if fields[i].strip() in removed:
                                    store_refs += 1
                    except Exception:
                        pass
                for f in drop_files:
                    try:
                        data = f.read_bytes()
                        parsed = parse_ini(data, FIELD_INDEX, source_label=f.name)
                        group_size = 4
                        for rec in parsed.records:
                            fields = rec.fields
                            i = 0
                            while i < len(fields):
                                if fields[i].strip() in removed:
                                    drop_refs += 1
                                    i += group_size
                                else:
                                    i += 1
                    except Exception:
                        pass
            lines = ["=== PRÉ-VISUALIZAÇÃO (nenhuma alteração) ===\n"]
            lines.append("Itens a remover por arquivo:")
            for name, cnt in counts.items():
                lines.append(f"  {name}: {cnt if cnt >= 0 else 'ERRO'}")
            lines.append(f"\nTotal de itens: {len(all_ids)}")
            if all_ids:
                lines.append(f"IDs: {', '.join(all_ids)}")
                lines.append(f"\nReferências na loja: {store_refs}")
                lines.append(f"Referências nos drops: {drop_refs}")
            else:
                lines.append("Nenhum item atende aos critérios.")
            self._write_removal_report("\n".join(lines))
        except Exception as e:
            messagebox.showerror("Erro", str(e), parent=self.root)

    def _format_removal_report(self, report: RemovalReport) -> str:
        lines = ["=== RELATÓRIO DE REMOÇÃO ===\n"]
        lines.append(f"Itens removidos: {report.items_removed_total}")
        lines.append(f"Refs loja: {report.store_refs_removed}")
        lines.append(f"Refs drop: {report.drop_refs_removed}")
        if report.removed_ids:
            lines.append(f"\nIDs removidos ({len(report.removed_ids)}):")
            for i in range(0, len(report.removed_ids), 10):
                lines.append("  " + ", ".join(report.removed_ids[i:i+10]))
        if report.item_file_counts:
            lines.append("\nPor arquivo:")
            for name, cnt in report.item_file_counts.items():
                lines.append(f"  {name}: {cnt}")
        return "\n".join(lines)

    # -------------------------------------------------------------------------
    # Spell Removal Callbacks
    # -------------------------------------------------------------------------
    def select_spell_input_folder(self) -> None:
        f = filedialog.askdirectory(parent=self.root, title="Selecione a pasta com C_Spell.ini e C_Enchant.ini")
        if f:
            self.spell_input_folder_var.set(f)
            self.spell_status_var.set(f"Entrada: {f}")
            self._update_spell_status()

    def select_spell_output_folder(self) -> None:
        f = filedialog.askdirectory(parent=self.root, title="Selecione a pasta de saída")
        if f:
            self.spell_output_folder_var.set(f)
            self.spell_status_var.set(f"Saída: {f}")

    def _update_spell_status(self) -> None:
        folder = self.spell_input_folder_var.get().strip()
        if not folder:
            return
        path = Path(folder)
        files = ["C_Spell.ini", "C_Enchant.ini", "C_Item.ini", "C_ItemMall.ini", "C_Store.ini", "C_DropItem.ini"]
        present = [f for f in files if (path / f).exists()]
        missing = [f for f in files if not (path / f).exists()]
        self.spell_status_var.set(f"Encontrados: {', '.join(present) if present else 'nenhum'} | Ausentes: {', '.join(missing) if missing else 'nenhum'}")

    def _get_selected_class_masks(self) -> set[int] | None:
        masks = set()
        for group_name, subgroups in self.class_vars_map.items():
            for sub_name, classes in subgroups:
                for class_name, var, mask in classes:
                    if var.get():
                        masks.add(mask)
        return masks if masks else None

    def _get_spell_files(self) -> tuple[Path, Path, Path]:
        inp = self.spell_input_folder_var.get().strip()
        out = self.spell_output_folder_var.get().strip()
        if not inp or not out:
            raise ItemIniError("Selecione as pastas de entrada e saída.")
        in_path = Path(inp)
        out_path = Path(out)
        spell = in_path / "C_Spell.ini"
        enchant = in_path / "C_Enchant.ini"
        if not spell.exists():
            raise ItemIniError("C_Spell.ini não encontrado.")
        if not enchant.exists():
            raise ItemIniError("C_Enchant.ini não encontrado.")
        return spell, enchant, out_path

    def run_spell_removal(self) -> None:
        try:
            spell_file, enchant_file, out_path = self._get_spell_files()
            force_id = self.spell_force_id_var.get().strip()
            if force_id and not force_id.isdigit():
                raise ItemIniError("ID deve ser numérico.")
            keep = self.spell_keep_spells_var.get()
            absolute_force = self.spell_absolute_force_var.get()
            selected_masks = self._get_selected_class_masks()

            msg_lines = [
                "Processar com as configurações definidas?",
                f"ID Alvo: {force_id if force_id else 'Filtro por Profissões'}",
            ]
            if not force_id:
                if selected_masks:
                    mode_str = "Absoluto" if absolute_force else "Subconjunto"
                    msg_lines.append(f"Filtro: {len(selected_masks)} classes marcadas ({mode_str})")
                else:
                    msg_lines.append("Filtro padrão do sistema (Nível <= 30 e classes padrão)")

            msg_lines.append(f"Destino da gravação: {out_path}")
            if not messagebox.askyesno("Confirmar Remoção", "\n".join(msg_lines), parent=self.root):
                return

            self.spell_progress_var.set("Processando...")
            self.root.update_idletasks()

            report = process_spell_removal(
                Path(self.spell_input_folder_var.get()), out_path,
                progress_callback=lambda msg: self.spell_progress_var.set(msg),
                force_root_id=force_id if force_id else None,
                class_masks=selected_masks,
                keep_spells=keep,
                absolute_force=absolute_force
            )
            self.spell_progress_var.set("Concluído!")
            self._write_spell_report(self._format_spell_report(report))
            summary = (
                f"Spells deletadas: {report.spells_removed}\n"
                f"Enchants deletados: {report.enchants_removed}\n"
                f"Itens afetados deletados: {report.items_removed_by_enchant_ref}\n"
                f"Referências limpas em Drops: {report.item_drop_refs_removed}"
            )
            messagebox.showinfo("Concluído", summary, parent=self.root)
        except Exception as e:
            self.spell_progress_var.set("Erro")
            messagebox.showerror("Erro", str(e), parent=self.root)

    def preview_spell_removal(self) -> None:
        try:
            spell_file, enchant_file, _ = self._get_spell_files()
            force_id = self.spell_force_id_var.get().strip()
            if force_id and not force_id.isdigit():
                raise ItemIniError("ID deve ser numérico.")
            selected_masks = self._get_selected_class_masks()
            absolute_force = self.spell_absolute_force_var.get()

            spell_data = spell_file.read_bytes()
            ids, _ = collect_spell_ids_to_remove(
                spell_data, force_id if force_id else None, selected_masks, absolute_force
            )
            lines = ["=== PRÉ-VISUALIZAÇÃO (NENHUM ARQUIVO FOI ALTERADO) ===\n"]
            if force_id:
                lines.append(f"Modo ID específico: {force_id}")
            elif selected_masks:
                mode_str = "Forçar Absoluto" if absolute_force else "Subconjunto"
                lines.append(f"Filtro ativo por {len(selected_masks)} classes combinadas ({mode_str})")
            else:
                lines.append("Filtro padrão de segurança: Nível <= 30 e classes padrão")

            if not ids:
                lines.append("\nNenhuma spell atende aos critérios configurados.")
                self._write_spell_report("\n".join(lines))
                return

            dep_map = build_dependency_map(spell_data)
            expanded = expand_chain(ids, dep_map)
            lines.append(f"\nSpells alvo encontradas (com suas dependências): {len(expanded)}")
            if expanded:
                ids_str = ", ".join(sorted(expanded)[:50])
                if len(expanded) > 50:
                    ids_str += f" ... (+ {len(expanded)-50} itens ocultados)"
                lines.append(f"Amostra de IDs: {ids_str}")

            keep = self.spell_keep_spells_var.get()
            if keep:
                protected = get_all_buff_enchants(spell_data)
                lines.append(f"\nModo 'Apenas referências' ativo. Mantendo spells e protegendo {len(protected)} enchants.")
            else:
                protected = get_protected_enchants_from_spells(spell_data, expanded)
                lines.append(f"\nEnchants protegidos (Apoio a spells ativas): {len(protected)}")

            candidates, _ = find_enchants_referencing_spells(enchant_file.read_bytes(), expanded, protected)
            lines.append(f"Candidatos iniciais para exclusão em C_Enchant.ini: {len(candidates)}")

            self._write_spell_report("\n".join(lines))
        except Exception as e:
            messagebox.showerror("Erro", str(e), parent=self.root)

    def _format_spell_report(self, report: SpellRemovalReport) -> str:
        lines = ["=== RELATÓRIO DO PROCESSAMENTO DE SPELLS ===\n"]
        lines.append(f"Spells excluídas do arquivo: {report.spells_removed}")
        lines.append(f"Enchants removidos: {report.enchants_removed}")
        lines.append(f"Spells associadas removidas por cascata: {report.spells_removed_by_enchant_ref}")
        lines.append(f"Itens vinculados a enchants inativos deletados: {report.items_removed_by_enchant_ref}")
        lines.append(f"Referências limpas em Lojas: {report.item_store_refs_removed}")
        lines.append(f"Referências limpas em DropItem: {report.item_drop_refs_removed}")
        
        if report.spells_removed_ids:
            lines.append(f"\nSpells Removidas ({len(report.spells_removed_ids)}):")
            for i in range(0, len(report.spells_removed_ids), 10):
                lines.append("  " + ", ".join(report.spells_removed_ids[i:i+10]))
        if report.enchants_removed_ids:
            lines.append(f"\nEnchants Removidos ({len(report.enchants_removed_ids)}):")
            for i in range(0, len(report.enchants_removed_ids), 10):
                lines.append("  " + ", ".join(report.enchants_removed_ids[i:i+10]))
        if report.items_removed_by_enchant_ref_ids:
            lines.append(f"\nItens Removidos ({len(report.items_removed_by_enchant_ref_ids)}):")
            for i in range(0, len(report.items_removed_by_enchant_ref_ids), 10):
                lines.append("  " + ", ".join(report.items_removed_by_enchant_ref_ids[i:i+10]))
        return "\n".join(lines)


def main() -> None:
    root = tk.Tk()
    try:
        style = ttk.Style(root)
        if "vista" in style.theme_names():
            style.theme_use("vista")
        elif "clam" in style.theme_names():
            style.theme_use("clam")
    except tk.TclError:
        pass
    ItemBalancerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()