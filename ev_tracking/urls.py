# ============================================================
# EV TRACKING URLS
# ============================================================

from django.urls import path, include
from django.shortcuts import redirect
from rest_framework.routers import DefaultRouter

from .views import (
    EVVehicleViewSet,
    ChargingStationViewSet,
    RouteViewSet,
    TripViewSet,
    ChargingLogViewSet,
    AlertViewSet,
    TrafficSnapshotViewSet,

    DriverDashboardView,
    VehiclesPageView,
    BatteryAnalyticsView,
    ChargingFinderView,
    StationsEnhancedView,
    RoutePlannerView,
    WeatherTrafficView,
    AIRecommendationsView,
    RewardsView,
    NotificationsView,
    UserProfileView,
    AdminDashboardView,
)


# ============================================================
# API ROUTER
# ============================================================

router = DefaultRouter()

router.register(
    r"vehicles",
    EVVehicleViewSet,
    basename="vehicle",
)

router.register(
    r"stations",
    ChargingStationViewSet,
    basename="charging-station",
)

router.register(
    r"routes",
    RouteViewSet,
    basename="route",
)

router.register(
    r"trips",
    TripViewSet,
    basename="trip",
)

router.register(
    r"charging-logs",
    ChargingLogViewSet,
    basename="charging-log",
)

router.register(
    r"alerts",
    AlertViewSet,
    basename="alert",
)

router.register(
    r"traffic",
    TrafficSnapshotViewSet,
    basename="traffic",
)


# ============================================================
# HOME
# ============================================================

def home(request):
    return redirect("driver_dashboard")


# ============================================================
# URL PATTERNS
# ============================================================

urlpatterns = [

    # --------------------------------------------------------
    # HOME
    # --------------------------------------------------------

    path(
        "",
        home,
        name="home",
    ),

    # --------------------------------------------------------
    # DRIVER DASHBOARD
    # --------------------------------------------------------

    path(
        "driver/dashboard/",
        DriverDashboardView.as_view(),
        name="driver_dashboard",
    ),

    # --------------------------------------------------------
    # VEHICLES
    # --------------------------------------------------------

    path(
        "vehicles/",
        VehiclesPageView.as_view(),
        name="vehicles",
    ),

    # --------------------------------------------------------
    # BATTERY ANALYTICS
    # --------------------------------------------------------

    path(
        "battery-analytics/",
        BatteryAnalyticsView.as_view(),
        name="battery_analytics",
    ),

    # --------------------------------------------------------
    # CHARGING FINDER
    # --------------------------------------------------------

    path(
        "charging-finder/",
        ChargingFinderView.as_view(),
        name="charging_finder",
    ),

    # --------------------------------------------------------
    # ENHANCED STATIONS
    # --------------------------------------------------------

    path(
        "stations-enhanced/",
        StationsEnhancedView.as_view(),
        name="stations_enhanced",
    ),

    # --------------------------------------------------------
    # ROUTE PLANNER
    # --------------------------------------------------------

    path(
        "route-planner/",
        RoutePlannerView.as_view(),
        name="route_planner",
    ),

    # --------------------------------------------------------
    # SMART ROUTE PLANNER
    # --------------------------------------------------------

    path(
        "smart-route-planner/",
        RoutePlannerView.as_view(),
        name="smart_route_planner",
    ),

    # --------------------------------------------------------
    # WEATHER & TRAFFIC
    # --------------------------------------------------------

    path(
        "weather-traffic/",
        WeatherTrafficView.as_view(),
        name="weather_traffic",
    ),

    # --------------------------------------------------------
    # AI RECOMMENDATIONS
    # --------------------------------------------------------

    path(
        "ai-recommendations/",
        AIRecommendationsView.as_view(),
        name="ai_recommendations",
    ),
    path(
    "rewards/",
    RewardsView.as_view(),
    name="rewards",
),
path(
        "notifications/",
        NotificationsView.as_view(),
        name="notifications",
    ),
    path(
    "user-profile/",
    UserProfileView.as_view(),
    name="user_profile",
),
# --------------------------------------------------------
# ADMIN DASHBOARD
# --------------------------------------------------------

path(
    "admin-dashboard/",
    AdminDashboardView.as_view(),
    name="admin_dashboard",
),
    

    # --------------------------------------------------------
    # REST API
    # --------------------------------------------------------

    path(
        "api/",
        include(router.urls),
    ),
]