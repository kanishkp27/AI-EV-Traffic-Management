
# ============================================================
# EV TRACKING VIEWS
# ============================================================

from math import radians, sin, cos, sqrt, atan2

from django.shortcuts import render
from django.views import View

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import (
    EVVehicle,
    ChargingStation,
    Route,
    Trip,
    ChargingLog,
    Alert,
    TrafficSnapshot,
)

from .serializers import (
    EVVehicleSerializer,
    ChargingStationSerializer,
    RouteSerializer,
    TripSerializer,
    ChargingLogSerializer,
    AlertSerializer,
    TrafficSnapshotSerializer,
)

# ============================================================
# HELPER - DISTANCE BETWEEN TWO GPS POINTS
# ============================================================

def calculate_distance_km(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two GPS coordinates in kilometers.
    Uses the Haversine formula.
    """

    try:
        lat1 = float(lat1)
        lon1 = float(lon1)
        lat2 = float(lat2)
        lon2 = float(lon2)
    except (TypeError, ValueError):
        return None

    earth_radius = 6371.0

    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)

    a = (
        sin(d_lat / 2) ** 2
        + cos(radians(lat1))
        * cos(radians(lat2))
        * sin(d_lon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return earth_radius * c


# ============================================================
# EV VEHICLE API
# ============================================================

# ============================================================
# EV VEHICLE API
# ============================================================

class EVVehicleViewSet(viewsets.ModelViewSet):

    """
    EV Vehicle REST API.

    Endpoints:
        /api/vehicles/
        /api/vehicles/fleet_status/
    """

    queryset = EVVehicle.objects.all().order_by("-id")
    serializer_class = EVVehicleSerializer
    permission_classes = [AllowAny]

    # --------------------------------------------------------
    # FLEET STATUS
    # --------------------------------------------------------

    @action(
        detail=False,
        methods=["get"],
        url_path="fleet_status"
    )
    def fleet_status(self, request):
        """
        Return overall EV fleet status.
        """

        vehicles = list(
            EVVehicle.objects.all()
        )

        total_vehicles = len(vehicles)

        active_vehicles = 0
        driving = 0
        charging = 0
        idle = 0
        maintenance = 0

        for vehicle in vehicles:

            # is_active
            if getattr(vehicle, "is_active", True):
                active_vehicles += 1

            # vehicle status
            vehicle_status = str(
                getattr(vehicle, "status", "")
            ).lower()

            if vehicle_status == "driving":
                driving += 1

            elif vehicle_status == "charging":
                charging += 1

            elif vehicle_status == "idle":
                idle += 1

            elif vehicle_status == "maintenance":
                maintenance += 1

        return Response({
            "total_vehicles": total_vehicles,
            "active_vehicles": active_vehicles,
            "driving": driving,
            "charging": charging,
            "idle": idle,
            "maintenance": maintenance,
        })


# ============================================================
# CHARGING STATION API
# ============================================================

class ChargingStationViewSet(viewsets.ModelViewSet):

    """
    Charging Station REST API.

    Includes:
        /api/stations/
        /api/stations/nearby/
    """

    queryset = ChargingStation.objects.all().order_by("id")
    serializer_class = ChargingStationSerializer
    permission_classes = [AllowAny]

    # --------------------------------------------------------
    # NEARBY CHARGING STATIONS
 

    @action(
        detail=False,
        methods=["get"],
        url_path="nearby",
    )
    def nearby(self, request):
        """
        Find charging stations near a latitude/longitude.

        Example:

        /api/stations/nearby/?lat=28.6139&lon=77.2090&radius=50
        """

       
        # GET PARAMETERS
       

        try:
            latitude = float(
                request.query_params.get(
                    "lat",
                    28.6139,
                )
            )

            longitude = float(
                request.query_params.get(
                    "lon",
                    77.2090,
                )
            )

            radius = float(
                request.query_params.get(
                    "radius",
                    50,
                )
            )

        except (TypeError, ValueError):

            return Response(
                {
                    "error": "Invalid latitude, longitude, or radius."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ----------------------------------------------------
        # VALIDATE RADIUS
        # ----------------------------------------------------

        if radius <= 0:
            radius = 50

        if radius > 500:
            radius = 500

        # ----------------------------------------------------
        # GET ALL STATIONS
        # ----------------------------------------------------

        stations = ChargingStation.objects.all()

        results = []

        # ----------------------------------------------------
        # CALCULATE DISTANCE
        # ----------------------------------------------------

        for station in stations:

            station_lat = getattr(
                station,
                "latitude",
                None,
            )

            station_lon = getattr(
                station,
                "longitude",
                None,
            )

            if station_lat is None or station_lon is None:
                continue

            distance = calculate_distance_km(
                latitude,
                longitude,
                station_lat,
                station_lon,
            )

            if distance is None:
                continue

            if distance > radius:
                continue

            # ------------------------------------------------
            # SERIALIZE STATION
            # ------------------------------------------------

            serializer = self.get_serializer(station)

            data = dict(serializer.data)

            # ------------------------------------------------
            # ADD DISTANCE
            # ------------------------------------------------

            data["distance"] = round(
                distance,
                2,
            )

            # ------------------------------------------------
            # SAFE DEFAULTS
            # ------------------------------------------------

            data.setdefault(
                "chargers_total",
                getattr(
                    station,
                    "chargers_total",
                    0,
                ),
            )

            data.setdefault(
                "chargers_available",
                getattr(
                    station,
                    "chargers_available",
                    0,
                ),
            )

            data.setdefault(
                "power_capacity",
                getattr(
                    station,
                    "power_capacity",
                    0,
                ),
            )

            data.setdefault(
                "charger_type",
                getattr(
                    station,
                    "charger_type",
                    "",
                ),
            )

            data.setdefault(
                "average_rating",
                getattr(
                    station,
                    "average_rating",
                    0,
                ),
            )

            data.setdefault(
                "price_per_kwh",
                getattr(
                    station,
                    "price_per_kwh",
                    None,
                ),
            )

            data.setdefault(
                "amenities",
                getattr(
                    station,
                    "amenities",
                    "",
                ),
            )

            # ------------------------------------------------
            # AVAILABILITY PERCENTAGE
            # ------------------------------------------------

            total = float(
                data.get(
                    "chargers_total",
                    0,
                ) or 0
            )

            available = float(
                data.get(
                    "chargers_available",
                    0,
                ) or 0
            )

            if total > 0:
                availability = (
                    available / total
                ) * 100
            else:
                availability = 0

            data["availability_percentage"] = round(
                availability,
                1,
            )

            # ------------------------------------------------
            # OPTIONAL AMENITIES
            

            amenities = str(
                data.get(
                    "amenities",
                    "",
                )
                or ""
            ).lower()

            data["has_restaurant"] = (
                "restaurant" in amenities
            )

            data["has_restroom"] = (
                "restroom" in amenities
                or "toilet" in amenities
                or "शौचालय" in amenities
            )

            results.append(data)

        # ----------------------------------------------------
        # SORT BY DISTANCE
        # ----------------------------------------------------

        results.sort(
            key=lambda item: item.get(
                "distance",
                999999,
            )
        )

        return Response(results)



# ROUTE API


class RouteViewSet(viewsets.ModelViewSet):

    """
    Route REST API.
    """

    queryset = Route.objects.all().order_by("-id")
    serializer_class = RouteSerializer
    permission_classes = [AllowAny]



# TRIP API


class TripViewSet(viewsets.ModelViewSet):

    """
    Trip REST API.
    """

    queryset = Trip.objects.all().order_by("-id")
    serializer_class = TripSerializer
    permission_classes = [AllowAny]


# CHARGING LOG API


class ChargingLogViewSet(viewsets.ModelViewSet):

    """
    Charging history REST API.
    """

    queryset = ChargingLog.objects.all().order_by("-id")
    serializer_class = ChargingLogSerializer
    permission_classes = [AllowAny]




# ============================================================
# ALERT API
# ============================================================

class AlertViewSet(viewsets.ModelViewSet):

    """
    EV Alert REST API.

    Endpoints:
        /api/alerts/
        /api/alerts/active/
    """

    queryset = Alert.objects.all().order_by("-id")
    serializer_class = AlertSerializer
    permission_classes = [AllowAny]

    
    # ACTIVE ALERTS
   

    @action(
        detail=False,
        methods=["get"],
        url_path="active"
    )
    def active(self, request):
        """
        Return active alerts.

        Uses is_active if the model has that field.
        Otherwise returns the latest alerts.
        """

        alerts = Alert.objects.all().order_by("-id")

        # Check whether Alert model contains is_active
        alert_fields = {
            field.name
            for field in Alert._meta.get_fields()
        }

        if "is_active" in alert_fields:
            alerts = alerts.filter(
                is_active=True
            )

        serializer = self.get_serializer(
            alerts,
            many=True
        )

        return Response(serializer.data)


# TRAFFIC SNAPSHOT API


class TrafficSnapshotViewSet(viewsets.ModelViewSet):

    """
    Traffic information REST API.
    """

    queryset = TrafficSnapshot.objects.all().order_by("-id")
    serializer_class = TrafficSnapshotSerializer
    permission_classes = [AllowAny]



# HOME VIEW


class HomeView(View):

    """
    EV Manager home page.
    """

    def get(self, request):

        return render(
            request,
            "home.html",
            {
                "page_title": "EV Manager India",
            },
        )


# DRIVER DASHBOARD


class DriverDashboardView(View):

    """
    Main EV Driver Dashboard.
    """

    def get(self, request):

        vehicles = EVVehicle.objects.all().order_by("-id")

        stations = ChargingStation.objects.all().order_by("id")

        alerts = Alert.objects.all().order_by("-id")[:10]

        traffic = TrafficSnapshot.objects.all().order_by("-id")[:10]

        context = {
            "page_title": "EV Driver Dashboard",
            "vehicles": vehicles,
            "stations": stations,
            "alerts": alerts,
            "traffic": traffic,
        }

        return render(
            request,
            "driver_dashboard.html",
            context,
        )



# VEHICLES PAGE


class VehiclesPageView(View):

    """
    My Vehicles page.
    """

    def get(self, request):

        vehicles = (
            EVVehicle.objects
            .all()
            .order_by("-id")
        )

        context = {
            "page_title": "My Vehicles",
            "vehicles": vehicles,
        }

        return render(
            request,
            "vehicles.html",
            context,
        )



# BATTERY ANALYTICS


class BatteryAnalyticsView(View):

    """
    Battery Analytics dashboard.
    """

    def get(self, request):

        vehicles = (
            EVVehicle.objects
            .all()
            .order_by("-id")
        )

        context = {
            "page_title": "Battery Analytics",
            "vehicles": vehicles,
        }

        return render(
            request,
            "battery_analytics.html",
            context,
        )



# CHARGING FINDER PAGE


class ChargingFinderView(View):

    """
    Charging Station Finder page.
    """

    def get(self, request):

        stations = (
            ChargingStation.objects
            .all()
            .order_by("id")
        )

        context = {
            "page_title": "Charging Station Finder",
            "stations": stations,
        }

        return render(
            request,
            "charging_finder.html",
            context,
        )
    
# ENHANCED CHARGING STATIONS PAGE


class StationsEnhancedView(View):
    """
    Enhanced Charging Stations page.
    """

    def get(self, request):

        stations = (
            ChargingStation.objects
            .all()
            .order_by("id")
        )

        context = {
            "page_title": "Enhanced Charging Stations",
            "stations": stations,
        }

        return render(
            request,
            "stations_enhanced.html",
            context,
        )
  
# ROUTE PLANNER VIEW


class RoutePlannerView(View):
    """
    Route Planner page.
    """

    def get(self, request):
        context = {
            "page_title": "Route Planner",
        }

        return render(
            request,
            "route_planner.html",
            context,
        )
   
# WEATHER & TRAFFIC VIEW


class WeatherTrafficView(View):
    """
    Weather and traffic information page.
    """

    def get(self, request):

        context = {
            "page_title": "Weather & Traffic",
        }

        return render(
            request,
            "weather_traffic.html",
            context,
        )
   
# AI RECOMMENDATIONS VIEW


class AIRecommendationsView(View):
    """
    AI-powered EV recommendations page.
    """

    def get(self, request):

        context = {
            "page_title": "AI Recommendations",
        }

        return render(
            request,
            "ai_recommendations.html",
            context,
        )
   

class RewardsView(View):
    """
    Rewards page for EV drivers.
    """

    def get(self, request):
        context = {
            "page_title": "EV Rewards",
        }

        return render(
            request,
            "rewards.html",
            context
        )
   
# NOTIFICATIONS PAGE VIEW


class NotificationsView(View):
    """
    Display notifications and alerts page.
    """

    def get(self, request):
        context = {
            "page_title": "Notifications & Alerts",
        }

        return render(
            request,
            "notifications_alerts.html",
            context
        )
    # ============================================================
# USER PROFILE PAGE


class UserProfileView(View):
    """
    Display the user profile page.
    """

    def get(self, request):
        context = {
            "page_title": "User Profile",
        }

        return render(
            request,
            "user_profile.html",
            context
        )
    # ============================================================
# ADMIN DASHBOARD



class AdminDashboardView(View):
    """
    Display the admin dashboard.
    """

    def get(self, request):
        context = {
            "page_title": "Admin Dashboard",
        }

        return render(
            request,
            "admin_dashboard.html",
            context
        )