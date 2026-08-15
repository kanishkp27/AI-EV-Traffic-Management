from django.db import models
from django.conf import settings

class EVVehicle(models.Model):
    
    STATUS_CHOICES = [
        ('idle', 'Idle'),
        ('driving', 'Driving'),
        ('charging', 'Charging'),
        ('maintenance', 'Maintenance'),
        ('offline', 'Offline'),
    ]

    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ev_vehicles'
    )

    vehicle_type = models.CharField(
        max_length=100,
        default='Tata Nexon EV'
    )

    registration_number = models.CharField(
        max_length=30,
        blank=True
    )

    color = models.CharField(
        max_length=50,
        blank=True
    )

    registration_year = models.IntegerField(
        null=True,
        blank=True
    )

    battery_capacity = models.FloatField(default=75.0)
    current_charge = models.FloatField(default=75.0)

    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

    speed = models.FloatField(default=0.0)
    mileage = models.FloatField(default=0.0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='idle'
    )

    vin = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        unique=True
    )

    manufacturer = models.CharField(
        max_length=100,
        blank=True
    )

    model_name = models.CharField(
        max_length=100,
        blank=True
    )

    battery_temperature = models.FloatField(default=25.0)

    estimated_range = models.FloatField(default=0.0)

    odometer = models.FloatField(default=0.0)

    is_active = models.BooleanField(default=True)

    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-last_updated']

    def battery_percentage(self):
        if self.battery_capacity <= 0:
            return 0

        percentage = (
            self.current_charge / self.battery_capacity
        ) * 100

        return round(max(0, min(percentage, 100)), 2)

    def __str__(self):
        if self.registration_number:
            return f"{self.vehicle_type} - {self.registration_number}"
        return f"{self.vehicle_type} #{self.pk}"


# ============================================================
# CHARGING STATION
# ============================================================

class ChargingStation(models.Model):

    CHARGER_TYPES = [
        ('level1', 'Level 1'),
        ('level2', 'Level 2'),
        ('dcfc', 'DC Fast Charging'),
    ]

    STATUS_CHOICES = [
        ('operational', 'Operational'),
        ('maintenance', 'Maintenance'),
        ('offline', 'Offline'),
    ]

    name = models.CharField(max_length=200)

    operator_name = models.CharField(
        max_length=100,
        blank=True
    )

    latitude = models.FloatField()
    longitude = models.FloatField()

    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)

    chargers_available = models.IntegerField(default=4)
    chargers_total = models.IntegerField(default=4)

    charger_type = models.CharField(
        max_length=20,
        choices=CHARGER_TYPES,
        default='level2'
    )

    power_capacity = models.FloatField(default=50.0)

    price_per_kwh = models.FloatField(default=12.0)

    amenities = models.TextField(blank=True)

    has_restroom = models.BooleanField(default=False)
    has_restaurant = models.BooleanField(default=False)
    wheelchair_accessible = models.BooleanField(default=False)

    accepts_reservations = models.BooleanField(default=True)

    qr_code_enabled = models.BooleanField(default=False)

    average_rating = models.FloatField(default=0.0)
    total_reviews = models.IntegerField(default=0)

    waitlist_size = models.IntegerField(default=0)

    operational_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='operational'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def availability_percentage(self):
        if self.chargers_total <= 0:
            return 0

        return round(
            (self.chargers_available / self.chargers_total) * 100,
            2
        )

    def __str__(self):
        return self.name


# ============================================================
# ROUTE
# ============================================================

class Route(models.Model):

    origin_name = models.CharField(
        max_length=200,
        blank=True
    )

    destination_name = models.CharField(
        max_length=200,
        blank=True
    )

    origin_lat = models.FloatField()
    origin_lon = models.FloatField()

    destination_lat = models.FloatField()
    destination_lon = models.FloatField()

    distance = models.FloatField()

    estimated_duration = models.IntegerField()

    estimated_energy = models.FloatField(default=0.0)

    estimated_cost = models.FloatField(default=0.0)

    toll_cost = models.FloatField(default=0.0)

    traffic_level = models.CharField(
        max_length=20,
        default='clear'
    )

    route_type = models.CharField(
        max_length=20,
        choices=[
            ('fastest', 'Fastest'),
            ('eco', 'Eco Friendly'),
            ('cheapest', 'Cheapest'),
        ],
        default='fastest'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.origin_name and self.destination_name:
            return f"{self.origin_name} → {self.destination_name}"

        return f"Route #{self.pk}"


# ============================================================
# TRIP
# ============================================================

class Trip(models.Model):

    vehicle = models.ForeignKey(
        EVVehicle,
        on_delete=models.CASCADE,
        related_name='trips'
    )

    route = models.ForeignKey(
        Route,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='trips'
    )

    start_time = models.DateTimeField()

    end_time = models.DateTimeField(
        null=True,
        blank=True
    )

    energy_used = models.FloatField(default=0.0)

    distance_traveled = models.FloatField(default=0.0)

    charging_stops = models.IntegerField(default=0)

    average_speed = models.FloatField(default=0.0)

    maximum_speed = models.FloatField(default=0.0)

    estimated_cost = models.FloatField(default=0.0)

    co2_saved = models.FloatField(default=0.0)

    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_time']

    def __str__(self):
        return f"Trip #{self.pk} - {self.vehicle}"


# ============================================================
# CHARGING LOG
# ============================================================

class ChargingLog(models.Model):

    vehicle = models.ForeignKey(
        EVVehicle,
        on_delete=models.CASCADE,
        related_name='charging_logs'
    )

    station = models.ForeignKey(
        ChargingStation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='charging_logs'
    )

    start_time = models.DateTimeField()

    end_time = models.DateTimeField(
        null=True,
        blank=True
    )

    charge_amount = models.FloatField(default=0.0)

    duration = models.IntegerField(
        null=True,
        blank=True
    )

    cost = models.FloatField(default=0.0)

    battery_before = models.FloatField(default=0.0)
    battery_after = models.FloatField(default=0.0)

    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('paid', 'Paid'),
            ('failed', 'Failed'),
        ],
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_time']

    def __str__(self):
        return f"Charging #{self.pk} - {self.vehicle}"


# ============================================================
# ALERT
# ============================================================

class Alert(models.Model):

    ALERT_TYPES = [
        ('low_battery', 'Low Battery'),
        ('overheating', 'Overheating'),
        ('maintenance', 'Maintenance Required'),
        ('charging_available', 'Charging Available'),
        ('route_suggestion', 'Route Suggestion'),
        ('emergency', 'Emergency'),
        ('traffic', 'Traffic'),
        ('weather', 'Weather'),
        ('security', 'Security'),
        ('accident', 'Accident'),
    ]

    vehicle = models.ForeignKey(
        EVVehicle,
        on_delete=models.CASCADE,
        related_name='alerts'
    )

    alert_type = models.CharField(
        max_length=30,
        choices=ALERT_TYPES
    )

    message = models.TextField()

    severity = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('critical', 'Critical'),
        ],
        default='medium'
    )

    resolved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    resolved_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.alert_type} - {self.vehicle}"


# ============================================================
# TRAFFIC SNAPSHOT
# ============================================================

class TrafficSnapshot(models.Model):

    expressway_section = models.CharField(
        max_length=100
    )

    timestamp = models.DateTimeField()

    vehicle_count = models.IntegerField(default=0)

    average_speed = models.FloatField(default=0.0)

    congestion_level = models.CharField(
        max_length=20,
        choices=[
            ('clear', 'Clear'),
            ('moderate', 'Moderate'),
            ('heavy', 'Heavy'),
            ('severe', 'Severe'),
        ],
        default='clear'
    )

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    incident_reported = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

        indexes = [
            models.Index(
                fields=['expressway_section', '-timestamp']
            )
        ]

    def __str__(self):
        return f"{self.expressway_section} - {self.congestion_level}"
    # ============================================================
# WEATHER DATA
# ============================================================

