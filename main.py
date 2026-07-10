from __future__ import annotations

import re
import tkinter as tk
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation, ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_UP
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Callable

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

# Class masks for spell removal
CLASS_MASKS = {
    # Fighter
    0x0002, 0x0004, 0x0008, 0x0010, 0x20000, 0x40000, 0x100000000, 0x200000000,
    0x10000000000, 0x20000000000,
    # Hunter
    0x0020, 0x0040, 0x0080, 0x0100, 0x80000, 0x100000, 0x400000000, 0x800000000,
    0x40000000000, 0x80000000000,
    # Acolyte
    0x0200, 0x0400, 0x0800, 0x1000, 0x200000, 0x400000, 0x1000000000, 0x2000000000,
    0x100000000000, 0x200000000000,
    # Warlock
    0x2000, 0x4000, 0x8000, 0x10000, 0x800000, 0x1000000, 0x4000000000, 0x8000000000,
    0x400000000000, 0x800000000000,
    # Machinist
    0x2000000, 0x4000000, 0x8000000, 0x10000000, 0x20000000, 0x40000000,
    0x1000000000000, 0x2000000000000, 0x4000000000000, 0x8000000000000,
    # Traveler
    0x10000000000000, 0x20000000000000, 0x40000000000000, 0x80000000000000,
    0x100000000000000, 0x200000000000000, 0x400000000000000, 0x800000000000000,
    0x1000000000000000, 0x2000000000000000,
}
# Commands that reference spells (including 1999, 2142, 6002, 6003)
SPELL_COMMANDS = {"1999", "2064", "2065", "2066", "6002", "6003", "2142"}

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
# SPELL REMOVAL (C_Spell.ini & C_Enchant.ini) + removal of items using removed enchants
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

def spell_meets_criteria(fields: list[str]) -> bool:
    level = parse_int_field(fields[SPELL_INDEX["RestrictLeve"]])
    if level is None or level > 30:
        return False
    class_mask = parse_class_mask(fields[SPELL_INDEX["RestrictClass"]])
    if class_mask is None:
        return False
    return any(class_mask & cm for cm in CLASS_MASKS)

def collect_spell_ids_to_remove(data: bytes, force_root_id: str | None = None) -> tuple[set[str], list[str]]:
    parsed = parse_spell_ini(data, "spell file")
    id_to_fields: dict[str, list[str]] = {}
    for record in parsed.records:
        sid = record.fields[SPELL_INDEX["Id"]].strip()
        if sid:
            id_to_fields[sid] = record.fields

    if force_root_id:
        if force_root_id not in id_to_fields:
            raise ItemIniError(f"Spell ID {force_root_id} não encontrado.")
        roots = {force_root_id}
    else:
        roots: set[str] = set()
        for sid, fields in id_to_fields.items():
            if is_root_spell(fields) and spell_meets_criteria(fields):
                roots.add(sid)

    if not roots:
        return set(), []

    to_remove: set[str] = set()
    dep_map: dict[str, list[str]] = {}
    for sid, fields in id_to_fields.items():
        dep = fields[SPELL_INDEX["LearnDependentSpellId"]].strip()
        if dep and dep in id_to_fields:
            dep_map.setdefault(dep, []).append(sid)

    def add_chain(spell_id: str) -> None:
        if spell_id in to_remove:
            return
        to_remove.add(spell_id)
        for child in dep_map.get(spell_id, []):
            add_chain(child)

    for root in roots:
        add_chain(root)

    id_list = sorted(to_remove) if to_remove else []
    return to_remove, id_list

def build_dependency_map(data: bytes) -> dict[str, list[str]]:
    """Build dependency map: parent -> list of children."""
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
    """Given a set of spell IDs, add all descendants recursively."""
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

def find_enchants_to_remove(data: bytes, spell_ids: set[str]) -> tuple[set[str], list[str]]:
    parsed = parse_enchant_ini(data, "enchant file")
    enchants_to_remove: set[str] = set()
    id_list: list[str] = []
    for record in parsed.records:
        fields = record.fields
        for cmd in (1, 2, 3, 4):
            cmd_id = fields[ENCHANT_INDEX[f"Cmd{cmd}_Id"]].strip()
            if cmd_id not in SPELL_COMMANDS:
                continue
            for p in range(1, 7):
                param = fields[ENCHANT_INDEX[f"Cmd{cmd}_Param{p}"]].strip()
                if param in spell_ids:
                    enchant_id = fields[ENCHANT_INDEX["Id"]].strip()
                    if enchant_id:
                        enchants_to_remove.add(enchant_id)
                        id_list.append(enchant_id)
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

def remove_item_ids_from_multiple_files(item_data_dict: dict[str, bytes], ids_to_remove: set[str]) -> dict[str, bytes]:
    result = {}
    for name, data in item_data_dict.items():
        result[name] = remove_item_ids_from_file(data, ids_to_remove)
    return result

