"""Terraform plan parser

Parses `terraform plan` and groups
resources by action and type.
"""
from __future__ import annotations  # note: must be at top (after docstring only)

from collections import defaultdict
from pathlib import Path
from typing import DefaultDict, Dict, List
import re


class TfPlanParser:
    """
    single-pass Terraform plan parser

    Examples
    --------
    >>> TfPlanParser("plan.txt").parse()
    {'create': {'google_storage_bucket': ['main']}, ...}
    """

    _PATTERNS: Dict[str, re.Pattern[str]] = {
        "create":  re.compile(
            r"^\s*#\s+(?P<type>[\w_]+)\.(?P<name>[\w-]+)\s+will be created"
        ),
        "destroy": re.compile(
            r"^\s*#\s+(?P<type>[\w_]+)\.(?P<name>[\w-]+)\s+will be destroyed"
        ),
        "update":  re.compile(
            r"^\s*#\s+(?P<type>[\w_]+)\.(?P<name>[\w-]+)\s+will be updated in-place"
        ),
        "replace": re.compile(
            r"^\s*#\s+(?P<type>[\w_]+)\.(?P<name>[\w-]+)\s+must be replaced"
        ),
    }

    def __init__(self, plan_path: str | Path) -> None:
        self.plan_path = Path(plan_path)

    # public
    def parse(self) -> Dict[str, DefaultDict[str, List[str]]]:
        """
        Returns a nested dict grouped by action → resource-type → [names].
        """
        changes: Dict[str, DefaultDict[str, List[str]]] = {
            action: defaultdict(list) for action in self._PATTERNS
        }

        with self.plan_path.open(encoding="utf-8") as fh:
            for line in fh:
                for action, pattern in self._PATTERNS.items():
                    if (match := pattern.search(line)):
                        changes[action][match["type"]].append(match["name"])
                        break  # only one pattern can match a given line
        return changes