class WeatherData(models.Model):

    WEATHER_CONDITIONS = [
        ('clear', 'Clear'),
        ('sunny', 'Sunny'),
        ('cloudy', 'Cloudy'),
        ('rain', 'Rain'),
        ('heavy_rain', 'Heavy Rain'),
        ('thunderstorm', 'Thunderstorm'),
        ('fog', 'Fog'),
        ('mist', 'Mist'),
        ('haze', 'Haze'),
        ('dust', 'Dust'),
        ('heatwave', 'Heatwave'),
        ('cold_wave', 'Cold Wave'),
    ]

    ROAD_CONDITIONS = [
        ('dry', 'Dry'),
        ('wet', 'Wet'),
        ('waterlogged', 'Waterlogged'),
        ('foggy', 'Foggy'),
        ('dangerous', 'Dangerous'),
    ]

    RISK_LEVELS = [
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    # --------------------------------------------------------
    # LOCATION
    # --------------------------------------------------------

    latitude = models.FloatField()
    longitude = models.FloatField()

    city = models.CharField(
        max_length=100,
        blank=True
    )

    district = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    country = models.CharField(
        max_length=100,
        default='India'
    )

    # --------------------------------------------------------
    # TEMPERATURE
    # --------------------------------------------------------

    temperature = models.FloatField()

    feels_like = models.FloatField(
        null=True,
        blank=True
    )

    min_temperature = models.FloatField(
        null=True,
        blank=True
    )

    max_temperature = models.FloatField(
        null=True,
        blank=True
    )

    # --------------------------------------------------------
    # WEATHER
    # --------------------------------------------------------

    humidity = models.IntegerField(default=0)

    weather_condition = models.CharField(
        max_length=50,
        choices=WEATHER_CONDITIONS,
        default='clear'
    )

    weather_description = models.CharField(
        max_length=200,
        blank=True
    )

    # --------------------------------------------------------
    # WIND
    # --------------------------------------------------------

    wind_speed = models.FloatField(default=0.0)

    wind_direction = models.FloatField(
        default=0.0,
        help_text='Wind direction in degrees'
    )

    wind_gust = models.FloatField(
        default=0.0
    )

    # --------------------------------------------------------
    # RAIN / PRECIPITATION
    # --------------------------------------------------------

    precipitation_chance = models.IntegerField(
        default=0
    )

    rainfall_mm = models.FloatField(
        default=0.0
    )

    # --------------------------------------------------------
    # VISIBILITY
    # --------------------------------------------------------

    visibility_km = models.FloatField(
        default=10.0
    )

    # --------------------------------------------------------
    # ATMOSPHERIC DATA
    # --------------------------------------------------------

    pressure = models.FloatField(
        default=1013.25
    )

    uv_index = models.FloatField(
        default=0.0
    )

    air_quality_index = models.IntegerField(
        null=True,
        blank=True
    )

    # --------------------------------------------------------
    # EV BATTERY IMPACT
    # --------------------------------------------------------

    battery_impact = models.FloatField(
        default=0.0,
        help_text='Estimated battery impact percentage'
    )

    range_impact_percentage = models.FloatField(
        default=0.0
    )

    estimated_range_loss_km = models.FloatField(
        default=0.0
    )

    # --------------------------------------------------------
    # ROAD CONDITIONS
    # --------------------------------------------------------

    road_condition = models.CharField(
        max_length=30,
        choices=ROAD_CONDITIONS,
        default='dry'
    )

    driving_risk = models.CharField(
        max_length=20,
        choices=RISK_LEVELS,
        default='low'
    )

    # --------------------------------------------------------
    # INDIA-SPECIFIC ALERTS
    # --------------------------------------------------------

    monsoon_alert = models.BooleanField(
        default=False
    )

    heatwave_alert = models.BooleanField(
        default=False
    )

    fog_alert = models.BooleanField(
        default=False
    )

    storm_alert = models.BooleanField(
        default=False
    )

    flood_alert = models.BooleanField(
        default=False
    )

    dust_storm_alert = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # EV DRIVER RECOMMENDATION
    # --------------------------------------------------------

    ev_recommendation = models.TextField(
        blank=True
    )

    route_recommendation = models.TextField(
        blank=True
    )

    charging_recommendation = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # DATA SOURCE
    # --------------------------------------------------------

    data_source = models.CharField(
        max_length=100,
        default='system'
    )

    # --------------------------------------------------------
    # TIMESTAMPS
    # --------------------------------------------------------

    timestamp = models.DateTimeField(
        auto_now=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-timestamp']

        indexes = [
            models.Index(
                fields=['city', '-timestamp']
            ),
            models.Index(
                fields=['state', '-timestamp']
            ),
            models.Index(
                fields=['latitude', 'longitude']
            ),
        ]

    def __str__(self):
        location = (
            self.city
            or self.district
            or self.state
            or 'Unknown Location'
        )

        return (
            f"{location} - "
            f"{self.temperature}°C - "
            f"{self.weather_condition}"
        )

    # --------------------------------------------------------
    # WEATHER HELPERS
    # --------------------------------------------------------

    def is_bad_weather(self):
        return self.weather_condition in [
            'heavy_rain',
            'thunderstorm',
            'fog',
            'dust',
            'heatwave',
            'cold_wave',
        ]

    def is_safe_for_driving(self):
        return self.driving_risk in [
            'low',
            'moderate'
        ]

    def has_weather_alert(self):
        return any([
            self.monsoon_alert,
            self.heatwave_alert,
            self.fog_alert,
            self.storm_alert,
            self.flood_alert,
            self.dust_storm_alert,
        ])

    def calculate_ev_range_impact(self):
        """
        Simple estimated EV range impact based on
        temperature and weather.
        """

        impact = 0

        # Extreme heat
        if self.temperature >= 40:
            impact += 10

        # Extreme cold
        elif self.temperature <= 5:
            impact += 15

        # Heavy rain
        if self.weather_condition == 'heavy_rain':
            impact += 5

        # Thunderstorm
        if self.weather_condition == 'thunderstorm':
            impact += 7

        # High wind
        if self.wind_speed >= 40:
            impact += 5

        return min(impact, 50)
    # ============================================================
# BATTERY ANALYSIS
# ============================================================

class BatteryAnalysis(models.Model):

    HEALTH_STATUS_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('critical', 'Critical'),
    ]

    CHARGING_STATUS_CHOICES = [
        ('not_charging', 'Not Charging'),
        ('slow_charging', 'Slow Charging'),
        ('fast_charging', 'Fast Charging'),
        ('fully_charged', 'Fully Charged'),
    ]

    # One battery analysis record for each vehicle
    vehicle = models.OneToOneField(
        EVVehicle,
        on_delete=models.CASCADE,
        related_name='battery_analysis'
    )

    # --------------------------------------------------------
    # BATTERY HEALTH
    # --------------------------------------------------------

    battery_health_percentage = models.FloatField(
        default=100.0
    )

    health_status = models.CharField(
        max_length=20,
        choices=HEALTH_STATUS_CHOICES,
        default='excellent'
    )

    charge_cycles = models.IntegerField(
        default=0
    )

    degradation_rate = models.FloatField(
        default=0.0,
        help_text='Battery degradation percentage'
    )

    # --------------------------------------------------------
    # BATTERY CAPACITY
    # --------------------------------------------------------

    original_capacity = models.FloatField(
        default=75.0,
        help_text='Original battery capacity in kWh'
    )

    current_capacity = models.FloatField(
        default=75.0,
        help_text='Current usable battery capacity in kWh'
    )

    current_charge_percentage = models.FloatField(
        default=100.0
    )

    # --------------------------------------------------------
    # RANGE ANALYSIS
    # --------------------------------------------------------

    estimated_range = models.FloatField(
        default=0.0,
        help_text='Estimated driving range in kilometres'
    )

    city_range = models.FloatField(
        default=0.0
    )

    highway_range = models.FloatField(
        default=0.0
    )

    predicted_range = models.FloatField(
        default=0.0
    )

    range_efficiency = models.FloatField(
        default=0.0,
        help_text='Kilometres per kWh'
    )

    # --------------------------------------------------------
    # TEMPERATURE
    # --------------------------------------------------------

    battery_temperature = models.FloatField(
        default=25.0
    )

    maximum_temperature = models.FloatField(
        default=25.0
    )

    minimum_temperature = models.FloatField(
        default=25.0
    )

    overheating = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # CHARGING
    # --------------------------------------------------------

    charging_status = models.CharField(
        max_length=30,
        choices=CHARGING_STATUS_CHOICES,
        default='not_charging'
    )

    charging_power = models.FloatField(
        default=0.0,
        help_text='Current charging power in kW'
    )

    estimated_charging_time = models.IntegerField(
        default=0,
        help_text='Estimated charging time in minutes'
    )

    fast_charging_sessions = models.IntegerField(
        default=0
    )

    slow_charging_sessions = models.IntegerField(
        default=0
    )

    # --------------------------------------------------------
    # ENERGY
    # --------------------------------------------------------

    total_energy_consumed = models.FloatField(
        default=0.0
    )

    total_energy_charged = models.FloatField(
        default=0.0
    )

    average_energy_consumption = models.FloatField(
        default=0.0,
        help_text='Average energy consumption in kWh/100km'
    )

    # --------------------------------------------------------
    # AI / PREDICTIVE ANALYTICS
    # --------------------------------------------------------

    predicted_battery_life_months = models.IntegerField(
        null=True,
        blank=True
    )

    predicted_replacement_date = models.DateField(
        null=True,
        blank=True
    )

    battery_risk_score = models.FloatField(
        default=0.0
    )

    anomaly_detected = models.BooleanField(
        default=False
    )

    ai_recommendation = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # ENVIRONMENTAL IMPACT
    # --------------------------------------------------------

    temperature_impact = models.FloatField(
        default=0.0
    )

    weather_impact = models.FloatField(
        default=0.0
    )

    traffic_impact = models.FloatField(
        default=0.0
    )

    # --------------------------------------------------------
    # SAFETY
    # --------------------------------------------------------

    voltage_warning = models.BooleanField(
        default=False
    )

    temperature_warning = models.BooleanField(
        default=False
    )

    degradation_warning = models.BooleanField(
        default=False
    )

    service_required = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # TIMESTAMPS
    # --------------------------------------------------------

    last_checked = models.DateTimeField(
        auto_now=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-last_checked']

        indexes = [
            models.Index(
                fields=['battery_health_percentage']
            ),
            models.Index(
                fields=['health_status']
            ),
        ]

    # --------------------------------------------------------
    # HELPER METHODS
    # --------------------------------------------------------

    def calculate_health_status(self):

        health = self.battery_health_percentage

        if health >= 90:
            return 'excellent'

        elif health >= 75:
            return 'good'

        elif health >= 60:
            return 'fair'

        elif health >= 40:
            return 'poor'

        return 'critical'

    def calculate_degradation(self):

        if self.original_capacity <= 0:
            return 0

        degradation = (
            (
                self.original_capacity -
                self.current_capacity
            )
            / self.original_capacity
        ) * 100

        return round(
            max(0, degradation),
            2
        )

    def calculate_range(self):

        if self.range_efficiency <= 0:
            return self.estimated_range

        return round(
            self.current_capacity *
            self.range_efficiency,
            2
        )

    def needs_service(self):

        return (
            self.battery_health_percentage < 70
            or self.overheating
            or self.anomaly_detected
            or self.degradation_warning
        )

    def __str__(self):

        return (
            f"{self.vehicle} - "
            f"Battery Health "
            f"{self.battery_health_percentage}%"
        )
   
  

class ChargingBooking(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
        ('no_show', 'No Show'),
    ]

    CHARGING_TYPE_CHOICES = [
        ('level1', 'Level 1'),
        ('level2', 'Level 2'),
        ('dcfc', 'DC Fast Charging'),
        ('ultra_fast', 'Ultra Fast Charging'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    # --------------------------------------------------------
    # RELATIONSHIPS
    # --------------------------------------------------------

    vehicle = models.ForeignKey(
        EVVehicle,
        on_delete=models.CASCADE,
        related_name='charging_bookings'
    )

    station = models.ForeignKey(
        ChargingStation,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    # --------------------------------------------------------
    # BOOKING INFORMATION
    # --------------------------------------------------------

    booking_time = models.DateTimeField()

    expected_duration = models.IntegerField(
        default=30,
        help_text='Expected charging duration in minutes'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    charging_type = models.CharField(
        max_length=20,
        choices=CHARGING_TYPE_CHOICES,
        default='level2'
    )

    # --------------------------------------------------------
    # CHARGING SLOT
    # --------------------------------------------------------

    charger_number = models.IntegerField(
        null=True,
        blank=True
    )

    slot_number = models.CharField(
        max_length=30,
        blank=True
    )

    connector_type = models.CharField(
        max_length=50,
        blank=True,
        help_text='CCS2, CHAdeMO, Type 2, GB/T etc.'
    )

    charging_power_kw = models.FloatField(
        default=0.0
    )

    # --------------------------------------------------------
    # BATTERY INFORMATION
    # --------------------------------------------------------

    battery_before_charge = models.FloatField(
        default=0.0,
        help_text='Battery percentage before charging'
    )

    target_battery_percentage = models.FloatField(
        default=80.0
    )

    battery_after_charge = models.FloatField(
        null=True,
        blank=True
    )

    energy_required_kwh = models.FloatField(
        default=0.0
    )

    energy_delivered_kwh = models.FloatField(
        default=0.0
    )

    # --------------------------------------------------------
    # COST
    # --------------------------------------------------------

    price_per_kwh = models.FloatField(
        default=12.0
    )

    estimated_cost = models.FloatField(
        default=0.0
    )

    actual_cost = models.FloatField(
        null=True,
        blank=True
    )

    booking_fee = models.FloatField(
        default=0.0
    )

    tax_amount = models.FloatField(
        default=0.0
    )

    discount_amount = models.FloatField(
        default=0.0
    )

    final_amount = models.FloatField(
        default=0.0
    )

    # --------------------------------------------------------
    # INDIA PAYMENT SUPPORT
    # --------------------------------------------------------

    payment_method = models.CharField(
        max_length=30,
        choices=[
            ('upi', 'UPI'),
            ('card', 'Credit/Debit Card'),
            ('wallet', 'Wallet'),
            ('netbanking', 'Net Banking'),
            ('cash', 'Cash'),
            ('fastag', 'FASTag'),
        ],
        default='upi'
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )

    transaction_id = models.CharField(
        max_length=150,
        blank=True
    )

    # --------------------------------------------------------
    # QUEUE / WAITING
    # --------------------------------------------------------

    queue_position = models.IntegerField(
        null=True,
        blank=True
    )

    estimated_wait_time = models.IntegerField(
        default=0,
        help_text='Estimated waiting time in minutes'
    )

    # --------------------------------------------------------
    # BOOKING TIME TRACKING
    # --------------------------------------------------------

    check_in_time = models.DateTimeField(
        null=True,
        blank=True
    )

    charging_started_at = models.DateTimeField(
        null=True,
        blank=True
    )

    charging_completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    cancelled_at = models.DateTimeField(
        null=True,
        blank=True
    )

    # --------------------------------------------------------
    # SMART BOOKING
    # --------------------------------------------------------

    auto_booking = models.BooleanField(
        default=False
    )

    smart_charging_enabled = models.BooleanField(
        default=False
    )

    off_peak_charging = models.BooleanField(
        default=False
    )

    renewable_energy_preferred = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # AI FEATURES
    # --------------------------------------------------------

    ai_recommended = models.BooleanField(
        default=False
    )

    ai_recommendation_reason = models.TextField(
        blank=True
    )

    predicted_wait_time = models.IntegerField(
        null=True,
        blank=True
    )

    predicted_charging_duration = models.IntegerField(
        null=True,
        blank=True
    )

    predicted_cost = models.FloatField(
        null=True,
        blank=True
    )

    # --------------------------------------------------------
    # RATING / FEEDBACK
    # --------------------------------------------------------

    rating = models.IntegerField(
        choices=[
            (1, '1 Star'),
            (2, '2 Stars'),
            (3, '3 Stars'),
            (4, '4 Stars'),
            (5, '5 Stars'),
        ],
        null=True,
        blank=True
    )

    feedback = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # CANCELLATION
    # --------------------------------------------------------

    cancellation_reason = models.TextField(
        blank=True
    )

    cancellation_fee = models.FloatField(
        default=0.0
    )

    # --------------------------------------------------------
    # NOTIFICATIONS
    # --------------------------------------------------------

    reminder_sent = models.BooleanField(
        default=False
    )

    completion_notification_sent = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # TIMESTAMPS
    # --------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ['-booking_time']

        indexes = [
            models.Index(
                fields=['station', 'booking_time']
            ),
            models.Index(
                fields=['vehicle', '-booking_time']
            ),
            models.Index(
                fields=['status']
            ),
            models.Index(
                fields=['payment_status']
            ),
        ]

    # --------------------------------------------------------
    # FUNCTIONS
    # --------------------------------------------------------

    def calculate_estimated_cost(self):

        energy = self.energy_required_kwh or 0
        rate = self.price_per_kwh or 0

        cost = energy * rate

        cost += self.booking_fee
        cost += self.tax_amount
        cost -= self.discount_amount

        return round(
            max(cost, 0),
            2
        )

    def calculate_final_amount(self):

        base = (
            self.actual_cost
            if self.actual_cost is not None
            else self.estimated_cost
        )

        amount = (
            base
            + self.booking_fee
            + self.tax_amount
            - self.discount_amount
        )

        return round(
            max(amount, 0),
            2
        )

    def is_active(self):

        return self.status in [
            'pending',
            'confirmed',
            'in_progress',
        ]

    def is_completed(self):

        return self.status == 'completed'

    def __str__(self):

        return (
            f"{self.vehicle} - "
            f"{self.station} - "
            f"{self.booking_time}"
        )
    # ============================================================
# NOTIFICATION
# ============================================================

class Notification(models.Model):

    NOTIFICATION_TYPES = [
        ('battery_low', 'Battery Low'),
        ('charging_complete', 'Charging Complete'),
        ('booking_confirmed', 'Booking Confirmed'),
        ('booking_reminder', 'Booking Reminder'),
        ('charger_unavailable', 'Charger Unavailable'),
        ('traffic_alert', 'Traffic Alert'),
        ('weather_warning', 'Weather Warning'),
        ('maintenance_reminder', 'Maintenance Reminder'),
        ('payment_success', 'Payment Success'),
        ('payment_failed', 'Payment Failed'),
        ('route_update', 'Route Update'),
        ('emergency', 'Emergency'),
        ('system', 'System'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    vehicle = models.ForeignKey(
        'EVVehicle',
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True,
        blank=True
    )

    notification_type = models.CharField(
        max_length=30,
        choices=NOTIFICATION_TYPES,
        default='system'
    )

    title = models.CharField(max_length=200)

    message = models.TextField()

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium'
    )

    is_read = models.BooleanField(default=False)

    action_url = models.CharField(
        max_length=500,
        blank=True
    )

    sent_email = models.BooleanField(default=False)
    sent_sms = models.BooleanField(default=False)
    sent_push = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    read_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['is_read']),
            models.Index(fields=['notification_type']),
        ]

    def __str__(self):
        return f"{self.title} - {self.user}"
    # ============================================================
# PAYMENT
# ============================================================

class Payment(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ('upi', 'UPI'),
        ('card', 'Credit/Debit Card'),
        ('wallet', 'Wallet'),
        ('netbanking', 'Net Banking'),
        ('cash', 'Cash'),
        ('fastag', 'FASTag'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ev_payments'
    )

    charging_session = models.ForeignKey(
        'ChargingLog',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments'
    )

    charging_booking = models.ForeignKey(
        'ChargingBooking',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments'
    )

    amount = models.FloatField(default=0.0)

    tax_amount = models.FloatField(default=0.0)

    discount_amount = models.FloatField(default=0.0)

    final_amount = models.FloatField(default=0.0)

    currency = models.CharField(
        max_length=10,
        default='INR'
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='upi'
    )

    transaction_id = models.CharField(
        max_length=150,
        unique=True
    )

    gateway_transaction_id = models.CharField(
        max_length=200,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    upi_id = models.CharField(
        max_length=100,
        blank=True
    )

    payment_gateway = models.CharField(
        max_length=100,
        blank=True
    )

    failure_reason = models.TextField(
        blank=True
    )

    refund_amount = models.FloatField(
        default=0.0
    )

    refund_transaction_id = models.CharField(
        max_length=150,
        blank=True
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )

    refunded_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['transaction_id']),
            models.Index(fields=['status']),
            models.Index(fields=['payment_method']),
            models.Index(fields=['user', '-created_at']),
        ]

    def calculate_final_amount(self):
        amount = (
            self.amount
            + self.tax_amount
            - self.discount_amount
        )
        return round(max(amount, 0), 2)

    def __str__(self):
        return (
            f"{self.transaction_id} - "
            f"₹{self.final_amount} - "
            f"{self.status}"
        )
    # ============================================================
# USER PROFILE
# ============================================================

class UserProfile(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ('upi', 'UPI'),
        ('card', 'Card'),
        ('wallet', 'Wallet'),
        ('netbanking', 'Net Banking'),
    ]

    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('hi', 'हिंदी'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ev_profile'
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    profile_picture = models.ImageField(
        upload_to='profiles/',
        null=True,
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    district = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    pincode = models.CharField(
        max_length=10,
        blank=True
    )

    language = models.CharField(
        max_length=10,
        choices=LANGUAGE_CHOICES,
        default='en'
    )

    # Driving statistics
    total_trips = models.IntegerField(default=0)
    total_distance = models.FloatField(default=0.0)
    total_energy_consumed = models.FloatField(default=0.0)
    total_charging_sessions = models.IntegerField(default=0)

    # Environmental statistics
    co2_saved = models.FloatField(default=0.0)
    green_kilometres = models.FloatField(default=0.0)

    # Wallet
    wallet_balance = models.FloatField(default=0.0)

    preferred_payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='wallet'
    )

    # Saved EVs
    saved_vehicles = models.ManyToManyField(
        'EVVehicle',
        blank=True,
        related_name='saved_by_users'
    )

    # Favourite charging stations
    favorite_stations = models.ManyToManyField(
        'ChargingStation',
        blank=True,
        related_name='favorite_of_users'
    )

    # Preferences
    notifications_enabled = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    push_notifications = models.BooleanField(default=True)

    weather_alerts = models.BooleanField(default=True)
    traffic_alerts = models.BooleanField(default=True)
    charging_alerts = models.BooleanField(default=True)
    maintenance_alerts = models.BooleanField(default=True)

    # Smart EV preferences
    smart_route_enabled = models.BooleanField(default=True)
    eco_route_preferred = models.BooleanField(default=False)
    avoid_tolls = models.BooleanField(default=False)
    renewable_charging_preferred = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - EV Profile"
    # ============================================================
# VEHICLE HEALTH
# ============================================================

class VehicleHealth(models.Model):

    HEALTH_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('critical', 'Critical'),
    ]

    vehicle = models.OneToOneField(
        'EVVehicle',
        on_delete=models.CASCADE,
        related_name='health'
    )

    # Overall vehicle health
    overall_health = models.CharField(
        max_length=20,
        choices=HEALTH_CHOICES,
        default='excellent'
    )

    health_score = models.FloatField(
        default=100.0
    )

    # Vehicle usage
    mileage = models.FloatField(
        default=0.0
    )

    total_driving_hours = models.FloatField(
        default=0.0
    )

    # Service information
    last_service_date = models.DateField(
        null=True,
        blank=True
    )

    next_service_date = models.DateField(
        null=True,
        blank=True
    )

    service_interval_km = models.IntegerField(
        default=10000
    )

    maintenance_records = models.TextField(
        blank=True
    )

    # Tyre health
    tire_health = models.IntegerField(
        default=100
    )

    tire_pressure_front = models.FloatField(
        null=True,
        blank=True
    )

    tire_pressure_rear = models.FloatField(
        null=True,
        blank=True
    )

    # Brake health
    brake_health = models.IntegerField(
        default=100
    )

    brake_pad_health = models.IntegerField(
        default=100
    )

    # Motor health
    motor_health = models.IntegerField(
        default=100
    )

    motor_temperature = models.FloatField(
        default=25.0
    )

    # Battery related health
    battery_cooling_health = models.IntegerField(
        default=100
    )

    battery_temperature = models.FloatField(
        default=25.0
    )

    # Electrical system
    electrical_system_health = models.IntegerField(
        default=100
    )

    charging_port_health = models.IntegerField(
        default=100
    )

    # Suspension
    suspension_health = models.IntegerField(
        default=100
    )

    # Cooling
    cooling_system_health = models.IntegerField(
        default=100
    )

    # Software
    software_version = models.CharField(
        max_length=50,
        blank=True
    )

    software_update_available = models.BooleanField(
        default=False
    )

    # Diagnostics
    diagnostic_code = models.CharField(
        max_length=100,
        blank=True
    )

    diagnostic_message = models.TextField(
        blank=True
    )

    warning_light_active = models.BooleanField(
        default=False
    )

    # Predictive maintenance
    maintenance_required = models.BooleanField(
        default=False
    )

    predicted_issue = models.CharField(
        max_length=200,
        blank=True
    )

    maintenance_priority = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('critical', 'Critical'),
        ],
        default='low'
    )

    estimated_maintenance_cost = models.FloatField(
        default=0.0
    )

    # Safety
    safe_to_drive = models.BooleanField(
        default=True
    )

    # Last inspection
    last_inspection_date = models.DateField(
        null=True,
        blank=True
    )

    # Timestamps
    last_updated = models.DateTimeField(
        auto_now=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-last_updated']

        indexes = [
            models.Index(fields=['overall_health']),
            models.Index(fields=['maintenance_required']),
            models.Index(fields=['safe_to_drive']),
        ]

    def __str__(self):
        return (
            f"{self.vehicle.vehicle_type} - "
            f"{self.overall_health}"
        )

    def calculate_health_score(self):
        """
        Calculate average health score from major vehicle components.
        """

        scores = [
            self.tire_health,
            self.brake_health,
            self.brake_pad_health,
            self.motor_health,
            self.battery_cooling_health,
            self.electrical_system_health,
            self.charging_port_health,
            self.suspension_health,
            self.cooling_system_health,
        ]

        if not scores:
            return 0

        return round(sum(scores) / len(scores), 2)

    def update_health_status(self):
        """
        Update overall health based on calculated health score.
        """

        score = self.calculate_health_score()

        self.health_score = score

        if score >= 90:
            self.overall_health = 'excellent'

        elif score >= 75:
            self.overall_health = 'good'

        elif score >= 60:
            self.overall_health = 'fair'

        elif score >= 40:
            self.overall_health = 'poor'

        else:
            self.overall_health = 'critical'

        self.safe_to_drive = score >= 40

        self.maintenance_required = score < 75

        self.save()
        # ============================================================
# VEHICLE INSURANCE
# ============================================================

class VehicleInsurance(models.Model):

    COVERAGE_CHOICES = [
        ('comprehensive', 'Comprehensive'),
        ('third_party', 'Third Party'),
        ('own_damage', 'Own Damage'),
        ('zero_depreciation', 'Zero Depreciation'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expiring_soon', 'Expiring Soon'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]

    vehicle = models.OneToOneField(
        'EVVehicle',
        on_delete=models.CASCADE,
        related_name='insurance'
    )

    provider = models.CharField(
        max_length=100
    )

    policy_number = models.CharField(
        max_length=50,
        unique=True
    )

    coverage_type = models.CharField(
        max_length=50,
        choices=COVERAGE_CHOICES,
        default='comprehensive'
    )

    valid_from = models.DateField()

    valid_until = models.DateField()

    premium_amount = models.FloatField(
        default=0.0
    )

    insured_value = models.FloatField(
        default=0.0
    )

    last_renewed = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    # India-specific insurance details
    insurer_contact = models.CharField(
        max_length=20,
        blank=True
    )

    insurer_email = models.EmailField(
        blank=True
    )

    policy_document_url = models.URLField(
        blank=True
    )

    # Claim information
    total_claims = models.IntegerField(
        default=0
    )

    last_claim_date = models.DateField(
        null=True,
        blank=True
    )

    last_claim_amount = models.FloatField(
        default=0.0
    )

    claim_in_progress = models.BooleanField(
        default=False
    )

    # Renewal reminder
    auto_renewal = models.BooleanField(
        default=False
    )

    renewal_reminder_enabled = models.BooleanField(
        default=True
    )

    reminder_days_before = models.IntegerField(
        default=30
    )

    # EV-specific coverage
    battery_covered = models.BooleanField(
        default=True
    )

    charger_covered = models.BooleanField(
        default=False
    )

    roadside_assistance = models.BooleanField(
        default=False
    )

    battery_replacement_covered = models.BooleanField(
        default=False
    )

    towing_covered = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['valid_until']

        indexes = [
            models.Index(fields=['policy_number']),
            models.Index(fields=['valid_until']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return (
            f"{self.vehicle.vehicle_type} - "
            f"{self.provider} - "
            f"{self.policy_number}"
        )

    @property
    def is_expired(self):
        from django.utils import timezone

        return self.valid_until < timezone.localdate()

    @property
    def days_until_expiry(self):
        from django.utils import timezone

        return (
            self.valid_until - timezone.localdate()
        ).days
# ============================================================
# CHARGING STATION QUEUE
# ============================================================

class ChargingStationQueue(models.Model):

    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('charging_next', 'Charging Next'),
        ('charging', 'Charging'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]

    PRIORITY_CHOICES = [
        ('normal', 'Normal'),
        ('priority', 'Priority'),
        ('emergency', 'Emergency'),
    ]

    station = models.ForeignKey(
        'ChargingStation',
        on_delete=models.CASCADE,
        related_name='queue'
    )

    vehicle = models.ForeignKey(
        'EVVehicle',
        on_delete=models.CASCADE,
        related_name='charging_queues'
    )

    # Queue position
    position = models.PositiveIntegerField(
        default=1
    )

    # Estimated waiting time in minutes
    estimated_wait_time = models.PositiveIntegerField(
        default=0
    )

    # Expected charging duration in minutes
    expected_charging_duration = models.PositiveIntegerField(
        default=30
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='waiting'
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='normal'
    )

    # Battery information when joining queue
    battery_percentage_on_join = models.FloatField(
        default=0.0
    )

    requested_charge_percentage = models.FloatField(
        default=80.0
    )

    # Estimated energy needed
    estimated_energy_required = models.FloatField(
        default=0.0
    )

    # Estimated charging cost
    estimated_cost = models.FloatField(
        default=0.0
    )

    # Queue intelligence
    people_ahead = models.PositiveIntegerField(
        default=0
    )

    ai_wait_time_prediction = models.FloatField(
        default=0.0
    )

    queue_congestion_level = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('moderate', 'Moderate'),
            ('high', 'High'),
            ('very_high', 'Very High'),
        ],
        default='low'
    )

    # Notifications
    notification_sent = models.BooleanField(
        default=False
    )

    ready_notification_sent = models.BooleanField(
        default=False
    )

    # Time fields
    joined_at = models.DateTimeField(
        auto_now_add=True
    )

    charging_started_at = models.DateTimeField(
        null=True,
        blank=True
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    cancelled_at = models.DateTimeField(
        null=True,
        blank=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['position', 'joined_at']

        indexes = [
            models.Index(
                fields=['station', 'status']
            ),
            models.Index(
                fields=['station', 'position']
            ),
            models.Index(
                fields=['vehicle', 'status']
            ),
        ]

    def __str__(self):
        return (
            f"{self.vehicle} - "
            f"{self.station} - "
            f"Position {self.position}"
        )

    def calculate_wait_time(self):
        """
        Basic estimated waiting time calculation.
        Assumes approximately 30 minutes per vehicle ahead.
        """

        average_session_minutes = 30

        self.estimated_wait_time = (
            self.people_ahead * average_session_minutes
        )

        return self.estimated_wait_time

    def calculate_congestion(self):
        """
        Determine queue congestion from the number
        of vehicles ahead.
        """

        if self.people_ahead <= 2:
            return 'low'

        elif self.people_ahead <= 5:
            return 'moderate'

        elif self.people_ahead <= 10:
            return 'high'

        return 'very_high'

    def save(self, *args, **kwargs):

        self.queue_congestion_level = (
            self.calculate_congestion()
        )

        super().save(*args, **kwargs)

# ============================================================
# CHARGING STATION REVIEW
# ============================================================

class StationReview(models.Model):

    RATING_CHOICES = [
        (1, '1 - Very Poor'),
        (2, '2 - Poor'),
        (3, '3 - Average'),
        (4, '4 - Good'),
        (5, '5 - Excellent'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='station_reviews'
    )

    station = models.ForeignKey(
        'ChargingStation',
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    # ========================================================
    # MAIN REVIEW
    # ========================================================

    rating = models.IntegerField(
        choices=RATING_CHOICES
    )

    title = models.CharField(
        max_length=200
    )

    comment = models.TextField()

    # ========================================================
    # DETAILED RATINGS
    # ========================================================

    cleanliness = models.IntegerField(
        choices=RATING_CHOICES,
        null=True,
        blank=True
    )

    availability = models.IntegerField(
        choices=RATING_CHOICES,
        null=True,
        blank=True
    )

    service_quality = models.IntegerField(
        choices=RATING_CHOICES,
        null=True,
        blank=True
    )

    charging_speed_rating = models.IntegerField(
        choices=RATING_CHOICES,
        null=True,
        blank=True
    )

    location_rating = models.IntegerField(
        choices=RATING_CHOICES,
        null=True,
        blank=True
    )

    safety_rating = models.IntegerField(
        choices=RATING_CHOICES,
        null=True,
        blank=True
    )

    value_for_money = models.IntegerField(
        choices=RATING_CHOICES,
        null=True,
        blank=True
    )

    # ========================================================
    # CHARGING EXPERIENCE
    # ========================================================

    charger_working = models.BooleanField(
        default=True
    )

    charger_available = models.BooleanField(
        default=True
    )

    waiting_time_minutes = models.PositiveIntegerField(
        default=0
    )

    charging_speed_kw = models.FloatField(
        default=0.0
    )

    # ========================================================
    # STATION FACILITIES
    # ========================================================

    restroom_available = models.BooleanField(
        default=False
    )

    restaurant_available = models.BooleanField(
        default=False
    )

    wifi_available = models.BooleanField(
        default=False
    )

    parking_available = models.BooleanField(
        default=True
    )

    wheelchair_accessible = models.BooleanField(
        default=False
    )

    # ========================================================
    # REVIEW VERIFICATION
    # ========================================================

    verified_visit = models.BooleanField(
        default=False
    )

    verified_charging_session = models.BooleanField(
        default=False
    )

    # ========================================================
    # COMMUNITY FEATURES
    # ========================================================

    helpful_count = models.PositiveIntegerField(
        default=0
    )

    report_count = models.PositiveIntegerField(
        default=0
    )

    is_reported = models.BooleanField(
        default=False
    )

    is_visible = models.BooleanField(
        default=True
    )

    # ========================================================
    # OWNER / ADMIN RESPONSE
    # ========================================================

    owner_response = models.TextField(
        blank=True
    )

    owner_responded_at = models.DateTimeField(
        null=True,
        blank=True
    )

    # ========================================================
    # TIMESTAMPS
    # ========================================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']

        indexes = [
            models.Index(
                fields=['station', '-created_at']
            ),
            models.Index(
                fields=['station', 'rating']
            ),
            models.Index(
                fields=['user', '-created_at']
            ),
        ]

        # One user should normally review a station once.
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'station'],
                name='unique_user_station_review'
            )
        ]

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.station.name} - "
            f"{self.rating}/5"
        )

    def detailed_average_rating(self):
        """
        Calculate average from available detailed ratings.
        """

        ratings = [
            self.cleanliness,
            self.availability,
            self.service_quality,
            self.charging_speed_rating,
            self.location_rating,
            self.safety_rating,
            self.value_for_money,
        ]

        ratings = [
            rating
            for rating in ratings
            if rating is not None
        ]

        if not ratings:
            return float(self.rating)

        return round(
            sum(ratings) / len(ratings),
            2
        )
    # ============================================================
# ECO SCORE / GREEN DRIVING REWARDS
# ============================================================

class EcoScore(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='eco_score'
    )

    # Points & score
    total_points = models.IntegerField(default=0)

    eco_driving_score = models.FloatField(
        default=100.0
    )

    green_miles = models.FloatField(
        default=0.0
    )

    co2_avoided = models.FloatField(
        default=0.0
    )

    # Driving behaviour
    smooth_acceleration_trips = models.IntegerField(
        default=0
    )

    efficient_routes_used = models.IntegerField(
        default=0
    )

    off_peak_charging_sessions = models.IntegerField(
        default=0
    )

    regenerative_braking_score = models.FloatField(
        default=100.0
    )

    energy_efficiency_score = models.FloatField(
        default=100.0
    )

    safe_driving_score = models.FloatField(
        default=100.0
    )

    # Environmental impact
    energy_saved_kwh = models.FloatField(
        default=0.0
    )

    renewable_energy_used_kwh = models.FloatField(
        default=0.0
    )

    trees_equivalent = models.FloatField(
        default=0.0
    )

    # Gamification
    level = models.IntegerField(
        default=1
    )

    badges_earned = models.TextField(
        blank=True
    )

    current_streak = models.IntegerField(
        default=0
    )

    longest_streak = models.IntegerField(
        default=0
    )

    # Rankings
    weekly_rank = models.IntegerField(
        null=True,
        blank=True
    )

    monthly_rank = models.IntegerField(
        null=True,
        blank=True
    )

    all_time_rank = models.IntegerField(
        null=True,
        blank=True
    )

    # Charging behaviour
    smart_charging_sessions = models.IntegerField(
        default=0
    )

    fast_charging_sessions = models.IntegerField(
        default=0
    )

    home_charging_sessions = models.IntegerField(
        default=0
    )

    renewable_charging_sessions = models.IntegerField(
        default=0
    )

    # Trip statistics
    total_eco_trips = models.IntegerField(
        default=0
    )

    eco_distance = models.FloatField(
        default=0.0
    )

    average_energy_consumption = models.FloatField(
        default=0.0
    )

    # Rewards
    reward_points_available = models.IntegerField(
        default=0
    )

    reward_points_redeemed = models.IntegerField(
        default=0
    )

    # Timestamps
    last_updated = models.DateTimeField(
        auto_now=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-total_points']

        indexes = [
            models.Index(fields=['-total_points']),
            models.Index(fields=['-eco_driving_score']),
            models.Index(fields=['weekly_rank']),
            models.Index(fields=['monthly_rank']),
        ]

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"Eco Score: {self.eco_driving_score:.1f}"
        )

    def calculate_level(self):
        """
        Calculate user eco level from total points.
        """

        if self.total_points >= 10000:
            return 10
        elif self.total_points >= 7500:
            return 9
        elif self.total_points >= 5000:
            return 8
        elif self.total_points >= 3500:
            return 7
        elif self.total_points >= 2500:
            return 6
        elif self.total_points >= 1500:
            return 5
        elif self.total_points >= 1000:
            return 4
        elif self.total_points >= 500:
            return 3
        elif self.total_points >= 200:
            return 2

        return 1

    def calculate_overall_score(self):
        """
        Calculate overall eco-driving score.
        """

        scores = [
            self.regenerative_braking_score,
            self.energy_efficiency_score,
            self.safe_driving_score,
        ]

        return round(sum(scores) / len(scores), 2)

    def add_points(self, points):
        """
        Add eco reward points.
        """

        if points <= 0:
            return

        self.total_points += points
        self.reward_points_available += points

        self.level = self.calculate_level()

        self.eco_driving_score = (
            self.calculate_overall_score()
        )

        self.save()

    def add_green_distance(self, distance_km):
        """
        Record eco-friendly distance.
        """

        if distance_km <= 0:
            return

        self.green_miles += distance_km
        self.eco_distance += distance_km

        self.save()

    def redeem_points(self, points):
        """
        Redeem available reward points.
        """

        if points <= 0:
            return False

        if points > self.reward_points_available:
            return False

        self.reward_points_available -= points
        self.reward_points_redeemed += points

        self.save()

        return True
    # ============================================================
# MULTI STOP ROUTE
# ============================================================

class MultiStopRoute(models.Model):

    ROUTE_TYPE_CHOICES = [
        ('eco', 'Eco-Friendly'),
        ('fastest', 'Fastest'),
        ('shortest', 'Shortest'),
        ('scenic', 'Scenic'),
        ('charging_optimized', 'Charging Optimized'),
        ('traffic_optimized', 'Traffic Optimized'),
    ]

    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='multi_stop_routes'
    )

    name = models.CharField(
        max_length=200
    )

    # Number of stops
    stops = models.PositiveIntegerField(
        default=0
    )

    # Store waypoint data as JSON/text
    waypoints = models.TextField()

    route_type = models.CharField(
        max_length=30,
        choices=ROUTE_TYPE_CHOICES,
        default='eco'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='planned'
    )

    # ========================================================
    # DISTANCE & TIME
    # ========================================================

    total_distance = models.FloatField(
        default=0.0,
        help_text='Total route distance in kilometres'
    )

    total_estimated_duration = models.PositiveIntegerField(
        default=0,
        help_text='Estimated duration in minutes'
    )

    # ========================================================
    # ENERGY INFORMATION
    # ========================================================

    estimated_energy = models.FloatField(
        default=0.0,
        help_text='Estimated energy consumption in kWh'
    )

    estimated_battery_usage = models.FloatField(
        default=0.0,
        help_text='Estimated battery usage percentage'
    )

    estimated_remaining_battery = models.FloatField(
        default=0.0
    )

    # ========================================================
    # CHARGING
    # ========================================================

    charging_stops_required = models.PositiveIntegerField(
        default=0
    )

    estimated_charging_time = models.PositiveIntegerField(
        default=0,
        help_text='Charging time in minutes'
    )

    estimated_charging_cost = models.FloatField(
        default=0.0
    )

    # ========================================================
    # TRAFFIC
    # ========================================================

    traffic_delay_minutes = models.PositiveIntegerField(
        default=0
    )

    congestion_level = models.CharField(
        max_length=20,
        choices=[
            ('clear', 'Clear'),
            ('moderate', 'Moderate'),
            ('heavy', 'Heavy'),
            ('severe', 'Severe'),
        ],
        default='clear'
    )

    # ========================================================
    # TOLL INFORMATION
    # ========================================================

    toll_cost = models.FloatField(
        default=0.0
    )

    toll_plazas = models.PositiveIntegerField(
        default=0
    )

    # ========================================================
    # WEATHER
    # ========================================================

    weather_risk = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('moderate', 'Moderate'),
            ('high', 'High'),
            ('critical', 'Critical'),
        ],
        default='low'
    )

    weather_warning = models.TextField(
        blank=True
    )

    # ========================================================
    # AI ROUTE INTELLIGENCE
    # ========================================================

    ai_optimized = models.BooleanField(
        default=False
    )

    ai_score = models.FloatField(
        default=0.0
    )

    ai_recommendation = models.TextField(
        blank=True
    )

    # ========================================================
    # ENVIRONMENTAL IMPACT
    # ========================================================

    estimated_co2_saved = models.FloatField(
        default=0.0
    )

    eco_score = models.FloatField(
        default=0.0
    )

    # ========================================================
    # START / END
    # ========================================================

    origin_name = models.CharField(
        max_length=200,
        blank=True
    )

    destination_name = models.CharField(
        max_length=200,
        blank=True
    )

    origin_latitude = models.FloatField(
        null=True,
        blank=True
    )

    origin_longitude = models.FloatField(
        null=True,
        blank=True
    )

    destination_latitude = models.FloatField(
        null=True,
        blank=True
    )

    destination_longitude = models.FloatField(
        null=True,
        blank=True
    )

    # ========================================================
    # TRIP TIME
    # ========================================================

    scheduled_start = models.DateTimeField(
        null=True,
        blank=True
    )

    actual_start = models.DateTimeField(
        null=True,
        blank=True
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    # ========================================================
    # TIMESTAMPS
    # ========================================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['route_type']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.name} - {self.route_type}"

    def calculate_total_cost(self):
        """
        Calculate charging + toll cost.
        """
        return round(
            self.estimated_charging_cost + self.toll_cost,
            2
        )

    def calculate_efficiency(self):
        """
        Energy consumption per kilometre.
        """

        if self.total_distance <= 0:
            return 0.0

        return round(
            self.estimated_energy / self.total_distance,
            3
        )
    # ============================================================
# VEHICLE LOCATION HISTORY
# ============================================================

class VehicleLocationHistory(models.Model):

    vehicle = models.ForeignKey(
        'EVVehicle',
        on_delete=models.CASCADE,
        related_name='location_history'
    )

    # ========================================================
    # LOCATION
    # ========================================================

    latitude = models.FloatField()
    longitude = models.FloatField()

    altitude = models.FloatField(
        null=True,
        blank=True
    )

    accuracy = models.FloatField(
        null=True,
        blank=True,
        help_text='GPS accuracy in meters'
    )

    # ========================================================
    # INDIA LOCATION INFORMATION
    # ========================================================

    city = models.CharField(
        max_length=100,
        blank=True
    )

    district = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    pincode = models.CharField(
        max_length=10,
        blank=True
    )

    road_name = models.CharField(
        max_length=200,
        blank=True
    )

    highway_name = models.CharField(
        max_length=200,
        blank=True
    )

    expressway_section = models.CharField(
        max_length=200,
        blank=True
    )

    # ========================================================
    # VEHICLE MOVEMENT
    # ========================================================

    speed = models.FloatField(
        default=0.0,
        help_text='Vehicle speed in km/h'
    )

    heading = models.FloatField(
        default=0.0,
        help_text='Direction in degrees'
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ('idle', 'Idle'),
            ('driving', 'Driving'),
            ('charging', 'Charging'),
            ('parked', 'Parked'),
            ('offline', 'Offline'),
        ],
        default='idle'
    )

    # ========================================================
    # BATTERY INFORMATION
    # ========================================================

    battery_percentage = models.FloatField(
        default=0.0
    )

    battery_temperature = models.FloatField(
        null=True,
        blank=True
    )

    estimated_range = models.FloatField(
        default=0.0,
        help_text='Estimated remaining range in km'
    )

    # ========================================================
    # TRIP INFORMATION
    # ========================================================

    distance_from_previous = models.FloatField(
        default=0.0,
        help_text='Distance from previous location in km'
    )

    total_trip_distance = models.FloatField(
        default=0.0
    )

    # ========================================================
    # TRAFFIC
    # ========================================================

    traffic_level = models.CharField(
        max_length=20,
        choices=[
            ('clear', 'Clear'),
            ('light', 'Light'),
            ('moderate', 'Moderate'),
            ('heavy', 'Heavy'),
            ('severe', 'Severe'),
        ],
        default='clear'
    )

    # ========================================================
    # ROAD CONDITIONS
    # ========================================================

    road_condition = models.CharField(
        max_length=30,
        choices=[
            ('good', 'Good'),
            ('average', 'Average'),
            ('poor', 'Poor'),
            ('wet', 'Wet'),
            ('waterlogged', 'Waterlogged'),
            ('construction', 'Construction'),
        ],
        default='good'
    )

    # ========================================================
    # GPS / TRACKING
    # ========================================================

    gps_signal_strength = models.CharField(
        max_length=20,
        choices=[
            ('excellent', 'Excellent'),
            ('good', 'Good'),
            ('weak', 'Weak'),
            ('lost', 'Lost'),
        ],
        default='good'
    )

    is_live = models.BooleanField(
        default=True
    )

    # ========================================================
    # SAFETY INFORMATION
    # ========================================================

    overspeeding = models.BooleanField(
        default=False
    )

    harsh_braking_detected = models.BooleanField(
        default=False
    )

    harsh_acceleration_detected = models.BooleanField(
        default=False
    )

    emergency_detected = models.BooleanField(
        default=False
    )

    # ========================================================
    # AI INTELLIGENCE
    # ========================================================

    ai_risk_score = models.FloatField(
        default=0.0
    )

    ai_recommendation = models.TextField(
        blank=True
    )

    # ========================================================
    # TIMESTAMP
    # ========================================================

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-timestamp']

        indexes = [
            models.Index(
                fields=['vehicle', '-timestamp']
            ),
            models.Index(
                fields=['latitude', 'longitude']
            ),
            models.Index(
                fields=['city', '-timestamp']
            ),
            models.Index(
                fields=['district', '-timestamp']
            ),
            models.Index(
                fields=['state', '-timestamp']
            ),
        ]

    def __str__(self):
        return (
            f"{self.vehicle} - "
            f"{self.latitude}, {self.longitude} - "
            f"{self.timestamp}"
        )
    # ============================================================
# AI RANGE PREDICTION
# ============================================================

class AIRangePrediction(models.Model):

    CONFIDENCE_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    vehicle = models.ForeignKey(
        'EVVehicle',
        on_delete=models.CASCADE,
        related_name='ai_range_predictions'
    )

    # Current vehicle state
    battery_percentage = models.FloatField(default=0.0)
    battery_health = models.FloatField(default=100.0)
    battery_temperature = models.FloatField(default=25.0)

    # AI predicted range
    predicted_range_km = models.FloatField(default=0.0)

    # Normal/basic range before environmental adjustments
    base_range_km = models.FloatField(default=0.0)

    # Energy consumption
    predicted_energy_consumption = models.FloatField(
        default=0.0,
        help_text='Predicted energy consumption in kWh'
    )

    consumption_per_km = models.FloatField(
        default=0.0,
        help_text='Predicted kWh consumed per kilometre'
    )

    # ========================================================
    # WEATHER IMPACT
    # ========================================================

    temperature = models.FloatField(
        null=True,
        blank=True
    )

    weather_condition = models.CharField(
        max_length=50,
        blank=True
    )

    weather_impact_percentage = models.FloatField(
        default=0.0
    )

    # ========================================================
    # TRAFFIC IMPACT
    # ========================================================

    traffic_level = models.CharField(
        max_length=20,
        choices=[
            ('clear', 'Clear'),
            ('light', 'Light'),
            ('moderate', 'Moderate'),
            ('heavy', 'Heavy'),
            ('severe', 'Severe'),
        ],
        default='clear'
    )

    traffic_impact_percentage = models.FloatField(
        default=0.0
    )

    # ========================================================
    # ROAD / ROUTE IMPACT
    # ========================================================

    road_condition = models.CharField(
        max_length=30,
        choices=[
            ('good', 'Good'),
            ('average', 'Average'),
            ('poor', 'Poor'),
            ('wet', 'Wet'),
            ('waterlogged', 'Waterlogged'),
        ],
        default='good'
    )

    road_impact_percentage = models.FloatField(
        default=0.0
    )

    elevation_impact_percentage = models.FloatField(
        default=0.0
    )

    # ========================================================
    # DRIVING BEHAVIOUR
    # ========================================================

    average_speed = models.FloatField(default=0.0)

    driving_style = models.CharField(
        max_length=20,
        choices=[
            ('eco', 'Eco'),
            ('normal', 'Normal'),
            ('aggressive', 'Aggressive'),
        ],
        default='normal'
    )

    driving_style_impact = models.FloatField(default=0.0)

    # ========================================================
    # AC / CLIMATE CONTROL
    # ========================================================

    ac_enabled = models.BooleanField(default=False)

    ac_impact_percentage = models.FloatField(default=0.0)

    # ========================================================
    # LOAD
    # ========================================================

    passenger_count = models.PositiveIntegerField(default=1)

    additional_load_kg = models.FloatField(default=0.0)

    load_impact_percentage = models.FloatField(default=0.0)

    # ========================================================
    # LOCATION
    # ========================================================

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    district = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    # ========================================================
    # DESTINATION
    # ========================================================

    destination_name = models.CharField(
        max_length=200,
        blank=True
    )

    destination_distance_km = models.FloatField(
        default=0.0
    )

    can_reach_destination = models.BooleanField(
        default=True
    )

    # ========================================================
    # CHARGING INTELLIGENCE
    # ========================================================

    charging_required = models.BooleanField(default=False)

    recommended_charging_stop = models.ForeignKey(
        'ChargingStation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='range_prediction_recommendations'
    )

    recommended_charge_percentage = models.FloatField(
        default=80.0
    )

    # ========================================================
    # AI INFORMATION
    # ========================================================

    confidence_score = models.FloatField(
        default=0.0
    )

    confidence_level = models.CharField(
        max_length=20,
        choices=CONFIDENCE_CHOICES,
        default='medium'
    )

    model_version = models.CharField(
        max_length=50,
        blank=True
    )

    ai_recommendation = models.TextField(
        blank=True
    )

    # ========================================================
    # SAFETY RANGE
    # ========================================================

    reserve_range_km = models.FloatField(
        default=20.0
    )

    safe_range_km = models.FloatField(
        default=0.0
    )

    range_anxiety_risk = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('moderate', 'Moderate'),
            ('high', 'High'),
            ('critical', 'Critical'),
        ],
        default='low'
    )

    # ========================================================
    # TIMESTAMPS
    # ========================================================

    predicted_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-predicted_at']

        indexes = [
            models.Index(
                fields=['vehicle', '-predicted_at']
            ),
            models.Index(
                fields=['city', '-predicted_at']
            ),
            models.Index(
                fields=['charging_required']
            ),
        ]

    def __str__(self):
        return (
            f"{self.vehicle} - "
            f"{self.predicted_range_km:.1f} km"
        )

    def calculate_safe_range(self):
        """
        Range available while keeping emergency reserve.
        """
        return round(
            max(
                self.predicted_range_km - self.reserve_range_km,
                0
            ),
            2
        )

    def check_destination_reachability(self):
        """
        Check whether the EV can safely reach destination.
        """
        safe_range = self.calculate_safe_range()

        return self.destination_distance_km <= safe_range

    def update_range_status(self):
        """
        Update charging requirement and range risk.
        """

        self.safe_range_km = self.calculate_safe_range()

        self.can_reach_destination = (
            self.check_destination_reachability()
        )

        if self.battery_percentage <= 10:
            self.range_anxiety_risk = 'critical'
            self.charging_required = True

        elif self.battery_percentage <= 20:
            self.range_anxiety_risk = 'high'
            self.charging_required = True

        elif self.battery_percentage <= 35:
            self.range_anxiety_risk = 'moderate'

        else:
            self.range_anxiety_risk = 'low'

        if not self.can_reach_destination:
            self.charging_required = True

        self.save()
        # ============================================================
