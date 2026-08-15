from rest_framework import serializers

from .models import (
    EVVehicle,
    ChargingStation,
    Route,
    Trip,
    ChargingLog,
    Alert,
    TrafficSnapshot,

    # Advanced models
    WeatherData,
    BatteryAnalysis,
    ChargingBooking,
    Notification,
    Payment,
    UserProfile,
    VehicleHealth,
    VehicleInsurance,
    ChargingStationQueue,
    StationReview,
    EcoScore,
    MultiStopRoute,

    # AI / EV features
    VehicleLocationHistory,
    AIRangePrediction,
    AIRouteRecommendation,
    ChargingPrediction,
    ElectricityPrice,
    StationFaultReport,
    EmergencySOS,
    RoadsideAssistance,
    EVServiceCenter,
    ServiceBooking,
    VehicleDocument,
    TollPlaza,
    TripExpense,
    CarbonSaving,
    SavedRoute,
    EVParkingStation,

    # More advanced AI
    PredictiveMaintenance,
    DrivingBehavior,
    BatteryAnomaly,
    ChargingDemandForecast,
    SmartChargingSchedule,
    VehicleGeofence,
    GeofenceEvent,
    VehicleSecurityEvent,
    AccidentDetection,
    EmergencyContact,
    DriverProfile,
    Fleet,
    FleetDriverAssignment,
    RenewableEnergyUsage,
    VehicleToGridTransaction,
    TripRiskAnalysis,
    AIAssistantConversation,
    EVUserPreference,
)


# ============================================================
# EV VEHICLE
# ============================================================

class EVVehicleSerializer(serializers.ModelSerializer):

    battery_percentage = serializers.SerializerMethodField()

    class Meta:
        model = EVVehicle
        fields = [
            'id',
            'vehicle_type',
            'battery_capacity',
            'current_charge',
            'battery_percentage',
            'latitude',
            'longitude',
            'speed',
            'status',
            'last_updated',
            'created_at',
        ]

    def get_battery_percentage(self, obj):

        # Use your model method if available
        if hasattr(obj, 'battery_percentage'):
            value = obj.battery_percentage

            if callable(value):
                return value()

            return value

        # fallback calculation
        if obj.battery_capacity:
            return round(
                (obj.current_charge / obj.battery_capacity) * 100,
                2
            )

        return 0


# ============================================================
# CHARGING STATION
# ============================================================

class ChargingStationSerializer(serializers.ModelSerializer):

    availability_percentage = serializers.SerializerMethodField()

    class Meta:
        model = ChargingStation
        fields = [
            'id',
            'name',
            'latitude',
            'longitude',
            'chargers_available',
            'chargers_total',
            'availability_percentage',
            'charger_type',
            'power_capacity',
            'amenities',

            # new station features
            'price_per_kwh',
            'operator_name',
            'operational_status',
            'average_rating',
            'total_reviews',
            'waitlist_size',
            'accepts_reservations',
            'qr_code_enabled',
            'has_restroom',
            'has_restaurant',
            'wheelchair_accessible',
        ]

    def get_availability_percentage(self, obj):

        if not obj.chargers_total:
            return 0

        return round(
            (obj.chargers_available / obj.chargers_total) * 100,
            2
        )


# ============================================================
# ROUTE
# ============================================================

class RouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = '__all__'


# ============================================================
# TRIP
# ============================================================

class TripSerializer(serializers.ModelSerializer):

    vehicle_detail = EVVehicleSerializer(
        source='vehicle',
        read_only=True
    )

    route_detail = RouteSerializer(
        source='route',
        read_only=True
    )

    class Meta:
        model = Trip
        fields = [
            'id',
            'vehicle',
            'vehicle_detail',
            'route',
            'route_detail',
            'start_time',
            'end_time',
            'energy_used',
            'distance_traveled',
            'charging_stops',
            'created_at',
        ]


# ============================================================
# CHARGING LOG
# ============================================================

class ChargingLogSerializer(serializers.ModelSerializer):

    vehicle_detail = EVVehicleSerializer(
        source='vehicle',
        read_only=True
    )

    station_detail = ChargingStationSerializer(
        source='station',
        read_only=True
    )

    class Meta:
        model = ChargingLog
        fields = '__all__'


