import folium
import pandas as pd
import requests
from geopy.distance import geodesic

url_bab = "https://verkehr.autobahn.de/o/autobahn"


def get_warnings(autobahn_id):
    """
    Get traffic warnings for a specific autobahn.

    Parameters
    ----------
    autobahn_id : str
        The ID of the autobahn.

    Returns
    -------
    list
        A list of warnings.
    """
    url = f"{url_bab}/{autobahn_id}/services/warning"
    response = requests.get(url)
    return response.json()["warning"]


class TrafficWarning:
    """
    A class to represent a traffic warning.

    Attributes
    ----------
    isBlocked : bool
        Indicates if the road is blocked.
    display_type : str
        The type of display for the warning.
    subtitle : str
        The subtitle of the warning.
    title : str
        The title of the warning.
    startTimestamp : str
        The start timestamp of the warning.
    delayTimeValue : int
        The delay time value in minutes.
    abnormalTrafficType : str
        The type of abnormal traffic.
    averageSpeed : float
        The average speed of traffic.
    description : str
        The description of the warning.
    routeRecommendation : str
        The recommended route.
    lorryParkingFeatureIcons : list
        Icons for lorry parking features.
    geometry : dict
        The geometry of the warning.
    geo_df : pandas.DataFrame
        A DataFrame containing the geographical coordinates.

    Methods
    -------
    create_geo_dataframe(coordinates):
        Creates a DataFrame from geographical coordinates.
    """

    def __init__(self, data):
        """
        Initialize the TrafficWarning class with data from the dictionary.

        Parameters
        ----------
        data : dict
            A dictionary containing traffic event information.
        """
        self.isBlocked = data.get("isBlocked")
        self.display_type = data.get("display_type")
        self.subtitle = data.get("subtitle")
        self.title = data.get("title")
        self.startTimestamp = data.get("startTimestamp")
        self.delayTimeValue = data.get("delayTimeValue")
        self.abnormalTrafficType = data.get("abnormalTrafficType")
        self.averageSpeed = data.get("averageSpeed")
        self.description = data.get("description")
        self.routeRecommendation = data.get("routeRecommendation")
        self.lorryParkingFeatureIcons = data.get("lorryParkingFeatureIcons")
        self.geometry = data.get("geometry")
        self.geo_df = self.create_geo_dataframe(self.geometry["coordinates"])

    def create_geo_dataframe(self, coordinates):
        """
        Create a DataFrame from geographical coordinates.

        Parameters
        ----------
        coordinates : list
            A list of geographical coordinates.

        Returns
        -------
        pandas.DataFrame
            A DataFrame containing the geographical coordinates.
        """
        df = pd.DataFrame(
            {
                "lat": [coord[0] for coord in coordinates],
                "long": [coord[1] for coord in coordinates],
            }
        ).dropna()
        return df


def calculate_traffic_length(coordinates):
    """
    Calculate the total length of traffic from coordinates.

    Parameters
    ----------
    coordinates : list
        A list of geographical coordinates.

    Returns
    -------
    float
        The total length of traffic in kilometers.
    """
    total_length = 0.0
    for i in range(len(coordinates) - 1):
        total_length += geodesic(coordinates.loc[i], coordinates.loc[i + 1]).kilometers
    return total_length


def map_plot(plotlist, on="aveg_speed"):
    """
    Plot a map with traffic data.

    Parameters
    ----------
    plotlist : list
        A list of DataFrames containing traffic data.
    on : str, optional
        The column to base the color mapping on (default is "aveg_speed").

    Returns
    -------
    folium.Map
        A Folium map with the plotted traffic data.
    """
    on_stats = pd.concat(df[on] for df in plotlist).describe()
    colormap = folium.LinearColormap(
        ["green", "yellow", "red"], vmin=on_stats["min"], vmax=on_stats["max"]
    )

    m = folium.Map(
        pd.concat([data[["long", "lat"]] for data in plotlist]).mean(), zoom_start=10
    )
    for df in plotlist:
        points_ = [(point[0], point[1]) for point in df[["long", "lat"]].to_numpy()]
        folium.features.ColorLine(
            points_,
            colors=[data for data in df[on]],
            colormap=colormap,
            weight=5,
            smooth_factor=3,
        ).add_to(m)
    return m