# AI ROUTE RECOMMENDATION
# ============================================================

class AIRouteRecommendation(models.Model):

    ROUTE_TYPE_CHOICES = [
        ('fastest', 'Fastest Route'),
        ('shortest', 'Shortest Route'),
        ('eco', 'Eco-Friendly Route'),
        ('charging', 'Charging Optimized'),
        ('traffic', 'Traffic Optimized'),
        ('weather', 'Weather Optimized'),
        ('balanced', 'Balanced Route'),
    ]

    RISK_CHOICES = [
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    vehicle = models.ForeignKey(
        'EVVehicle',
        on_delete=models.CASCADE,
        related_name='ai_route_recommendations'
    )

    route = models.ForeignKey(
        'Route',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ai_recommendations'
    )

    # --------------------------------------------------------
    # ORIGIN
    # --------------------------------------------------------

    origin_name = models.CharField(
        max_length=200,
        blank=True
    )

    origin_latitude = models.FloatField(
        null=True,
        blank=True
    )

    origin_longitude = models.FloatField(
        null=True,
        blank=True
    )

    # --------------------------------------------------------
    # DESTINATION
    # --------------------------------------------------------

    destination_name = models.CharField(
        max_length=200,
        blank=True
    )

    destination_latitude = models.FloatField(
        null=True,
        blank=True
    )

    destination_longitude = models.FloatField(
        null=True,
        blank=True
    )

    # --------------------------------------------------------
    # ROUTE INFORMATION
    # --------------------------------------------------------

    route_type = models.CharField(
        max_length=30,
        choices=ROUTE_TYPE_CHOICES,
        default='balanced'
    )

    distance_km = models.FloatField(
        default=0.0
    )

    estimated_duration_minutes = models.PositiveIntegerField(
        default=0
    )

    # --------------------------------------------------------
    # BATTERY / ENERGY
    # --------------------------------------------------------

    starting_battery_percentage = models.FloatField(
        default=100.0
    )

    estimated_battery_usage = models.FloatField(
        default=0.0
    )

    estimated_battery_at_destination = models.FloatField(
        default=0.0
    )

    estimated_energy_kwh = models.FloatField(
        default=0.0
    )

    energy_efficiency = models.FloatField(
        default=0.0
    )

    # --------------------------------------------------------
    # CHARGING INTELLIGENCE
    # --------------------------------------------------------

    charging_required = models.BooleanField(
        default=False
    )

    charging_stops = models.PositiveIntegerField(
        default=0
    )

    recommended_station = models.ForeignKey(
        'ChargingStation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ai_route_recommendations'
    )

    estimated_charging_time = models.PositiveIntegerField(
        default=0
    )

    estimated_charging_cost = models.FloatField(
        default=0.0
    )

    # --------------------------------------------------------
    # TRAFFIC
    # --------------------------------------------------------

    traffic_level = models.CharField(
        max_length=20,
        choices=[
            ('clear', 'Clear'),
            ('light', 'Light'),
            ('moderate', 'Moderate'),
            ('heavy', 'Heavy'),
            ('severe', 'Severe'),
        ],
        default='clear'
    )

    traffic_delay_minutes = models.PositiveIntegerField(
        default=0
    )

    traffic_score = models.FloatField(
        default=100.0
    )

    # --------------------------------------------------------
    # WEATHER
    # --------------------------------------------------------

    weather_condition = models.CharField(
        max_length=50,
        blank=True
    )

    weather_risk = models.CharField(
        max_length=20,
        choices=RISK_CHOICES,
        default='low'
    )

    weather_delay_minutes = models.PositiveIntegerField(
        default=0
    )

    weather_warning = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # INDIA-SPECIFIC ROAD INFORMATION
    # --------------------------------------------------------

    expressway_name = models.CharField(
        max_length=200,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    district = models.CharField(
        max_length=100,
        blank=True
    )

    toll_plazas = models.PositiveIntegerField(
        default=0
    )

    estimated_toll_cost = models.FloatField(
        default=0.0
    )

    # --------------------------------------------------------
    # AI SCORES
    # --------------------------------------------------------

    ai_score = models.FloatField(
        default=0.0
    )

    safety_score = models.FloatField(
        default=100.0
    )

    eco_score = models.FloatField(
        default=100.0
    )

    charging_score = models.FloatField(
        default=100.0
    )

    overall_route_score = models.FloatField(
        default=0.0
    )

    confidence_score = models.FloatField(
        default=0.0
    )

    # --------------------------------------------------------
    # AI RECOMMENDATION
    # --------------------------------------------------------

    recommendation = models.TextField(
        blank=True
    )

    reason = models.TextField(
        blank=True
    )

    alternative_route_available = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # ENVIRONMENT
    # --------------------------------------------------------

    estimated_co2_saved_kg = models.FloatField(
        default=0.0
    )

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    is_recommended = models.BooleanField(
        default=True
    )

    selected_by_user = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # TIMESTAMPS
    # --------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']

        indexes = [
            models.Index(
                fields=['vehicle', '-created_at']
            ),
            models.Index(
                fields=['route_type']
            ),
            models.Index(
                fields=['is_recommended']
            ),
        ]

    def __str__(self):
        return (
            f"{self.vehicle} - "
            f"{self.origin_name} → "
            f"{self.destination_name}"
        )

    def calculate_destination_battery(self):
        remaining = (
            self.starting_battery_percentage
            - self.estimated_battery_usage
        )

        return round(max(remaining, 0), 2)

    def calculate_total_cost(self):
        return round(
            self.estimated_charging_cost
            + self.estimated_toll_cost,
            2
        )

    def calculate_overall_score(self):
        scores = [
            self.safety_score,
            self.eco_score,
            self.charging_score,
            self.traffic_score,
        ]

        return round(
            sum(scores) / len(scores),
            2
        )

    def save(self, *args, **kwargs):
        self.estimated_battery_at_destination = (
            self.calculate_destination_battery()
        )

        self.overall_route_score = (
            self.calculate_overall_score()
        )

        super().save(*args, **kwargs)
        # ============================================================
# AI CHARGING PREDICTION
# ============================================================

class ChargingPrediction(models.Model):

    PREDICTION_TYPE_CHOICES = [
        ('charging_time', 'Charging Time'),
        ('charging_cost', 'Charging Cost'),
        ('station_demand', 'Station Demand'),
        ('queue_time', 'Queue Time'),
        ('best_time', 'Best Charging Time'),
        ('energy_required', 'Energy Required'),
    ]

    CONFIDENCE_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    DEMAND_CHOICES = [
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('high', 'High'),
        ('very_high', 'Very High'),
    ]

    # --------------------------------------------------------
    # VEHICLE
    # --------------------------------------------------------

    vehicle = models.ForeignKey(
        'EVVehicle',
        on_delete=models.CASCADE,
        related_name='charging_predictions'
    )

    # --------------------------------------------------------
    # CHARGING STATION
    # --------------------------------------------------------

    station = models.ForeignKey(
        'ChargingStation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='charging_predictions'
    )

    # --------------------------------------------------------
    # PREDICTION TYPE
    # --------------------------------------------------------

    prediction_type = models.CharField(
        max_length=30,
        choices=PREDICTION_TYPE_CHOICES,
        default='charging_time'
    )

    # --------------------------------------------------------
    # CURRENT BATTERY INFORMATION
    # --------------------------------------------------------

    current_battery_percentage = models.FloatField(
        default=0.0
    )

    target_battery_percentage = models.FloatField(
        default=80.0
    )

    battery_capacity_kwh = models.FloatField(
        default=0.0
    )

    battery_health_percentage = models.FloatField(
        default=100.0
    )

    battery_temperature = models.FloatField(
        null=True,
        blank=True
    )

    # --------------------------------------------------------
    # ENERGY PREDICTION
    # --------------------------------------------------------

    energy_required_kwh = models.FloatField(
        default=0.0
    )

    predicted_energy_delivered_kwh = models.FloatField(
        default=0.0
    )

    # --------------------------------------------------------
    # CHARGING TIME
    # --------------------------------------------------------

    predicted_charging_time_minutes = models.PositiveIntegerField(
        default=0
    )

    predicted_queue_time_minutes = models.PositiveIntegerField(
        default=0
    )

    total_expected_time_minutes = models.PositiveIntegerField(
        default=0
    )

    # --------------------------------------------------------
    # CHARGING COST
    # --------------------------------------------------------

    price_per_kwh = models.FloatField(
        default=0.0
    )

    predicted_cost = models.FloatField(
        default=0.0
    )

    estimated_savings = models.FloatField(
        default=0.0
    )

    # --------------------------------------------------------
    # CHARGER INFORMATION
    # --------------------------------------------------------

    charger_type = models.CharField(
        max_length=30,
        choices=[
            ('level1', 'Level 1'),
            ('level2', 'Level 2'),
            ('dcfc', 'DC Fast Charging'),
            ('fast', 'Fast Charging'),
            ('ultra_fast', 'Ultra Fast Charging'),
        ],
        default='dcfc'
    )

    charger_power_kw = models.FloatField(
        default=0.0
    )

    # --------------------------------------------------------
    # STATION DEMAND
    # --------------------------------------------------------

    predicted_station_demand = models.CharField(
        max_length=20,
        choices=DEMAND_CHOICES,
        default='moderate'
    )

    expected_vehicles = models.PositiveIntegerField(
        default=0
    )

    chargers_available_prediction = models.PositiveIntegerField(
        default=0
    )

    # --------------------------------------------------------
    # BEST CHARGING TIME
    # --------------------------------------------------------

    recommended_charging_time = models.DateTimeField(
        null=True,
        blank=True
    )

    off_peak_recommended = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # LOCATION
    # --------------------------------------------------------

    city = models.CharField(
        max_length=100,
        blank=True
    )

    district = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    # --------------------------------------------------------
    # TRAFFIC
    # --------------------------------------------------------

    traffic_level = models.CharField(
        max_length=20,
        choices=[
            ('clear', 'Clear'),
            ('light', 'Light'),
            ('moderate', 'Moderate'),
            ('heavy', 'Heavy'),
            ('severe', 'Severe'),
        ],
        default='clear'
    )

    traffic_delay_minutes = models.PositiveIntegerField(
        default=0
    )

    # --------------------------------------------------------
    # WEATHER
    # --------------------------------------------------------

    temperature = models.FloatField(
        null=True,
        blank=True
    )

    weather_condition = models.CharField(
        max_length=50,
        blank=True
    )

    weather_impact_percentage = models.FloatField(
        default=0.0
    )

    # --------------------------------------------------------
    # AI INFORMATION
    # --------------------------------------------------------

    confidence_score = models.FloatField(
        default=0.0
    )

    confidence_level = models.CharField(
        max_length=20,
        choices=CONFIDENCE_CHOICES,
        default='medium'
    )

    ai_model_name = models.CharField(
        max_length=100,
        blank=True
    )

    ai_model_version = models.CharField(
        max_length=50,
        blank=True
    )

    ai_recommendation = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # INDIA-SPECIFIC INTELLIGENCE
    # --------------------------------------------------------

    peak_hour = models.BooleanField(
        default=False
    )

    festival_traffic = models.BooleanField(
        default=False
    )

    monsoon_impact = models.BooleanField(
        default=False
    )

    power_grid_load = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('normal', 'Normal'),
            ('high', 'High'),
            ('critical', 'Critical'),
        ],
        default='normal'
    )

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    is_active = models.BooleanField(
        default=True
    )

    # --------------------------------------------------------
    # TIMESTAMPS
    # --------------------------------------------------------

    predicted_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-predicted_at']

        indexes = [
            models.Index(
                fields=['vehicle', '-predicted_at']
            ),
            models.Index(
                fields=['station', '-predicted_at']
            ),
            models.Index(
                fields=['prediction_type']
            ),
            models.Index(
                fields=['city', '-predicted_at']
            ),
        ]

    def __str__(self):
        station_name = (
            self.station.name
            if self.station
            else 'No Station'
        )

        return (
            f"{self.vehicle} - "
            f"{station_name} - "
            f"{self.prediction_type}"
        )

    # --------------------------------------------------------
    # ENERGY CALCULATION
    # --------------------------------------------------------

    def calculate_energy_required(self):
        """
        Calculate energy required to reach target battery level.
        """

        if self.battery_capacity_kwh <= 0:
            return 0.0

        difference = (
            self.target_battery_percentage
            - self.current_battery_percentage
        )

        if difference <= 0:
            return 0.0

        return round(
            self.battery_capacity_kwh
            * (difference / 100),
            2
        )

    # --------------------------------------------------------
    # COST CALCULATION
    # --------------------------------------------------------

    def calculate_predicted_cost(self):
        return round(
            self.energy_required_kwh
            * self.price_per_kwh,
            2
        )

    # --------------------------------------------------------
    # TOTAL TIME
    # --------------------------------------------------------

    def calculate_total_time(self):
        return (
            self.predicted_queue_time_minutes
            + self.predicted_charging_time_minutes
        )

    # --------------------------------------------------------
    # UPDATE CALCULATIONS
    # --------------------------------------------------------

    def update_prediction_values(self):

        self.energy_required_kwh = (
            self.calculate_energy_required()
        )

        self.predicted_cost = (
            self.calculate_predicted_cost()
        )

        self.total_expected_time_minutes = (
            self.calculate_total_time()
        )

    def save(self, *args, **kwargs):

        self.update_prediction_values()

        super().save(*args, **kwargs)
        # ============================================================
# ELECTRICITY PRICE
# India EV Charging Electricity Tariff Model
# ============================================================

class ElectricityPrice(models.Model):

    CHARGER_TYPE_CHOICES = [
        ('level1', 'Level 1'),
        ('level2', 'Level 2'),
        ('dcfc', 'DC Fast Charging'),
        ('fast', 'Fast Charging'),
        ('ultra_fast', 'Ultra Fast Charging'),
        ('home', 'Home Charging'),
    ]

    TARIFF_TYPE_CHOICES = [
        ('standard', 'Standard'),
        ('peak', 'Peak Hour'),
        ('off_peak', 'Off Peak'),
        ('night', 'Night Tariff'),
        ('solar', 'Solar / Renewable'),
        ('dynamic', 'Dynamic Pricing'),
    ]

    PROVIDER_TYPE_CHOICES = [
        ('tata_power', 'Tata Power'),
        ('chargezone', 'ChargeZone'),
        ('statiq', 'Statiq'),
        ('jio_bp', 'Jio-bp pulse'),
        ('ather_grid', 'Ather Grid'),
        ('zeon', 'Zeon Charging'),
        ('iocl', 'IOCL'),
        ('bpcl', 'BPCL'),
        ('hpcl', 'HPCL'),
        ('adani', 'Adani'),
        ('other', 'Other'),
    ]

    # --------------------------------------------------------
    # LOCATION
    # --------------------------------------------------------

    state = models.CharField(
        max_length=100
    )

    district = models.CharField(
        max_length=100,
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    pincode = models.CharField(
        max_length=10,
        blank=True
    )

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    # --------------------------------------------------------
    # PROVIDER
    # --------------------------------------------------------

    provider = models.CharField(
        max_length=50,
        choices=PROVIDER_TYPE_CHOICES,
        default='other'
    )

    provider_name = models.CharField(
        max_length=150,
        blank=True
    )

    # --------------------------------------------------------
    # CHARGING INFORMATION
    # --------------------------------------------------------

    charger_type = models.CharField(
        max_length=30,
        choices=CHARGER_TYPE_CHOICES,
        default='dcfc'
    )

    tariff_type = models.CharField(
        max_length=30,
        choices=TARIFF_TYPE_CHOICES,
        default='standard'
    )

    # ₹ per kWh
    price_per_kwh = models.FloatField(
        default=12.0
    )

    # Optional fixed/session fee
    session_fee = models.FloatField(
        default=0.0
    )

    # Parking charge
    parking_fee_per_hour = models.FloatField(
        default=0.0
    )

    # Tax percentage
    tax_percentage = models.FloatField(
        default=0.0
    )

    # --------------------------------------------------------
    # TIME-BASED PRICING
    # --------------------------------------------------------

    peak_price_per_kwh = models.FloatField(
        null=True,
        blank=True
    )

    off_peak_price_per_kwh = models.FloatField(
        null=True,
        blank=True
    )

    peak_start_time = models.TimeField(
        null=True,
        blank=True
    )

    peak_end_time = models.TimeField(
        null=True,
        blank=True
    )

    # --------------------------------------------------------
    # POWER INFORMATION
    # --------------------------------------------------------

    charger_power_kw = models.FloatField(
        default=0.0
    )

    grid_load = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('normal', 'Normal'),
            ('high', 'High'),
            ('critical', 'Critical'),
        ],
        default='normal'
    )

    # --------------------------------------------------------
    # RENEWABLE ENERGY
    # --------------------------------------------------------

    renewable_energy_available = models.BooleanField(
        default=False
    )

    renewable_percentage = models.FloatField(
        default=0.0
    )

    solar_charging_available = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # AI / DYNAMIC PRICE INFORMATION
    # --------------------------------------------------------

    dynamic_pricing_enabled = models.BooleanField(
        default=False
    )

    demand_multiplier = models.FloatField(
        default=1.0
    )

    predicted_price_per_kwh = models.FloatField(
        null=True,
        blank=True
    )

    ai_recommendation = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    is_active = models.BooleanField(
        default=True
    )

    effective_from = models.DateTimeField(
        null=True,
        blank=True
    )

    effective_until = models.DateTimeField(
        null=True,
        blank=True
    )

    # --------------------------------------------------------
    # TIMESTAMPS
    # --------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            'state',
            'city',
            'price_per_kwh'
        ]

        indexes = [
            models.Index(
                fields=['state', 'city']
            ),
            models.Index(
                fields=['provider']
            ),
            models.Index(
                fields=['charger_type']
            ),
            models.Index(
                fields=['price_per_kwh']
            ),
        ]

    def __str__(self):
        location = self.city or self.district or self.state

        return (
            f"{location} - "
            f"{self.provider_name or self.provider} - "
            f"₹{self.price_per_kwh}/kWh"
        )

    # --------------------------------------------------------
    # CALCULATE CHARGING COST
    # --------------------------------------------------------

    def calculate_charging_cost(self, energy_kwh):
        """
        Calculate estimated charging cost.
        """

        if energy_kwh <= 0:
            return 0.0

        energy_cost = energy_kwh * self.price_per_kwh

        subtotal = energy_cost + self.session_fee

        tax = subtotal * (
            self.tax_percentage / 100
        )

        return round(
            subtotal + tax,
            2
        )

    # --------------------------------------------------------
    # DYNAMIC PRICE
    # --------------------------------------------------------

    def calculate_dynamic_price(self):
        """
        Calculate electricity price based on demand.
        """

        if not self.dynamic_pricing_enabled:
            return self.price_per_kwh

        return round(
            self.price_per_kwh
            * self.demand_multiplier,
            2
        )
    # ============================================================
# CHARGING STATION FAULT REPORT
# ============================================================

class StationFaultReport(models.Model):

    FAULT_TYPE_CHOICES = [
        ('charger_not_working', 'Charger Not Working'),
        ('connector_damaged', 'Connector Damaged'),
        ('slow_charging', 'Slow Charging'),
        ('payment_issue', 'Payment Issue'),
        ('power_failure', 'Power Failure'),
        ('display_issue', 'Display Issue'),
        ('network_issue', 'Network Issue'),
        ('overheating', 'Overheating'),
        ('cable_damage', 'Charging Cable Damage'),
        ('emergency_stop', 'Emergency Stop Issue'),
        ('station_offline', 'Station Offline'),
        ('other', 'Other'),
    ]

    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    STATUS_CHOICES = [
        ('reported', 'Reported'),
        ('acknowledged', 'Acknowledged'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    ]

    # --------------------------------------------------------
    # CHARGING STATION
    # --------------------------------------------------------

    station = models.ForeignKey(
        'ChargingStation',
        on_delete=models.CASCADE,
        related_name='fault_reports'
    )

    # --------------------------------------------------------
    # USER WHO REPORTED THE FAULT
    # --------------------------------------------------------

    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='station_fault_reports'
    )

    # --------------------------------------------------------
    # FAULT DETAILS
    # --------------------------------------------------------

    fault_type = models.CharField(
        max_length=50,
        choices=FAULT_TYPE_CHOICES,
        default='other'
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        default='medium'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='reported'
    )

    # --------------------------------------------------------
    # CHARGER INFORMATION
    # --------------------------------------------------------

    charger_number = models.CharField(
        max_length=50,
        blank=True
    )

    charger_type = models.CharField(
        max_length=50,
        blank=True
    )

    connector_type = models.CharField(
        max_length=50,
        blank=True
    )

    # --------------------------------------------------------
    # LOCATION INFORMATION
    # --------------------------------------------------------

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    district = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    # --------------------------------------------------------
    # VEHICLE INFORMATION
    # --------------------------------------------------------

    vehicle = models.ForeignKey(
        'EVVehicle',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='station_fault_reports'
    )

    # --------------------------------------------------------
    # FAULT IMPACT
    # --------------------------------------------------------

    charger_usable = models.BooleanField(
        default=False
    )

    station_partially_available = models.BooleanField(
        default=True
    )

    safety_risk = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # ADMIN / MAINTENANCE
    # --------------------------------------------------------

    assigned_to = models.CharField(
        max_length=150,
        blank=True
    )

    technician_notes = models.TextField(
        blank=True
    )

    resolution_notes = models.TextField(
        blank=True
    )

    estimated_resolution_time = models.DateTimeField(
        null=True,
        blank=True
    )

    resolved_at = models.DateTimeField(
        null=True,
        blank=True
    )

    # --------------------------------------------------------
    # AI FAULT ANALYSIS
    # --------------------------------------------------------

    ai_detected = models.BooleanField(
        default=False
    )

    ai_fault_probability = models.FloatField(
        default=0.0
    )

    ai_recommendation = models.TextField(
        blank=True
    )

    predictive_maintenance_required = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # REPORT VERIFICATION
    # --------------------------------------------------------

    verified = models.BooleanField(
        default=False
    )

    duplicate_report = models.BooleanField(
        default=False
    )

    report_count = models.PositiveIntegerField(
        default=1
    )

    # --------------------------------------------------------
    # TIMESTAMPS
    # --------------------------------------------------------

    reported_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-reported_at']

        indexes = [
            models.Index(
                fields=['station', '-reported_at']
            ),
            models.Index(
                fields=['status']
            ),
            models.Index(
                fields=['severity']
            ),
            models.Index(
                fields=['fault_type']
            ),
        ]

    def __str__(self):
        return (
            f"{self.station} - "
            f"{self.fault_type} - "
            f"{self.status}"
        )

    def mark_resolved(self, notes=''):
        """
        Mark fault report as resolved.
        """
        from django.utils import timezone

        self.status = 'resolved'
        self.resolved_at = timezone.now()

        if notes:
            self.resolution_notes = notes

        self.save()

    @property
    def is_resolved(self):
        return self.status == 'resolved'

    @property
    def requires_immediate_attention(self):
        return (
            self.severity == 'critical'
            or self.safety_risk
        )
    # ============================================================
# EMERGENCY SOS
# ============================================================