# ============================================================
# ALERT
# ============================================================

class AlertSerializer(serializers.ModelSerializer):

    alert_type_display = serializers.CharField(
        source='get_alert_type_display',
        read_only=True
    )

    vehicle_detail = EVVehicleSerializer(
        source='vehicle',
        read_only=True
    )

    class Meta:
        model = Alert
        fields = '__all__'


# ============================================================
# TRAFFIC
# ============================================================

class TrafficSnapshotSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrafficSnapshot
        fields = '__all__'


# ============================================================
# WEATHER
# ============================================================

class WeatherDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = WeatherData
        fields = '__all__'


# ============================================================
# BATTERY ANALYSIS
# ============================================================

class BatteryAnalysisSerializer(serializers.ModelSerializer):

    vehicle_detail = EVVehicleSerializer(
        source='vehicle',
        read_only=True
    )

    class Meta:
        model = BatteryAnalysis
        fields = '__all__'


# ============================================================
# CHARGING BOOKING
# ============================================================

class ChargingBookingSerializer(serializers.ModelSerializer):

    vehicle_detail = EVVehicleSerializer(
        source='vehicle',
        read_only=True
    )

    station_detail = ChargingStationSerializer(
        source='station',
        read_only=True
    )

    class Meta:
        model = ChargingBooking
        fields = '__all__'


# ============================================================
# NOTIFICATION
# ============================================================

class NotificationSerializer(serializers.ModelSerializer):

    notification_type_display = serializers.CharField(
        source='get_notification_type_display',
        read_only=True
    )

    class Meta:
        model = Notification
        fields = '__all__'


# ============================================================
# PAYMENT
# ============================================================

class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'

        read_only_fields = [
            'transaction_id',
            'created_at',
        ]


# ============================================================
# USER PROFILE
# ============================================================

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = '__all__'


# ============================================================
# VEHICLE HEALTH
# ============================================================

class VehicleHealthSerializer(serializers.ModelSerializer):

    vehicle_detail = EVVehicleSerializer(
        source='vehicle',
        read_only=True
    )

    class Meta:
        model = VehicleHealth
        fields = '__all__'


# ============================================================
# INSURANCE
# ============================================================

class VehicleInsuranceSerializer(serializers.ModelSerializer):

    class Meta:
        model = VehicleInsurance
        fields = '__all__'


# ============================================================
# CHARGING QUEUE
# ============================================================

class ChargingStationQueueSerializer(serializers.ModelSerializer):

    station_detail = ChargingStationSerializer(
        source='station',
        read_only=True
    )

    vehicle_detail = EVVehicleSerializer(
        source='vehicle',
        read_only=True
    )

    class Meta:
        model = ChargingStationQueue
        fields = '__all__'


# ============================================================
# STATION REVIEW
# ============================================================

class StationReviewSerializer(serializers.ModelSerializer):

    station_detail = ChargingStationSerializer(
        source='station',
        read_only=True
    )

    class Meta:
        model = StationReview
        fields = '__all__'

        read_only_fields = [
            'created_at',
            'updated_at',
        ]

    def validate_rating(self, value):

        if value < 1 or value > 5:
            raise serializers.ValidationError(
                "Rating must be between 1 and 5."
            )

        return value


# ============================================================
# ECO SCORE
# ============================================================

class EcoScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = EcoScore
        fields = '__all__'


# ============================================================
# MULTI STOP ROUTE
# ============================================================

class MultiStopRouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = MultiStopRoute
        fields = '__all__'


# ============================================================
# LIVE GPS
# ============================================================

class VehicleLocationHistorySerializer(serializers.ModelSerializer):

    vehicle_detail = EVVehicleSerializer(
        source='vehicle',
        read_only=True
    )

    class Meta:
        model = VehicleLocationHistory
        fields = '__all__'


# ============================================================
# AI RANGE PREDICTION
# ============================================================

class AIRangePredictionSerializer(serializers.ModelSerializer):

    vehicle_detail = EVVehicleSerializer(
        source='vehicle',
        read_only=True
    )

    class Meta:
        model = AIRangePrediction
        fields = '__all__'

        read_only_fields = [
            'predicted_range',
            'predicted_energy_consumption',
            'confidence_score',
            'created_at',
        ]


