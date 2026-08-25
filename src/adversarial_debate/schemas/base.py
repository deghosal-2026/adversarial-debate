"""Shared schema base: frozen instances (audit safety), strict types, no extras."""

from pydantic import BaseModel, ConfigDict


class SchemaBase(BaseModel):
    """Base for all v0.1.0 schemas.

    Frozen because every entity is an audit-log fact; mutations are new events
    (glossary: "a concession is a new event, not an edit"). Strict so malformed
    inputs fail loudly instead of coercing silently (WBS M1 exit gate).
    """

    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)