class EmergencySOS(models.Model):

    EMERGENCY_TYPE_CHOICES = [
        ('accident', 'Accident'),
        ('vehicle_breakdown', 'Vehicle Breakdown'),
        ('battery_dead', 'Battery Dead'),
        ('battery_fire', 'Battery Fire'),
        ('overheating', 'Battery Overheating'),
        ('medical', 'Medical Emergency'),
        ('stranded', 'Vehicle Stranded'),
        ('charging_issue', 'Charging Emergency'),
        ('theft', 'Vehicle Theft'),
        ('unsafe_location', 'Unsafe Location'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('acknowledged', 'Acknowledged'),
        ('help_dispatched', 'Help Dispatched'),
        ('resolved', 'Resolved'),
        ('cancelled', 'Cancelled'),
    ]

    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    # ========================================================
    # USER / VEHICLE
    # ========================================================

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='emergency_sos_requests'
    )

    vehicle = models.ForeignKey(
        'EVVehicle',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='emergency_sos_requests'
    )

    # ========================================================
    # EMERGENCY DETAILS
    # ========================================================

    emergency_type = models.CharField(
        max_length=50,
        choices=EMERGENCY_TYPE_CHOICES,
        default='other'
    )

    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        default='high'
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='active'
    )

    message = models.TextField(
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    # ========================================================
    # LOCATION
    # ========================================================

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    district = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    pincode = models.CharField(
        max_length=10,
        blank=True
    )

    highway = models.CharField(
        max_length=200,
        blank=True
    )

    # ========================================================
    # VEHICLE STATE
    # ========================================================

    battery_percentage = models.FloatField(
        null=True,
        blank=True
    )

    vehicle_speed = models.FloatField(
        default=0.0
    )

    battery_temperature = models.FloatField(
        null=True,
        blank=True
    )

    # ========================================================
    # EMERGENCY CONTACT
    # ========================================================

    emergency_contact_name = models.CharField(
        max_length=150,
        blank=True
    )

    emergency_contact_phone = models.CharField(
        max_length=20,
        blank=True
    )

    emergency_contact_notified = models.BooleanField(
        default=False
    )

    # ========================================================
    # RESPONSE / ASSISTANCE
    # ========================================================

    police_notified = models.BooleanField(
        default=False
    )

    ambulance_notified = models.BooleanField(
        default=False
    )

    roadside_assistance_notified = models.BooleanField(
        default=False
    )

    fire_service_notified = models.BooleanField(
        default=False
    )

    help_dispatched = models.BooleanField(
        default=False
    )

    responder_name = models.CharField(
        max_length=150,
        blank=True
    )

    responder_phone = models.CharField(
        max_length=20,
        blank=True
    )

    estimated_arrival_minutes = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    # ========================================================
    # NEAREST CHARGING STATION
    # ========================================================

    nearest_station = models.ForeignKey(
        'ChargingStation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='emergency_sos_requests'
    )

    nearest_station_distance_km = models.FloatField(
        null=True,
        blank=True
    )

    # ========================================================
    # AI EMERGENCY ANALYSIS
    # ========================================================

    ai_detected = models.BooleanField(
        default=False
    )

    ai_risk_score = models.FloatField(
        default=0.0
    )

    ai_recommendation = models.TextField(
        blank=True
    )

    automatic_sos = models.BooleanField(
        default=False
    )

    # ========================================================
    # RESOLUTION
    # ========================================================

    resolution_notes = models.TextField(
        blank=True
    )

    acknowledged_at = models.DateTimeField(
        null=True,
        blank=True
    )

    help_dispatched_at = models.DateTimeField(
        null=True,
        blank=True
    )

    resolved_at = models.DateTimeField(
        null=True,
        blank=True
    )

    # ========================================================
    # TIMESTAMPS
    # ========================================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']

        indexes = [
            models.Index(
                fields=['status', '-created_at']
            ),
            models.Index(
                fields=['vehicle', '-created_at']
            ),
            models.Index(
                fields=['user', '-created_at']
            ),
            models.Index(
                fields=['emergency_type']
            ),
            models.Index(
                fields=['severity']
            ),
        ]

    def __str__(self):
        return (
            f"SOS #{self.pk} - "
            f"{self.emergency_type} - "
            f"{self.status}"
        )

    # ========================================================
    # ACKNOWLEDGE SOS
    # ========================================================

    def acknowledge(self):
        from django.utils import timezone

        self.status = 'acknowledged'
        self.acknowledged_at = timezone.now()

        self.save(
            update_fields=[
                'status',
                'acknowledged_at',
                'updated_at'
            ]
        )

    # ========================================================
    # DISPATCH HELP
    # ========================================================

    def dispatch_help(self):
        from django.utils import timezone

        self.status = 'help_dispatched'
        self.help_dispatched = True
        self.help_dispatched_at = timezone.now()

        self.save(
            update_fields=[
                'status',
                'help_dispatched',
                'help_dispatched_at',
                'updated_at'
            ]
        )

    # ========================================================
    # RESOLVE EMERGENCY
    # ========================================================

    def resolve(self, notes=''):
        from django.utils import timezone

        self.status = 'resolved'
        self.resolved_at = timezone.now()

        if notes:
            self.resolution_notes = notes

        self.save()

    # ========================================================
    # EMERGENCY STATE
    # ========================================================

    @property
    def is_active(self):
        return self.status in [
            'active',
            'acknowledged',
            'help_dispatched'
        ]

    @property
    def requires_immediate_attention(self):
        return (
            self.severity == 'critical'
            or self.emergency_type in [
                'accident',
                'battery_fire',
                'medical',
            ]
        )
    # ============================================================
# ROADSIDE ASSISTANCE
# ============================================================

class RoadsideAssistance(models.Model):

    SERVICE_TYPE_CHOICES = [
        ('towing', 'Vehicle Towing'),
        ('battery_support', 'Battery Support'),
        ('mobile_charging', 'Mobile EV Charging'),
        ('flat_tyre', 'Flat Tyre Assistance'),
        ('breakdown', 'Vehicle Breakdown'),
        ('accident', 'Accident Assistance'),
        ('battery_dead', 'Battery Dead'),
        ('battery_overheating', 'Battery Overheating'),
        ('electrical_fault', 'Electrical Fault'),
        ('lockout', 'Vehicle Lockout'),
        ('emergency', 'Emergency Assistance'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
        ('assigned', 'Assigned'),
        ('on_the_way', 'On The Way'),
        ('arrived', 'Arrived'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    # ========================================================
    # USER
    # ========================================================

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='roadside_assistance_requests'
    )

    # ========================================================
    # VEHICLE
    # ========================================================

    vehicle = models.ForeignKey(
        'EVVehicle',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='roadside_assistance_requests'
    )

    # ========================================================
    # OPTIONAL SOS CONNECTION
    # ========================================================

    emergency_sos = models.ForeignKey(
        'EmergencySOS',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='roadside_assistance_requests'
    )

    # ========================================================
    # SERVICE DETAILS
    # ========================================================

    service_type = models.CharField(
        max_length=50,
        choices=SERVICE_TYPE_CHOICES,
        default='breakdown'
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium'
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='requested'
    )

    description = models.TextField(
        blank=True
    )

    problem_description = models.TextField(
        blank=True
    )

    # ========================================================
    # LOCATION
    # ========================================================

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    district = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    pincode = models.CharField(
        max_length=10,
        blank=True
    )

    highway = models.CharField(
        max_length=200,
        blank=True
    )

    # ========================================================
    # SERVICE PROVIDER
    # ========================================================

    provider_name = models.CharField(
        max_length=150,
        blank=True
    )

    provider_phone = models.CharField(
        max_length=20,
        blank=True
    )

    technician_name = models.CharField(
        max_length=150,
        blank=True
    )

    technician_phone = models.CharField(
        max_length=20,
        blank=True
    )

    service_vehicle_number = models.CharField(
        max_length=50,
        blank=True
    )

    # ========================================================
    # DISTANCE / ETA
    # ========================================================

    provider_distance_km = models.FloatField(
        null=True,
        blank=True
    )

    estimated_arrival_minutes = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    actual_arrival_minutes = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    # ========================================================
    # EV INFORMATION
    # ========================================================

    battery_percentage = models.FloatField(
        null=True,
        blank=True
    )

    battery_temperature = models.FloatField(
        null=True,
        blank=True
    )

    mobile_charging_required = models.BooleanField(
        default=False
    )

    requested_energy_kwh = models.FloatField(
        default=0.0
    )

    # ========================================================
    # NEAREST CHARGING STATION
    # ========================================================

    nearest_station = models.ForeignKey(
        'ChargingStation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='roadside_assistance_requests'
    )

    nearest_station_distance_km = models.FloatField(
        null=True,
        blank=True
    )

    # ========================================================
    # TOWING
    # ========================================================

    towing_required = models.BooleanField(
        default=False
    )

    towing_destination = models.CharField(
        max_length=250,
        blank=True
    )

    towing_distance_km = models.FloatField(
        default=0.0
    )

    # ========================================================
    # PAYMENT
    # ========================================================

    estimated_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    final_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('paid', 'Paid'),
            ('failed', 'Failed'),
            ('refunded', 'Refunded'),
        ],
        default='pending'
    )

    # ========================================================
    # AI ASSISTANCE
    # ========================================================

    ai_detected_issue = models.CharField(
        max_length=200,
        blank=True
    )

    ai_risk_score = models.FloatField(
        default=0.0
    )

    ai_recommendation = models.TextField(
        blank=True
    )

    automatic_request = models.BooleanField(
        default=False
    )

    # ========================================================
    # RESOLUTION
    # ========================================================

    resolution_notes = models.TextField(
        blank=True
    )

    customer_rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )

    customer_feedback = models.TextField(
        blank=True
    )

    # ========================================================
    # TIMESTAMPS
    # ========================================================

    requested_at = models.DateTimeField(
        auto_now_add=True
    )

    assigned_at = models.DateTimeField(
        null=True,
        blank=True
    )

    arrived_at = models.DateTimeField(
        null=True,
        blank=True
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-requested_at']

        indexes = [
            models.Index(
                fields=['status', '-requested_at']
            ),
            models.Index(
                fields=['vehicle', '-requested_at']
            ),
            models.Index(
                fields=['user', '-requested_at']
            ),
            models.Index(
                fields=['service_type']
            ),
            models.Index(
                fields=['priority']
            ),
        ]

    def __str__(self):
        return (
            f"Roadside Assistance #{self.pk} - "
            f"{self.service_type} - "
            f"{self.status}"
        )

    def assign_provider(
        self,
        provider_name='',
        technician_name=''
    ):
        from django.utils import timezone

        self.status = 'assigned'
        self.provider_name = provider_name
        self.technician_name = technician_name
        self.assigned_at = timezone.now()

        self.save()

    def mark_arrived(self):
        from django.utils import timezone

        self.status = 'arrived'
        self.arrived_at = timezone.now()

        self.save()

    def mark_completed(self, notes=''):
        from django.utils import timezone

        self.status = 'completed'
        self.completed_at = timezone.now()

        if notes:
            self.resolution_notes = notes

        self.save()

    @property
    def is_active(self):
        return self.status not in [
            'completed',
            'cancelled'
        ]
    # ============================================================
# EV SERVICE CENTER
# ============================================================

class EVServiceCenter(models.Model):

    CENTER_TYPE_CHOICES = [
        ('authorized', 'Authorized Service Center'),
        ('independent', 'Independent EV Service Center'),
        ('battery', 'Battery Service Center'),
        ('tyre', 'Tyre Service Center'),
        ('roadside', 'Roadside Assistance Center'),
        ('multi_brand', 'Multi-Brand EV Service Center'),
    ]

    # Basic information
    name = models.CharField(
        max_length=200
    )

    center_type = models.CharField(
        max_length=30,
        choices=CENTER_TYPE_CHOICES,
        default='authorized'
    )

    brand = models.CharField(
        max_length=100,
        blank=True,
        help_text='Example: Tata, Mahindra, MG, Hyundai, BYD'
    )

    # Contact
    phone = models.CharField(
        max_length=20,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    website = models.URLField(
        blank=True
    )

    # Location
    address = models.TextField(
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    district = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    pincode = models.CharField(
        max_length=10,
        blank=True
    )

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    # Services
    battery_service = models.BooleanField(default=True)
    battery_replacement = models.BooleanField(default=False)
    general_service = models.BooleanField(default=True)
    tyre_service = models.BooleanField(default=True)
    software_diagnostics = models.BooleanField(default=True)
    motor_service = models.BooleanField(default=True)
    charging_system_service = models.BooleanField(default=True)
    roadside_assistance = models.BooleanField(default=False)
    towing_available = models.BooleanField(default=False)

    # Opening hours
    opening_time = models.TimeField(
        null=True,
        blank=True
    )

    closing_time = models.TimeField(
        null=True,
        blank=True
    )

    open_24_hours = models.BooleanField(
        default=False
    )

    # Appointment
    appointment_available = models.BooleanField(
        default=True
    )

    emergency_service_available = models.BooleanField(
        default=False
    )

    # Cost
    inspection_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    average_service_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # Rating
    rating = models.FloatField(
        default=0.0
    )

    total_reviews = models.PositiveIntegerField(
        default=0
    )

    # Capacity
    service_bays = models.PositiveIntegerField(
        default=1
    )

    available_bays = models.PositiveIntegerField(
        default=1
    )

    estimated_wait_minutes = models.PositiveIntegerField(
        default=0
    )

    # EV brands supported
    supported_brands = models.TextField(
        blank=True,
        help_text='Comma separated EV brands'
    )

    # AI recommendation
    ai_recommended = models.BooleanField(
        default=False
    )

    ai_score = models.FloatField(
        default=0.0
    )

    ai_recommendation = models.TextField(
        blank=True
    )

    # Status
    is_active = models.BooleanField(
        default=True
    )

    verified = models.BooleanField(
        default=False
    )

    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            '-rating',
            'name'
        ]

        indexes = [
            models.Index(
                fields=['city', 'state']
            ),
            models.Index(
                fields=['center_type']
            ),
            models.Index(
                fields=['brand']
            ),
            models.Index(
                fields=['is_active']
            ),
        ]

    def __str__(self):
        location = self.city or self.district or self.state

        return f"{self.name} - {location}"

    @property
    def has_capacity(self):
        return self.available_bays > 0

    @property
    def availability_status(self):

        if not self.is_active:
            return 'Closed'

        if self.available_bays <= 0:
            return 'Busy'

        return 'Available'
    # ============================================================
# EV SERVICE BOOKING
# ============================================================

class ServiceBooking(models.Model):

    SERVICE_TYPE_CHOICES = [
        ('general_service', 'General Service'),
        ('battery_check', 'Battery Health Check'),
        ('battery_repair', 'Battery Repair'),
        ('battery_replacement', 'Battery Replacement'),
        ('motor_service', 'Motor Service'),
        ('software_diagnostics', 'Software Diagnostics'),
        ('charging_system', 'Charging System Service'),
        ('brake_service', 'Brake Service'),
        ('tyre_service', 'Tyre Service'),
        ('ac_service', 'AC Service'),
        ('electrical', 'Electrical Repair'),
        ('accident_repair', 'Accident Repair'),
        ('inspection', 'Vehicle Inspection'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('vehicle_received', 'Vehicle Received'),
        ('inspection', 'Inspection'),
        ('in_progress', 'In Progress'),
        ('waiting_parts', 'Waiting for Parts'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    # --------------------------------------------------------
    # USER
    # --------------------------------------------------------

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='service_bookings'
    )

    # --------------------------------------------------------
    # VEHICLE
    # --------------------------------------------------------

    vehicle = models.ForeignKey(
        'EVVehicle',
        on_delete=models.CASCADE,
        related_name='service_bookings'
    )

    # --------------------------------------------------------
    # SERVICE CENTER
    # --------------------------------------------------------

    service_center = models.ForeignKey(
        'EVServiceCenter',
        on_delete=models.CASCADE,
        related_name='service_bookings'
    )

    # --------------------------------------------------------
    # SERVICE DETAILS
    # --------------------------------------------------------

    service_type = models.CharField(
        max_length=50,
        choices=SERVICE_TYPE_CHOICES,
        default='general_service'
    )

    problem_description = models.TextField(
        blank=True
    )

    customer_notes = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # BOOKING DATE / TIME
    # --------------------------------------------------------

    booking_date = models.DateField()

    booking_time = models.TimeField(
        null=True,
        blank=True
    )

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # --------------------------------------------------------
    # VEHICLE INFORMATION
    # --------------------------------------------------------

    current_mileage = models.PositiveIntegerField(
        default=0
    )

    battery_percentage = models.FloatField(
        null=True,
        blank=True
    )

    battery_health_percentage = models.FloatField(
        null=True,
        blank=True
    )

    # --------------------------------------------------------
    # PICKUP / DROP
    # --------------------------------------------------------

    pickup_required = models.BooleanField(
        default=False
    )

    pickup_address = models.TextField(
        blank=True
    )

    pickup_latitude = models.FloatField(
        null=True,
        blank=True
    )

    pickup_longitude = models.FloatField(
        null=True,
        blank=True
    )

    drop_required = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # COST
    # --------------------------------------------------------

    estimated_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    final_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # --------------------------------------------------------
    # PAYMENT
    # --------------------------------------------------------

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )

    payment_method = models.CharField(
        max_length=30,
        blank=True
    )

    transaction_id = models.CharField(
        max_length=150,
        blank=True
    )

    # --------------------------------------------------------
    # TECHNICIAN
    # --------------------------------------------------------

    technician_name = models.CharField(
        max_length=150,
        blank=True
    )

    technician_phone = models.CharField(
        max_length=20,
        blank=True
    )

    technician_notes = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # DIAGNOSTIC / SERVICE RESULT
    # --------------------------------------------------------

    diagnostic_report = models.TextField(
        blank=True
    )

    work_performed = models.TextField(
        blank=True
    )

    parts_replaced = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # AI MAINTENANCE
    # --------------------------------------------------------

    ai_recommended = models.BooleanField(
        default=False
    )

    ai_detected_issue = models.CharField(
        max_length=250,
        blank=True
    )

    ai_risk_score = models.FloatField(
        default=0.0
    )

    ai_recommendation = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # NEXT SERVICE
    # --------------------------------------------------------

    next_service_date = models.DateField(
        null=True,
        blank=True
    )

    next_service_mileage = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    # --------------------------------------------------------
    # CUSTOMER FEEDBACK
    # --------------------------------------------------------

    rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )

    feedback = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # CANCELLATION
    # --------------------------------------------------------

    cancellation_reason = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # TIMESTAMPS
    # --------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    cancelled_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-created_at']

        indexes = [
            models.Index(
                fields=['user', '-created_at']
            ),
            models.Index(
                fields=['vehicle', '-created_at']
            ),
            models.Index(
                fields=['service_center', 'booking_date']
            ),
            models.Index(
                fields=['status']
            ),
            models.Index(
                fields=['booking_date']
            ),
        ]

    def __str__(self):
        return (
            f"Service Booking #{self.pk} - "
            f"{self.vehicle} - "
            f"{self.service_type}"
        )

    # --------------------------------------------------------
    # CONFIRM BOOKING
    # --------------------------------------------------------

    def confirm_booking(self):
        self.status = 'confirmed'
        self.save()

    # --------------------------------------------------------
    # START SERVICE
    # --------------------------------------------------------

    def start_service(self):
        self.status = 'in_progress'
        self.save()

    # --------------------------------------------------------
    # COMPLETE SERVICE
    # --------------------------------------------------------

    def complete_service(self):
        from django.utils import timezone

        self.status = 'completed'
        self.completed_at = timezone.now()

        self.save()

    # --------------------------------------------------------
    # CANCEL BOOKING
    # --------------------------------------------------------

    def cancel_booking(self, reason=''):
        from django.utils import timezone

        self.status = 'cancelled'
        self.cancelled_at = timezone.now()

        if reason:
            self.cancellation_reason = reason

        self.save()

    @property
    def is_completed(self):
        return self.status == 'completed'

    @property
    def is_cancelled(self):
        return self.status == 'cancelled'
    # ============================================================
# VEHICLE DOCUMENT
# ============================================================

class VehicleDocument(models.Model):

    DOCUMENT_TYPE_CHOICES = [
        ('registration', 'Registration Certificate (RC)'),
        ('insurance', 'Vehicle Insurance'),
        ('puc', 'Pollution Certificate (PUC)'),
        ('driving_license', 'Driving License'),
        ('purchase_invoice', 'Purchase Invoice'),
        ('warranty', 'Vehicle Warranty'),
        ('battery_warranty', 'Battery Warranty'),
        ('service_record', 'Service Record'),
        ('road_tax', 'Road Tax Document'),
        ('fastag', 'FASTag Document'),
        ('fitness', 'Fitness Certificate'),
        ('permit', 'Vehicle Permit'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('valid', 'Valid'),
        ('expiring_soon', 'Expiring Soon'),
        ('expired', 'Expired'),
        ('pending', 'Pending Verification'),
        ('rejected', 'Rejected'),
    ]

    # --------------------------------------------------------
    # VEHICLE
    # --------------------------------------------------------

    vehicle = models.ForeignKey(
        'EVVehicle',
        on_delete=models.CASCADE,
        related_name='documents'
    )

    # --------------------------------------------------------
    # USER / OWNER
    # --------------------------------------------------------

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='vehicle_documents'
    )

    # --------------------------------------------------------
    # DOCUMENT INFORMATION
    # --------------------------------------------------------

    document_type = models.CharField(
        max_length=50,
        choices=DOCUMENT_TYPE_CHOICES
    )

    document_name = models.CharField(
        max_length=200,
        blank=True
    )

    document_number = models.CharField(
        max_length=100,
        blank=True
    )

    # --------------------------------------------------------
    # DOCUMENT FILE
    # --------------------------------------------------------

    document_file = models.FileField(
        upload_to='vehicle_documents/',
        null=True,
        blank=True
    )

    # Optional image/scan
    document_image = models.ImageField(
        upload_to='vehicle_documents/images/',
        null=True,
        blank=True
    )

    # --------------------------------------------------------
    # ISSUING INFORMATION
    # --------------------------------------------------------

    issuing_authority = models.CharField(
        max_length=200,
        blank=True
    )

    issuing_state = models.CharField(
        max_length=100,
        blank=True
    )

    # --------------------------------------------------------
    # DATES
    # --------------------------------------------------------

    issue_date = models.DateField(
        null=True,
        blank=True
    )

    expiry_date = models.DateField(
        null=True,
        blank=True
    )

    # --------------------------------------------------------
    # DOCUMENT STATUS
    # --------------------------------------------------------

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='pending'
    )

    is_verified = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # EXPIRY ALERT
    # --------------------------------------------------------

    expiry_alert_enabled = models.BooleanField(
        default=True
    )

    alert_days_before = models.PositiveIntegerField(
        default=30
    )

    alert_sent = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # VERIFICATION
    # --------------------------------------------------------

    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_vehicle_documents'
    )

    verified_at = models.DateTimeField(
        null=True,
        blank=True
    )

    verification_notes = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # INDIA-SPECIFIC INFORMATION
    # --------------------------------------------------------

    registration_number = models.CharField(
        max_length=30,
        blank=True
    )

    rto_code = models.CharField(
        max_length=20,
        blank=True
    )

    # --------------------------------------------------------
    # AI DOCUMENT CHECK
    # --------------------------------------------------------

    ai_verified = models.BooleanField(
        default=False
    )

    ai_confidence_score = models.FloatField(
        default=0.0
    )

    ai_detected_document_number = models.CharField(
        max_length=100,
        blank=True
    )

    ai_warning = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # NOTES
    # --------------------------------------------------------

    notes = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # TIMESTAMPS
    # --------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']

        indexes = [
            models.Index(
                fields=['vehicle', 'document_type']
            ),
            models.Index(
                fields=['status']
            ),
            models.Index(
                fields=['expiry_date']
            ),
        ]

    def __str__(self):
        return (
            f"{self.vehicle} - "
            f"{self.get_document_type_display()}"
        )

    # --------------------------------------------------------
    # CHECK DOCUMENT EXPIRY
    # --------------------------------------------------------

    @property
    def is_expired(self):

        if not self.expiry_date:
            return False

        from django.utils import timezone

        return self.expiry_date < timezone.localdate()

    # --------------------------------------------------------
    # DAYS UNTIL EXPIRY
    # --------------------------------------------------------

    @property
    def days_until_expiry(self):

        if not self.expiry_date:
            return None

        from django.utils import timezone

        difference = (
            self.expiry_date -
            timezone.localdate()
        )

        return difference.days

    # --------------------------------------------------------
    # UPDATE DOCUMENT STATUS
    # --------------------------------------------------------

    def update_document_status(self):

        days = self.days_until_expiry

        if days is None:
            return

        if days < 0:
            self.status = 'expired'

        elif days <= self.alert_days_before:
            self.status = 'expiring_soon'

        else:
            self.status = 'valid'

        self.save(update_fields=['status'])

    # --------------------------------------------------------
    # VERIFY DOCUMENT
    # --------------------------------------------------------

    def verify_document(self, user=None):

        from django.utils import timezone

        self.is_verified = True
        self.status = 'valid'
        self.verified_by = user
        self.verified_at = timezone.now()

        self.save()

    # ============================================================
# TOLL PLAZA
# India Expressway / Highway Toll Management
# ============================================================

class TollPlaza(models.Model):

    TOLL_TYPE_CHOICES = [
        ('national_highway', 'National Highway'),
        ('expressway', 'Expressway'),
        ('state_highway', 'State Highway'),
        ('city_toll', 'City Toll'),
        ('bridge', 'Bridge Toll'),
        ('other', 'Other'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('fastag', 'FASTag'),
        ('cash', 'Cash'),
        ('upi', 'UPI'),
        ('card', 'Card'),
        ('mixed', 'Multiple Payment Methods'),
    ]

    TRAFFIC_CHOICES = [
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('high', 'High'),
        ('severe', 'Severe'),
    ]

    # --------------------------------------------------------
    # BASIC INFORMATION
    # --------------------------------------------------------

    name = models.CharField(
        max_length=200
    )

    toll_code = models.CharField(
        max_length=50,
        blank=True
    )

    toll_type = models.CharField(
        max_length=30,
        choices=TOLL_TYPE_CHOICES,
        default='national_highway'
    )

    # --------------------------------------------------------
    # ROAD / EXPRESSWAY
    # --------------------------------------------------------

    highway_name = models.CharField(
        max_length=200,
        blank=True
    )

    highway_number = models.CharField(
        max_length=50,
        blank=True
    )

    expressway_name = models.CharField(
        max_length=200,
        blank=True
    )

    # --------------------------------------------------------
    # LOCATION
    # --------------------------------------------------------

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    district = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    pincode = models.CharField(
        max_length=10,
        blank=True
    )

    # --------------------------------------------------------
    # TOLL CHARGES
    # --------------------------------------------------------

    car_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    light_commercial_vehicle_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    bus_truck_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    multi_axle_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # EV-specific toll
    ev_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    ev_discount_percentage = models.FloatField(
        default=0.0
    )

    # --------------------------------------------------------
    # FASTAG
    # --------------------------------------------------------

    fastag_available = models.BooleanField(
        default=True
    )

    fastag_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # --------------------------------------------------------
    # PAYMENT
    # --------------------------------------------------------

    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHOD_CHOICES,
        default='fastag'
    )

    upi_available = models.BooleanField(
        default=True
    )

    card_available = models.BooleanField(
        default=True
    )

    cash_available = models.BooleanField(
        default=True
    )

    # --------------------------------------------------------
    # LANES
    # --------------------------------------------------------

    total_lanes = models.PositiveIntegerField(
        default=1
    )

    fastag_lanes = models.PositiveIntegerField(
        default=1
    )

    operational_lanes = models.PositiveIntegerField(
        default=1
    )

    # --------------------------------------------------------
    # TRAFFIC / QUEUE
    # --------------------------------------------------------

    traffic_level = models.CharField(
        max_length=20,
        choices=TRAFFIC_CHOICES,
        default='low'
    )

    queue_length = models.PositiveIntegerField(
        default=0
    )

    estimated_wait_minutes = models.PositiveIntegerField(
        default=0
    )

    average_crossing_time_minutes = models.FloatField(
        default=1.0
    )

    # --------------------------------------------------------
    # AI TRAFFIC PREDICTION
    # --------------------------------------------------------

    predicted_traffic_level = models.CharField(
        max_length=20,
        choices=TRAFFIC_CHOICES,
        default='low'
    )

    predicted_wait_minutes = models.PositiveIntegerField(
        default=0
    )

    congestion_score = models.FloatField(
        default=0.0
    )

    ai_recommendation = models.TextField(
        blank=True
    )

    alternative_route_available = models.BooleanField(
        default=False
    )

    alternative_route = models.CharField(
        max_length=250,
        blank=True
    )

    # --------------------------------------------------------
    # EV FACILITIES
    # --------------------------------------------------------

    ev_charging_available = models.BooleanField(
        default=False
    )

    charging_station = models.ForeignKey(
        'ChargingStation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='nearby_toll_plazas'
    )

    # --------------------------------------------------------
    # FACILITIES
    # --------------------------------------------------------

    restroom_available = models.BooleanField(
        default=False
    )

    food_available = models.BooleanField(
        default=False
    )

    parking_available = models.BooleanField(
        default=False
    )

    emergency_service_available = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    is_active = models.BooleanField(
        default=True
    )

    is_24_hours = models.BooleanField(
        default=True
    )

    # --------------------------------------------------------
    # TIMESTAMPS
    # --------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            'state',
            'highway_name',
            'name'
        ]

        indexes = [
            models.Index(
                fields=['state', 'city']
            ),
            models.Index(
                fields=['highway_name']
            ),
            models.Index(
                fields=['expressway_name']
            ),
            models.Index(
                fields=['traffic_level']
            ),
            models.Index(
                fields=['is_active']
            ),
        ]

    def __str__(self):
        road = (
            self.expressway_name
            or self.highway_name
            or self.highway_number
            or 'Unknown Road'
        )

        return f"{self.name} - {road}"

    # --------------------------------------------------------
    # EV TOLL CALCULATION
    # --------------------------------------------------------

    def calculate_ev_toll(self):
        """
        Calculate toll price for an EV.
        """

        if self.ev_fee is not None:
            return self.ev_fee

        if self.ev_discount_percentage <= 0:
            return self.car_fee

        discount = (
            self.car_fee
            * self.ev_discount_percentage
            / 100
        )

        return self.car_fee - discount

    # --------------------------------------------------------
    # CONGESTION CHECK
    # --------------------------------------------------------

    @property
    def is_congested(self):
        return self.traffic_level in [
            'high',
            'severe'
        ]

    # --------------------------------------------------------
    # FASTAG STATUS
    # --------------------------------------------------------

    @property
    def has_fastag_lane(self):
        return (
            self.fastag_available
            and self.fastag_lanes > 0
        )
    # ============================================================