# ============================================================
# AI ROUTE RECOMMENDATION
# ============================================================

class AIRouteRecommendationSerializer(serializers.ModelSerializer):

    vehicle_detail = EVVehicleSerializer(
        source='vehicle',
        read_only=True
    )

    class Meta:
        model = AIRouteRecommendation
        fields = '__all__'

        read_only_fields = [
            'ai_score',
            'traffic_score',
            'weather_score',
            'recommendation_reason',
            'created_at',
        ]


# ============================================================
# CHARGING PREDICTION
# ============================================================

class ChargingPredictionSerializer(serializers.ModelSerializer):

    vehicle_detail = EVVehicleSerializer(
        source='vehicle',
        read_only=True
    )

    station_detail = ChargingStationSerializer(
        source='station',
        read_only=True
    )

    class Meta:
        model = ChargingPrediction
        fields = '__all__'


# ============================================================
# ELECTRICITY PRICE
# ============================================================

class ElectricityPriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ElectricityPrice
        fields = '__all__'


# ============================================================
# STATION FAULT
# ============================================================

class StationFaultReportSerializer(serializers.ModelSerializer):

    station_detail = ChargingStationSerializer(
        source='station',
        read_only=True
    )

    class Meta:
        model = StationFaultReport
        fields = '__all__'


# ============================================================
# EMERGENCY SOS
# ============================================================

class EmergencySOSSerializer(serializers.ModelSerializer):

    vehicle_detail = EVVehicleSerializer(
        source='vehicle',
        read_only=True
    )

    class Meta:
        model = EmergencySOS
        fields = '__all__'

        read_only_fields = [
            'created_at',
            'resolved_at',
        ]


# ============================================================
# ROADSIDE ASSISTANCE
# ============================================================

class RoadsideAssistanceSerializer(serializers.ModelSerializer):

    vehicle_detail = EVVehicleSerializer(
        source='vehicle',
        read_only=True
    )

    class Meta:
        model = RoadsideAssistance
        fields = '__all__'


# ============================================================
# SERVICE CENTER
# ============================================================

class EVServiceCenterSerializer(serializers.ModelSerializer):

    class Meta:
        model = EVServiceCenter
        fields = '__all__'


# ============================================================
# SERVICE BOOKING
# ============================================================

class ServiceBookingSerializer(serializers.ModelSerializer):

    vehicle_detail = EVVehicleSerializer(
        source='vehicle',
        read_only=True
    )

    service_center_detail = EVServiceCenterSerializer(
        source='service_center',
        read_only=True
    )

    class Meta:
        model = ServiceBooking
        fields = '__all__'


# ============================================================
# VEHICLE DOCUMENT
# ============================================================

class VehicleDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = VehicleDocument
        fields = '__all__'


# ============================================================
# TOLL
# ============================================================

class TollPlazaSerializer(serializers.ModelSerializer):

    class Meta:
        model = TollPlaza
        fields = '__all__'


# ============================================================
# TRIP EXPENSE
# ============================================================

class TripExpenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = TripExpense
        fields = '__all__'


# ============================================================
# CARBON SAVING
# ============================================================

class CarbonSavingSerializer(serializers.ModelSerializer):

    vehicle_detail = EVVehicleSerializer(
        source='vehicle',
        read_only=True
    )

    class Meta:
        model = CarbonSaving
        fields = '__all__'


# ============================================================
# SAVED ROUTE
# ============================================================

class SavedRouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = SavedRoute
        fields = '__all__'


# ============================================================
# EV PARKING
# ============================================================

class EVParkingStationSerializer(serializers.ModelSerializer):

    availability_percentage = serializers.SerializerMethodField()

    class Meta:
        model = EVParkingStation
        fields = '__all__'

    def get_availability_percentage(self, obj):

        if not obj.total_spaces:
            return 0

        return round(
            (obj.available_spaces / obj.total_spaces) * 100,
            2
        )


# ============================================================
# AI PREDICTIVE MAINTENANCE
# ============================================================

class PredictiveMaintenanceSerializer(serializers.ModelSerializer):

    vehicle_detail = EVVehicleSerializer(
        source='vehicle',
        read_only=True
    )

    class Meta:
        model = PredictiveMaintenance
        fields = '__all__'


