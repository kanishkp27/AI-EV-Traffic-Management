// ============================================================
// FLEET ENERGY-PERFORMANCE INDICATOR
// AI ANALYTICS ENGINE
// ============================================================

class FleetEnergyPerformance {

    constructor() {
        this.vehicleData = [];
        this.chargingData = [];
        this.routeData = [];
        this.stationData = [];
        this.trafficData = [];
        this.weatherData = [];
    }


    // ============================================================
    // FETCH DATA FROM DJANGO REST API
    // ============================================================

    async fetchData() {

        try {

            const [
                vehicles,
                charging,
                routes,
                stations,
                traffic
            ] = await Promise.all([

                fetch("/api/vehicles/")
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(
                                `Vehicles API failed: ${response.status}`
                            );
                        }

                        return response.json();
                    }),

                fetch("/api/charging-logs/")
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(
                                `Charging API failed: ${response.status}`
                            );
                        }

                        return response.json();
                    }),

                fetch("/api/routes/")
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(
                                `Routes API failed: ${response.status}`
                            );
                        }

                        return response.json();
                    }),

                fetch("/api/stations/")
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(
                                `Stations API failed: ${response.status}`
                            );
                        }

                        return response.json();
                    }),

                fetch("/api/traffic/")
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(
                                `Traffic API failed: ${response.status}`
                            );
                        }

                        return response.json();
                    })

            ]);


            // ----------------------------------------------------
            // Django REST Framework pagination support
            // ----------------------------------------------------

            this.vehicleData =
                Array.isArray(vehicles)
                    ? vehicles
                    : (vehicles.results || []);


            this.chargingData =
                Array.isArray(charging)
                    ? charging
                    : (charging.results || []);


            this.routeData =
                Array.isArray(routes)
                    ? routes
                    : (routes.results || []);


            this.stationData =
                Array.isArray(stations)
                    ? stations
                    : (stations.results || []);


            this.trafficData =
                Array.isArray(traffic)
                    ? traffic
                    : (traffic.results || []);


            console.log(
                "AI EV data loaded successfully"
            );

            console.log(
                "Vehicles:",
                this.vehicleData
            );

            console.log(
                "Charging:",
                this.chargingData
            );

            console.log(
                "Routes:",
                this.routeData
            );

            console.log(
                "Stations:",
                this.stationData
            );

            console.log(
                "Traffic:",
                this.trafficData
            );


            return true;

        } catch (error) {

            console.error(
                "AI data loading error:",
                error
            );

            return false;
        }
    }


    // ============================================================
    // WEATHER IMPACT ANALYSIS
    // ============================================================

    analyzeWeatherImpact() {

        // Demo values.
        // Connect these later to your WeatherData API.

        const temperature = 34;
        const condition = "Hot";

        let rangeImpact = 0;

        let recommendation =
            "Weather conditions are suitable for EV driving.";


        if (temperature >= 35) {

            rangeImpact = -10;

            recommendation =
                "High temperature may reduce battery efficiency. " +
                "Avoid aggressive acceleration and park in shaded areas.";

        } else if (temperature >= 30) {

            rangeImpact = -8;

            recommendation =
                "Warm weather may slightly reduce battery efficiency. " +
                "Drive smoothly and avoid unnecessary acceleration.";

        } else if (temperature <= 5) {

            rangeImpact = -12;

            recommendation =
                "Low temperature can reduce battery performance. " +
                "Pre-condition the battery before long trips.";
        }


        return {
            temperature: temperature,
            condition: condition,
            rangeImpact: rangeImpact,
            recommendation: recommendation,
            confidence: 88
        };
    }


    // ============================================================
    // TRAFFIC ANALYSIS
    // ============================================================

    analyzeTraffic() {

        if (!this.trafficData.length) {

            return {
                congestion: "Unknown",
                speed: 0,
                recommendation:
                    "Traffic information is currently unavailable."
            };
        }


        const speeds = this.trafficData.map(item => {

            return Number(
                item.average_speed ??
                item.speed ??
                0
            );

        });


        const totalSpeed = speeds.reduce(
            (sum, speed) => sum + speed,
            0
        );


        const avgSpeed =
            speeds.length > 0
                ? totalSpeed / speeds.length
                : 0;


        let congestion = "Low";


        if (avgSpeed < 25) {

            congestion = "Heavy";

        } else if (avgSpeed < 45) {

            congestion = "Moderate";
        }


        let recommendation;


        if (congestion === "Heavy") {

            recommendation =
                "Consider an alternative AI-optimized route " +
                "to reduce energy consumption.";

        } else if (congestion === "Moderate") {

            recommendation =
                "Moderate traffic detected. " +
                "Maintain steady speed to improve efficiency.";

        } else {

            recommendation =
                "Current traffic conditions are acceptable.";
        }


        return {
            congestion: congestion,
            speed: avgSpeed,
            recommendation: recommendation
        };
    }


    // ============================================================
    // CHARGING STATION RECOMMENDATION
    // ============================================================

    recommendChargingStation() {

        if (!this.stationData.length) {
            return null;
        }


        const stations = [...this.stationData];


        stations.sort((a, b) => {

            const aAvailable =
                Number(
                    a.chargers_available ?? 0
                );


            const bAvailable =
                Number(
                    b.chargers_available ?? 0
                );


            return bAvailable - aAvailable;
        });


        return stations[0];
    }


    // ============================================================
    // VEHICLE ANOMALY DETECTION
    // ============================================================

    detectAnomalies() {

        const anomalies = [];


        this.vehicleData.forEach(vehicle => {

            const batteryCapacity =
                Number(
                    vehicle.battery_capacity ?? 0
                );


            const currentCharge =
                Number(
                    vehicle.current_charge ?? 0
                );


            let battery =
                Number(
                    vehicle.battery_percentage
                );


            if (!Number.isFinite(battery)) {

                if (batteryCapacity > 0) {

                    battery =
                        (
                            currentCharge /
                            batteryCapacity
                        ) * 100;

                } else {

                    battery = 0;
                }
            }


            const speed =
                Number(
                    vehicle.speed ?? 0
                );


            const status =
                String(
                    vehicle.status ?? ""
                ).toLowerCase();


            // ----------------------------------------------------
            // LOW BATTERY
            // ----------------------------------------------------

            if (battery < 15) {

                anomalies.push({

                    vehicle: vehicle.id,

                    severity: "Critical",

                    issue:
                        "Extremely Low Battery",

                    action:
                        "Send vehicle to the nearest " +
                        "charging station."
                });
            }


            // ----------------------------------------------------
            // HIGH SPEED
            // ----------------------------------------------------

            if (speed > 120) {

                anomalies.push({

                    vehicle: vehicle.id,

                    severity: "High",

                    issue:
                        "Abnormal Speed",

                    action:
                        "Check driver behaviour and " +
                        "vehicle telemetry."
                });

            } else if (speed > 100) {

                anomalies.push({

                    vehicle: vehicle.id,

                    severity: "Medium",

                    issue:
                        "High Speed",

                    action:
                        "Reduce speed to improve safety " +
                        "and energy efficiency."
                });
            }


            // ----------------------------------------------------
            // MAINTENANCE
            // ----------------------------------------------------

            if (status === "maintenance") {

                anomalies.push({

                    vehicle: vehicle.id,

                    severity: "Medium",

                    issue:
                        "Maintenance Required",

                    action:
                        "Schedule vehicle inspection."
                });
            }

        });


        return anomalies;
    }


    // ============================================================
    // ECO SCORE
    // ============================================================

    calculateEcoScore() {

        if (!this.vehicleData.length) {
            return 0;
        }


        let score = 100;


        this.vehicleData.forEach(vehicle => {

            const speed =
                Number(
                    vehicle.speed ?? 0
                );


            if (speed > 100) {
                score -= 3;
            }


            if (speed > 120) {
                score -= 5;
            }


            const batteryCapacity =
                Number(
                    vehicle.battery_capacity ?? 0
                );


            const currentCharge =
                Number(
                    vehicle.current_charge ?? 0
                );


            if (
                batteryCapacity > 0 &&
                currentCharge / batteryCapacity < 0.15
            ) {

                score -= 2;
            }

        });


        return Math.max(
            0,
            Math.min(100, score)
        );
    }


    // ============================================================
    // TOTAL ENERGY CONSUMPTION
    // ============================================================

    calculateTotalEnergy() {

        return this.chargingData.reduce(
            (sum, log) => {

                return sum +
                    Number(
                        log.charge_amount ??
                        log.energy_added ??
                        log.energy_consumed ??
                        0
                    );

            },
            0
        );
    }


    // ============================================================
    // CO2 AVOIDED
    // ============================================================

    calculateCO2Avoided(totalEnergy) {

        const emissionFactor = 0.82;

        return totalEnergy * emissionFactor;
    }


    // ============================================================
    // SAFE ELEMENT UPDATE
    // ============================================================

    updateElement(id, html) {

        const element =
            document.getElementById(id);


        if (element) {
            element.innerHTML = html;
        }
    }


    // ============================================================
    // RENDER ADVANCED AI DASHBOARD
    // ============================================================

    renderAdvancedAI() {

        // ========================================================
        // WEATHER
        // ========================================================

        const weather =
            this.analyzeWeatherImpact();


        this.updateElement(
            "weather-ai",

            `
            <div class="ai-result">

                <h5>
                    <i class="fas fa-temperature-high"></i>
                    ${weather.temperature}°C
                </h5>

                <p>
                    <strong>Condition:</strong>
                    ${weather.condition}
                </p>

                <p>
                    <strong>Range Impact:</strong>
                    ${weather.rangeImpact}%
                </p>

                <p>
                    ${weather.recommendation}
                </p>

                <small>
                    AI Confidence:
                    ${weather.confidence}%
                </small>

            </div>
            `
        );


        // ========================================================
        // TRAFFIC
        // ========================================================

        const traffic =
            this.analyzeTraffic();


        this.updateElement(
            "traffic-ai",

            `
            <div class="ai-result">

                <h5>
                    <i class="fas fa-traffic-light"></i>
                    ${traffic.congestion} Traffic
                </h5>

                <p>
                    <strong>Average Speed:</strong>
                    ${traffic.speed.toFixed(1)} km/h
                </p>

                <p>
                    ${traffic.recommendation}
                </p>

            </div>
            `
        );


        // ========================================================
        // CHARGING STATION
        // ========================================================

        const station =
            this.recommendChargingStation();


        if (station) {

            this.updateElement(
                "station-ai",

                `
                <div class="ai-result">

                    <h5>
                        <i class="fas fa-charging-station"></i>
                        Recommended Station
                    </h5>

                    <p>
                        <strong>
                            ${station.name || "Charging Station"}
                        </strong>
                    </p>

                    <p>
                        Available Chargers:
                        ${station.chargers_available ?? 0}
                    </p>

                    <p>
                        Charger:
                        ${station.charger_type || "N/A"}
                    </p>

                    <p>
                        Power:
                        ${station.power_capacity ?? 0} kW
                    </p>

                    <a
                        href="/charging-finder/"
                        class="btn btn-primary btn-sm"
                    >
                        <i class="fas fa-location-arrow"></i>
                        Navigate
                    </a>

                </div>
                `
            );

        } else {

            this.updateElement(
                "station-ai",

                `
                <div class="alert alert-warning">
                    No charging station data available.
                </div>
                `
            );
        }


        // ========================================================
        // ANOMALIES
        // ========================================================

        const anomalies =
            this.detectAnomalies();


        const anomalyContainer =
            document.getElementById("anomaly-ai");


        if (anomalyContainer) {

            if (!anomalies.length) {

                anomalyContainer.innerHTML = `
                    <div class="alert alert-success">

                        <i class="fas fa-check-circle"></i>

                        No abnormal vehicle behaviour detected.

                    </div>
                `;

            } else {

                anomalyContainer.innerHTML =
                    anomalies
                        .slice(0, 5)
                        .map(anomaly => `

                            <div class="alert alert-warning">

                                <strong>
                                    Vehicle #${anomaly.vehicle}
                                </strong>

                                <br>

                                <strong>
                                    ${anomaly.severity}
                                </strong>

                                <br>

                                ${anomaly.issue}

                                <br>

                                <small>
                                    ${anomaly.action}
                                </small>

                            </div>

                        `)
                        .join("");
            }
        }


        // ========================================================
        // ECO SCORE
        // ========================================================

        const ecoScore =
            this.calculateEcoScore();


        const ecoScoreElement =
            document.getElementById("eco-score");


        if (ecoScoreElement) {

            ecoScoreElement.textContent =
                `${ecoScore}/100`;
        }


        // ========================================================
        // TOTAL ENERGY
        // ========================================================

        const totalEnergy =
            this.calculateTotalEnergy();


        const energyElement =
            document.getElementById("total-energy");


        if (energyElement) {

            energyElement.textContent =
                `${totalEnergy.toFixed(1)} kWh`;
        }


        // ========================================================
        // CO2 AVOIDED
        // ========================================================

        const estimatedCO2 =
            this.calculateCO2Avoided(
                totalEnergy
            );


        const co2Element =
            document.getElementById("co2-avoided");


        if (co2Element) {

            co2Element.textContent =
                `${estimatedCO2.toFixed(1)} kg`;
        }


        // ========================================================
        // ENERGY EFFICIENCY
        // ========================================================

        let efficiency =
            "Needs Improvement";


        if (ecoScore >= 85) {

            efficiency = "Excellent";

        } else if (ecoScore >= 70) {

            efficiency = "Good";
        }


        const efficiencyElement =
            document.getElementById(
                "energy-efficiency"
            );


        if (efficiencyElement) {

            efficiencyElement.textContent =
                efficiency;
        }


        console.log(
            "AI Fleet Analysis completed"
        );
    }
}


// ============================================================
// CREATE AI ENGINE
// ============================================================

const fleetAI =
    new FleetEnergyPerformance();


// ============================================================
// START AFTER PAGE LOAD
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    async function () {

        console.log(
            "Starting Fleet AI..."
        );


        const loaded =
            await fleetAI.fetchData();


        if (loaded) {

            fleetAI.renderAdvancedAI();

        } else {

            console.warn(
                "Fleet AI could not load API data."
            );
        }

    }
);