# TRIP EXPENSE
# ============================================================

class TripExpense(models.Model):

    EXPENSE_TYPE_CHOICES = [
        ('charging', 'EV Charging'),
        ('toll', 'Toll / FASTag'),
        ('parking', 'Parking'),
        ('service', 'Vehicle Service'),
        ('repair', 'Vehicle Repair'),
        ('food', 'Food'),
        ('accommodation', 'Accommodation'),
        ('roadside', 'Roadside Assistance'),
        ('other', 'Other'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('upi', 'UPI'),
        ('card', 'Debit/Credit Card'),
        ('fastag', 'FASTag'),
        ('wallet', 'Wallet'),
        ('net_banking', 'Net Banking'),
        ('other', 'Other'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    # User
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='trip_expenses'
    )

    # Vehicle
    vehicle = models.ForeignKey(
        'EVVehicle',
        on_delete=models.CASCADE,
        related_name='trip_expenses'
    )

    # Optional route
    route = models.ForeignKey(
        'Route',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='trip_expenses'
    )

    # Expense information
    expense_type = models.CharField(
        max_length=30,
        choices=EXPENSE_TYPE_CHOICES,
        default='other'
    )

    title = models.CharField(
        max_length=200,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    tax_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # Charging-specific information
    energy_consumed_kwh = models.FloatField(
        default=0.0
    )

    price_per_kwh = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    charging_station = models.ForeignKey(
        'ChargingStation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='trip_expenses'
    )

    # Toll-specific information
    toll_plaza = models.ForeignKey(
        'TollPlaza',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='trip_expenses'
    )

    # Trip details
    trip_name = models.CharField(
        max_length=200,
        blank=True
    )

    start_location = models.CharField(
        max_length=200,
        blank=True
    )

    destination = models.CharField(
        max_length=200,
        blank=True
    )

    distance_km = models.FloatField(
        default=0.0
    )

    # Location where expense occurred
    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    # Payment
    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHOD_CHOICES,
        default='upi'
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='paid'
    )

    transaction_id = models.CharField(
        max_length=150,
        blank=True
    )

    # Receipt
    receipt_number = models.CharField(
        max_length=100,
        blank=True
    )

    receipt_file = models.FileField(
        upload_to='trip_expenses/receipts/',
        null=True,
        blank=True
    )

    # AI cost analysis
    ai_predicted_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    ai_savings = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    ai_recommendation = models.TextField(
        blank=True
    )

    # Date / time
    expense_date = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['vehicle', '-created_at']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['expense_type']),
            models.Index(fields=['expense_date']),
        ]

    def __str__(self):
        return (
            f"{self.vehicle} - "
            f"{self.get_expense_type_display()} - "
            f"₹{self.amount}"
        )

    @property
    def total_amount(self):
        """
        Final expense after tax and discount.
        """
        return (
            self.amount
            + self.tax_amount
            - self.discount_amount
        )
    # ============================================================
# CARBON SAVING
# Tracks CO2 savings from EV usage
# ============================================================

class CarbonSaving(models.Model):

    CALCULATION_TYPE_CHOICES = [
        ('trip', 'Trip'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('charging', 'Charging Session'),
        ('lifetime', 'Lifetime'),
    ]

    # User
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='carbon_savings'
    )

    # Vehicle
    vehicle = models.ForeignKey(
        'EVVehicle',
        on_delete=models.CASCADE,
        related_name='carbon_savings'
    )

    # Optional route
    route = models.ForeignKey(
        'Route',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='carbon_savings'
    )

    calculation_type = models.CharField(
        max_length=30,
        choices=CALCULATION_TYPE_CHOICES,
        default='trip'
    )

    # --------------------------------------------------------
    # DISTANCE
    # --------------------------------------------------------

    distance_km = models.FloatField(
        default=0.0
    )

    # --------------------------------------------------------
    # EV ENERGY CONSUMPTION
    # --------------------------------------------------------

    energy_consumed_kwh = models.FloatField(
        default=0.0
    )

    efficiency_kwh_per_km = models.FloatField(
        default=0.0
    )

    # --------------------------------------------------------
    # CARBON CALCULATION
    # --------------------------------------------------------

    # Estimated emissions of comparable petrol/diesel vehicle
    conventional_vehicle_co2_kg = models.FloatField(
        default=0.0
    )

    # Estimated emissions caused by electricity generation
    ev_co2_kg = models.FloatField(
        default=0.0
    )

    # Final CO2 saving
    co2_saved_kg = models.FloatField(
        default=0.0
    )

    # --------------------------------------------------------
    # FUEL SAVINGS
    # --------------------------------------------------------

    fuel_saved_litres = models.FloatField(
        default=0.0
    )

    estimated_fuel_cost_saved = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # --------------------------------------------------------
    # ENVIRONMENTAL EQUIVALENTS
    # --------------------------------------------------------

    trees_equivalent = models.FloatField(
        default=0.0
    )

    petrol_vehicle_km_avoided = models.FloatField(
        default=0.0
    )

    # --------------------------------------------------------
    # RENEWABLE ENERGY
    # --------------------------------------------------------

    renewable_energy_used = models.BooleanField(
        default=False
    )

    renewable_energy_percentage = models.FloatField(
        default=0.0
    )

    solar_energy_kwh = models.FloatField(
        default=0.0
    )

    # --------------------------------------------------------
    # ECO INFORMATION
    # --------------------------------------------------------

    eco_score = models.FloatField(
        default=0.0
    )

    green_points = models.PositiveIntegerField(
        default=0
    )

    # --------------------------------------------------------
    # LOCATION
    # --------------------------------------------------------

    start_location = models.CharField(
        max_length=200,
        blank=True
    )

    destination = models.CharField(
        max_length=200,
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    # --------------------------------------------------------
    # AI ENVIRONMENTAL ANALYSIS
    # --------------------------------------------------------

    ai_predicted_saving_kg = models.FloatField(
        default=0.0
    )

    ai_recommendation = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # DATE / TIME
    # --------------------------------------------------------

    calculation_date = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']

        indexes = [
            models.Index(
                fields=['vehicle', '-created_at']
            ),
            models.Index(
                fields=['user', '-created_at']
            ),
            models.Index(
                fields=['calculation_type']
            ),
            models.Index(
                fields=['calculation_date']
            ),
        ]

    def __str__(self):
        return (
            f"{self.vehicle} - "
            f"{self.co2_saved_kg:.2f} kg CO2 saved"
        )

    # --------------------------------------------------------
    # CALCULATE CO2 SAVING
    # --------------------------------------------------------

    def calculate_co2_saving(self):
        """
        CO2 saved =
        conventional vehicle emissions - EV emissions
        """

        saving = (
            self.conventional_vehicle_co2_kg
            - self.ev_co2_kg
        )

        return round(
            max(saving, 0),
            2
        )

    # --------------------------------------------------------
    # TREE EQUIVALENT
    # --------------------------------------------------------

    def calculate_tree_equivalent(self):
        """
        Approximate environmental equivalent.
        """

        if self.co2_saved_kg <= 0:
            return 0.0

        # Approximate annual CO2 absorption per tree
        return round(
            self.co2_saved_kg / 21.0,
            3
        )

    # --------------------------------------------------------
    # GREEN POINTS
    # --------------------------------------------------------

    def calculate_green_points(self):
        """
        Example reward system:
        1 kg CO2 saved = 10 green points
        """

        return max(
            int(self.co2_saved_kg * 10),
            0
        )

    # --------------------------------------------------------
    # UPDATE CALCULATED VALUES
    # --------------------------------------------------------

    def save(self, *args, **kwargs):

        self.co2_saved_kg = (
            self.calculate_co2_saving()
        )

        self.trees_equivalent = (
            self.calculate_tree_equivalent()
        )

        self.green_points = (
            self.calculate_green_points()
        )

        super().save(*args, **kwargs)
    # ============================================================
# SAVED ROUTE
# ============================================================

class SavedRoute(models.Model):

    ROUTE_TYPE_CHOICES = [
        ('fastest', 'Fastest Route'),
        ('shortest', 'Shortest Route'),
        ('eco', 'Eco-Friendly Route'),
        ('charging', 'Charging Optimized'),
        ('traffic', 'Traffic Optimized'),
        ('balanced', 'Balanced Route'),
    ]

    # User who saved the route
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='saved_routes'
    )

    # Optional vehicle
    vehicle = models.ForeignKey(
        'EVVehicle',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='saved_routes'
    )

    # Optional existing route
    route = models.ForeignKey(
        'Route',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='saved_route_entries'
    )

    # Route name
    name = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    route_type = models.CharField(
        max_length=30,
        choices=ROUTE_TYPE_CHOICES,
        default='balanced'
    )

    # ========================================================
    # START LOCATION
    # ========================================================

    start_location = models.CharField(
        max_length=200
    )

    start_latitude = models.FloatField(
        null=True,
        blank=True
    )

    start_longitude = models.FloatField(
        null=True,
        blank=True
    )

    # ========================================================
    # DESTINATION
    # ========================================================

    destination = models.CharField(
        max_length=200
    )

    destination_latitude = models.FloatField(
        null=True,
        blank=True
    )

    destination_longitude = models.FloatField(
        null=True,
        blank=True
    )

    # ========================================================
    # ROUTE DETAILS
    # ========================================================

    distance_km = models.FloatField(
        default=0.0
    )

    estimated_duration_minutes = models.PositiveIntegerField(
        default=0
    )

    expressway_name = models.CharField(
        max_length=200,
        blank=True
    )

    highway_name = models.CharField(
        max_length=200,
        blank=True
    )

    # Store map/polyline data if needed
    route_data = models.JSONField(
        default=dict,
        blank=True
    )

    # ========================================================
    # BATTERY / ENERGY
    # ========================================================

    estimated_energy_kwh = models.FloatField(
        default=0.0
    )

    estimated_battery_usage = models.FloatField(
        default=0.0
    )

    minimum_battery_required = models.FloatField(
        default=0.0
    )

    # ========================================================
    # CHARGING
    # ========================================================

    charging_required = models.BooleanField(
        default=False
    )

    charging_stops = models.PositiveIntegerField(
        default=0
    )

    preferred_charging_station = models.ForeignKey(
        'ChargingStation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='preferred_saved_routes'
    )

    estimated_charging_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # ========================================================
    # TOLL
    # ========================================================

    toll_plazas_count = models.PositiveIntegerField(
        default=0
    )

    estimated_toll_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # ========================================================
    # TRAFFIC
    # ========================================================

    traffic_level = models.CharField(
        max_length=20,
        choices=[
            ('clear', 'Clear'),
            ('light', 'Light'),
            ('moderate', 'Moderate'),
            ('heavy', 'Heavy'),
            ('severe', 'Severe'),
        ],
        default='clear'
    )

    estimated_traffic_delay_minutes = models.PositiveIntegerField(
        default=0
    )

    # ========================================================
    # WEATHER
    # ========================================================

    weather_condition = models.CharField(
        max_length=50,
        blank=True
    )

    weather_warning = models.TextField(
        blank=True
    )

    # ========================================================
    # AI INFORMATION
    # ========================================================

    ai_recommended = models.BooleanField(
        default=False
    )

    ai_score = models.FloatField(
        default=0.0
    )

    ai_recommendation = models.TextField(
        blank=True
    )

    # ========================================================
    # ECO INFORMATION
    # ========================================================

    estimated_co2_saved_kg = models.FloatField(
        default=0.0
    )

    eco_score = models.FloatField(
        default=0.0
    )

    # ========================================================
    # USER OPTIONS
    # ========================================================

    is_favorite = models.BooleanField(
        default=False
    )

    use_count = models.PositiveIntegerField(
        default=0
    )

    last_used_at = models.DateTimeField(
        null=True,
        blank=True
    )

    # ========================================================
    # TIMESTAMPS
    # ========================================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            '-is_favorite',
            '-created_at'
        ]

        indexes = [
            models.Index(
                fields=['user', '-created_at']
            ),
            models.Index(
                fields=['user', 'is_favorite']
            ),
            models.Index(
                fields=['vehicle']
            ),
            models.Index(
                fields=['route_type']
            ),
        ]

    def __str__(self):
        return (
            f"{self.name}: "
            f"{self.start_location} → "
            f"{self.destination}"
        )

    @property
    def total_estimated_cost(self):
        """
        Charging cost + toll cost.
        """
        return (
            self.estimated_charging_cost
            + self.estimated_toll_cost
        )

    def mark_used(self):
        """
        Increase route usage counter.
        """
        from django.utils import timezone

        self.use_count += 1
        self.last_used_at = timezone.now()

        self.save(
            update_fields=[
                'use_count',
                'last_used_at',
                'updated_at'
            ]
        )

    def toggle_favorite(self):
        """
        Add/remove route from favorites.
        """
        self.is_favorite = not self.is_favorite

        self.save(
            update_fields=[
                'is_favorite',
                'updated_at'
            ]
        )

        return self.is_favorite
    # ============================================================
# EV PARKING STATION
# ============================================================

class EVParkingStation(models.Model):

    PARKING_TYPE_CHOICES = [
        ('public', 'Public Parking'),
        ('private', 'Private Parking'),
        ('mall', 'Shopping Mall'),
        ('office', 'Office Parking'),
        ('airport', 'Airport Parking'),
        ('railway', 'Railway Station Parking'),
        ('metro', 'Metro Station Parking'),
        ('hotel', 'Hotel Parking'),
        ('highway', 'Highway Parking'),
        ('smart', 'Smart EV Parking'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('limited', 'Limited Availability'),
        ('full', 'Full'),
        ('closed', 'Closed'),
        ('maintenance', 'Under Maintenance'),
    ]

    # --------------------------------------------------------
    # BASIC INFORMATION
    # --------------------------------------------------------

    name = models.CharField(
        max_length=200
    )

    parking_code = models.CharField(
        max_length=50,
        blank=True
    )

    parking_type = models.CharField(
        max_length=30,
        choices=PARKING_TYPE_CHOICES,
        default='public'
    )

    description = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # LOCATION
    # --------------------------------------------------------

    address = models.TextField(
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    district = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    pincode = models.CharField(
        max_length=10,
        blank=True
    )

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    # --------------------------------------------------------
    # PARKING CAPACITY
    # --------------------------------------------------------

    total_slots = models.PositiveIntegerField(
        default=0
    )

    available_slots = models.PositiveIntegerField(
        default=0
    )

    ev_slots = models.PositiveIntegerField(
        default=0
    )

    available_ev_slots = models.PositiveIntegerField(
        default=0
    )

    reserved_slots = models.PositiveIntegerField(
        default=0
    )

    # --------------------------------------------------------
    # CHARGING FACILITY
    # --------------------------------------------------------

    charging_available = models.BooleanField(
        default=False
    )

    total_chargers = models.PositiveIntegerField(
        default=0
    )

    available_chargers = models.PositiveIntegerField(
        default=0
    )

    fast_charging_available = models.BooleanField(
        default=False
    )

    charging_station = models.ForeignKey(
        'ChargingStation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='parking_stations'
    )

    # --------------------------------------------------------
    # PARKING PRICE
    # --------------------------------------------------------

    hourly_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    daily_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    ev_hourly_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    charging_price_per_kwh = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # --------------------------------------------------------
    # PAYMENT
    # --------------------------------------------------------

    cash_available = models.BooleanField(
        default=True
    )

    upi_available = models.BooleanField(
        default=True
    )

    card_available = models.BooleanField(
        default=True
    )

    fastag_payment_available = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # SMART PARKING
    # --------------------------------------------------------

    online_booking_available = models.BooleanField(
        default=True
    )

    qr_entry_available = models.BooleanField(
        default=False
    )

    automatic_number_plate_recognition = models.BooleanField(
        default=False
    )

    smart_sensor_enabled = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # FACILITIES
    # --------------------------------------------------------

    cctv_available = models.BooleanField(
        default=False
    )

    security_available = models.BooleanField(
        default=False
    )

    restroom_available = models.BooleanField(
        default=False
    )

    food_available = models.BooleanField(
        default=False
    )

    wheelchair_accessible = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # OPERATING INFORMATION
    # --------------------------------------------------------

    open_24_hours = models.BooleanField(
        default=True
    )

    opening_time = models.TimeField(
        null=True,
        blank=True
    )

    closing_time = models.TimeField(
        null=True,
        blank=True
    )

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='available'
    )

    is_active = models.BooleanField(
        default=True
    )

    verified = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # RATING
    # --------------------------------------------------------

    rating = models.FloatField(
        default=0.0
    )

    total_reviews = models.PositiveIntegerField(
        default=0
    )

    # --------------------------------------------------------
    # TRAFFIC / WAITING
    # --------------------------------------------------------

    estimated_wait_minutes = models.PositiveIntegerField(
        default=0
    )

    congestion_level = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('moderate', 'Moderate'),
            ('high', 'High'),
            ('full', 'Full'),
        ],
        default='low'
    )

    # --------------------------------------------------------
    # AI PARKING PREDICTION
    # --------------------------------------------------------

    predicted_available_slots = models.PositiveIntegerField(
        default=0
    )

    predicted_ev_slots = models.PositiveIntegerField(
        default=0
    )

    ai_demand_score = models.FloatField(
        default=0.0
    )

    ai_recommended = models.BooleanField(
        default=False
    )

    ai_recommendation = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # INDIA-SPECIFIC INFORMATION
    # --------------------------------------------------------

    near_highway = models.BooleanField(
        default=False
    )

    highway_name = models.CharField(
        max_length=200,
        blank=True
    )

    near_metro = models.BooleanField(
        default=False
    )

    metro_station_name = models.CharField(
        max_length=200,
        blank=True
    )

    # --------------------------------------------------------
    # CONTACT
    # --------------------------------------------------------

    contact_number = models.CharField(
        max_length=20,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    # --------------------------------------------------------
    # TIMESTAMPS
    # --------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            '-available_ev_slots',
            '-rating',
            'name'
        ]

        indexes = [
            models.Index(fields=['city', 'state']),
            models.Index(fields=['status']),
            models.Index(fields=['is_active']),
            models.Index(fields=['charging_available']),
        ]

    def __str__(self):
        location = self.city or self.district or self.state or 'Unknown'
        return f"{self.name} - {location}"

    # --------------------------------------------------------
    # EV SLOT AVAILABILITY
    # --------------------------------------------------------

    @property
    def has_ev_parking(self):
        return self.available_ev_slots > 0

    # --------------------------------------------------------
    # CHARGER AVAILABILITY
    # --------------------------------------------------------

    @property
    def has_available_charger(self):
        return (
            self.charging_available
            and self.available_chargers > 0
        )

    # --------------------------------------------------------
    # OCCUPANCY PERCENTAGE
    # --------------------------------------------------------

    @property
    def occupancy_percentage(self):

        if self.total_slots <= 0:
            return 0

        occupied = (
            self.total_slots -
            self.available_slots
        )

        return round(
            (occupied / self.total_slots) * 100,
            2
        )

    # --------------------------------------------------------
    # UPDATE STATUS
    # --------------------------------------------------------

    def update_parking_status(self):

        if not self.is_active:
            self.status = 'closed'

        elif self.available_slots <= 0:
            self.status = 'full'

        elif self.available_slots <= 5:
            self.status = 'limited'

        else:
            self.status = 'available'

        self.save(update_fields=['status'])
# ============================================================
# PREDICTIVE MAINTENANCE
# AI-Based EV Maintenance Prediction
# ============================================================

class PredictiveMaintenance(models.Model):

    COMPONENT_CHOICES = [
        ('battery', 'Battery'),
        ('motor', 'Electric Motor'),
        ('brakes', 'Braking System'),
        ('tyres', 'Tyres'),
        ('charging_port', 'Charging Port'),
        ('cooling_system', 'Cooling System'),
        ('suspension', 'Suspension'),
        ('electronics', 'Electronics'),
        ('software', 'Vehicle Software'),
        ('other', 'Other'),
    ]

    RISK_CHOICES = [
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    STATUS_CHOICES = [
        ('healthy', 'Healthy'),
        ('monitor', 'Monitor'),
        ('service_soon', 'Service Soon'),
        ('maintenance_required', 'Maintenance Required'),
        ('critical', 'Critical'),
        ('resolved', 'Resolved'),
    ]

    # Vehicle
    vehicle = models.ForeignKey(
        'EVVehicle',
        on_delete=models.CASCADE,
        related_name='predictive_maintenance'
    )

    # Component being monitored
    component = models.CharField(
        max_length=50,
        choices=COMPONENT_CHOICES,
        default='battery'
    )

    # Current vehicle information
    current_mileage = models.PositiveIntegerField(
        default=0
    )

    battery_percentage = models.FloatField(
        default=0.0
    )

    battery_health_percentage = models.FloatField(
        default=100.0
    )

    battery_temperature = models.FloatField(
        null=True,
        blank=True
    )

    motor_temperature = models.FloatField(
        null=True,
        blank=True
    )

    # AI prediction
    failure_probability = models.FloatField(
        default=0.0
    )

    risk_score = models.FloatField(
        default=0.0
    )

    risk_level = models.CharField(
        max_length=20,
        choices=RISK_CHOICES,
        default='low'
    )

    predicted_issue = models.CharField(
        max_length=250,
        blank=True
    )

    predicted_failure_date = models.DateField(
        null=True,
        blank=True
    )

    remaining_useful_life_days = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    # Maintenance recommendation
    maintenance_required = models.BooleanField(
        default=False
    )

    recommendation = models.TextField(
        blank=True
    )

    recommended_action = models.TextField(
        blank=True
    )

    recommended_service_date = models.DateField(
        null=True,
        blank=True
    )

    # Estimated cost in INR
    estimated_repair_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # Diagnostic information
    diagnostic_data = models.JSONField(
        default=dict,
        blank=True
    )

    ai_confidence = models.FloatField(
        default=0.0
    )

    # Status
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='healthy'
    )

    is_resolved = models.BooleanField(
        default=False
    )

    resolved_at = models.DateTimeField(
        null=True,
        blank=True
    )

    # Notes
    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['vehicle', '-created_at']),
            models.Index(fields=['component']),
            models.Index(fields=['risk_level']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return (
            f"{self.vehicle} - "
            f"{self.get_component_display()} - "
            f"{self.get_risk_level_display()}"
        )

    def update_risk_level(self):
        """
        Automatically determine risk level
        from risk score (0-100).
        """

        score = self.risk_score

        if score >= 80:
            self.risk_level = 'critical'
            self.maintenance_required = True
            self.status = 'critical'

        elif score >= 60:
            self.risk_level = 'high'
            self.maintenance_required = True
            self.status = 'maintenance_required'

        elif score >= 30:
            self.risk_level = 'moderate'
            self.status = 'service_soon'

        else:
            self.risk_level = 'low'
            self.status = 'healthy'

    def mark_resolved(self):
        from django.utils import timezone

        self.is_resolved = True
        self.status = 'resolved'
        self.resolved_at = timezone.now()

        self.save(
            update_fields=[
                'is_resolved',
                'status',
                'resolved_at',
                'updated_at',
            ]
        )
        # ============================================================
# DRIVING BEHAVIOR
# EV Driver Behaviour & Eco-Driving Analysis
# ============================================================

class DrivingBehavior(models.Model):

    RISK_LEVEL_CHOICES = [
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    DRIVING_STYLE_CHOICES = [
        ('eco', 'Eco Driving'),
        ('normal', 'Normal'),
        ('aggressive', 'Aggressive'),
        ('unsafe', 'Unsafe'),
    ]

    # Vehicle
    vehicle = models.ForeignKey(
        'EVVehicle',
        on_delete=models.CASCADE,
        related_name='driving_behaviors'
    )

    # User / driver
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='driving_behaviors'
    )

    # Trip information
    trip_name = models.CharField(
        max_length=200,
        blank=True
    )

    distance_km = models.FloatField(
        default=0.0
    )

    driving_duration_minutes = models.PositiveIntegerField(
        default=0
    )

    # Speed
    average_speed = models.FloatField(
        default=0.0
    )

    maximum_speed = models.FloatField(
        default=0.0
    )

    speeding_events = models.PositiveIntegerField(
        default=0
    )

    # Acceleration / braking
    harsh_acceleration_count = models.PositiveIntegerField(
        default=0
    )

    harsh_braking_count = models.PositiveIntegerField(
        default=0
    )

    sudden_turn_count = models.PositiveIntegerField(
        default=0
    )

    rapid_acceleration_count = models.PositiveIntegerField(
        default=0
    )

    # Idle time
    idle_time_minutes = models.FloatField(
        default=0.0
    )

    # Energy usage
    energy_consumed_kwh = models.FloatField(
        default=0.0
    )

    energy_efficiency = models.FloatField(
        default=0.0,
        help_text='Energy efficiency in kWh/km'
    )

    regenerative_energy_kwh = models.FloatField(
        default=0.0
    )

    # Battery
    battery_start_percentage = models.FloatField(
        default=0.0
    )

    battery_end_percentage = models.FloatField(
        default=0.0
    )

    battery_consumed_percentage = models.FloatField(
        default=0.0
    )

    # Eco score
    eco_score = models.FloatField(
        default=0.0
    )

    safety_score = models.FloatField(
        default=0.0
    )

    efficiency_score = models.FloatField(
        default=0.0
    )

    overall_score = models.FloatField(
        default=0.0
    )

    # Driving style
    driving_style = models.CharField(
        max_length=20,
        choices=DRIVING_STYLE_CHOICES,
        default='normal'
    )

    # Risk
    risk_level = models.CharField(
        max_length=20,
        choices=RISK_LEVEL_CHOICES,
        default='low'
    )

    # AI analysis
    ai_risk_score = models.FloatField(
        default=0.0
    )

    ai_recommendation = models.TextField(
        blank=True
    )

    ai_detected_pattern = models.CharField(
        max_length=250,
        blank=True
    )

    # Environmental impact
    estimated_co2_saved_kg = models.FloatField(
        default=0.0
    )

    green_points = models.PositiveIntegerField(
        default=0
    )

    # Location
    start_location = models.CharField(
        max_length=200,
        blank=True
    )

    destination = models.CharField(
        max_length=200,
        blank=True
    )

    # Date / timestamps
    trip_date = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['vehicle', '-created_at']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['driving_style']),
            models.Index(fields=['risk_level']),
        ]

    def __str__(self):
        return (
            f"{self.vehicle} - "
            f"{self.get_driving_style_display()} - "
            f"Score {self.overall_score:.1f}"
        )

    def calculate_overall_score(self):
        """
        Calculate overall driving score.
        """

        scores = [
            self.eco_score,
            self.safety_score,
            self.efficiency_score
        ]

        return round(sum(scores) / len(scores), 2)

    def update_driving_style(self):
        """
        Determine driving style using overall score
        and unsafe driving events.
        """

        unsafe_events = (
            self.harsh_acceleration_count
            + self.harsh_braking_count
            + self.sudden_turn_count
            + self.speeding_events
        )

        if unsafe_events >= 15 or self.overall_score < 40:
            self.driving_style = 'unsafe'
            self.risk_level = 'critical'

        elif unsafe_events >= 8 or self.overall_score < 60:
            self.driving_style = 'aggressive'
            self.risk_level = 'high'

        elif self.overall_score >= 85:
            self.driving_style = 'eco'
            self.risk_level = 'low'

        else:
            self.driving_style = 'normal'
            self.risk_level = 'moderate'

    def save(self, *args, **kwargs):

        self.overall_score = self.calculate_overall_score()

        self.update_driving_style()

        super().save(*args, **kwargs)
        # ============================================================