# ============================================================
# DRIVING BEHAVIOUR AI
# ============================================================

class DrivingBehaviorSerializer(serializers.ModelSerializer):

    vehicle_detail = EVVehicleSerializer(
        source='vehicle',
        read_only=True
    )

    class Meta:
        model = DrivingBehavior
        fields = '__all__'


# ============================================================
# BATTERY ANOMALY
# ============================================================

class BatteryAnomalySerializer(serializers.ModelSerializer):

    vehicle_detail = EVVehicleSerializer(
        source='vehicle',
        read_only=True
    )

    class Meta:
        model = BatteryAnomaly
        fields = '__all__'


# ============================================================
# CHARGING DEMAND FORECAST
# ============================================================

class ChargingDemandForecastSerializer(serializers.ModelSerializer):

    station_detail = ChargingStationSerializer(
        source='station',
        read_only=True
    )

    class Meta:
        model = ChargingDemandForecast
        fields = '__all__'


# ============================================================
# SMART CHARGING
# ============================================================

class SmartChargingScheduleSerializer(serializers.ModelSerializer):

    vehicle_detail = EVVehicleSerializer(
        source='vehicle',
        read_only=True
    )

    class Meta:
        model = SmartChargingSchedule
        fields = '__all__'


# ============================================================
# GEOFENCE
# ============================================================

class VehicleGeofenceSerializer(serializers.ModelSerializer):

    vehicle_detail = EVVehicleSerializer(
        source='vehicle',
        read_only=True
    )

    class Meta:
        model = VehicleGeofence
        fields = '__all__'


class GeofenceEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = GeofenceEvent
        fields = '__all__'


# ============================================================
# VEHICLE SECURITY
# ============================================================

class VehicleSecurityEventSerializer(serializers.ModelSerializer):

    vehicle_detail = EVVehicleSerializer(
        source='vehicle',
        read_only=True
    )

    class Meta:
        model = VehicleSecurityEvent
        fields = '__all__'


# ============================================================
# ACCIDENT DETECTION
# ============================================================

class AccidentDetectionSerializer(serializers.ModelSerializer):

    vehicle_detail = EVVehicleSerializer(
        source='vehicle',
        read_only=True
    )

    class Meta:
        model = AccidentDetection
        fields = '__all__'


# ============================================================
# EMERGENCY CONTACT
# ============================================================

class EmergencyContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmergencyContact
        fields = '__all__'


# ============================================================
# DRIVER PROFILE
# ============================================================

class DriverProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = DriverProfile
        fields = '__all__'


# ============================================================
# FLEET
# ============================================================

class FleetSerializer(serializers.ModelSerializer):

    vehicle_details = EVVehicleSerializer(
        source='vehicles',
        many=True,
        read_only=True
    )

    class Meta:
        model = Fleet
        fields = '__all__'


class FleetDriverAssignmentSerializer(serializers.ModelSerializer):

    vehicle_detail = EVVehicleSerializer(
        source='vehicle',
        read_only=True
    )

    class Meta:
        model = FleetDriverAssignment
        fields = '__all__'


# ============================================================
# RENEWABLE ENERGY
# ============================================================

class RenewableEnergyUsageSerializer(serializers.ModelSerializer):

    class Meta:
        model = RenewableEnergyUsage
        fields = '__all__'


# ============================================================
# VEHICLE TO GRID
# ============================================================

class VehicleToGridTransactionSerializer(serializers.ModelSerializer):

    vehicle_detail = EVVehicleSerializer(
        source='vehicle',
        read_only=True
    )

    class Meta:
        model = VehicleToGridTransaction
        fields = '__all__'


# ============================================================
# TRIP RISK ANALYSIS
# ============================================================

class TripRiskAnalysisSerializer(serializers.ModelSerializer):

    class Meta:
        model = TripRiskAnalysis
        fields = '__all__'


# ============================================================
# AI ASSISTANT
# ============================================================

class AIAssistantConversationSerializer(serializers.ModelSerializer):

    class Meta:
        model = AIAssistantConversation
        fields = '__all__'

        read_only_fields = [
            'ai_response',
            'intent',
            'created_at',
        ]


# ============================================================
# USER EV PREFERENCES
# ============================================================

class EVUserPreferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = EVUserPreference
        fields = '__all__'