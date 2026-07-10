from __future__ import annotations

import re
import tkinter as tk
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation, ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_UP
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Callable

# =============================================================================
# Índices baseados no cabeçalho fornecido: |V.6|194|
# Os índices são zero-based.
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


# =============================================================================
# Data classes
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
            self.battle_axes_updated
            + self.katanas_updated
            + self.keys_updated
            + self.heads_level_updated
            + self.traveler_equipment_updated
            + self.cooldown_enchant_updated
            + self.rebirth_count_cleared
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


# =============================================================================
# Core parsing / encoding helpers
# =============================================================================

class ItemIniError(ValueError):
    pass


def detect_encoding(data: bytes) -> tuple[str, str]:
    candidates: tuple[tuple[str, str], ...] = (
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

    raise ItemIniError(
        "Não foi possível identificar uma codificação compatível com Big5/CP950 ou UTF-8."
    )


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

    max_required_index = max(FIELD_INDEX.values())
    if pipes_per_record <= max_required_index:
        raise ItemIniError(
            "A quantidade de pipes declarada no cabeçalho é insuficiente para localizar os campos necessários."
        )

    return version, pipes_per_record


def parse_item_ini(data: bytes, *, source_label: str) -> ParsedIni:
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


# -----------------------------------------------------------------------------
# Existing balance processing
# -----------------------------------------------------------------------------

def process_item_file(
    data: bytes,
    options: ProcessingOptions,
    *,
    base_data: bytes | None = None,
) -> tuple[bytes, ProcessingReport]:
    parsed = parse_item_ini(data, source_label="principal")

    enchant_lookup: EnchantLookup | None = None
    fields_to_copy: tuple[str, ...] = ()
    base_parsed: ParsedIni | None = None
    if options.apply_cooldown_enchant_replace:
        if base_data is None:
            raise ItemIniError("Selecione o INI base para substituir os enchants por CoolDownGroup.")
        base_parsed = parse_item_ini(base_data, source_label="base de enchants")
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
# Item Removal Feature (only C_* files, output folder)
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
    # IconFilename between I00595 and I00609 (inclusive)
    icon = fields[FIELD_INDEX["IconFilename"]]
    if not icon_filename_between(icon, 595, 614):
        return False

    # CastingTime = 30
    casting = fields[FIELD_INDEX["CastingTime"]].strip()
    if casting != "30":
        return False

    # CoolDownTime = 10
    cooldown_time = fields[FIELD_INDEX["CoolDownTime"]].strip()
    if cooldown_time != "10":
        return False

    # CoolDownGroup = 994
    cooldown_group = fields[FIELD_INDEX["CoolDownGroup"]].strip()
    if cooldown_group != "994":
        return False

    # AuctionType = 32
    auction = fields[FIELD_INDEX["AuctionType"]].strip()
    if auction != "32":
        return False

    return True


def remove_items_from_item_file(data: bytes) -> tuple[bytes, list[str]]:
    parsed = parse_item_ini(data, source_label="item file (C_)")
    new_records: list[ItemRecord] = []
    found_ids: list[str] = []

    for record in parsed.records:
        fields = record.fields
        if match_removal_criteria(fields):
            item_id = fields[FIELD_INDEX["Id"]].strip()
            if item_id:
                found_ids.append(item_id)
            # Skip this record (remove it)
        else:
            new_records.append(record)

    parsed.records = new_records
    return encode_parsed_ini(parsed), found_ids


# =============================================================================
# CORRIGIDO: Store.ini com offset=2 para pular ID do vendedor e nome
# =============================================================================
def remove_references_from_store(data: bytes, removed_ids: set[str]) -> tuple[bytes, int]:
    """
    Remove references to removed item IDs from C_Store.ini.
    Each record has 2 initial fields (vendor ID, vendor name) followed by
    groups of 3 fields: ItemID | Name | Quantity.
    When a match is found, clear all 3 fields.
    """
    parsed = parse_item_ini(data, source_label="store file (C_)")
    group_size = 3
    offset = 2  # Pular os dois campos iniciais (vendedor e nome)
    total_cleared = 0

    for record in parsed.records:
        fields = record.fields
        for i in range(offset, len(fields), group_size):
            if i + group_size > len(fields):
                break
            item_id = fields[i].strip()
            if item_id in removed_ids:
                for j in range(i, i + group_size):
                    fields[j] = ""
                total_cleared += 1

    return encode_parsed_ini(parsed), total_cleared


# =============================================================================
# CORRIGIDO: DropItem.ini com offset=1 para pular o ID do drop source
# =============================================================================
def remove_references_from_drop(data: bytes, removed_ids: set[str]) -> tuple[bytes, int]:
    """
    Remove references to removed item IDs from C_DropItem.ini.
    Each record has 1 initial field (drop source ID) followed by
    groups of 4 fields: ItemID | Name | Quantity | Percentage.
    When a match is found, clear all 4 fields.
    """
    parsed = parse_item_ini(data, source_label="drop file (C_)")
    group_size = 4
    offset = 1  # Pular o primeiro campo (ID do drop source)
    total_cleared = 0

    for record in parsed.records:
        fields = record.fields
        for i in range(offset, len(fields), group_size):
            if i + group_size > len(fields):
                break
            item_id = fields[i].strip()
            if item_id in removed_ids:
                for j in range(i, i + group_size):
                    fields[j] = ""
                total_cleared += 1

    return encode_parsed_ini(parsed), total_cleared


def process_removal(
    input_folder: Path,
    output_folder: Path,
    *,
    progress_callback: Callable[[str], None] | None = None,
) -> RemovalReport:
    report = RemovalReport()

    output_folder.mkdir(parents=True, exist_ok=True)

    # Only C_* files
    item_files = [
        input_folder / "C_Item.ini",
        input_folder / "C_ItemMall.ini",
    ]
    store_files = [
        input_folder / "C_Store.ini",
    ]
    drop_files = [
        input_folder / "C_DropItem.ini",
    ]

    item_files = [f for f in item_files if f.exists()]
    store_files = [f for f in store_files if f.exists()]
    drop_files = [f for f in drop_files if f.exists()]

    if not item_files:
        raise ItemIniError("Nenhum arquivo C_Item ou C_ItemMall encontrado na pasta de entrada.")

    all_removed_ids: list[str] = []

    # ---- Step 1: Process item files ----
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

    # ---- Step 2: Build set of removed IDs ----
    removed_set = set(all_removed_ids)
    report.removed_ids = sorted(all_removed_ids) if all_removed_ids else []

    # ---- Step 3: Process Store files ----
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

    # ---- Step 4: Process DropItem files ----
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
# GUI Application (balance + removal tabs)
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
        self.root.title("S_Item.ini — Balanceador + Remoção de itens")
        self.root.geometry("1080x940")
        self.root.minsize(960, 800)

        self.input_path: Path | None = None
        self.base_path: Path | None = None

        # ---- Balancing options ----
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

        # ---- Removal options ----
        self.removal_input_folder_var = tk.StringVar(value="")
        self.removal_output_folder_var = tk.StringVar(value="")
        self.removal_status_var = tk.StringVar(value="Nenhuma pasta selecionada.")
        self.removal_progress_var = tk.StringVar(value="Aguardando...")

        self._build_interface()

    def _build_interface(self) -> None:
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=8, pady=8)

        # ---- Tab 1: Balancing ----
        balance_frame = ttk.Frame(notebook, padding=12)
        notebook.add(balance_frame, text="Balanceamento")
        self._build_balance_tab(balance_frame)

        # ---- Tab 2: Removal ----
        removal_frame = ttk.Frame(notebook, padding=12)
        notebook.add(removal_frame, text="Remoção de itens")
        self._build_removal_tab(removal_frame)

        # ---- Status bar ----
        status_bar = ttk.Frame(self.root)
        status_bar.pack(fill="x", padx=8, pady=(0, 8))
        ttk.Label(status_bar, textvariable=self.status_var, wraplength=1060).pack(anchor="w")

    # -------------------------------------------------------------------------
    # Balance Tab
    # -------------------------------------------------------------------------

    def _build_balance_tab(self, parent: ttk.Frame) -> None:
        title = ttk.Label(
            parent,
            text="Balanceador de S_Item.ini",
            font=("Segoe UI", 16, "bold"),
        )
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

    # -------------------------------------------------------------------------
    # Removal Tab
    # -------------------------------------------------------------------------

    def _build_removal_tab(self, parent: ttk.Frame) -> None:
        title = ttk.Label(
            parent,
            text="Remoção automática de itens (apenas C_*)",
            font=("Segoe UI", 16, "bold"),
        )
        title.pack(anchor="w")

        desc = ttk.Label(
            parent,
            text=(
                "Remove itens que atendem TODOS os critérios abaixo:\n"
                "• IconFilename entre I00595 e I00609 (inclusive)\n"
                "• CastingTime = 30\n"
                "• CoolDownTime = 10\n"
                "• CoolDownGroup = 994\n"
                "• AuctionType = 32\n\n"
                "Os itens são removidos de C_Item.ini e C_ItemMall.ini.\n"
                "Em seguida, todas as referências são limpas em C_Store.ini e C_DropItem.ini.\n"
                "Os arquivos originais NÃO são modificados – as versões alteradas são salvas na pasta de saída."
            ),
            wraplength=1000,
            justify="left",
        )
        desc.pack(anchor="w", pady=(4, 12))

        # ---- Folder selection ----
        folder_frame = ttk.LabelFrame(parent, text="1. Pastas", padding=10)
        folder_frame.pack(fill="x")

        # Input folder
        input_row = ttk.Frame(folder_frame)
        input_row.pack(fill="x", pady=(0, 6))
        ttk.Label(input_row, text="Pasta de entrada (com C_*.ini):").pack(side="left")
        self.input_folder_entry = ttk.Entry(input_row, textvariable=self.removal_input_folder_var, width=50)
        self.input_folder_entry.pack(side="left", padx=(8, 8))
        ttk.Button(input_row, text="Selecionar...", command=self.select_removal_input_folder).pack(side="left")

        # Output folder
        output_row = ttk.Frame(folder_frame)
        output_row.pack(fill="x", pady=(0, 6))
        ttk.Label(output_row, text="Pasta de saída (modificados):").pack(side="left")
        self.output_folder_entry = ttk.Entry(output_row, textvariable=self.removal_output_folder_var, width=50)
        self.output_folder_entry.pack(side="left", padx=(8, 8))
        ttk.Button(output_row, text="Selecionar...", command=self.select_removal_output_folder).pack(side="left")

        ttk.Label(folder_frame, textvariable=self.removal_status_var, wraplength=980).pack(anchor="w", pady=(6, 0))

        # ---- Progress ----
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

        # ---- Report ----
        report_frame = ttk.LabelFrame(parent, text="3. Relatório de remoção", padding=10)
        report_frame.pack(fill="both", expand=True, pady=(12, 0))

        self.removal_report_text = tk.Text(report_frame, height=12, wrap="word", state="disabled")
        self.removal_report_text.pack(side="left", fill="both", expand=True)

        scroll2 = ttk.Scrollbar(report_frame, orient="vertical", command=self.removal_report_text.yview)
        scroll2.pack(side="right", fill="y")
        self.removal_report_text.configure(yscrollcommand=scroll2.set)

        self._write_removal_report("Aguardando execução...")

    def _write_removal_report(self, text: str) -> None:
        self.removal_report_text.configure(state="normal")
        self.removal_report_text.delete("1.0", "end")
        self.removal_report_text.insert("1.0", text)
        self.removal_report_text.configure(state="disabled")

    # ---- Removal callbacks ----

    def select_removal_input_folder(self) -> None:
        folder = filedialog.askdirectory(
            parent=self.root,
            title="Selecione a pasta com os arquivos C_*.ini",
        )
        if not folder:
            return
        self.removal_input_folder_var.set(folder)
        self.removal_status_var.set(f"Pasta de entrada: {folder}")
        self._update_removal_status()

    def select_removal_output_folder(self) -> None:
        folder = filedialog.askdirectory(
            parent=self.root,
            title="Selecione a pasta de saída para os arquivos modificados",
        )
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

        item_files = [
            in_path / "C_Item.ini",
            in_path / "C_ItemMall.ini",
        ]
        store_files = [
            in_path / "C_Store.ini",
        ]
        drop_files = [
            in_path / "C_DropItem.ini",
        ]

        item_files = [f for f in item_files if f.exists()]
        store_files = [f for f in store_files if f.exists()]
        drop_files = [f for f in drop_files if f.exists()]

        if not item_files:
            raise ItemIniError("Nenhum arquivo C_Item ou C_ItemMall encontrado na pasta de entrada.")

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
                "Os originais NÃO serão alterados.\n\n"
                "Deseja continuar?"
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

    # =========================================================================
    # CORRIGIDO: preview_removal com offset=1 para Drop
    # =========================================================================
    def preview_removal(self) -> None:
        try:
            item_files, store_files, drop_files, _ = self._get_removal_files()

            all_ids: list[str] = []
            file_counts: dict[str, int] = {}

            for file_path in item_files:
                try:
                    data = file_path.read_bytes()
                    parsed = parse_item_ini(data, source_label=file_path.name)
                    count = 0
                    for record in parsed.records:
                        if match_removal_criteria(record.fields):
                            item_id = record.fields[FIELD_INDEX["Id"]].strip()
                            if item_id:
                                all_ids.append(item_id)
                                count += 1
                    file_counts[file_path.name] = count
                except Exception as e:
                    file_counts[file_path.name] = -1

            store_refs = 0
            drop_refs = 0
            removed_set = set(all_ids)

            if removed_set:
                # Store com offset=2
                for file_path in store_files:
                    try:
                        data = file_path.read_bytes()
                        parsed = parse_item_ini(data, source_label=file_path.name)
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

                # Drop com offset=1
                for file_path in drop_files:
                    try:
                        data = file_path.read_bytes()
                        parsed = parse_item_ini(data, source_label=file_path.name)
                        group_size = 4
                        offset = 1
                        for record in parsed.records:
                            fields = record.fields
                            for i in range(offset, len(fields), group_size):
                                if i + group_size > len(fields):
                                    break
                                if fields[i].strip() in removed_set:
                                    drop_refs += 1
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

    # -------------------------------------------------------------------------
    # Existing balance methods (unchanged)
    # -------------------------------------------------------------------------

    def _write_report(self, text: str) -> None:
        self.report_text.configure(state="normal")
        self.report_text.delete("1.0", "end")
        self.report_text.insert("1.0", text)
        self.report_text.configure(state="disabled")

    def select_file(self) -> None:
        input_name = filedialog.askopenfilename(
            parent=self.root,
            title="Selecione o INI principal",
            filetypes=(
                ("Arquivo INI", "*.ini"),
                ("Todos os arquivos", "*.*"),
            ),
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
            filetypes=(
                ("Arquivo INI", "*.ini"),
                ("Todos os arquivos", "*.*"),
            ),
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
            self.battleaxe_var.get()
            or self.katana_var.get()
            or self.key_var.get()
            or self.head_level_var.get()
            or self.traveler_equipment_var.get()
            or self.cooldown_enchant_var.get()
            or self.clear_rebirth_var.get()
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
                filetypes=(
                    ("Arquivo INI", "*.ini"),
                    ("Todos os arquivos", "*.*"),
                ),
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