# BATTERY ANOMALY
# AI-Based EV Battery Anomaly Detection
# ============================================================

class BatteryAnomaly(models.Model):

    ANOMALY_TYPE_CHOICES = [
        ('temperature', 'Battery Temperature Anomaly'),
        ('voltage', 'Voltage Anomaly'),
        ('current', 'Current Anomaly'),
        ('rapid_drain', 'Rapid Battery Drain'),
        ('slow_charging', 'Slow Charging'),
        ('overcharging', 'Overcharging'),
        ('cell_imbalance', 'Cell Imbalance'),
        ('capacity_loss', 'Battery Capacity Loss'),
        ('health_degradation', 'Battery Health Degradation'),
        ('charging_failure', 'Charging Failure'),
        ('range_drop', 'Unexpected Range Drop'),
        ('other', 'Other'),
    ]

    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    STATUS_CHOICES = [
        ('detected', 'Detected'),
        ('monitoring', 'Monitoring'),
        ('investigating', 'Investigating'),
        ('maintenance_required', 'Maintenance Required'),
        ('resolved', 'Resolved'),
        ('ignored', 'Ignored'),
    ]

    # --------------------------------------------------------
    # VEHICLE
    # --------------------------------------------------------

    vehicle = models.ForeignKey(
        'EVVehicle',
        on_delete=models.CASCADE,
        related_name='battery_anomalies'
    )

    # --------------------------------------------------------
    # ANOMALY INFORMATION
    # --------------------------------------------------------

    anomaly_type = models.CharField(
        max_length=50,
        choices=ANOMALY_TYPE_CHOICES,
        default='other'
    )

    title = models.CharField(
        max_length=200,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # BATTERY INFORMATION
    # --------------------------------------------------------

    battery_percentage = models.FloatField(
        default=0.0
    )

    battery_health_percentage = models.FloatField(
        default=100.0
    )

    battery_temperature = models.FloatField(
        null=True,
        blank=True
    )

    voltage = models.FloatField(
        null=True,
        blank=True
    )

    current = models.FloatField(
        null=True,
        blank=True
    )

    battery_capacity_kwh = models.FloatField(
        null=True,
        blank=True
    )

    current_charge_kwh = models.FloatField(
        null=True,
        blank=True
    )

    # --------------------------------------------------------
    # CHARGING INFORMATION
    # --------------------------------------------------------

    is_charging = models.BooleanField(
        default=False
    )

    charging_power_kw = models.FloatField(
        default=0.0
    )

    charging_rate_kw = models.FloatField(
        default=0.0
    )

    charging_duration_minutes = models.PositiveIntegerField(
        default=0
    )

    # --------------------------------------------------------
    # EXPECTED VS ACTUAL
    # --------------------------------------------------------

    expected_value = models.FloatField(
        null=True,
        blank=True
    )

    actual_value = models.FloatField(
        null=True,
        blank=True
    )

    deviation_percentage = models.FloatField(
        default=0.0
    )

    # --------------------------------------------------------
    # AI ANOMALY DETECTION
    # --------------------------------------------------------

    anomaly_score = models.FloatField(
        default=0.0,
        help_text='AI anomaly score from 0 to 100'
    )

    confidence_score = models.FloatField(
        default=0.0
    )

    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        default='low'
    )

    ai_detected = models.BooleanField(
        default=True
    )

    ai_explanation = models.TextField(
        blank=True
    )

    ai_recommendation = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # MAINTENANCE
    # --------------------------------------------------------

    maintenance_required = models.BooleanField(
        default=False
    )

    recommended_action = models.TextField(
        blank=True
    )

    estimated_repair_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # --------------------------------------------------------
    # VEHICLE CONDITIONS
    # --------------------------------------------------------

    vehicle_speed = models.FloatField(
        default=0.0
    )

    mileage = models.PositiveIntegerField(
        default=0
    )

    outside_temperature = models.FloatField(
        null=True,
        blank=True
    )

    # --------------------------------------------------------
    # LOCATION
    # --------------------------------------------------------

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='detected'
    )

    is_active = models.BooleanField(
        default=True
    )

    # --------------------------------------------------------
    # RESOLUTION
    # --------------------------------------------------------

    resolution_notes = models.TextField(
        blank=True
    )

    resolved_at = models.DateTimeField(
        null=True,
        blank=True
    )

    # --------------------------------------------------------
    # TIMESTAMPS
    # --------------------------------------------------------

    detected_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-detected_at']

        indexes = [
            models.Index(
                fields=['vehicle', '-detected_at']
            ),
            models.Index(
                fields=['anomaly_type']
            ),
            models.Index(
                fields=['severity']
            ),
            models.Index(
                fields=['status']
            ),
            models.Index(
                fields=['is_active']
            ),
        ]

    def __str__(self):
        return (
            f"{self.vehicle} - "
            f"{self.get_anomaly_type_display()} - "
            f"{self.get_severity_display()}"
        )

    # --------------------------------------------------------
    # UPDATE SEVERITY
    # --------------------------------------------------------

    def update_severity(self):

        score = self.anomaly_score

        if score >= 80:
            self.severity = 'critical'
            self.maintenance_required = True
            self.status = 'maintenance_required'

        elif score >= 60:
            self.severity = 'high'
            self.maintenance_required = True

        elif score >= 30:
            self.severity = 'moderate'

        else:
            self.severity = 'low'

    # --------------------------------------------------------
    # CALCULATE DEVIATION
    # --------------------------------------------------------

    def calculate_deviation(self):

        if (
            self.expected_value is None
            or self.actual_value is None
            or self.expected_value == 0
        ):
            return 0.0

        difference = abs(
            self.actual_value -
            self.expected_value
        )

        return round(
            (difference / abs(self.expected_value)) * 100,
            2
        )

    # --------------------------------------------------------
    # RESOLVE ANOMALY
    # --------------------------------------------------------

    def resolve(self, notes=''):

        from django.utils import timezone

        self.status = 'resolved'
        self.is_active = False
        self.resolved_at = timezone.now()

        if notes:
            self.resolution_notes = notes

        self.save()

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    def save(self, *args, **kwargs):

        self.deviation_percentage = (
            self.calculate_deviation()
        )

        self.update_severity()

        super().save(*args, **kwargs)
        # ============================================================
# CHARGING DEMAND FORECAST
# AI-Based EV Charging Demand Prediction
# ============================================================

class ChargingDemandForecast(models.Model):

    DEMAND_LEVEL_CHOICES = [
        ('very_low', 'Very Low'),
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('high', 'High'),
        ('very_high', 'Very High'),
        ('critical', 'Critical'),
    ]

    FORECAST_TYPE_CHOICES = [
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('festival', 'Festival'),
        ('peak_hour', 'Peak Hour'),
        ('weather', 'Weather Based'),
    ]

    # Charging station
    station = models.ForeignKey(
        'ChargingStation',
        on_delete=models.CASCADE,
        related_name='demand_forecasts'
    )

    # Forecast information
    forecast_type = models.CharField(
        max_length=30,
        choices=FORECAST_TYPE_CHOICES,
        default='hourly'
    )

    forecast_date = models.DateField()

    forecast_hour = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text='Hour from 0 to 23'
    )

    # Predicted demand
    predicted_vehicles = models.PositiveIntegerField(
        default=0
    )

    predicted_energy_kwh = models.FloatField(
        default=0.0
    )

    demand_level = models.CharField(
        max_length=20,
        choices=DEMAND_LEVEL_CHOICES,
        default='moderate'
    )

    demand_score = models.FloatField(
        default=0.0,
        help_text='Demand score from 0 to 100'
    )

    # Charger availability prediction
    predicted_available_chargers = models.PositiveIntegerField(
        default=0
    )

    predicted_busy_chargers = models.PositiveIntegerField(
        default=0
    )

    predicted_queue_length = models.PositiveIntegerField(
        default=0
    )

    predicted_wait_minutes = models.PositiveIntegerField(
        default=0
    )

    # Pricing prediction
    predicted_price_per_kwh = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    estimated_revenue = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    # Traffic information
    traffic_level = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('moderate', 'Moderate'),
            ('high', 'High'),
            ('severe', 'Severe'),
        ],
        default='low'
    )

    traffic_score = models.FloatField(
        default=0.0
    )

    # Weather information
    temperature = models.FloatField(
        null=True,
        blank=True
    )

    weather_condition = models.CharField(
        max_length=50,
        blank=True
    )

    rainfall_mm = models.FloatField(
        default=0.0
    )

    weather_impact_score = models.FloatField(
        default=0.0
    )

    # India-specific intelligence
    is_peak_hour = models.BooleanField(
        default=False
    )

    is_weekend = models.BooleanField(
        default=False
    )

    is_holiday = models.BooleanField(
        default=False
    )

    festival_name = models.CharField(
        max_length=100,
        blank=True
    )

    monsoon_impact = models.BooleanField(
        default=False
    )

    # AI prediction
    ai_model_name = models.CharField(
        max_length=100,
        blank=True
    )

    confidence_score = models.FloatField(
        default=0.0
    )

    ai_recommendation = models.TextField(
        blank=True
    )

    # Historical comparison
    previous_average_vehicles = models.FloatField(
        default=0.0
    )

    demand_change_percentage = models.FloatField(
        default=0.0
    )

    # Location
    city = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    # Status
    is_active = models.BooleanField(
        default=True
    )

    generated_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            'forecast_date',
            'forecast_hour'
        ]

        indexes = [
            models.Index(
                fields=['station', 'forecast_date']
            ),
            models.Index(
                fields=['demand_level']
            ),
            models.Index(
                fields=['forecast_type']
            ),
            models.Index(
                fields=['city', 'forecast_date']
            ),
        ]

    def __str__(self):
        return (
            f"{self.station} - "
            f"{self.forecast_date} - "
            f"{self.get_demand_level_display()}"
        )

    def calculate_demand_level(self):
        """
        Convert demand score into demand category.
        """

        score = self.demand_score

        if score >= 90:
            return 'critical'

        elif score >= 75:
            return 'very_high'

        elif score >= 60:
            return 'high'

        elif score >= 40:
            return 'moderate'

        elif score >= 20:
            return 'low'

        return 'very_low'

    def calculate_demand_change(self):
        """
        Compare predicted demand with historical average.
        """

        if self.previous_average_vehicles <= 0:
            return 0.0

        difference = (
            self.predicted_vehicles
            - self.previous_average_vehicles
        )

        return round(
            (
                difference
                / self.previous_average_vehicles
            ) * 100,
            2
        )

    def update_peak_hour(self):
        """
        Indian common traffic/charging peak hours:
        7-10 AM and 5-9 PM.
        """

        if self.forecast_hour is None:
            return

        self.is_peak_hour = (
            7 <= self.forecast_hour <= 10
            or
            17 <= self.forecast_hour <= 21
        )

    def save(self, *args, **kwargs):

        self.demand_level = (
            self.calculate_demand_level()
        )

        self.demand_change_percentage = (
            self.calculate_demand_change()
        )

        self.update_peak_hour()

        super().save(*args, **kwargs)
        # ============================================================
# SMART CHARGING SCHEDULE
# AI-Based EV Charging Scheduling & Cost Optimization
# ============================================================

class SmartChargingSchedule(models.Model):

    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('waiting', 'Waiting'),
        ('charging', 'Charging'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('failed', 'Failed'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('emergency', 'Emergency'),
    ]

    CHARGING_MODE_CHOICES = [
        ('normal', 'Normal Charging'),
        ('fast', 'Fast Charging'),
        ('eco', 'Eco Charging'),
        ('smart', 'AI Smart Charging'),
        ('off_peak', 'Off-Peak Charging'),
        ('solar', 'Solar Charging'),
    ]

    # --------------------------------------------------------
    # USER
    # --------------------------------------------------------

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='smart_charging_schedules'
    )

    # --------------------------------------------------------
    # VEHICLE
    # --------------------------------------------------------

    vehicle = models.ForeignKey(
        'EVVehicle',
        on_delete=models.CASCADE,
        related_name='smart_charging_schedules'
    )

    # --------------------------------------------------------
    # CHARGING STATION
    # --------------------------------------------------------

    station = models.ForeignKey(
        'ChargingStation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='smart_charging_schedules'
    )

    # --------------------------------------------------------
    # SCHEDULE
    # --------------------------------------------------------

    scheduled_date = models.DateField()

    scheduled_start_time = models.TimeField(
        null=True,
        blank=True
    )

    scheduled_end_time = models.TimeField(
        null=True,
        blank=True
    )

    actual_start_time = models.DateTimeField(
        null=True,
        blank=True
    )

    actual_end_time = models.DateTimeField(
        null=True,
        blank=True
    )

    # --------------------------------------------------------
    # BATTERY INFORMATION
    # --------------------------------------------------------

    current_battery_percentage = models.FloatField(
        default=0.0
    )

    target_battery_percentage = models.FloatField(
        default=80.0
    )

    battery_capacity_kwh = models.FloatField(
        default=0.0
    )

    required_energy_kwh = models.FloatField(
        default=0.0
    )

    # --------------------------------------------------------
    # CHARGING INFORMATION
    # --------------------------------------------------------

    charging_mode = models.CharField(
        max_length=30,
        choices=CHARGING_MODE_CHOICES,
        default='smart'
    )

    charging_power_kw = models.FloatField(
        default=0.0
    )

    estimated_duration_minutes = models.PositiveIntegerField(
        default=0
    )

    # --------------------------------------------------------
    # COST
    # --------------------------------------------------------

    electricity_price_per_kwh = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    estimated_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    actual_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    estimated_savings = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # --------------------------------------------------------
    # SMART / OFF-PEAK CHARGING
    # --------------------------------------------------------

    use_off_peak = models.BooleanField(
        default=True
    )

    off_peak_start_time = models.TimeField(
        null=True,
        blank=True
    )

    off_peak_end_time = models.TimeField(
        null=True,
        blank=True
    )

    # --------------------------------------------------------
    # RENEWABLE ENERGY
    # --------------------------------------------------------

    prefer_renewable_energy = models.BooleanField(
        default=False
    )

    solar_available = models.BooleanField(
        default=False
    )

    renewable_energy_percentage = models.FloatField(
        default=0.0
    )

    # --------------------------------------------------------
    # GRID INFORMATION
    # --------------------------------------------------------

    grid_load_percentage = models.FloatField(
        default=0.0
    )

    avoid_peak_grid_load = models.BooleanField(
        default=True
    )

    # --------------------------------------------------------
    # PRIORITY
    # --------------------------------------------------------

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='normal'
    )

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled'
    )

    is_active = models.BooleanField(
        default=True
    )

    # --------------------------------------------------------
    # AI OPTIMIZATION
    # --------------------------------------------------------

    ai_optimized = models.BooleanField(
        default=False
    )

    ai_score = models.FloatField(
        default=0.0
    )

    ai_recommendation = models.TextField(
        blank=True
    )

    predicted_wait_minutes = models.PositiveIntegerField(
        default=0
    )

    # --------------------------------------------------------
    # NOTIFICATIONS
    # --------------------------------------------------------

    reminder_enabled = models.BooleanField(
        default=True
    )

    reminder_sent = models.BooleanField(
        default=False
    )

    completion_notification_sent = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # NOTES
    # --------------------------------------------------------

    notes = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # TIMESTAMPS
    # --------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            'scheduled_date',
            'scheduled_start_time'
        ]

        indexes = [
            models.Index(
                fields=['vehicle', 'scheduled_date']
            ),
            models.Index(
                fields=['station', 'scheduled_date']
            ),
            models.Index(
                fields=['status']
            ),
            models.Index(
                fields=['priority']
            ),
        ]

    def __str__(self):
        return (
            f"{self.vehicle} - "
            f"{self.scheduled_date} - "
            f"{self.get_charging_mode_display()}"
        )

    # --------------------------------------------------------
    # CALCULATE REQUIRED ENERGY
    # --------------------------------------------------------

    def calculate_required_energy(self):

        if self.battery_capacity_kwh <= 0:
            return 0.0

        difference = (
            self.target_battery_percentage
            - self.current_battery_percentage
        )

        if difference <= 0:
            return 0.0

        return round(
            self.battery_capacity_kwh
            * (difference / 100),
            2
        )

    # --------------------------------------------------------
    # ESTIMATE CHARGING DURATION
    # --------------------------------------------------------

    def calculate_duration(self):

        if self.charging_power_kw <= 0:
            return 0

        hours = (
            self.required_energy_kwh
            / self.charging_power_kw
        )

        return max(
            int(hours * 60),
            0
        )

    # --------------------------------------------------------
    # ESTIMATE COST
    # --------------------------------------------------------

    def calculate_estimated_cost(self):

        return (
            self.required_energy_kwh
            * self.electricity_price_per_kwh
        )

    # --------------------------------------------------------
    # START CHARGING
    # --------------------------------------------------------

    def start_charging(self):

        from django.utils import timezone

        self.status = 'charging'
        self.actual_start_time = timezone.now()

        self.save(
            update_fields=[
                'status',
                'actual_start_time',
                'updated_at'
            ]
        )

    # --------------------------------------------------------
    # COMPLETE CHARGING
    # --------------------------------------------------------

    def complete_charging(self):

        from django.utils import timezone

        self.status = 'completed'
        self.actual_end_time = timezone.now()
        self.is_active = False

        self.save(
            update_fields=[
                'status',
                'actual_end_time',
                'is_active',
                'updated_at'
            ]
        )

    # --------------------------------------------------------
    # CANCEL
    # --------------------------------------------------------

    def cancel_schedule(self):

        self.status = 'cancelled'
        self.is_active = False

        self.save(
            update_fields=[
                'status',
                'is_active',
                'updated_at'
            ]
        )

    # --------------------------------------------------------
    # AUTO CALCULATIONS
    # --------------------------------------------------------

    def save(self, *args, **kwargs):

        self.required_energy_kwh = (
            self.calculate_required_energy()
        )

        self.estimated_duration_minutes = (
            self.calculate_duration()
        )

        self.estimated_cost = (
            self.calculate_estimated_cost()
        )

        super().save(*args, **kwargs)
        # ============================================================
# VEHICLE GEOFENCE
# Location Boundary & Vehicle Safety Monitoring
# ============================================================

class VehicleGeofence(models.Model):

    GEOFENCE_TYPE_CHOICES = [
        ('home', 'Home'),
        ('office', 'Office'),
        ('charging_station', 'Charging Station'),
        ('service_center', 'Service Center'),
        ('parking', 'Parking Area'),
        ('city', 'City Zone'),
        ('highway', 'Highway / Expressway'),
        ('restricted', 'Restricted Area'),
        ('safe_zone', 'Safe Zone'),
        ('custom', 'Custom Zone'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('breached', 'Breached'),
    ]

    # Vehicle
    vehicle = models.ForeignKey(
        'EVVehicle',
        on_delete=models.CASCADE,
        related_name='geofences'
    )

    # User / owner
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='vehicle_geofences'
    )

    # Basic information
    name = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    geofence_type = models.CharField(
        max_length=30,
        choices=GEOFENCE_TYPE_CHOICES,
        default='custom'
    )

    # Center point
    latitude = models.FloatField()

    longitude = models.FloatField()

    # Radius in meters
    radius_meters = models.FloatField(
        default=500.0
    )

    # Optional address information
    address = models.TextField(
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    district = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    pincode = models.CharField(
        max_length=10,
        blank=True
    )

    # Entry / exit alerts
    alert_on_entry = models.BooleanField(
        default=True
    )

    alert_on_exit = models.BooleanField(
        default=True
    )

    notification_enabled = models.BooleanField(
        default=True
    )

    # Restriction
    is_restricted = models.BooleanField(
        default=False
    )

    # Speed monitoring
    speed_limit_enabled = models.BooleanField(
        default=False
    )

    speed_limit_kmph = models.FloatField(
        default=0.0
    )

    # Time-based geofence
    schedule_enabled = models.BooleanField(
        default=False
    )

    active_from = models.TimeField(
        null=True,
        blank=True
    )

    active_until = models.TimeField(
        null=True,
        blank=True
    )

    # Current vehicle state
    vehicle_inside = models.BooleanField(
        default=False
    )

    last_entry_at = models.DateTimeField(
        null=True,
        blank=True
    )

    last_exit_at = models.DateTimeField(
        null=True,
        blank=True
    )

    last_breach_at = models.DateTimeField(
        null=True,
        blank=True
    )

    breach_count = models.PositiveIntegerField(
        default=0
    )

    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    is_active = models.BooleanField(
        default=True
    )

    # AI monitoring
    ai_monitoring_enabled = models.BooleanField(
        default=True
    )

    ai_risk_score = models.FloatField(
        default=0.0
    )

    ai_recommendation = models.TextField(
        blank=True
    )

    # Optional polygon/custom map information
    boundary_data = models.JSONField(
        default=dict,
        blank=True
    )

    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['vehicle', 'is_active']),
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['geofence_type']),
            models.Index(fields=['city', 'state']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.name} - {self.vehicle}"

    # --------------------------------------------------------
    # DISTANCE FROM GEOFENCE CENTER
    # --------------------------------------------------------

    def distance_from_center(self, latitude, longitude):
        """
        Calculate approximate distance in meters between
        the vehicle and geofence center using Haversine.
        """

        from math import radians, sin, cos, sqrt, atan2

        earth_radius = 6371000

        lat1 = radians(self.latitude)
        lon1 = radians(self.longitude)

        lat2 = radians(latitude)
        lon2 = radians(longitude)

        delta_lat = lat2 - lat1
        delta_lon = lon2 - lon1

        a = (
            sin(delta_lat / 2) ** 2
            + cos(lat1)
            * cos(lat2)
            * sin(delta_lon / 2) ** 2
        )

        c = 2 * atan2(
            sqrt(a),
            sqrt(1 - a)
        )

        return earth_radius * c

    # --------------------------------------------------------
    # CHECK VEHICLE INSIDE GEOFENCE
    # --------------------------------------------------------

    def contains_location(self, latitude, longitude):

        distance = self.distance_from_center(
            latitude,
            longitude
        )

        return distance <= self.radius_meters

    # --------------------------------------------------------
    # UPDATE VEHICLE LOCATION
    # --------------------------------------------------------

    def check_vehicle_location(self, latitude, longitude):

        from django.utils import timezone

        currently_inside = self.contains_location(
            latitude,
            longitude
        )

        previous_state = self.vehicle_inside

        # Vehicle entered geofence
        if currently_inside and not previous_state:

            self.vehicle_inside = True
            self.last_entry_at = timezone.now()

        # Vehicle exited geofence
        elif not currently_inside and previous_state:

            self.vehicle_inside = False
            self.last_exit_at = timezone.now()

            if self.is_restricted:
                self.status = 'breached'
                self.last_breach_at = timezone.now()
                self.breach_count += 1

        self.save()

        return currently_inside

    # --------------------------------------------------------
    # CHECK SPEED VIOLATION
    # --------------------------------------------------------

    def check_speed_violation(self, speed):

        if not self.speed_limit_enabled:
            return False

        if self.speed_limit_kmph <= 0:
            return False

        return speed > self.speed_limit_kmph
    # ============================================================
# GEOFENCE EVENT
# Records Vehicle Entry / Exit / Breach / Speed Events
# ============================================================

class GeofenceEvent(models.Model):

    EVENT_TYPE_CHOICES = [
        ('entry', 'Vehicle Entered Geofence'),
        ('exit', 'Vehicle Exited Geofence'),
        ('breach', 'Restricted Zone Breach'),
        ('speed_violation', 'Speed Limit Violation'),
        ('unauthorized_entry', 'Unauthorized Entry'),
        ('unauthorized_exit', 'Unauthorized Exit'),
        ('warning', 'Geofence Warning'),
        ('other', 'Other'),
    ]

    SEVERITY_CHOICES = [
        ('info', 'Information'),
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('acknowledged', 'Acknowledged'),
        ('resolved', 'Resolved'),
        ('ignored', 'Ignored'),
    ]

    # --------------------------------------------------------
    # GEOFENCE
    # --------------------------------------------------------

    geofence = models.ForeignKey(
        'VehicleGeofence',
        on_delete=models.CASCADE,
        related_name='events'
    )

    # --------------------------------------------------------
    # VEHICLE
    # --------------------------------------------------------

    vehicle = models.ForeignKey(
        'EVVehicle',
        on_delete=models.CASCADE,
        related_name='geofence_events'
    )

    # --------------------------------------------------------
    # USER / OWNER
    # --------------------------------------------------------

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='geofence_events'
    )

    # --------------------------------------------------------
    # EVENT
    # --------------------------------------------------------

    event_type = models.CharField(
        max_length=30,
        choices=EVENT_TYPE_CHOICES,
        default='entry'
    )

    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        default='info'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    title = models.CharField(
        max_length=200,
        blank=True
    )

    message = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # VEHICLE LOCATION
    # --------------------------------------------------------

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    # --------------------------------------------------------
    # VEHICLE INFORMATION
    # --------------------------------------------------------

    vehicle_speed = models.FloatField(
        default=0.0
    )

    battery_percentage = models.FloatField(
        null=True,
        blank=True
    )

    # --------------------------------------------------------
    # SPEED VIOLATION
    # --------------------------------------------------------

    speed_limit = models.FloatField(
        null=True,
        blank=True
    )

    speed_exceeded_by = models.FloatField(
        default=0.0
    )

    # --------------------------------------------------------
    # DISTANCE
    # --------------------------------------------------------

    distance_from_center_meters = models.FloatField(
        null=True,
        blank=True
    )

    # --------------------------------------------------------
    # ALERT / NOTIFICATION
    # --------------------------------------------------------

    alert_generated = models.BooleanField(
        default=False
    )

    notification_sent = models.BooleanField(
        default=False
    )

    sms_sent = models.BooleanField(
        default=False
    )

    email_sent = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # AI ANALYSIS
    # --------------------------------------------------------

    ai_risk_score = models.FloatField(
        default=0.0
    )

    ai_detected = models.BooleanField(
        default=False
    )

    ai_recommendation = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # RESOLUTION
    # --------------------------------------------------------

    resolution_notes = models.TextField(
        blank=True
    )

    acknowledged_at = models.DateTimeField(
        null=True,
        blank=True
    )

    resolved_at = models.DateTimeField(
        null=True,
        blank=True
    )

    # --------------------------------------------------------
    # TIMESTAMPS
    # --------------------------------------------------------

    event_time = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-event_time']

        indexes = [
            models.Index(
                fields=['geofence', '-event_time']
            ),
            models.Index(
                fields=['vehicle', '-event_time']
            ),
            models.Index(
                fields=['event_type']
            ),
            models.Index(
                fields=['severity']
            ),
            models.Index(
                fields=['status']
            ),
        ]

    def __str__(self):
        return (
            f"{self.vehicle} - "
            f"{self.get_event_type_display()} - "
            f"{self.geofence.name}"
        )

    # --------------------------------------------------------
    # CALCULATE SPEED EXCESS
    # --------------------------------------------------------

    def calculate_speed_excess(self):

        if self.speed_limit is None:
            return 0.0

        if self.vehicle_speed <= self.speed_limit:
            return 0.0

        return round(
            self.vehicle_speed - self.speed_limit,
            2
        )

    # --------------------------------------------------------
    # ACKNOWLEDGE EVENT
    # --------------------------------------------------------

    def acknowledge(self):

        from django.utils import timezone

        self.status = 'acknowledged'
        self.acknowledged_at = timezone.now()

        self.save(
            update_fields=[
                'status',
                'acknowledged_at',
                'updated_at'
            ]
        )

    # --------------------------------------------------------
    # RESOLVE EVENT
    # --------------------------------------------------------

    def resolve(self, notes=''):

        from django.utils import timezone

        self.status = 'resolved'
        self.resolved_at = timezone.now()

        if notes:
            self.resolution_notes = notes

        self.save()

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    def save(self, *args, **kwargs):

        self.speed_exceeded_by = (
            self.calculate_speed_excess()
        )

        # Automatically classify serious violations
        if self.event_type in [
            'breach',
            'unauthorized_entry',
            'unauthorized_exit'
        ]:
            if self.severity == 'info':
                self.severity = 'high'

        if (
            self.event_type == 'speed_violation'
            and self.speed_exceeded_by >= 30
        ):
            self.severity = 'critical'

        super().save(*args, **kwargs)
        # ============================================================
