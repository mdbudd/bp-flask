# from resources.hierarchy import (
#     HierarchyOverview,
#     HierarchyManagement,
#     HierarchySearch,
#     HierarchyInfo,
#     HierarchyEmployee,
#     HierarchyChange,
#     HierarchyChangeData,
#     HierarchyChangePosition,
# )
from resources.user import UserAuth
# from resources.user import UserRefresh, UserImpersonate, UserDetails, UserInfo, UserLogout
# from resources.data import Data

from resources.awesome import AwesomeAPI

resourceList = [
    # {"class": HierarchyOverview, "route(s)": ["/reportees"]},
    # {"class": HierarchyManagement, "route(s)": ["/managers/<int:positionId>"]},
    # {"class": Data, "route(s)": ["/data"]},
    {"class": UserAuth, "route(s)": ["/auth"]},
    # {"class": UserLogin, "route(s)": ["/login"]},
    # {"class": UserRefresh, "route(s)": ["/refresh"]},
    # {"class": UserImpersonate, "route(s)": ["/impersonate"]},
    # {"class": UserDetails, "route(s)": ["/details"]},
    # {"class": UserInfo, "route(s)": ["/info"]},
    # {"class": UserLogout, "route(s)": ["/logout"]},
    {"class": AwesomeAPI, "route(s)": ["/awesome"]},
]
