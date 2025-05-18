from pathlib import Path
import tempfile
from textwrap import dedent

from tfplan_parser.parser import TfPlanParser


def _sample() -> str:
    return dedent(
        """\
        # google_storage_bucket.main will be created
        # google_storage_bucket.logs will be updated in-place
        # google_compute_instance.vm will be destroyed
        # google_sql_database.main must be replaced
        """
    )


def test_parse_sample() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        plan = Path(tmp) / "plan.txt"
        plan.write_text(_sample())

        changes = TfPlanParser(plan).parse()

        assert changes["create"]["google_storage_bucket"] == ["main"]
        assert changes["update"]["google_storage_bucket"] == ["logs"]
        assert changes["destroy"]["google_compute_instance"] == ["vm"]
        assert changes["replace"]["google_sql_database"] == ["main"]