# VEHICLE SECURITY EVENT
# EV Theft / Tampering / Unauthorized Access Monitoring
# ============================================================

class VehicleSecurityEvent(models.Model):

    EVENT_TYPE_CHOICES = [
        ('unauthorized_access', 'Unauthorized Access'),
        ('theft_attempt', 'Theft Attempt'),
        ('vehicle_moved', 'Unauthorized Vehicle Movement'),
        ('door_open', 'Unauthorized Door Open'),
        ('window_break', 'Window Break Detection'),
        ('tampering', 'Vehicle Tampering'),
        ('battery_tampering', 'Battery Tampering'),
        ('charging_tampering', 'Charging Port Tampering'),
        ('gps_disabled', 'GPS Disabled'),
        ('geofence_breach', 'Geofence Breach'),
        ('ignition', 'Unauthorized Ignition'),
        ('tow_detected', 'Vehicle Towing Detected'),
        ('collision', 'Collision Detected'),
        ('panic', 'Panic / Emergency Event'),
        ('other', 'Other Security Event'),
    ]

    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    STATUS_CHOICES = [
        ('detected', 'Detected'),
        ('investigating', 'Investigating'),
        ('acknowledged', 'Acknowledged'),
        ('resolved', 'Resolved'),
        ('false_alarm', 'False Alarm'),
    ]

    # --------------------------------------------------------
    # VEHICLE
    # --------------------------------------------------------

    vehicle = models.ForeignKey(
        'EVVehicle',
        on_delete=models.CASCADE,
        related_name='security_events'
    )

    # --------------------------------------------------------
    # USER / OWNER
    # --------------------------------------------------------

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='vehicle_security_events'
    )

    # --------------------------------------------------------
    # SECURITY EVENT
    # --------------------------------------------------------

    event_type = models.CharField(
        max_length=40,
        choices=EVENT_TYPE_CHOICES,
        default='other'
    )

    title = models.CharField(
        max_length=200,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        default='low'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='detected'
    )

    # --------------------------------------------------------
    # LOCATION
    # --------------------------------------------------------

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    # --------------------------------------------------------
    # VEHICLE STATE
    # --------------------------------------------------------

    vehicle_speed = models.FloatField(
        default=0.0
    )

    battery_percentage = models.FloatField(
        null=True,
        blank=True
    )

    ignition_on = models.BooleanField(
        default=False
    )

    doors_locked = models.BooleanField(
        default=True
    )

    gps_active = models.BooleanField(
        default=True
    )

    # --------------------------------------------------------
    # MOVEMENT / THEFT DETECTION
    # --------------------------------------------------------

    unauthorized_movement = models.BooleanField(
        default=False
    )

    movement_distance_meters = models.FloatField(
        default=0.0
    )

    theft_suspected = models.BooleanField(
        default=False
    )

    tampering_detected = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # GEOFENCE
    # --------------------------------------------------------

    geofence = models.ForeignKey(
        'VehicleGeofence',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='security_events'
    )

    geofence_breached = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # AI SECURITY ANALYSIS
    # --------------------------------------------------------

    ai_detected = models.BooleanField(
        default=False
    )

    ai_risk_score = models.FloatField(
        default=0.0,
        help_text='AI security risk score from 0 to 100'
    )

    ai_confidence = models.FloatField(
        default=0.0
    )

    ai_analysis = models.TextField(
        blank=True
    )

    ai_recommendation = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # SECURITY ACTIONS
    # --------------------------------------------------------

    alarm_triggered = models.BooleanField(
        default=False
    )

    vehicle_locked_remotely = models.BooleanField(
        default=False
    )

    emergency_services_required = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # NOTIFICATIONS
    # --------------------------------------------------------

    notification_sent = models.BooleanField(
        default=False
    )

    sms_sent = models.BooleanField(
        default=False
    )

    email_sent = models.BooleanField(
        default=False
    )

    owner_notified = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # RESOLUTION
    # --------------------------------------------------------

    resolution_notes = models.TextField(
        blank=True
    )

    acknowledged_at = models.DateTimeField(
        null=True,
        blank=True
    )

    resolved_at = models.DateTimeField(
        null=True,
        blank=True
    )

    # --------------------------------------------------------
    # TIMESTAMPS
    # --------------------------------------------------------

    event_time = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-event_time']

        indexes = [
            models.Index(
                fields=['vehicle', '-event_time']
            ),
            models.Index(
                fields=['event_type']
            ),
            models.Index(
                fields=['severity']
            ),
            models.Index(
                fields=['status']
            ),
            models.Index(
                fields=['theft_suspected']
            ),
        ]

    def __str__(self):
        return (
            f"{self.vehicle} - "
            f"{self.get_event_type_display()} - "
            f"{self.get_severity_display()}"
        )

    # --------------------------------------------------------
    # UPDATE SECURITY SEVERITY
    # --------------------------------------------------------

    def update_severity(self):

        if (
            self.theft_suspected
            or self.event_type == 'theft_attempt'
        ):
            self.severity = 'critical'
            self.alarm_triggered = True

        elif (
            self.tampering_detected
            or self.geofence_breached
            or self.unauthorized_movement
        ):
            self.severity = 'high'

        elif self.ai_risk_score >= 80:
            self.severity = 'critical'

        elif self.ai_risk_score >= 60:
            self.severity = 'high'

        elif self.ai_risk_score >= 30:
            self.severity = 'moderate'

    # --------------------------------------------------------
    # ACKNOWLEDGE EVENT
    # --------------------------------------------------------

    def acknowledge(self):

        from django.utils import timezone

        self.status = 'acknowledged'
        self.acknowledged_at = timezone.now()

        self.save(
            update_fields=[
                'status',
                'acknowledged_at',
                'updated_at'
            ]
        )

    # --------------------------------------------------------
    # RESOLVE EVENT
    # --------------------------------------------------------

    def resolve(self, notes=''):

        from django.utils import timezone

        self.status = 'resolved'
        self.resolved_at = timezone.now()

        if notes:
            self.resolution_notes = notes

        self.save()

    # --------------------------------------------------------
    # MARK AS FALSE ALARM
    # --------------------------------------------------------

    def mark_false_alarm(self):

        from django.utils import timezone

        self.status = 'false_alarm'
        self.resolved_at = timezone.now()
        self.theft_suspected = False

        self.save()

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    def save(self, *args, **kwargs):

        self.update_severity()

        super().save(*args, **kwargs)
        # ============================================================
# ACCIDENT DETECTION
# AI-Based EV Accident / Collision Detection
# ============================================================

class AccidentDetection(models.Model):

    ACCIDENT_TYPE_CHOICES = [
        ('collision', 'Vehicle Collision'),
        ('front_collision', 'Front Collision'),
        ('rear_collision', 'Rear Collision'),
        ('side_collision', 'Side Collision'),
        ('rollover', 'Vehicle Rollover'),
        ('pedestrian', 'Pedestrian Accident'),
        ('object_collision', 'Object Collision'),
        ('sudden_impact', 'Sudden Impact'),
        ('unknown', 'Unknown Accident'),
    ]

    SEVERITY_CHOICES = [
        ('minor', 'Minor'),
        ('moderate', 'Moderate'),
        ('serious', 'Serious'),
        ('critical', 'Critical'),
    ]

    STATUS_CHOICES = [
        ('detected', 'Detected'),
        ('verified', 'Verified'),
        ('emergency_sent', 'Emergency Sent'),
        ('assistance_requested', 'Assistance Requested'),
        ('resolved', 'Resolved'),
        ('false_alarm', 'False Alarm'),
    ]

    # --------------------------------------------------------
    # VEHICLE
    # --------------------------------------------------------

    vehicle = models.ForeignKey(
        'EVVehicle',
        on_delete=models.CASCADE,
        related_name='accident_detections'
    )

    # --------------------------------------------------------
    # USER / DRIVER
    # --------------------------------------------------------

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='accident_detections'
    )

    # --------------------------------------------------------
    # ACCIDENT INFORMATION
    # --------------------------------------------------------

    accident_type = models.CharField(
        max_length=30,
        choices=ACCIDENT_TYPE_CHOICES,
        default='unknown'
    )

    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        default='minor'
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='detected'
    )

    title = models.CharField(
        max_length=200,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # LOCATION
    # --------------------------------------------------------

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    district = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    # --------------------------------------------------------
    # VEHICLE DATA
    # --------------------------------------------------------

    vehicle_speed = models.FloatField(
        default=0.0
    )

    speed_before_accident = models.FloatField(
        default=0.0
    )

    speed_after_accident = models.FloatField(
        default=0.0
    )

    battery_percentage = models.FloatField(
        null=True,
        blank=True
    )

    # --------------------------------------------------------
    # SENSOR / IMPACT DATA
    # --------------------------------------------------------

    impact_force = models.FloatField(
        default=0.0
    )

    acceleration_force = models.FloatField(
        default=0.0
    )

    sudden_deceleration = models.BooleanField(
        default=False
    )

    airbag_deployed = models.BooleanField(
        default=False
    )

    rollover_detected = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # DRIVER / PASSENGER SAFETY
    # --------------------------------------------------------

    driver_response_received = models.BooleanField(
        default=False
    )

    driver_safe = models.BooleanField(
        null=True,
        blank=True
    )

    passenger_count = models.PositiveIntegerField(
        default=1
    )

    injuries_reported = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # AI ACCIDENT DETECTION
    # --------------------------------------------------------

    ai_detected = models.BooleanField(
        default=True
    )

    accident_probability = models.FloatField(
        default=0.0,
        help_text='AI accident probability from 0 to 100'
    )

    ai_confidence = models.FloatField(
        default=0.0
    )

    ai_risk_score = models.FloatField(
        default=0.0
    )

    ai_analysis = models.TextField(
        blank=True
    )

    ai_recommendation = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # EMERGENCY RESPONSE
    # --------------------------------------------------------

    emergency_required = models.BooleanField(
        default=False
    )

    sos_triggered = models.BooleanField(
        default=False
    )

    ambulance_requested = models.BooleanField(
        default=False
    )

    police_requested = models.BooleanField(
        default=False
    )

    roadside_assistance_requested = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # CONTACT / NOTIFICATION
    # --------------------------------------------------------

    emergency_contact_notified = models.BooleanField(
        default=False
    )

    owner_notified = models.BooleanField(
        default=False
    )

    notification_sent = models.BooleanField(
        default=False
    )

    sms_sent = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # EVIDENCE / EXTRA DATA
    # --------------------------------------------------------

    sensor_data = models.JSONField(
        default=dict,
        blank=True
    )

    accident_data = models.JSONField(
        default=dict,
        blank=True
    )

    notes = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # RESOLUTION
    # --------------------------------------------------------

    resolution_notes = models.TextField(
        blank=True
    )

    resolved_at = models.DateTimeField(
        null=True,
        blank=True
    )

    # --------------------------------------------------------
    # TIMESTAMPS
    # --------------------------------------------------------

    detected_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-detected_at']

        indexes = [
            models.Index(
                fields=['vehicle', '-detected_at']
            ),
            models.Index(
                fields=['accident_type']
            ),
            models.Index(
                fields=['severity']
            ),
            models.Index(
                fields=['status']
            ),
            models.Index(
                fields=['emergency_required']
            ),
        ]

    def __str__(self):
        return (
            f"{self.vehicle} - "
            f"{self.get_accident_type_display()} - "
            f"{self.get_severity_display()}"
        )

    # --------------------------------------------------------
    # AUTOMATIC SEVERITY
    # --------------------------------------------------------

    def update_severity(self):

        if (
            self.rollover_detected
            or self.airbag_deployed
            or self.injuries_reported
            or self.ai_risk_score >= 80
        ):
            self.severity = 'critical'
            self.emergency_required = True

        elif (
            self.impact_force >= 70
            or self.ai_risk_score >= 60
        ):
            self.severity = 'serious'
            self.emergency_required = True

        elif (
            self.impact_force >= 30
            or self.ai_risk_score >= 30
        ):
            self.severity = 'moderate'

        else:
            self.severity = 'minor'

    # --------------------------------------------------------
    # TRIGGER SOS
    # --------------------------------------------------------

    def trigger_sos(self):

        self.sos_triggered = True
        self.emergency_required = True
        self.status = 'emergency_sent'

        self.save(
            update_fields=[
                'sos_triggered',
                'emergency_required',
                'status',
                'updated_at'
            ]
        )

    # --------------------------------------------------------
    # RESOLVE ACCIDENT
    # --------------------------------------------------------

    def resolve(self, notes=''):

        from django.utils import timezone

        self.status = 'resolved'
        self.resolved_at = timezone.now()

        if notes:
            self.resolution_notes = notes

        self.save()

    # --------------------------------------------------------
    # FALSE ALARM
    # --------------------------------------------------------

    def mark_false_alarm(self):

        from django.utils import timezone

        self.status = 'false_alarm'
        self.emergency_required = False
        self.resolved_at = timezone.now()

        self.save()

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    def save(self, *args, **kwargs):

        self.update_severity()

        super().save(*args, **kwargs)
          # ============================================================
# EMERGENCY CONTACT
# Stores emergency contacts for EV users
# ============================================================

class EmergencyContact(models.Model):

    RELATIONSHIP_CHOICES = [
        ('parent', 'Parent'),
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('spouse', 'Spouse'),
        ('brother', 'Brother'),
        ('sister', 'Sister'),
        ('friend', 'Friend'),
        ('guardian', 'Guardian'),
        ('relative', 'Relative'),
        ('doctor', 'Doctor'),
        ('other', 'Other'),
    ]

    # User who owns this emergency contact
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='emergency_contacts'
    )

    # Contact details
    name = models.CharField(
        max_length=150
    )

    relationship = models.CharField(
        max_length=30,
        choices=RELATIONSHIP_CHOICES,
        default='other'
    )

    phone_number = models.CharField(
        max_length=20
    )

    alternate_phone_number = models.CharField(
        max_length=20,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    # Address
    address = models.TextField(
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    pincode = models.CharField(
        max_length=10,
        blank=True
    )

    # Priority
    priority = models.PositiveSmallIntegerField(
        default=1,
        help_text='1 = highest priority'
    )

    is_primary = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    # Emergency permissions
    notify_on_accident = models.BooleanField(
        default=True
    )

    notify_on_sos = models.BooleanField(
        default=True
    )

    notify_on_security_event = models.BooleanField(
        default=True
    )

    notify_on_geofence_breach = models.BooleanField(
        default=False
    )

    # Notification methods
    sms_enabled = models.BooleanField(
        default=True
    )

    call_enabled = models.BooleanField(
        default=True
    )

    email_enabled = models.BooleanField(
        default=False
    )

    whatsapp_enabled = models.BooleanField(
        default=False
    )

    # Optional medical/emergency note
    emergency_notes = models.TextField(
        blank=True
    )

    # Notification tracking
    last_notified_at = models.DateTimeField(
        null=True,
        blank=True
    )

    notification_count = models.PositiveIntegerField(
        default=0
    )

    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            'priority',
            '-is_primary',
            'name'
        ]

        indexes = [
            models.Index(
                fields=['user', 'is_active']
            ),
            models.Index(
                fields=['user', 'is_primary']
            ),
            models.Index(
                fields=['priority']
            ),
        ]

    def __str__(self):
        return (
            f"{self.name} - "
            f"{self.get_relationship_display()} - "
            f"{self.phone_number}"
        )

    def mark_notified(self):
        """
        Record that this emergency contact
        has received an emergency notification.
        """

        from django.utils import timezone

        self.last_notified_at = timezone.now()
        self.notification_count += 1

        self.save(
            update_fields=[
                'last_notified_at',
                'notification_count',
                'updated_at'
            ]
        )
        # ============================================================
# DRIVER PROFILE
# Driver Information, Licence & EV Driving Preferences
# ============================================================

class DriverProfile(models.Model):

    EXPERIENCE_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('experienced', 'Experienced'),
        ('professional', 'Professional'),
    ]

    DRIVING_STYLE_CHOICES = [
        ('eco', 'Eco'),
        ('normal', 'Normal'),
        ('sport', 'Sport'),
        ('adaptive', 'Adaptive'),
    ]

    # --------------------------------------------------------
    # USER
    # --------------------------------------------------------

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='driver_profile'
    )

    # --------------------------------------------------------
    # BASIC INFORMATION
    # --------------------------------------------------------

    full_name = models.CharField(
        max_length=150,
        blank=True
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    profile_photo = models.ImageField(
        upload_to='driver_profiles/',
        null=True,
        blank=True
    )

    # --------------------------------------------------------
    # DRIVING LICENCE
    # --------------------------------------------------------

    driving_license_number = models.CharField(
        max_length=50,
        blank=True
    )

    license_issue_date = models.DateField(
        null=True,
        blank=True
    )

    license_expiry_date = models.DateField(
        null=True,
        blank=True
    )

    license_verified = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # ADDRESS
    # --------------------------------------------------------

    address = models.TextField(
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    pincode = models.CharField(
        max_length=10,
        blank=True
    )

    country = models.CharField(
        max_length=100,
        default='India'
    )

    # --------------------------------------------------------
    # DRIVING EXPERIENCE
    # --------------------------------------------------------

    driving_experience_years = models.PositiveIntegerField(
        default=0
    )

    experience_level = models.CharField(
        max_length=20,
        choices=EXPERIENCE_CHOICES,
        default='beginner'
    )

    preferred_driving_style = models.CharField(
        max_length=20,
        choices=DRIVING_STYLE_CHOICES,
        default='normal'
    )

    # --------------------------------------------------------
    # DRIVING STATISTICS
    # --------------------------------------------------------

    total_trips = models.PositiveIntegerField(
        default=0
    )

    total_distance_km = models.FloatField(
        default=0.0
    )

    total_driving_hours = models.FloatField(
        default=0.0
    )

    average_speed = models.FloatField(
        default=0.0
    )

    # --------------------------------------------------------
    # DRIVER SCORE
    # --------------------------------------------------------

    driver_score = models.FloatField(
        default=100.0
    )

    safety_score = models.FloatField(
        default=100.0
    )

    eco_score = models.FloatField(
        default=100.0
    )

    efficiency_score = models.FloatField(
        default=100.0
    )

    # --------------------------------------------------------
    # DRIVING EVENTS
    # --------------------------------------------------------

    harsh_braking_count = models.PositiveIntegerField(
        default=0
    )

    harsh_acceleration_count = models.PositiveIntegerField(
        default=0
    )

    speeding_count = models.PositiveIntegerField(
        default=0
    )

    accident_count = models.PositiveIntegerField(
        default=0
    )

    # --------------------------------------------------------
    # EV PREFERENCES
    # --------------------------------------------------------

    preferred_charging_percentage = models.FloatField(
        default=80.0
    )

    minimum_battery_alert = models.FloatField(
        default=20.0
    )

    prefer_fast_charging = models.BooleanField(
        default=False
    )

    prefer_low_cost_charging = models.BooleanField(
        default=True
    )

    prefer_renewable_charging = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # ROUTE PREFERENCES
    # --------------------------------------------------------

    avoid_tolls = models.BooleanField(
        default=False
    )

    avoid_highways = models.BooleanField(
        default=False
    )

    prefer_shortest_route = models.BooleanField(
        default=False
    )

    prefer_energy_efficient_route = models.BooleanField(
        default=True
    )

    # --------------------------------------------------------
    # INDIA-SPECIFIC SETTINGS
    # --------------------------------------------------------

    preferred_language = models.CharField(
        max_length=10,
        choices=[
            ('en', 'English'),
            ('hi', 'हिंदी'),
        ],
        default='en'
    )

    fastag_enabled = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # SAFETY
    # --------------------------------------------------------

    emergency_sos_enabled = models.BooleanField(
        default=True
    )

    accident_detection_enabled = models.BooleanField(
        default=True
    )

    geofence_alerts_enabled = models.BooleanField(
        default=True
    )

    security_alerts_enabled = models.BooleanField(
        default=True
    )

    # --------------------------------------------------------
    # NOTIFICATIONS
    # --------------------------------------------------------

    push_notifications = models.BooleanField(
        default=True
    )

    email_notifications = models.BooleanField(
        default=True
    )

    sms_notifications = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # ACCOUNT STATUS
    # --------------------------------------------------------

    is_verified = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    # --------------------------------------------------------
    # TIMESTAMPS
    # --------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['city', 'state']),
            models.Index(fields=['is_verified']),
            models.Index(fields=['driver_score']),
        ]

    def __str__(self):

        if self.full_name:
            return self.full_name

        return self.user.username

    # --------------------------------------------------------
    # CALCULATE DRIVER SCORE
    # --------------------------------------------------------

    def calculate_driver_score(self):

        penalty = (
            self.harsh_braking_count * 0.5
            + self.harsh_acceleration_count * 0.5
            + self.speeding_count * 1.0
            + self.accident_count * 10
        )

        score = 100 - penalty

        return max(
            0.0,
            min(100.0, score)
        )

    # --------------------------------------------------------
    # UPDATE EXPERIENCE LEVEL
    # --------------------------------------------------------

    def update_experience_level(self):

        years = self.driving_experience_years

        if years >= 10:
            self.experience_level = 'professional'

        elif years >= 5:
            self.experience_level = 'experienced'

        elif years >= 2:
            self.experience_level = 'intermediate'

        else:
            self.experience_level = 'beginner'

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    def save(self, *args, **kwargs):

        self.driver_score = (
            self.calculate_driver_score()
        )

        self.update_experience_level()

        super().save(*args, **kwargs)
        # ============================================================
# FLEET MODEL
# EV Fleet Management
# ============================================================

class Fleet(models.Model):

    FLEET_TYPE_CHOICES = [
        ('personal', 'Personal Fleet'),
        ('commercial', 'Commercial Fleet'),
        ('taxi', 'Taxi / Cab Fleet'),
        ('delivery', 'Delivery Fleet'),
        ('logistics', 'Logistics Fleet'),
        ('corporate', 'Corporate Fleet'),
        ('government', 'Government Fleet'),
        ('rental', 'Rental Fleet'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Under Maintenance'),
        ('suspended', 'Suspended'),
    ]

    # Fleet owner / manager
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='fleets'
    )

    # Basic information
    name = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    fleet_type = models.CharField(
        max_length=30,
        choices=FLEET_TYPE_CHOICES,
        default='personal'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    # Vehicles
    vehicles = models.ManyToManyField(
        'EVVehicle',
        related_name='fleets',
        blank=True
    )

    # Company information
    company_name = models.CharField(
        max_length=150,
        blank=True
    )

    contact_number = models.CharField(
        max_length=20,
        blank=True
    )

    contact_email = models.EmailField(
        blank=True
    )

    # Location
    address = models.TextField(
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    pincode = models.CharField(
        max_length=10,
        blank=True
    )

    country = models.CharField(
        max_length=100,
        default='India'
    )

    # Fleet statistics
    total_distance_km = models.FloatField(
        default=0.0
    )

    total_energy_consumed_kwh = models.FloatField(
        default=0.0
    )

    total_charging_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    average_battery_health = models.FloatField(
        default=100.0
    )

    average_efficiency = models.FloatField(
        default=0.0
    )

    # Environmental statistics
    total_co2_saved_kg = models.FloatField(
        default=0.0
    )

    green_score = models.FloatField(
        default=0.0
    )

    # AI fleet management
    ai_optimization_enabled = models.BooleanField(
        default=True
    )

    ai_risk_score = models.FloatField(
        default=0.0
    )

    ai_recommendation = models.TextField(
        blank=True
    )

    # Fleet controls
    geofence_enabled = models.BooleanField(
        default=False
    )

    speed_monitoring_enabled = models.BooleanField(
        default=True
    )

    predictive_maintenance_enabled = models.BooleanField(
        default=True
    )

    charging_optimization_enabled = models.BooleanField(
        default=True
    )

    # Alerts
    low_battery_alerts = models.BooleanField(
        default=True
    )

    maintenance_alerts = models.BooleanField(
        default=True
    )

    security_alerts = models.BooleanField(
        default=True
    )

    accident_alerts = models.BooleanField(
        default=True
    )

    # Status
    is_active = models.BooleanField(
        default=True
    )

    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['name']

        indexes = [
            models.Index(fields=['owner', 'is_active']),
            models.Index(fields=['fleet_type']),
            models.Index(fields=['status']),
            models.Index(fields=['city', 'state']),
        ]

    def __str__(self):
        return self.name

    @property
    def total_vehicles(self):
        return self.vehicles.count()

    @property
    def active_vehicles(self):
        """
        Count active/driving vehicles when EVVehicle
        contains a status field.
        """
        try:
            return self.vehicles.filter(
                status__in=['active', 'driving', 'charging']
            ).count()
        except Exception:
            return self.vehicles.count()

    def calculate_average_battery_health(self):
        """
        Calculate average battery health if EVVehicle
        contains battery_percentage.
        """

        vehicles = self.vehicles.all()

        if not vehicles.exists():
            return 0.0

        values = []

        for vehicle in vehicles:
            value = getattr(
                vehicle,
                'battery_percentage',
                None
            )

            if value is not None:
                values.append(float(value))

        if not values:
            return 0.0

        return round(
            sum(values) / len(values),
            2
        )

    def update_statistics(self):
        """
        Refresh fleet statistics.
        """

        self.average_battery_health = (
            self.calculate_average_battery_health()
        )

        self.save(
            update_fields=[
                'average_battery_health',
                'updated_at'
            ]
        )
        # ============================================================
# FLEET DRIVER ASSIGNMENT
# Assign Drivers and Vehicles to EV Fleets
# ============================================================

class FleetDriverAssignment(models.Model):

    STATUS_CHOICES = [
        ('assigned', 'Assigned'),
        ('active', 'Active'),
        ('on_trip', 'On Trip'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('suspended', 'Suspended'),
    ]

    SHIFT_CHOICES = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
        ('night', 'Night'),
        ('full_day', 'Full Day'),
        ('custom', 'Custom'),
    ]

    # Fleet
    fleet = models.ForeignKey(
        'Fleet',
        on_delete=models.CASCADE,
        related_name='driver_assignments'
    )

    # Driver
    driver = models.ForeignKey(
        'DriverProfile',
        on_delete=models.CASCADE,
        related_name='fleet_assignments'
    )

    # Vehicle assigned to driver
    vehicle = models.ForeignKey(
        'EVVehicle',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='driver_assignments'
    )

    # Assignment status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='assigned'
    )

    is_active = models.BooleanField(
        default=True
    )

    # Shift information
    shift_type = models.CharField(
        max_length=20,
        choices=SHIFT_CHOICES,
        default='full_day'
    )

    shift_start_time = models.TimeField(
        null=True,
        blank=True
    )

    shift_end_time = models.TimeField(
        null=True,
        blank=True
    )

    # Assignment dates
    assigned_date = models.DateField(
        null=True,
        blank=True
    )

    start_date = models.DateField(
        null=True,
        blank=True
    )

    end_date = models.DateField(
        null=True,
        blank=True
    )

    # Route / duty information
    route_name = models.CharField(
        max_length=200,
        blank=True
    )

    start_location = models.CharField(
        max_length=200,
        blank=True
    )

    destination = models.CharField(
        max_length=200,
        blank=True
    )

    # Driver performance during assignment
    trips_completed = models.PositiveIntegerField(
        default=0
    )

    distance_driven_km = models.FloatField(
        default=0.0
    )

    energy_consumed_kwh = models.FloatField(
        default=0.0
    )

    average_speed = models.FloatField(
        default=0.0
    )

    # Safety
    harsh_braking_count = models.PositiveIntegerField(
        default=0
    )

    harsh_acceleration_count = models.PositiveIntegerField(
        default=0
    )

    speeding_events = models.PositiveIntegerField(
        default=0
    )

    accident_count = models.PositiveIntegerField(
        default=0
    )

    # Performance scores
    driver_score = models.FloatField(
        default=100.0
    )

    safety_score = models.FloatField(
        default=100.0
    )

    eco_score = models.FloatField(
        default=100.0
    )

    efficiency_score = models.FloatField(
        default=100.0
    )

    # Fleet manager notes
    notes = models.TextField(
        blank=True
    )

    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']

        indexes = [
            models.Index(
                fields=['fleet', 'status']
            ),
            models.Index(
                fields=['driver', 'is_active']
            ),
            models.Index(
                fields=['vehicle', 'is_active']
            ),
        ]

    def __str__(self):
        return (
            f"{self.driver} -> "
            f"{self.vehicle or 'No Vehicle'} -> "
            f"{self.fleet}"
        )

    def calculate_driver_score(self):
        """
        Calculate driver performance score.
        """

        penalty = (
            self.harsh_braking_count * 0.5
            + self.harsh_acceleration_count * 0.5
            + self.speeding_events * 1.0
            + self.accident_count * 10
        )

        return max(
            0.0,
            min(100.0, 100 - penalty)
        )

    def start_assignment(self):
        self.status = 'active'
        self.is_active = True

        self.save(
            update_fields=[
                'status',
                'is_active',
                'updated_at'
            ]
        )

    def start_trip(self):
        self.status = 'on_trip'
        self.is_active = True

        self.save(
            update_fields=[
                'status',
                'is_active',
                'updated_at'
            ]
        )

    def complete_assignment(self):
        from django.utils import timezone

        self.status = 'completed'
        self.is_active = False

        if self.end_date is None:
            self.end_date = timezone.localdate()

        self.save(
            update_fields=[
                'status',
                'is_active',
                'end_date',
                'updated_at'
            ]
        )

    def cancel_assignment(self):
        self.status = 'cancelled'
        self.is_active = False

        self.save(
            update_fields=[
                'status',
                'is_active',
                'updated_at'
            ]
        )

    def save(self, *args, **kwargs):
        self.driver_score = self.calculate_driver_score()

        super().save(*args, **kwargs)
           # ============================================================
# RENEWABLE ENERGY USAGE
# Tracks Renewable Energy Used for EV Charging
# ============================================================

class RenewableEnergyUsage(models.Model):

    ENERGY_SOURCE_CHOICES = [
        ('solar', 'Solar Energy'),
        ('wind', 'Wind Energy'),
        ('hydro', 'Hydroelectric Energy'),
        ('biomass', 'Biomass Energy'),
        ('grid_green', 'Green Grid Energy'),
        ('mixed', 'Mixed Renewable Energy'),
        ('other', 'Other Renewable Source'),
    ]

    STATUS_CHOICES = [
        ('recorded', 'Recorded'),
        ('verified', 'Verified'),
        ('estimated', 'Estimated'),
        ('completed', 'Completed'),
    ]

    # Vehicle
    vehicle = models.ForeignKey(
        'EVVehicle',
        on_delete=models.CASCADE,
        related_name='renewable_energy_usage'
    )

    # User
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='renewable_energy_usage'
    )

    # Charging station
    station = models.ForeignKey(
        'ChargingStation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='renewable_energy_usage'
    )

    # Energy source
    energy_source = models.CharField(
        max_length=30,
        choices=ENERGY_SOURCE_CHOICES,
        default='solar'
    )

    # Energy data
    total_energy_kwh = models.FloatField(
        default=0.0
    )

    renewable_energy_kwh = models.FloatField(
        default=0.0
    )

    grid_energy_kwh = models.FloatField(
        default=0.0
    )

    renewable_percentage = models.FloatField(
        default=0.0
    )

    # Solar-specific information
    solar_energy_kwh = models.FloatField(
        default=0.0
    )

    solar_generation_kwh = models.FloatField(
        default=0.0
    )

    # Wind
    wind_energy_kwh = models.FloatField(
        default=0.0
    )

    # Hydro
    hydro_energy_kwh = models.FloatField(
        default=0.0
    )

    # Charging information
    charging_session_id = models.CharField(
        max_length=100,
        blank=True
    )

    charging_duration_minutes = models.PositiveIntegerField(
        default=0
    )

    battery_before = models.FloatField(
        default=0.0
    )

    battery_after = models.FloatField(
        default=0.0
    )

    # Cost
    renewable_energy_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    grid_energy_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    total_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    money_saved = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # Environmental impact
    co2_saved_kg = models.FloatField(
        default=0.0
    )

    carbon_reduction_percentage = models.FloatField(
        default=0.0
    )

    green_points = models.PositiveIntegerField(
        default=0
    )

    # Location
    city = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    # AI / smart charging
    ai_optimized = models.BooleanField(
        default=False
    )

    ai_recommendation = models.TextField(
        blank=True
    )

    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='recorded'
    )

    is_verified = models.BooleanField(
        default=False
    )

    # Dates
    usage_date = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']

        indexes = [
            models.Index(
                fields=['vehicle', '-created_at']
            ),
            models.Index(
                fields=['station', '-created_at']
            ),
            models.Index(
                fields=['energy_source']
            ),
            models.Index(
                fields=['usage_date']
            ),
        ]

    def __str__(self):
        return (
            f"{self.vehicle} - "
            f"{self.get_energy_source_display()} - "
            f"{self.renewable_energy_kwh:.2f} kWh"
        )

    def calculate_renewable_percentage(self):
        if self.total_energy_kwh <= 0:
            return 0.0

        percentage = (
            self.renewable_energy_kwh
            / self.total_energy_kwh
        ) * 100

        return round(
            min(percentage, 100.0),
            2
        )

    def calculate_co2_saving(self):
        """
        Approximate CO2 saving for dashboard analytics.
        """
        return round(
            self.renewable_energy_kwh * 0.7,
            2
        )

    def calculate_green_points(self):
        return max(
            int(self.renewable_energy_kwh * 10),
            0
        )

    def save(self, *args, **kwargs):

        # Prevent negative values
        self.total_energy_kwh = max(
            self.total_energy_kwh,
            0
        )

        self.renewable_energy_kwh = max(
            self.renewable_energy_kwh,
            0
        )

        self.grid_energy_kwh = max(
            self.grid_energy_kwh,
            0
        )

        self.renewable_percentage = (
            self.calculate_renewable_percentage()
        )

        self.co2_saved_kg = (
            self.calculate_co2_saving()
        )

        self.green_points = (
            self.calculate_green_points()
        )

        super().save(*args, **kwargs)

        # ============================================================
