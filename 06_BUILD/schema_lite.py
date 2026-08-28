"""
schema_lite.py — bağımlılıksız, minimal JSON-Schema doğrulayıcı.

Desen: KOREAN-HANGUL-HANDWRITING-WORKBOOK / LICENSE-AND-LAUNCH-
CALIFORNIA-LIFE-HEALTH schema_lite.py. Bu dosya içerikten tamamen
bağımsız, genel amaçlı bir ALTYAPIDIR — kardeş projelerdeki mantığın
aynısını taşır (yöntem devralındı, içerik değil).
Tam JSON-Schema spesifikasyonunu uygulamaz, yalnızca bu projenin
şemalarının kullandığı alt kümeyi: type, required, additionalProperties,
enum, pattern, minLength/maxLength, minimum/maximum, minItems/maxItems,
items.
"""
from __future__ import annotations
import re


class SchemaError(Exception):
    pass


def _check_type(value, expected, path):
    if expected == "object":
        ok = isinstance(value, dict)
    elif expected == "array":
        ok = isinstance(value, list)
    elif expected == "string":
        ok = isinstance(value, str)
    elif expected == "integer":
        ok = isinstance(value, int) and not isinstance(value, bool)
    elif expected == "boolean":
        ok = isinstance(value, bool)
    elif expected == "null":
        ok = value is None
    else:
        raise SchemaError(f"bilinmeyen tip: {expected}")
    if not ok:
        raise SchemaError(f"{path}: tip {expected} bekleniyordu, {type(value).__name__} bulundu")


def validate(instance, schema, path="$") -> list[str]:
    """Hataları liste olarak döndürür. Boş liste = geçerli."""
    errors: list[str] = []
    types = schema.get("type")
    if types is not None:
        allowed = types if isinstance(types, list) else [types]
        matched = False
        for t in allowed:
            try:
                _check_type(instance, t, path)
                matched = True
                break
            except SchemaError:
                continue
        if not matched:
            errors.append(f"{path}: tip {allowed} bekleniyordu, {type(instance).__name__} bulundu")
            return errors  # tip yanlışsa alt kontrolleri anlamsız

    if instance is None:
        return errors

    if schema.get("type") == "object" or isinstance(instance, dict):
        if isinstance(instance, dict):
            props = schema.get("properties", {})
            for req in schema.get("required", []):
                if req not in instance:
                    errors.append(f"{path}: zorunlu alan eksik: {req}")
            if schema.get("additionalProperties") is False:
                for key in instance:
                    if key not in props:
                        errors.append(f"{path}: İZİN LİSTESİNDE OLMAYAN alan: {key}")
            for key, subschema in props.items():
                if key in instance:
                    errors.extend(validate(instance[key], subschema, f"{path}.{key}"))

    if schema.get("type") == "array" or isinstance(instance, list):
        if isinstance(instance, list):
            if "minItems" in schema and len(instance) < schema["minItems"]:
                errors.append(f"{path}: en az {schema['minItems']} öğe gerekli, {len(instance)} bulundu")
            if "maxItems" in schema and len(instance) > schema["maxItems"]:
                errors.append(f"{path}: en fazla {schema['maxItems']} öğe olmalı, {len(instance)} bulundu")
            item_schema = schema.get("items")
            if item_schema:
                for i, item in enumerate(instance):
                    errors.extend(validate(item, item_schema, f"{path}[{i}]"))

    if isinstance(instance, str):
        if "minLength" in schema and len(instance) < schema["minLength"]:
            errors.append(f"{path}: en az {schema['minLength']} karakter gerekli")
        if "maxLength" in schema and len(instance) > schema["maxLength"]:
            errors.append(f"{path}: en fazla {schema['maxLength']} karakter olmalı")
        if "pattern" in schema and not re.match(schema["pattern"], instance):
            errors.append(f"{path}: desenle eşleşmiyor: {schema['pattern']}")
        if "format" in schema and schema["format"] == "date":
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", instance):
                errors.append(f"{path}: tarih biçimi YYYY-MM-DD olmalı")

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            errors.append(f"{path}: en az {schema['minimum']} olmalı")
        if "maximum" in schema and instance > schema["maximum"]:
            errors.append(f"{path}: en fazla {schema['maximum']} olmalı")

    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: {schema['enum']} kümesinde olmalı, {instance!r} bulundu")

    return errors
