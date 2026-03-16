import pandas as pd
import pytest

from enterprise_ds.data import validate_columns


def test_validate_columns_raises_for_missing_columns() -> None:
    frame = pd.DataFrame({"known_column": [1, 2, 3]})

    with pytest.raises(ValueError, match="missing required columns"):
        validate_columns(frame, ["known_column", "missing_column"])