# VEHICLE TO GRID TRANSACTION
# V2G Energy Transfer & Revenue Tracking
# ============================================================

class VehicleToGridTransaction(models.Model):

    TRANSACTION_TYPE_CHOICES = [
        ('grid_to_vehicle', 'Grid to Vehicle'),
        ('vehicle_to_grid', 'Vehicle to Grid'),
        ('vehicle_to_home', 'Vehicle to Home'),
        ('vehicle_to_building', 'Vehicle to Building'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('scheduled', 'Scheduled'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('failed', 'Failed'),
    ]

    ENERGY_SOURCE_CHOICES = [
        ('grid', 'Electric Grid'),
        ('solar', 'Solar'),
        ('wind', 'Wind'),
        ('renewable', 'Renewable Energy'),
        ('mixed', 'Mixed Energy'),
    ]

    # --------------------------------------------------------
    # USER
    # --------------------------------------------------------

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='v2g_transactions'
    )

    # --------------------------------------------------------
    # VEHICLE
    # --------------------------------------------------------

    vehicle = models.ForeignKey(
        'EVVehicle',
        on_delete=models.CASCADE,
        related_name='v2g_transactions'
    )

    # --------------------------------------------------------
    # CHARGING STATION
    # --------------------------------------------------------

    station = models.ForeignKey(
        'ChargingStation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='v2g_transactions'
    )

    # --------------------------------------------------------
    # TRANSACTION INFORMATION
    # --------------------------------------------------------

    transaction_type = models.CharField(
        max_length=30,
        choices=TRANSACTION_TYPE_CHOICES,
        default='vehicle_to_grid'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    transaction_reference = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True
    )

    # --------------------------------------------------------
    # ENERGY
    # --------------------------------------------------------

    energy_source = models.CharField(
        max_length=20,
        choices=ENERGY_SOURCE_CHOICES,
        default='grid'
    )

    energy_kwh = models.FloatField(
        default=0.0
    )

    power_kw = models.FloatField(
        default=0.0
    )

    # --------------------------------------------------------
    # BATTERY
    # --------------------------------------------------------

    battery_before_percentage = models.FloatField(
        default=0.0
    )

    battery_after_percentage = models.FloatField(
        default=0.0
    )

    battery_capacity_kwh = models.FloatField(
        default=0.0
    )

    minimum_battery_percentage = models.FloatField(
        default=20.0
    )

    # --------------------------------------------------------
    # ELECTRICITY PRICE / PAYMENT
    # --------------------------------------------------------

    price_per_kwh = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    grid_credit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    # --------------------------------------------------------
    # GRID INFORMATION
    # --------------------------------------------------------

    grid_demand_percentage = models.FloatField(
        default=0.0
    )

    grid_frequency = models.FloatField(
        default=50.0,
        help_text='Grid frequency in Hz'
    )

    peak_demand = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # SMART GRID / AI
    # --------------------------------------------------------

    ai_optimized = models.BooleanField(
        default=False
    )

    ai_score = models.FloatField(
        default=0.0
    )

    ai_recommendation = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # RENEWABLE ENERGY
    # --------------------------------------------------------

    renewable_energy_percentage = models.FloatField(
        default=0.0
    )

    carbon_saving_kg = models.FloatField(
        default=0.0
    )

    # --------------------------------------------------------
    # LOCATION
    # --------------------------------------------------------

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    # --------------------------------------------------------
    # SCHEDULING
    # --------------------------------------------------------

    scheduled_start = models.DateTimeField(
        null=True,
        blank=True
    )

    scheduled_end = models.DateTimeField(
        null=True,
        blank=True
    )

    started_at = models.DateTimeField(
        null=True,
        blank=True
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    # --------------------------------------------------------
    # NOTES
    # --------------------------------------------------------

    notes = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # TIMESTAMPS
    # --------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']

        indexes = [
            models.Index(
                fields=['vehicle', '-created_at']
            ),
            models.Index(
                fields=['transaction_type']
            ),
            models.Index(
                fields=['status']
            ),
            models.Index(
                fields=['station', '-created_at']
            ),
        ]

    def __str__(self):
        return (
            f"{self.vehicle} - "
            f"{self.get_transaction_type_display()} - "
            f"{self.energy_kwh:.2f} kWh"
        )

    # --------------------------------------------------------
    # CALCULATE AMOUNT
    # --------------------------------------------------------

    def calculate_total_amount(self):

        from decimal import Decimal

        energy = Decimal(str(max(self.energy_kwh, 0)))
        price = self.price_per_kwh or Decimal('0')

        return energy * price

    # --------------------------------------------------------
    # CHECK V2G SAFETY
    # --------------------------------------------------------

    def can_export_energy(self):
        """
        Prevent V2G discharge if battery would fall
        below the configured minimum battery level.
        """

        if self.transaction_type != 'vehicle_to_grid':
            return True

        return (
            self.battery_after_percentage
            >= self.minimum_battery_percentage
        )

    # --------------------------------------------------------
    # START TRANSACTION
    # --------------------------------------------------------

    def start_transaction(self):

        from django.utils import timezone

        self.status = 'active'
        self.started_at = timezone.now()

        self.save(
            update_fields=[
                'status',
                'started_at',
                'updated_at'
            ]
        )

    # --------------------------------------------------------
    # COMPLETE TRANSACTION
    # --------------------------------------------------------

    def complete_transaction(self):

        from django.utils import timezone

        self.status = 'completed'
        self.completed_at = timezone.now()

        self.save(
            update_fields=[
                'status',
                'completed_at',
                'updated_at'
            ]
        )

    # --------------------------------------------------------
    # CANCEL TRANSACTION
    # --------------------------------------------------------

    def cancel_transaction(self):

        self.status = 'cancelled'

        self.save(
            update_fields=[
                'status',
                'updated_at'
            ]
        )

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    def save(self, *args, **kwargs):

        self.energy_kwh = max(
            self.energy_kwh,
            0.0
        )

        self.total_amount = (
            self.calculate_total_amount()
        )

        # Grid credit is money earned by exporting energy
        if self.transaction_type == 'vehicle_to_grid':
            self.grid_credit = self.total_amount

        super().save(*args, **kwargs)
          # ============================================================
# TRIP RISK ANALYSIS
# AI-Based EV Trip Safety & Risk Prediction
# ============================================================

class TripRiskAnalysis(models.Model):

    RISK_LEVEL_CHOICES = [
        ('low', 'Low Risk'),
        ('moderate', 'Moderate Risk'),
        ('high', 'High Risk'),
        ('critical', 'Critical Risk'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('analyzed', 'Analyzed'),
        ('warning', 'Warning Issued'),
        ('completed', 'Completed'),
    ]

    # Vehicle
    vehicle = models.ForeignKey(
        'EVVehicle',
        on_delete=models.CASCADE,
        related_name='trip_risk_analyses'
    )

    # Driver
    driver = models.ForeignKey(
        'DriverProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='trip_risk_analyses'
    )

    # User
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='trip_risk_analyses'
    )

    # Trip information
    trip_name = models.CharField(
        max_length=200,
        blank=True
    )

    start_location = models.CharField(
        max_length=200,
        blank=True
    )

    destination = models.CharField(
        max_length=200,
        blank=True
    )

    distance_km = models.FloatField(
        default=0.0
    )

    estimated_duration_minutes = models.PositiveIntegerField(
        default=0
    )

    # Coordinates
    start_latitude = models.FloatField(
        null=True,
        blank=True
    )

    start_longitude = models.FloatField(
        null=True,
        blank=True
    )

    destination_latitude = models.FloatField(
        null=True,
        blank=True
    )

    destination_longitude = models.FloatField(
        null=True,
        blank=True
    )

    # Battery risk
    battery_start_percentage = models.FloatField(
        default=100.0
    )

    predicted_battery_end_percentage = models.FloatField(
        default=0.0
    )

    battery_risk_score = models.FloatField(
        default=0.0
    )

    charging_stop_required = models.BooleanField(
        default=False
    )

    # Traffic risk
    traffic_level = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('moderate', 'Moderate'),
            ('heavy', 'Heavy'),
            ('severe', 'Severe'),
        ],
        default='low'
    )

    traffic_risk_score = models.FloatField(
        default=0.0
    )

    # Weather risk
    weather_condition = models.CharField(
        max_length=50,
        blank=True
    )

    temperature = models.FloatField(
        null=True,
        blank=True
    )

    visibility_km = models.FloatField(
        default=10.0
    )

    weather_risk_score = models.FloatField(
        default=0.0
    )

    # Road risk
    road_condition = models.CharField(
        max_length=30,
        choices=[
            ('good', 'Good'),
            ('average', 'Average'),
            ('poor', 'Poor'),
            ('wet', 'Wet'),
            ('foggy', 'Foggy'),
            ('waterlogged', 'Waterlogged'),
            ('dangerous', 'Dangerous'),
        ],
        default='good'
    )

    road_risk_score = models.FloatField(
        default=0.0
    )

    # Driver risk
    driver_risk_score = models.FloatField(
        default=0.0
    )

    speeding_risk = models.BooleanField(
        default=False
    )

    fatigue_risk = models.BooleanField(
        default=False
    )

    harsh_driving_risk = models.BooleanField(
        default=False
    )

    # Overall AI analysis
    overall_risk_score = models.FloatField(
        default=0.0
    )

    risk_level = models.CharField(
        max_length=20,
        choices=RISK_LEVEL_CHOICES,
        default='low'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    ai_confidence = models.FloatField(
        default=0.0
    )

    ai_analysis = models.TextField(
        blank=True
    )

    ai_recommendation = models.TextField(
        blank=True
    )

    # India-specific risks
    monsoon_risk = models.BooleanField(
        default=False
    )

    fog_risk = models.BooleanField(
        default=False
    )

    heatwave_risk = models.BooleanField(
        default=False
    )

    festival_traffic_risk = models.BooleanField(
        default=False
    )

    # Safety recommendations
    recommended_speed_kmh = models.FloatField(
        default=80.0
    )

    rest_stop_recommended = models.BooleanField(
        default=False
    )

    alternate_route_recommended = models.BooleanField(
        default=False
    )

    emergency_warning = models.BooleanField(
        default=False
    )

    # Additional information
    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['vehicle', '-created_at']),
            models.Index(fields=['risk_level']),
            models.Index(fields=['status']),
            models.Index(fields=['overall_risk_score']),
        ]

    def __str__(self):
        return (
            f"{self.vehicle} - "
            f"{self.start_location} → {self.destination} - "
            f"{self.get_risk_level_display()}"
        )

    def calculate_overall_risk(self):
        """
        Calculate overall trip risk using battery,
        traffic, weather, road and driver risks.
        """

        scores = [
            self.battery_risk_score,
            self.traffic_risk_score,
            self.weather_risk_score,
            self.road_risk_score,
            self.driver_risk_score,
        ]

        scores = [
            max(0.0, min(100.0, float(score or 0)))
            for score in scores
        ]

        return round(sum(scores) / len(scores), 2)

    def update_risk_level(self):

        score = self.overall_risk_score

        if score >= 80:
            self.risk_level = 'critical'
            self.emergency_warning = True

        elif score >= 60:
            self.risk_level = 'high'

        elif score >= 30:
            self.risk_level = 'moderate'

        else:
            self.risk_level = 'low'

    def analyze_trip(self):

        self.overall_risk_score = (
            self.calculate_overall_risk()
        )

        self.update_risk_level()

        self.status = 'analyzed'

        if self.overall_risk_score >= 60:
            self.status = 'warning'

        self.save()

    def save(self, *args, **kwargs):

        self.overall_risk_score = (
            self.calculate_overall_risk()
        )

        self.update_risk_level()

        super().save(*args, **kwargs)


# ============================================================
# AI ASSISTANT CONVERSATION
# Stores EV AI Assistant Conversations
# ============================================================

class AIAssistantConversation(models.Model):

    CONVERSATION_TYPE_CHOICES = [
        ('general', 'General EV Assistance'),
        ('battery', 'Battery Assistance'),
        ('charging', 'Charging Assistance'),
        ('route', 'Route Planning'),
        ('traffic', 'Traffic Assistance'),
        ('weather', 'Weather Assistance'),
        ('maintenance', 'Maintenance Assistance'),
        ('emergency', 'Emergency Assistance'),
        ('cost', 'Charging Cost Assistance'),
        ('vehicle', 'Vehicle Assistance'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ]

    # --------------------------------------------------------
    # USER
    # --------------------------------------------------------

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ai_assistant_conversations'
    )

    # --------------------------------------------------------
    # VEHICLE (OPTIONAL)
    # --------------------------------------------------------

    vehicle = models.ForeignKey(
        'EVVehicle',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ai_assistant_conversations'
    )

    # --------------------------------------------------------
    # CONVERSATION INFORMATION
    # --------------------------------------------------------

    title = models.CharField(
        max_length=200,
        blank=True
    )

    conversation_type = models.CharField(
        max_length=30,
        choices=CONVERSATION_TYPE_CHOICES,
        default='general'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    # --------------------------------------------------------
    # USER MESSAGE
    # --------------------------------------------------------

    user_message = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # AI RESPONSE
    # --------------------------------------------------------

    ai_response = models.TextField(
        blank=True
    )

    ai_recommendation = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # AI INFORMATION
    # --------------------------------------------------------

    ai_model = models.CharField(
        max_length=100,
        blank=True
    )

    ai_confidence = models.FloatField(
        default=0.0
    )

    intent = models.CharField(
        max_length=100,
        blank=True
    )

    # --------------------------------------------------------
    # LANGUAGE
    # --------------------------------------------------------

    language = models.CharField(
        max_length=10,
        choices=[
            ('en', 'English'),
            ('hi', 'हिंदी'),
        ],
        default='en'
    )

    # --------------------------------------------------------
    # EV CONTEXT
    # --------------------------------------------------------

    battery_percentage = models.FloatField(
        null=True,
        blank=True
    )

    estimated_range_km = models.FloatField(
        null=True,
        blank=True
    )

    vehicle_speed = models.FloatField(
        null=True,
        blank=True
    )

    # --------------------------------------------------------
    # LOCATION
    # --------------------------------------------------------

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    # --------------------------------------------------------
    # CONTEXT DATA
    # --------------------------------------------------------

    context_data = models.JSONField(
        default=dict,
        blank=True
    )

    # --------------------------------------------------------
    # RESPONSE FEATURES
    # --------------------------------------------------------

    route_suggested = models.BooleanField(
        default=False
    )

    charging_station_suggested = models.BooleanField(
        default=False
    )

    maintenance_suggested = models.BooleanField(
        default=False
    )

    emergency_suggested = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # USER FEEDBACK
    # --------------------------------------------------------

    helpful = models.BooleanField(
        null=True,
        blank=True
    )

    rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )

    feedback = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # TOKENS / PERFORMANCE
    # --------------------------------------------------------

    response_time_ms = models.PositiveIntegerField(
        default=0
    )

    tokens_used = models.PositiveIntegerField(
        default=0
    )

    # --------------------------------------------------------
    # TIMESTAMPS
    # --------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']

        indexes = [
            models.Index(
                fields=['user', '-created_at']
            ),
            models.Index(
                fields=['vehicle', '-created_at']
            ),
            models.Index(
                fields=['conversation_type']
            ),
            models.Index(
                fields=['status']
            ),
        ]

    def __str__(self):

        title = self.title or self.conversation_type

        return f"{self.user} - {title}"

    # --------------------------------------------------------
    # MARK COMPLETE
    # --------------------------------------------------------

    def complete_conversation(self):

        self.status = 'completed'

        self.save(
            update_fields=[
                'status',
                'updated_at'
            ]
        )

    # --------------------------------------------------------
    # ARCHIVE
    # --------------------------------------------------------

    def archive_conversation(self):

        self.status = 'archived'

        self.save(
            update_fields=[
                'status',
                'updated_at'
            ]
        )
        # ============================================================
# EV USER PREFERENCE
# Stores personalized EV user settings and preferences
# ============================================================

class EVUserPreference(models.Model):

    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('hi', 'हिंदी'),
    ]

    ROUTE_CHOICES = [
        ('fastest', 'Fastest Route'),
        ('shortest', 'Shortest Route'),
        ('eco', 'Eco-Friendly Route'),
        ('charging', 'Charging Optimized Route'),
        ('balanced', 'Balanced Route'),
    ]

    CHARGING_CHOICES = [
        ('fast', 'Fast Charging'),
        ('cheap', 'Lowest Cost'),
        ('nearby', 'Nearest Station'),
        ('renewable', 'Renewable Energy'),
        ('balanced', 'Balanced'),
    ]

    # --------------------------------------------------------
    # USER
    # --------------------------------------------------------

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ev_preferences'
    )

    # --------------------------------------------------------
    # LANGUAGE & UI
    # --------------------------------------------------------

    preferred_language = models.CharField(
        max_length=10,
        choices=LANGUAGE_CHOICES,
        default='en'
    )

    dark_mode = models.BooleanField(
        default=False
    )

    show_hindi_labels = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # ROUTE PREFERENCES
    # --------------------------------------------------------

    preferred_route_type = models.CharField(
        max_length=20,
        choices=ROUTE_CHOICES,
        default='balanced'
    )

    avoid_tolls = models.BooleanField(
        default=False
    )

    avoid_highways = models.BooleanField(
        default=False
    )

    avoid_heavy_traffic = models.BooleanField(
        default=True
    )

    avoid_poor_roads = models.BooleanField(
        default=True
    )

    prefer_expressways = models.BooleanField(
        default=True
    )

    # --------------------------------------------------------
    # CHARGING PREFERENCES
    # --------------------------------------------------------

    preferred_charging_type = models.CharField(
        max_length=20,
        choices=CHARGING_CHOICES,
        default='balanced'
    )

    preferred_charge_limit = models.FloatField(
        default=80.0
    )

    minimum_battery_percentage = models.FloatField(
        default=20.0
    )

    reserve_battery_percentage = models.FloatField(
        default=15.0
    )

    prefer_fast_charging = models.BooleanField(
        default=True
    )

    prefer_low_cost_charging = models.BooleanField(
        default=False
    )

    prefer_renewable_energy = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # CHARGING NETWORKS
    # --------------------------------------------------------

    preferred_charging_network = models.CharField(
        max_length=100,
        blank=True
    )

    # Example:
    # ["Tata Power", "ChargeUp", "IOCL"]
    preferred_networks = models.JSONField(
        default=list,
        blank=True
    )

    # --------------------------------------------------------
    # PRICE SETTINGS
    # --------------------------------------------------------

    maximum_charging_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )

    show_charging_cost = models.BooleanField(
        default=True
    )

    # --------------------------------------------------------
    # WEATHER
    # --------------------------------------------------------

    weather_alerts = models.BooleanField(
        default=True
    )

    monsoon_alerts = models.BooleanField(
        default=True
    )

    fog_alerts = models.BooleanField(
        default=True
    )

    heatwave_alerts = models.BooleanField(
        default=True
    )

    storm_alerts = models.BooleanField(
        default=True
    )

    # --------------------------------------------------------
    # TRAFFIC
    # --------------------------------------------------------

    traffic_alerts = models.BooleanField(
        default=True
    )

    accident_alerts = models.BooleanField(
        default=True
    )

    congestion_alerts = models.BooleanField(
        default=True
    )

    # --------------------------------------------------------
    # VEHICLE
    # --------------------------------------------------------

    low_battery_alert = models.BooleanField(
        default=True
    )

    battery_health_alert = models.BooleanField(
        default=True
    )

    maintenance_alert = models.BooleanField(
        default=True
    )

    insurance_expiry_alert = models.BooleanField(
        default=True
    )

    document_expiry_alert = models.BooleanField(
        default=True
    )

    # --------------------------------------------------------
    # SAFETY
    # --------------------------------------------------------

    emergency_sos_enabled = models.BooleanField(
        default=True
    )

    accident_detection_enabled = models.BooleanField(
        default=True
    )

    roadside_assistance_enabled = models.BooleanField(
        default=True
    )

    security_alerts_enabled = models.BooleanField(
        default=True
    )

    geofence_alerts_enabled = models.BooleanField(
        default=True
    )

    # --------------------------------------------------------
    # AI FEATURES
    # --------------------------------------------------------

    ai_range_prediction = models.BooleanField(
        default=True
    )

    ai_route_recommendation = models.BooleanField(
        default=True
    )

    ai_charging_prediction = models.BooleanField(
        default=True
    )

    ai_maintenance_prediction = models.BooleanField(
        default=True
    )

    ai_trip_risk_analysis = models.BooleanField(
        default=True
    )

    ai_assistant_enabled = models.BooleanField(
        default=True
    )

    # --------------------------------------------------------
    # SMART CHARGING / V2G
    # --------------------------------------------------------

    smart_charging_enabled = models.BooleanField(
        default=False
    )

    vehicle_to_grid_enabled = models.BooleanField(
        default=False
    )

    renewable_charging_enabled = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # NOTIFICATIONS
    # --------------------------------------------------------

    push_notifications = models.BooleanField(
        default=True
    )

    email_notifications = models.BooleanField(
        default=True
    )

    sms_notifications = models.BooleanField(
        default=False
    )

    whatsapp_notifications = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # TRIP SETTINGS
    # --------------------------------------------------------

    recommended_rest_interval_km = models.PositiveIntegerField(
        default=120
    )

    show_toll_cost = models.BooleanField(
        default=True
    )

    show_trip_expenses = models.BooleanField(
        default=True
    )

    show_carbon_savings = models.BooleanField(
        default=True
    )

    # --------------------------------------------------------
    # LOCATION
    # --------------------------------------------------------

    default_city = models.CharField(
        max_length=100,
        blank=True
    )

    default_state = models.CharField(
        max_length=100,
        blank=True
    )

    # --------------------------------------------------------
    # PRIVACY
    # --------------------------------------------------------

    location_tracking_enabled = models.BooleanField(
        default=True
    )

    driving_behavior_tracking = models.BooleanField(
        default=True
    )

    share_anonymous_analytics = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # TIMESTAMPS
    # --------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"EV Preferences - {self.user}"

    def save(self, *args, **kwargs):

        # Keep percentage values valid
        self.preferred_charge_limit = max(
            0.0,
            min(100.0, self.preferred_charge_limit)
        )

        self.minimum_battery_percentage = max(
            0.0,
            min(100.0, self.minimum_battery_percentage)
        )

        self.reserve_battery_percentage = max(
            0.0,
            min(100.0, self.reserve_battery_percentage)
        )

        super().save(*args, **kwargs)
        