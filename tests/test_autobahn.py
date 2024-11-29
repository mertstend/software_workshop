import pandas as pd
import numpy as np
from software_workshop.autobahn import (
    calculate_traffic_length,
)


def test_calculate_traffic_length_with_NaN():

    coordinates = pd.DataFrame({"lat": [1, 2, np.nan], "long": [3, 4, 5]})
    expected_length = 22.0
    actual_length = calculate_traffic_length(coordinates)
    assert abs(expected_length - actual_length) < 1e-6  # allow some