# =============================================================================
# CORRIGIDO: loop iterativo com expansão de cadeia
# =============================================================================
def process_spell_removal(
    input_folder: Path,
    output_folder: Path,
    *,
    progress_callback: Callable[[str], None] | None = None,
    force_root_id: str | None = None,
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

    # Build full dependency map once
    dep_map = build_dependency_map(spell_data)

    if progress_callback:
        if force_root_id:
            progress_callback(f"Coletando cadeia a partir da spell {force_root_id}...")
        else:
            progress_callback("Coletando spells a remover (nível <=30, primeira da cadeia, classes alvo)...")
    ids_to_remove, id_list = collect_spell_ids_to_remove(spell_data, force_root_id)
    if not ids_to_remove:
        if progress_callback:
            progress_callback("Nenhuma spell a remover.")
        # Copy all files unchanged
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

    # Expand initial chain
    ids_to_remove = expand_chain(ids_to_remove, dep_map)

    current_spell_data = spell_data
    current_enchant_data = enchant_data
    total_spells_removed = 0
    total_enchants_removed = 0
    total_spells_by_enchant = 0
    total_items_removed = 0
    all_removed_spell_ids = []
    all_removed_enchant_ids = []
    all_removed_spell_by_enchant_ids = []
    all_removed_item_ids = []

    iteration = 0
    while True:
        iteration += 1
        if progress_callback:
            progress_callback(f"Iteração {iteration}: removendo dependências...")

        # Remove spells that are already marked (initial + expanded)
        if ids_to_remove:
            new_spell_data = remove_spells_from_file(current_spell_data, ids_to_remove)
            if new_spell_data != current_spell_data:
                current_spell_data = new_spell_data
                # Record removed spells
                removed_this_round = ids_to_remove
                total_spells_removed += len(removed_this_round)
                all_removed_spell_ids.extend(sorted(removed_this_round))

        # Find enchants referencing current removed spells
        enchants_to_remove, enchant_id_list = find_enchants_to_remove(current_enchant_data, ids_to_remove)
        if enchants_to_remove:
            if progress_callback:
                progress_callback(f"Removendo {len(enchants_to_remove)} enchants...")
            current_enchant_data = remove_enchants_from_file(current_enchant_data, enchants_to_remove)
            total_enchants_removed += len(enchants_to_remove)
            all_removed_enchant_ids.extend(enchant_id_list)

        # Find spells referencing these removed enchants
        if enchants_to_remove:
            spells_to_remove_2, id_list_2 = find_spells_referencing_enchants(current_spell_data, enchants_to_remove)
            if spells_to_remove_2:
                # Expand this new set of spells with their descendants
                expanded = expand_chain(spells_to_remove_2, dep_map)
                # Remove any already processed
                new_spells = expanded - ids_to_remove
                if new_spells:
                    if progress_callback:
                        progress_callback(f"Removendo {len(new_spells)} novas spells (incluindo descendentes)...")
                    # Add to ids_to_remove for next iteration
                    ids_to_remove.update(new_spells)
                    total_spells_by_enchant += len(new_spells)
                    all_removed_spell_by_enchant_ids.extend(sorted(new_spells))
                    # Remove them now
                    current_spell_data = remove_spells_from_file(current_spell_data, new_spells)
                else:
                    # No new spells to remove, exit loop
                    break
            else:
                # No spells referencing removed enchants, exit loop
                break
        else:
            # No more enchants to remove, exit loop
            break

    # Save final spell and enchant files
    out_spell = output_folder / "C_Spell.ini"
    out_spell.write_bytes(current_spell_data)
    report.spell_files_processed.append(spell_file)
    report.spells_removed = total_spells_removed
    report.spells_removed_ids = all_removed_spell_ids
    report.enchants_removed = total_enchants_removed
    report.enchants_removed_ids = all_removed_enchant_ids
    report.spells_removed_by_enchant_ref = total_spells_by_enchant
    report.spells_removed_by_enchant_ref_ids = all_removed_spell_by_enchant_ids

    out_enchant = output_folder / "C_Enchant.ini"
    out_enchant.write_bytes(current_enchant_data)
    report.enchant_files_processed.append(enchant_file)

    # ----- Remove items that use removed enchants (all enchants removed) -----
    all_enchants_removed = set(all_removed_enchant_ids)
    if all_enchants_removed and item_data:
        if progress_callback:
            progress_callback("Procurando itens que usam enchants removidos...")
        all_item_ids_to_remove: set[str] = set()
        item_id_list: list[str] = []
        new_item_data = {}
        for name, data in item_data.items():
            ids, ids_list = find_items_using_enchants(data, all_enchants_removed)
            if ids:
                all_item_ids_to_remove.update(ids)
                item_id_list.extend(ids_list)
                new_data = remove_item_ids_from_file(data, ids)
                new_item_data[name] = new_data
            else:
                new_item_data[name] = data

        if all_item_ids_to_remove:
            if progress_callback:
                progress_callback(f"Removendo {len(all_item_ids_to_remove)} itens que usam enchants removidos...")
            for name, new_data in new_item_data.items():
                (output_folder / name).write_bytes(new_data)
            report.items_removed_by_enchant_ref = len(all_item_ids_to_remove)
            report.items_removed_by_enchant_ref_ids = sorted(item_id_list)
            total_items_removed = len(all_item_ids_to_remove)

            # Remove references from Store and Drop
            if store_data or drop_data:
                if progress_callback:
                    progress_callback("Limpando referências desses itens em Store e Drop...")
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
            # Write unchanged item files
            for name, data in item_data.items():
                (output_folder / name).write_bytes(data)
    else:
        # Write unchanged item files
        for name, data in item_data.items():
            (output_folder / name).write_bytes(data)

    # Copy Store/Drop if not processed above
    if not all_item_ids_to_remove:
        if store_data:
            (output_folder / "C_Store.ini").write_bytes(store_data)
        if drop_data:
            (output_folder / "C_DropItem.ini").write_bytes(drop_data)

    return report

# =============================================================================
# GUI APPLICATION (unchanged, but with updated spell tab description)
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
        self.root.title("S_Item.ini — Balanceador + Remoção de Itens/Spells")
        self.root.geometry("1120x1020")
        self.root.minsize(980, 880)

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
        self.status_var = tk.StringVar(value="Configure as opções, escolha os arquivos e processe.")

        self.removal_input_folder_var = tk.StringVar(value="")
        self.removal_output_folder_var = tk.StringVar(value="")
        self.removal_status_var = tk.StringVar(value="Nenhuma pasta selecionada.")
        self.removal_progress_var = tk.StringVar(value="Aguardando...")

        self.spell_input_folder_var = tk.StringVar(value="")
        self.spell_output_folder_var = tk.StringVar(value="")
        self.spell_status_var = tk.StringVar(value="Nenhuma pasta selecionada.")
        self.spell_progress_var = tk.StringVar(value="Aguardando...")
        self.spell_force_id_var = tk.StringVar(value="")

        self._build_interface()

    def _build_interface(self) -> None:
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=8, pady=8)

        balance_frame = ttk.Frame(notebook, padding=12)
        notebook.add(balance_frame, text="Balanceamento")
        self._build_balance_tab(balance_frame)

        removal_frame = ttk.Frame(notebook, padding=12)
        notebook.add(removal_frame, text="Remoção de Itens (C_*)")
        self._build_removal_tab(removal_frame)

        spell_frame = ttk.Frame(notebook, padding=12)
        notebook.add(spell_frame, text="Remoção de Spells (C_*)")
        self._build_spell_tab(spell_frame)

        status_bar = ttk.Frame(self.root)
        status_bar.pack(fill="x", padx=8, pady=(0, 8))
        ttk.Label(status_bar, textvariable=self.status_var, wraplength=1100).pack(anchor="w")

    # ===== BALANCE TAB =====
    def _build_balance_tab(self, parent: ttk.Frame) -> None:
        title = ttk.Label(parent, text="Balanceador de S_Item.ini", font=("Segoe UI", 16, "bold"))
        title.pack(anchor="w")
        subtitle = ttk.Label(
            parent,
            text=(
                "Processa armas, armaduras, níveis, RebirthCount e enchants por CoolDownGroup, "
                "preservando cabeçalho, codificação, quebras de linha e todos os campos não selecionados."
            ),
            wraplength=1000,
            justify="left",
        )
        subtitle.pack(anchor="w", pady=(4, 12))

        file_frame = ttk.LabelFrame(parent, text="1. Arquivos", padding=10)
        file_frame.pack(fill="x")
        ttk.Label(file_frame, textvariable=self.file_var, wraplength=990).pack(anchor="w")
        ttk.Label(file_frame, textvariable=self.base_file_var, wraplength=990).pack(anchor="w", pady=(4, 0))
        button_row = ttk.Frame(file_frame)
        button_row.pack(fill="x", pady=(10, 0))
        ttk.Button(button_row, text="Selecionar INI principal...", command=self.select_file).pack(side="left")
        ttk.Button(button_row, text="Selecionar INI base de enchants...", command=self.select_base_file).pack(side="left", padx=(8, 0))
        ttk.Button(button_row, text="Processar e salvar...", command=self.process_and_save).pack(side="left", padx=(8, 0))
        ttk.Button(button_row, text="Processar outro arquivo...", command=self.select_process_and_save).pack(side="left", padx=(8, 0))

        options_frame = ttk.LabelFrame(parent, text="2. Regras de alteração", padding=10)
        options_frame.pack(fill="x", pady=(12, 0))
        battleaxe_row = ttk.Frame(options_frame)
        battleaxe_row.pack(fill="x", pady=(0, 6))
        ttk.Checkbutton(
            battleaxe_row,
            variable=self.battleaxe_var,
            text="BattleAxe / machado de 2 mãos (ItemType 12): PhysicoDefence = Attack ×",
        ).pack(side="left")
        percent_entry = ttk.Entry(battleaxe_row, textvariable=self.percent_var, width=8)
        percent_entry.pack(side="left", padx=(6, 4))
        ttk.Label(battleaxe_row, text="%").pack(side="left")

        round_row = ttk.Frame(options_frame)
        round_row.pack(fill="x", pady=(0, 6))
        ttk.Label(round_row, text="Arredondamento da defesa:             ").pack(side="left")
        round_combo = ttk.Combobox(
            round_row,
            textvariable=self.round_mode_label_var,
            values=list(self.ROUND_VALUES_BY_LABEL.keys()),
            state="readonly",
            width=24,
        )
        round_combo.pack(side="left")

        ttk.Checkbutton(
            options_frame,
            variable=self.katana_var,
            text="CrystalKatana / Katana (ItemType 59): mover Str para Con e apagar Str",
        ).pack(anchor="w", pady=(0, 5))
        ttk.Checkbutton(
            options_frame,
            variable=self.key_var,
            text="CrystalKey / Chave (ItemType 60): mover Dex para Con e apagar Dex",
        ).pack(anchor="w", pady=(0, 5))
        ttk.Checkbutton(
            options_frame,
            variable=self.head_level_var,
            text="Head / Cabeça (EquipType 1): onde RestrictLevel for 41, trocar para 40",
        ).pack(anchor="w", pady=(0, 5))
        ttk.Checkbutton(
            options_frame,
            variable=self.traveler_equipment_var,
            text=(
                "Equipamentos Traveler/Nomad/Samurai/etc. em Head/Chest/Pants/Glove/Feet/Back "
                "(EquipType 1–6): mover Str e Dex para Con"
            ),
        ).pack(anchor="w", pady=(0, 5))
        ttk.Checkbutton(
            options_frame,
            variable=self.clear_rebirth_var,
            text="Limpar RebirthCount: qualquer item com RebirthCount preenchido fica com o campo vazio",
        ).pack(anchor="w", pady=(0, 5))
        ttk.Checkbutton(
            options_frame,
            variable=self.sum_con_var,
            text="Ao mover atributos, somar no Con existente. Se desmarcado, substitui o Con pelo valor movido.",
        ).pack(anchor="w")

        enchant_frame = ttk.LabelFrame(parent, text="3. Enchants por CoolDownGroup", padding=10)
        enchant_frame.pack(fill="x", pady=(12, 0))
        ttk.Checkbutton(
            enchant_frame,
            variable=self.cooldown_enchant_var,
            text="Substituir enchant dos itens do INI principal usando o item de mesmo Id no INI base",
        ).pack(anchor="w", pady=(0, 6))
        cooldown_row = ttk.Frame(enchant_frame)
        cooldown_row.pack(fill="x", pady=(0, 6))
        ttk.Label(cooldown_row, text="CoolDownGroup:").pack(side="left")
        ttk.Entry(cooldown_row, textvariable=self.cooldown_groups_var, width=26).pack(side="left", padx=(8, 12))
        ttk.Label(cooldown_row, text="Ex.: 998,999").pack(side="left")
        enchant_mode_row = ttk.Frame(enchant_frame)
        enchant_mode_row.pack(fill="x")
        ttk.Label(enchant_mode_row, text="Campos copiados do INI base:").pack(side="left")
        enchant_combo = ttk.Combobox(
            enchant_mode_row,
            textvariable=self.enchant_mode_label_var,
            values=list(self.ENCHANT_MODE_BY_LABEL.keys()),
            state="readonly",
            width=30,
        )
        enchant_combo.pack(side="left", padx=(8, 0))

        info_frame = ttk.LabelFrame(parent, text="4. Classes Traveler consideradas", padding=10)
        info_frame.pack(fill="x", pady=(12, 0))
        classes_text = (
            "Traveler, Nomad, Swordsman, Illusionist, Samurai, Augur, Ronin, Oracle, "
            "Dimensional Master e Chronos. O RestrictClass é lido como soma/máscara desses valores."
        )
        ttk.Label(info_frame, text=classes_text, wraplength=990, justify="left").pack(anchor="w")

        report_frame = ttk.LabelFrame(parent, text="5. Relatório", padding=10)
        report_frame.pack(fill="both", expand=True, pady=(12, 0))
        self.report_text = tk.Text(report_frame, height=14, wrap="word", state="disabled")
        self.report_text.pack(side="left", fill="both", expand=True)
        scroll = ttk.Scrollbar(report_frame, orient="vertical", command=self.report_text.yview)
        scroll.pack(side="right", fill="y")
        self.report_text.configure(yscrollcommand=scroll.set)
        self._write_report(
            "Pronto.\n\n"
            "Regras atuais:\n"
            "- BattleAxe: cria/atualiza PhysicoDefence com porcentagem configurável do Attack.\n"
            "- CrystalKatana: move Str para Con.\n"
            "- CrystalKey: move Dex para Con.\n"
            "- Head: troca RestrictLevel 41 para 40.\n"
            "- Equipamentos da árvore Traveler em EquipType 1–6: move Str e Dex para Con.\n"
            "- Enchants: para CoolDownGroup selecionado, busca o mesmo Id no INI base e copia os campos escolhidos.\n"
            "- RebirthCount: limpa qualquer valor preenchido.\n\n"
            "Dica: deixe 'somar no Con existente' marcado para não perder um Con que o item já possuía."
        )

    # ===== REMOVAL TAB (ITEMS) =====
    def _build_removal_tab(self, parent: ttk.Frame) -> None:
        title = ttk.Label(parent, text="Remoção automática de itens (apenas C_*)", font=("Segoe UI", 16, "bold"))
        title.pack(anchor="w")
        desc = ttk.Label(
            parent,
            text=(
                "Remove itens que atendem TODOS os critérios:\n"
                "• IconFilename entre I00595 e I00609 (inclusive)\n"
                "• CastingTime = 30\n"
                "• CoolDownTime = 10\n"
                "• CoolDownGroup = 994\n"
                "• AuctionType = 32\n\n"
                "Os itens são removidos de C_Item.ini e C_ItemMall.ini.\n"
                "Referências são limpas em C_Store.ini e C_DropItem.ini.\n"
                "Os originais NÃO são modificados – as versões alteradas são salvas na pasta de saída."
            ),
            wraplength=1000,
            justify="left",
        )
        desc.pack(anchor="w", pady=(4, 12))

        folder_frame = ttk.LabelFrame(parent, text="1. Pastas", padding=10)
        folder_frame.pack(fill="x")
        input_row = ttk.Frame(folder_frame)
        input_row.pack(fill="x", pady=(0, 6))
        ttk.Label(input_row, text="Pasta de entrada (com C_*.ini):").pack(side="left")
        self.input_folder_entry = ttk.Entry(input_row, textvariable=self.removal_input_folder_var, width=50)
        self.input_folder_entry.pack(side="left", padx=(8, 8))
        ttk.Button(input_row, text="Selecionar...", command=self.select_removal_input_folder).pack(side="left")

        output_row = ttk.Frame(folder_frame)
        output_row.pack(fill="x", pady=(0, 6))
        ttk.Label(output_row, text="Pasta de saída (modificados):").pack(side="left")
        self.output_folder_entry = ttk.Entry(output_row, textvariable=self.removal_output_folder_var, width=50)
        self.output_folder_entry.pack(side="left", padx=(8, 8))
        ttk.Button(output_row, text="Selecionar...", command=self.select_removal_output_folder).pack(side="left")
        ttk.Label(folder_frame, textvariable=self.removal_status_var, wraplength=980).pack(anchor="w", pady=(6, 0))

        progress_frame = ttk.LabelFrame(parent, text="2. Progresso", padding=10)
        progress_frame.pack(fill="x", pady=(12, 0))
        self.removal_progress_label = ttk.Label(progress_frame, textvariable=self.removal_progress_var)
        self.removal_progress_label.pack(anchor="w")
        self.removal_progress_bar = ttk.Progressbar(progress_frame, mode="indeterminate", length=400)
        self.removal_progress_bar.pack(anchor="w", pady=(6, 0))
        action_row = ttk.Frame(progress_frame)
        action_row.pack(fill="x", pady=(10, 0))
        ttk.Button(action_row, text="▶ Executar remoção", command=self.run_removal, width=20).pack(side="left")
        ttk.Button(action_row, text="Visualizar relatório apenas", command=self.preview_removal, width=25).pack(side="left", padx=(8, 0))

        report_frame = ttk.LabelFrame(parent, text="3. Relatório de remoção", padding=10)
        report_frame.pack(fill="both", expand=True, pady=(12, 0))
        self.removal_report_text = tk.Text(report_frame, height=12, wrap="word", state="disabled")
        self.removal_report_text.pack(side="left", fill="both", expand=True)
        scroll2 = ttk.Scrollbar(report_frame, orient="vertical", command=self.removal_report_text.yview)
        scroll2.pack(side="right", fill="y")
        self.removal_report_text.configure(yscrollcommand=scroll2.set)
        self._write_removal_report("Aguardando execução...")

    # ===== SPELL TAB =====
    def _build_spell_tab(self, parent: ttk.Frame) -> None:
        title = ttk.Label(parent, text="Remoção de Spells (cadeia completa) + Itens órfãos", font=("Segoe UI", 16, "bold"))
        title.pack(anchor="w")
        desc = ttk.Label(
            parent,
            text=(
                "Remove a primeira habilidade de cada cadeia (LearnDependentSpellId = 0) se:\n"
                "• RestrictLevel ≤ 30\n"
                "• RestrictClass pertence a Fighter, Hunter, Acolyte, Warlock, Machinist ou Traveler\n\n"
                "TODAS as habilidades da cadeia (dependentes) são removidas junto.\n\n"
                "Em seguida, em loop:\n"
                "• Remove enchants que referenciam essas spells (comandos 1999, 2064, 2065, 2066, 6002, 6003, 2142)\n"
                "• Remove spells que referenciam esses enchants (EnchantId ou SelfEnchantId)\n"
                "• Expande a cadeia para incluir todos os descendentes das novas spells removidas\n"
                "• Repete até não haver mais remoções\n\n"
                "Depois remove itens (C_Item, C_ItemMall) que usam enchants removidos\n"
                "e limpa referências em C_Store e C_DropItem.\n\n"
                "Você também pode forçar a remoção a partir de um ID específico (campo abaixo)."
            ),
            wraplength=1000,
            justify="left",
        )
        desc.pack(anchor="w", pady=(4, 12))

        folder_frame = ttk.LabelFrame(parent, text="1. Pastas e ID específico", padding=10)
        folder_frame.pack(fill="x")
        input_row = ttk.Frame(folder_frame)
        input_row.pack(fill="x", pady=(0, 6))
        ttk.Label(input_row, text="Pasta de entrada (com C_Spell.ini, C_Enchant.ini e C_*.ini):").pack(side="left")
        self.spell_input_entry = ttk.Entry(input_row, textvariable=self.spell_input_folder_var, width=50)
        self.spell_input_entry.pack(side="left", padx=(8, 8))
        ttk.Button(input_row, text="Selecionar...", command=self.select_spell_input_folder).pack(side="left")

        output_row = ttk.Frame(folder_frame)
        output_row.pack(fill="x", pady=(0, 6))
        ttk.Label(output_row, text="Pasta de saída (modificados):").pack(side="left")
        self.spell_output_entry = ttk.Entry(output_row, textvariable=self.spell_output_folder_var, width=50)
        self.spell_output_entry.pack(side="left", padx=(8, 8))
        ttk.Button(output_row, text="Selecionar...", command=self.select_spell_output_folder).pack(side="left")

        force_row = ttk.Frame(folder_frame)
        force_row.pack(fill="x", pady=(6, 0))
        ttk.Label(force_row, text="Forçar ID específico (opcional):").pack(side="left")
        self.spell_force_entry = ttk.Entry(force_row, textvariable=self.spell_force_id_var, width=12)
        self.spell_force_entry.pack(side="left", padx=(8, 8))
        ttk.Label(force_row, text="Deixe em branco para usar critérios automáticos.").pack(side="left")

        ttk.Label(folder_frame, textvariable=self.spell_status_var, wraplength=980).pack(anchor="w", pady=(6, 0))

        progress_frame = ttk.LabelFrame(parent, text="2. Progresso", padding=10)
        progress_frame.pack(fill="x", pady=(12, 0))
        self.spell_progress_label = ttk.Label(progress_frame, textvariable=self.spell_progress_var)
        self.spell_progress_label.pack(anchor="w")
        self.spell_progress_bar = ttk.Progressbar(progress_frame, mode="indeterminate", length=400)
        self.spell_progress_bar.pack(anchor="w", pady=(6, 0))
        action_row = ttk.Frame(progress_frame)
        action_row.pack(fill="x", pady=(10, 0))
        ttk.Button(action_row, text="▶ Executar remoção de spells", command=self.run_spell_removal, width=25).pack(side="left")
        ttk.Button(action_row, text="Visualizar relatório apenas", command=self.preview_spell_removal, width=25).pack(side="left", padx=(8, 0))

        report_frame = ttk.LabelFrame(parent, text="3. Relatório", padding=10)
        report_frame.pack(fill="both", expand=True, pady=(12, 0))
        self.spell_report_text = tk.Text(report_frame, height=14, wrap="word", state="disabled")
        self.spell_report_text.pack(side="left", fill="both", expand=True)
        scroll3 = ttk.Scrollbar(report_frame, orient="vertical", command=self.spell_report_text.yview)
        scroll3.pack(side="right", fill="y")
        self.spell_report_text.configure(yscrollcommand=scroll3.set)
        self._write_spell_report("Aguardando execução...")

    # ===== COMMON UI HELPERS =====
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

    # ===== BALANCE CALLBACKS =====
    def select_file(self) -> None:
        input_name = filedialog.askopenfilename(
            parent=self.root,
            title="Selecione o INI principal",
            filetypes=(("Arquivo INI", "*.ini"), ("Todos os arquivos", "*.*")),
        )
        if not input_name:
            return
        self.input_path = Path(input_name)
        self.file_var.set(f"INI principal: {self.input_path}")
        self.status_var.set("INI principal selecionado. Agora clique em 'Processar e salvar...'.")

    def select_base_file(self) -> None:
        base_name = filedialog.askopenfilename(
            parent=self.root,
            title="Selecione o INI base de enchants",
            filetypes=(("Arquivo INI", "*.ini"), ("Todos os arquivos", "*.*")),
        )
        if not base_name:
            return
        self.base_path = Path(base_name)
        self.base_file_var.set(f"INI base de enchants: {self.base_path}")
        self.status_var.set("INI base selecionado.")

    def select_process_and_save(self) -> None:
        self.select_file()
        if self.input_path is not None:
            self.process_and_save()

    def collect_options(self) -> ProcessingOptions:
        any_rule = (
            self.battleaxe_var.get() or self.katana_var.get() or self.key_var.get() or
            self.head_level_var.get() or self.traveler_equipment_var.get() or
            self.cooldown_enchant_var.get() or self.clear_rebirth_var.get()
        )
        if not any_rule:
            raise ItemIniError("Marque pelo menos uma regra de alteração.")
        round_label = self.round_mode_label_var.get()
        round_mode = self.ROUND_VALUES_BY_LABEL.get(round_label, "floor")
        enchant_label = self.enchant_mode_label_var.get()
        enchant_mode = self.ENCHANT_MODE_BY_LABEL.get(enchant_label, "all")
        cooldown_groups: set[str] = set()
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
        if self.base_path is not None:
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
                self.status_var.set("Processamento cancelado: INI base de enchants não selecionado.")
                return
            self.status_var.set("Processando arquivo...")
            self.root.update_idletasks()
            source_data = self.input_path.read_bytes()
            base_data = self.base_path.read_bytes() if options.apply_cooldown_enchant_replace and self.base_path else None
            output_data, report = process_item_file(source_data, options, base_data=base_data)
            suggested_name = self.build_suggested_output_name(self.input_path, options)
            output_name = filedialog.asksaveasfilename(
                parent=self.root,
                title="Salvar arquivo processado",
                initialdir=str(self.input_path.parent),
                initialfile=suggested_name,
                defaultextension=".ini",
                confirmoverwrite=True,
                filetypes=(("Arquivo INI", "*.ini"), ("Todos os arquivos", "*.*")),
            )
            if not output_name:
                self.status_var.set("Processamento concluído, mas o salvamento foi cancelado.")
                return
            output_path = Path(output_name)
            output_path.write_bytes(output_data)
            report_text = self.format_report(report, options, output_path)
            self._write_report(report_text)
            self.status_var.set(f"Concluído. {report.total_updated} alterações salvas em: {output_path}")
            messagebox.showinfo("Processamento concluído", report_text, parent=self.root)
        except (OSError, ItemIniError) as exc:
            self.status_var.set("Não foi possível processar o arquivo.")
            messagebox.showerror("Erro", str(exc), parent=self.root)
        except Exception as exc:
            self.status_var.set("Ocorreu um erro inesperado.")
            messagebox.showerror("Erro inesperado", str(exc), parent=self.root)

    @staticmethod
    def build_suggested_output_name(input_path: Path, options: ProcessingOptions) -> str:
        tags: list[str] = []
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
            groups_tag = "CDG_" + "_".join(sorted(options.cooldown_groups))
            tags.append(f"Enchant_{groups_tag}")
        if options.apply_clear_rebirth_count:
            tags.append("ClearRebirth")
        suffix = input_path.suffix or ".ini"
        return f"{input_path.stem}_{'_'.join(tags)}{suffix}"

    def format_report(self, report: ProcessingReport, options: ProcessingOptions, output_path: Path) -> str:
        round_label = self.ROUND_LABELS.get(options.defence_round_mode, options.defence_round_mode)
        move_mode = "somando no Con existente" if options.add_to_existing_con else "substituindo o Con"
        enchant_label = self.ENCHANT_MODE_LABELS.get(options.enchant_copy_mode, options.enchant_copy_mode)
        cooldown_groups = ", ".join(sorted(options.cooldown_groups)) if options.cooldown_groups else "nenhum"
        base_info = ""
        if options.apply_cooldown_enchant_replace:
            base_info = (
                "\nINI base de enchants:\n"
                f"- Versão: V.{report.base_version}\n"
                f"- Pipes por registro: {report.base_pipes_per_record}\n"
                f"- Codificação detectada: {report.base_detected_encoding}\n"
                f"- Registros lidos: {report.base_total_records}\n"
                f"- IDs duplicados no base: {report.base_duplicate_ids}\n"
            )
        return (
            "Arquivo salvo com sucesso.\n\n"
            f"Destino:\n{output_path}\n\n"
            "INI principal:\n"
            f"- Versão: V.{report.version}\n"
            f"- Pipes por registro: {report.pipes_per_record}\n"
            f"- Codificação detectada/preservada: {report.detected_encoding}\n"
            f"- Registros analisados: {report.total_records}\n"
            f"{base_info}\n"
            "BattleAxe / machado de 2 mãos:\n"
            f"- Regra: PhysicoDefence = Attack × {options.defence_percent}% ({round_label})\n"
            f"- Encontrados: {report.battle_axes_found}\n"
            f"- Atualizados: {report.battle_axes_updated}\n"
            f"- Defesas anteriores substituídas: {report.battle_axes_overwritten_defence}\n"
            f"- Attack inválido ignorado: {report.battle_axes_invalid_attack}\n\n"
            "CrystalKatana / Katana:\n"
            f"- Regra: Str -> Con, {move_mode}\n"
            f"- Encontradas: {report.katanas_found}\n"
            f"- Atualizadas: {report.katanas_updated}\n"
            f"- Con já preenchido: {report.katanas_overwritten_con}\n"
            f"- Str inválido ignorado: {report.katanas_invalid_str}\n"
            f"- Con inválido ignorado: {report.katanas_invalid_con}\n\n"
            "CrystalKey / Chave:\n"
            f"- Regra: Dex -> Con, {move_mode}\n"
            f"- Encontradas: {report.keys_found}\n"
            f"- Atualizadas: {report.keys_updated}\n"
            f"- Con já preenchido: {report.keys_overwritten_con}\n"
            f"- Dex inválido ignorado: {report.keys_invalid_dex}\n"
            f"- Con inválido ignorado: {report.keys_invalid_con}\n\n"
            "Head / Cabeça:\n"
            "- Regra: EquipType 1 com RestrictLevel 41 -> 40\n"
            f"- Heads encontrados: {report.heads_found}\n"
            f"- Heads lv41 encontrados: {report.heads_level_41_found}\n"
            f"- Heads atualizados para lv40: {report.heads_level_updated}\n\n"
            "Equipamentos da árvore Traveler:\n"
            f"- Regra: EquipType 1–6 com RestrictClass Traveler/Nomad/Samurai/etc.; Str e Dex -> Con, {move_mode}\n"
            f"- Equipamentos encontrados: {report.traveler_equipment_found}\n"
            f"- Equipamentos atualizados: {report.traveler_equipment_updated}\n"
            f"- Str movidos: {report.traveler_str_moved}\n"
            f"- Dex movidos: {report.traveler_dex_moved}\n"
            f"- Con já preenchido: {report.traveler_overwritten_con}\n"
            f"- Str inválido ignorado: {report.traveler_invalid_str}\n"
            f"- Dex inválido ignorado: {report.traveler_invalid_dex}\n"
            f"- Con inválido ignorado: {report.traveler_invalid_con}\n"
            f"- RestrictClass inválido ignorado: {report.traveler_invalid_class_mask}\n\n"
            "Enchants por CoolDownGroup:\n"
            f"- Grupos: {cooldown_groups}\n"
            f"- Campos copiados: {enchant_label}\n"
            f"- Itens encontrados no INI principal: {report.cooldown_items_found}\n"
            f"- Itens com enchant alterado: {report.cooldown_enchant_updated}\n"
            f"- Campos de enchant alterados: {report.cooldown_enchant_fields_changed}\n"
            f"- Itens sem mudança: {report.cooldown_enchant_no_change}\n"
            f"- Itens sem Id: {report.cooldown_enchant_empty_id}\n"
            f"- IDs não encontrados no INI base: {report.cooldown_enchant_missing_base_id}\n\n"
            "RebirthCount:\n"
            "- Regra: limpar qualquer valor preenchido\n"
            f"- Itens com RebirthCount preenchido: {report.rebirth_count_found}\n"
            f"- RebirthCount limpos: {report.rebirth_count_cleared}\n\n"
            f"Total de ações feitas: {report.total_updated}"
        )

    # ===== REMOVAL (ITEMS) CALLBACKS =====
    def select_removal_input_folder(self) -> None:
        folder = filedialog.askdirectory(parent=self.root, title="Selecione a pasta com os arquivos C_*.ini")
        if not folder:
            return
        self.removal_input_folder_var.set(folder)
        self.removal_status_var.set(f"Pasta de entrada: {folder}")
        self._update_removal_status()

    def select_removal_output_folder(self) -> None:
        folder = filedialog.askdirectory(parent=self.root, title="Selecione a pasta de saída para os arquivos modificados")
        if not folder:
            return
        self.removal_output_folder_var.set(folder)
        self.removal_status_var.set(f"Pasta de saída: {folder}")

    def _update_removal_status(self) -> None:
        folder = self.removal_input_folder_var.get().strip()
        if not folder:
            return
        path = Path(folder)
        c_files = ["C_Item.ini", "C_ItemMall.ini", "C_Store.ini", "C_DropItem.ini"]
        present = [f for f in c_files if (path / f).exists()]
        missing = [f for f in c_files if not (path / f).exists()]
        status = f"Encontrados: {', '.join(present) if present else 'nenhum'}"
        if missing:
            status += f" | Ausentes: {', '.join(missing)}"
        self.removal_status_var.set(status)

    def _get_removal_files(self) -> tuple[list[Path], list[Path], list[Path], Path]:
        input_folder = self.removal_input_folder_var.get().strip()
        output_folder = self.removal_output_folder_var.get().strip()
        if not input_folder:
            raise ItemIniError("Selecione a pasta de entrada.")
        if not output_folder:
            raise ItemIniError("Selecione a pasta de saída.")
        in_path = Path(input_folder)
        out_path = Path(output_folder)
        item_files = [in_path / "C_Item.ini", in_path / "C_ItemMall.ini"]
        store_files = [in_path / "C_Store.ini"]
        drop_files = [in_path / "C_DropItem.ini"]
        item_files = [f for f in item_files if f.exists()]
        store_files = [f for f in store_files if f.exists()]
        drop_files = [f for f in drop_files if f.exists()]
        if not item_files:
            raise ItemIniError("Nenhum arquivo C_Item ou C_ItemMall encontrado.")
        return item_files, store_files, drop_files, out_path

    def run_removal(self) -> None:
        try:
            item_files, store_files, drop_files, out_path = self._get_removal_files()
            msg = (
                f"Serão processados:\n"
                f"  - {len(item_files)} arquivo(s) de item (C_Item, C_ItemMall)\n"
                f"  - {len(store_files)} arquivo(s) de loja (C_Store)\n"
                f"  - {len(drop_files)} arquivo(s) de drop (C_DropItem)\n\n"
                f"Os arquivos modificados serão salvos em:\n{out_path}\n"
                "Os originais NÃO serão alterados.\n\nDeseja continuar?"
            )
            if not messagebox.askyesno("Confirmar remoção", msg, parent=self.root):
                return
            self.removal_progress_bar.start()
            self.removal_progress_var.set("Iniciando remoção...")
            self.root.update_idletasks()
            def progress_callback(msg: str) -> None:
                self.removal_progress_var.set(msg)
                self.root.update_idletasks()
            report = process_removal(
                Path(self.removal_input_folder_var.get()),
                out_path,
                progress_callback=progress_callback,
            )
            self.removal_progress_bar.stop()
            self.removal_progress_var.set("Concluído!")
            report_text = self._format_removal_report(report)
            self._write_removal_report(report_text)
            summary = (
                f"Itens removidos: {report.items_removed_total}\n"
                f"Refs removidas das lojas: {report.store_refs_removed}\n"
                f"Refs removidas dos drops: {report.drop_refs_removed}"
            )
            messagebox.showinfo("Remoção concluída", summary, parent=self.root)
        except ItemIniError as e:
            self.removal_progress_bar.stop()
            self.removal_progress_var.set("Erro")
            messagebox.showerror("Erro", str(e), parent=self.root)
        except Exception as e:
            self.removal_progress_bar.stop()
            self.removal_progress_var.set("Erro inesperado")
            messagebox.showerror("Erro inesperado", str(e), parent=self.root)

    def preview_removal(self) -> None:
        try:
            item_files, store_files, drop_files, _ = self._get_removal_files()
            all_ids: list[str] = []
            file_counts: dict[str, int] = {}
            for file_path in item_files:
                try:
                    data = file_path.read_bytes()
                    parsed = parse_ini(data, FIELD_INDEX, source_label=file_path.name)
                    count = 0
                    for record in parsed.records:
                        if match_removal_criteria(record.fields):
                            item_id = record.fields[FIELD_INDEX["Id"]].strip()
                            if item_id:
                                all_ids.append(item_id)
                                count += 1
                    file_counts[file_path.name] = count
                except Exception:
                    file_counts[file_path.name] = -1
            store_refs = 0
            drop_refs = 0
            removed_set = set(all_ids)
            if removed_set:
                for file_path in store_files:
                    try:
                        data = file_path.read_bytes()
                        parsed = parse_ini(data, FIELD_INDEX, source_label=file_path.name)
                        group_size = 3
                        offset = 2
                        for record in parsed.records:
                            fields = record.fields
                            for i in range(offset, len(fields), group_size):
                                if i + group_size > len(fields):
                                    break
                                if fields[i].strip() in removed_set:
                                    store_refs += 1
                    except Exception:
                        pass
                for file_path in drop_files:
                    try:
                        data = file_path.read_bytes()
                        parsed = parse_ini(data, FIELD_INDEX, source_label=file_path.name)
                        group_size = 4
                        for record in parsed.records:
                            fields = record.fields
                            i = 0
                            while i < len(fields):
                                if fields[i].strip() in removed_set:
                                    drop_refs += 1
                                    i += group_size
                                else:
                                    i += 1
                    except Exception:
                        pass
            lines = ["=== PRÉ-VISUALIZAÇÃO (nenhum arquivo foi modificado) ===\n"]
            lines.append("Itens encontrados por arquivo:")
            for name, count in file_counts.items():
                if count == -1:
                    lines.append(f"  {name}: ERRO ao ler")
                else:
                    lines.append(f"  {name}: {count} item(ns)")
            lines.append(f"\nTotal de itens a remover: {len(all_ids)}")
            if all_ids:
                lines.append(f"\nIDs dos itens a remover ({len(all_ids)}):")
                for i in range(0, len(all_ids), 10):
                    chunk = all_ids[i:i+10]
                    lines.append("  " + ", ".join(chunk))
                lines.append(f"\nReferências nas lojas: {store_refs}")
                lines.append(f"Referências nos drops: {drop_refs}")
            else:
                lines.append("\nNenhum item atende aos critérios de remoção.")
            self._write_removal_report("\n".join(lines))
        except ItemIniError as e:
            messagebox.showerror("Erro", str(e), parent=self.root)
        except Exception as e:
            messagebox.showerror("Erro inesperado", str(e), parent=self.root)

    def _format_removal_report(self, report: RemovalReport) -> str:
        lines = ["=== RELATÓRIO DE REMOÇÃO ===\n"]
        lines.append(f"Total de itens removidos: {report.items_removed_total}")
        lines.append(f"Total de referências removidas das lojas: {report.store_refs_removed}")
        lines.append(f"Total de referências removidas dos drops: {report.drop_refs_removed}")
        if report.removed_ids:
            lines.append(f"\nIDs removidos ({len(report.removed_ids)}):")
            for i in range(0, len(report.removed_ids), 10):
                chunk = report.removed_ids[i:i+10]
                lines.append("  " + ", ".join(chunk))
        if report.item_file_counts:
            lines.append("\nDetalhamento por arquivo:")
            for name, count in report.item_file_counts.items():
                lines.append(f"  {name}: {count} item(ns)")
        if report.store_files_processed:
            lines.append(f"\nArquivos de loja processados: {len(report.store_files_processed)}")
        if report.drop_files_processed:
            lines.append(f"Arquivos de drop processados: {len(report.drop_files_processed)}")
        return "\n".join(lines)

    # ===== SPELL REMOVAL CALLBACKS =====
    def select_spell_input_folder(self) -> None:
        folder = filedialog.askdirectory(parent=self.root, title="Selecione a pasta com C_Spell.ini, C_Enchant.ini e C_*.ini")
        if not folder:
            return
        self.spell_input_folder_var.set(folder)
        self.spell_status_var.set(f"Pasta de entrada: {folder}")
        self._update_spell_status()

    def select_spell_output_folder(self) -> None:
        folder = filedialog.askdirectory(parent=self.root, title="Selecione a pasta de saída para os arquivos modificados")
        if not folder:
            return
        self.spell_output_folder_var.set(folder)
        self.spell_status_var.set(f"Pasta de saída: {folder}")

    def _update_spell_status(self) -> None:
        folder = self.spell_input_folder_var.get().strip()
        if not folder:
            return
        path = Path(folder)
        files = ["C_Spell.ini", "C_Enchant.ini", "C_Item.ini", "C_ItemMall.ini", "C_Store.ini", "C_DropItem.ini"]
        present = [f for f in files if (path / f).exists()]
        missing = [f for f in files if not (path / f).exists()]
        status = f"Encontrados: {', '.join(present) if present else 'nenhum'}"
        if missing:
            status += f" | Ausentes: {', '.join(missing)}"
        self.spell_status_var.set(status)

    def _get_spell_files(self) -> tuple[Path, Path, Path]:
        input_folder = self.spell_input_folder_var.get().strip()
        output_folder = self.spell_output_folder_var.get().strip()
        if not input_folder:
            raise ItemIniError("Selecione a pasta de entrada.")
        if not output_folder:
            raise ItemIniError("Selecione a pasta de saída.")
        in_path = Path(input_folder)
        out_path = Path(output_folder)
        spell_file = in_path / "C_Spell.ini"
        enchant_file = in_path / "C_Enchant.ini"
        if not spell_file.exists():
            raise ItemIniError("C_Spell.ini não encontrado.")
        if not enchant_file.exists():
            raise ItemIniError("C_Enchant.ini não encontrado.")
        return spell_file, enchant_file, out_path

    def run_spell_removal(self) -> None:
        try:
            spell_file, enchant_file, out_path = self._get_spell_files()
            force_id = self.spell_force_id_var.get().strip()
            if force_id and not force_id.isdigit():
                raise ItemIniError("O ID forçado deve ser um número.")
            msg = (
                f"Serão processados:\n"
                f"  - C_Spell.ini\n"
                f"  - C_Enchant.ini\n"
                f"  - C_Item.ini / C_ItemMall.ini (se existirem)\n"
                f"  - C_Store.ini / C_DropItem.ini (se existirem)\n\n"
                "**O processo é iterativo** com expansão de cadeia: remove spells → enchants → novas spells (e seus descendentes) → enchants, até não haver mais alterações.\n"
            )
            if force_id:
                msg += f"  ** Forçando remoção a partir do ID {force_id} **"
            else:
                msg += "  ** Usando critérios automáticos (nível≤30, classe alvo) **"
            msg += f"\n\nOs arquivos modificados serão salvos em:\n{out_path}\n"
            msg += "Os originais NÃO serão alterados.\n\nDeseja continuar?"
            if not messagebox.askyesno("Confirmar remoção de spells", msg, parent=self.root):
                return
            self.spell_progress_bar.start()
            self.spell_progress_var.set("Iniciando remoção de spells (iterativo com expansão de cadeia)...")
            self.root.update_idletasks()
            def progress_callback(msg: str) -> None:
                self.spell_progress_var.set(msg)
                self.root.update_idletasks()
            report = process_spell_removal(
                Path(self.spell_input_folder_var.get()),
                out_path,
                progress_callback=progress_callback,
                force_root_id=force_id if force_id else None,
            )
            self.spell_progress_bar.stop()
            self.spell_progress_var.set("Concluído!")
            report_text = self._format_spell_report(report)
            self._write_spell_report(report_text)
            summary = (
                f"Spells removidas (cadeia inicial): {report.spells_removed}\n"
                f"Enchants removidos: {report.enchants_removed}\n"
                f"Spells removidas por referência a enchants: {report.spells_removed_by_enchant_ref}\n"
                f"Itens removidos por usar enchants removidos: {report.items_removed_by_enchant_ref}\n"
                f"Referências de itens removidas da loja: {report.item_store_refs_removed}\n"
                f"Referências de itens removidas dos drops: {report.item_drop_refs_removed}"
            )
            messagebox.showinfo("Remoção de spells concluída", summary, parent=self.root)
        except ItemIniError as e:
            self.spell_progress_bar.stop()
            self.spell_progress_var.set("Erro")
            messagebox.showerror("Erro", str(e), parent=self.root)
        except Exception as e:
            self.spell_progress_bar.stop()
            self.spell_progress_var.set("Erro inesperado")
            messagebox.showerror("Erro inesperado", str(e), parent=self.root)

    def preview_spell_removal(self) -> None:
        try:
            spell_file, enchant_file, _ = self._get_spell_files()
            force_id = self.spell_force_id_var.get().strip()
            if force_id and not force_id.isdigit():
                raise ItemIniError("O ID forçado deve ser um número.")
            spell_data = spell_file.read_bytes()
            ids_to_remove, id_list = collect_spell_ids_to_remove(spell_data, force_id if force_id else None)
            lines = ["=== PRÉ-VISUALIZAÇÃO (nenhum arquivo foi modificado) ===\n"]
            if force_id:
                lines.append(f"Modo forçado: removendo cadeia a partir do ID {force_id}")
            else:
                lines.append("Modo automático: critérios (nível≤30, classe alvo)")
            if not ids_to_remove:
                lines.append("Nenhuma spell a remover.")
                self._write_spell_report("\n".join(lines))
                return
            # Expand chain
            dep_map = build_dependency_map(spell_data)
            expanded = expand_chain(ids_to_remove, dep_map)
            lines.append(f"\nSpells a remover (cadeia completa expandida): {len(expanded)}")
            if expanded:
                lines.append("\nIDs:")
                sorted_ids = sorted(expanded)
                for i in range(0, len(sorted_ids), 10):
                    chunk = sorted_ids[i:i+10]
                    lines.append("  " + ", ".join(chunk))
            # enchants (primeira rodada)
            enchant_data = enchant_file.read_bytes()
            enchants_to_remove, enchant_id_list = find_enchants_to_remove(enchant_data, expanded)
            lines.append(f"\nEnchants a remover (referenciam as spells): {len(enchants_to_remove)}")
            if enchant_id_list:
                lines.append("IDs:")
                for i in range(0, len(enchant_id_list), 10):
                    chunk = enchant_id_list[i:i+10]
                    lines.append("  " + ", ".join(chunk))
            # spells that reference those enchants (segunda rodada)
            if enchants_to_remove:
                spells_to_remove_2, id_list_2 = find_spells_referencing_enchants(spell_data, set(enchants_to_remove))
                if spells_to_remove_2:
                    # expand again
                    expanded2 = expand_chain(spells_to_remove_2, dep_map)
                    lines.append(f"\nSpells adicionais a remover (referenciam enchants removidos, com descendentes): {len(expanded2)}")
                    if expanded2:
                        lines.append("IDs:")
                        sorted2 = sorted(expanded2)
                        for i in range(0, len(sorted2), 10):
                            chunk = sorted2[i:i+10]
                            lines.append("  " + ", ".join(chunk))
            # items that use removed enchants
            if enchants_to_remove:
                item_folder = Path(self.spell_input_folder_var.get())
                item_files = [item_folder / "C_Item.ini", item_folder / "C_ItemMall.ini"]
                item_ids_total = set()
                item_id_list_total = []
                for f in item_files:
                    if f.exists():
                        data = f.read_bytes()
                        ids, ids_list = find_items_using_enchants(data, set(enchants_to_remove))
                        item_ids_total.update(ids)
                        item_id_list_total.extend(ids_list)
                if item_ids_total:
                    lines.append(f"\nItens a remover (usam enchants removidos): {len(item_ids_total)}")
                    if item_id_list_total:
                        lines.append("IDs:")
                        for i in range(0, len(item_id_list_total), 10):
                            chunk = item_id_list_total[i:i+10]
                            lines.append("  " + ", ".join(chunk))
                else:
                    lines.append("\nNenhum item usa enchants removidos.")
            self._write_spell_report("\n".join(lines))
        except ItemIniError as e:
            messagebox.showerror("Erro", str(e), parent=self.root)
        except Exception as e:
            messagebox.showerror("Erro inesperado", str(e), parent=self.root)

    def _format_spell_report(self, report: SpellRemovalReport) -> str:
        lines = ["=== RELATÓRIO DE REMOÇÃO DE SPELLS ===\n"]
        lines.append(f"Spells removidas (cadeia inicial): {report.spells_removed}")
        lines.append(f"Enchants removidos: {report.enchants_removed}")
        lines.append(f"Spells removidas por referência a enchants: {report.spells_removed_by_enchant_ref}")
        lines.append(f"Itens removidos por usar enchants removidos: {report.items_removed_by_enchant_ref}")
        lines.append(f"Referências de itens removidas da loja: {report.item_store_refs_removed}")
        lines.append(f"Referências de itens removidas dos drops: {report.item_drop_refs_removed}")
        if report.spells_removed_ids:
            lines.append(f"\nIDs das spells iniciais removidas ({len(report.spells_removed_ids)}):")
            for i in range(0, len(report.spells_removed_ids), 10):
                chunk = report.spells_removed_ids[i:i+10]
                lines.append("  " + ", ".join(chunk))
        if report.enchants_removed_ids:
            lines.append(f"\nIDs dos enchants removidos ({len(report.enchants_removed_ids)}):")
            for i in range(0, len(report.enchants_removed_ids), 10):
                chunk = report.enchants_removed_ids[i:i+10]
                lines.append("  " + ", ".join(chunk))
        if report.spells_removed_by_enchant_ref_ids:
            lines.append(f"\nIDs das spells removidas por referência a enchants ({len(report.spells_removed_by_enchant_ref_ids)}):")
            for i in range(0, len(report.spells_removed_by_enchant_ref_ids), 10):
                chunk = report.spells_removed_by_enchant_ref_ids[i:i+10]
                lines.append("  " + ", ".join(chunk))
        if report.items_removed_by_enchant_ref_ids:
            lines.append(f"\nIDs dos itens removidos por usar enchants removidos ({len(report.items_removed_by_enchant_ref_ids)}):")
            for i in range(0, len(report.items_removed_by_enchant_ref_ids), 10):
                chunk = report.items_removed_by_enchant_ref_ids[i:i+10]
                lines.append("  " + ", ".join(chunk))
        if report.spell_files_processed:
            lines.append(f"\nArquivos de spell processados: {len(report.spell_files_processed)}")
        if report.enchant_files_processed:
            lines.append(f"Arquivos de enchant processados: {len(report.enchant_files_processed)}")
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