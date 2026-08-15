
"""
India-wide configuration for AI EV Management System.

Includes:
- States and Union Territories
- Districts
- Major EV corridors
- EV vehicle models
- Charging operators
- Charger standards
- Weather / terrain factors
- Toll / road categories
- Emergency information categories
- UI translations
- Charging pricing configuration

NOTE:
Static values here should be treated as application/demo configuration.
Live charging availability, prices, traffic and station counts should come
from APIs or the project database.
"""


# ============================================================
# 1. INDIA STATES / UNION TERRITORIES AND DISTRICTS
# ============================================================

INDIA_STATES_DISTRICTS = {

    "Andhra Pradesh": [
        "Alluri Sitharama Raju",
        "Anakapalli",
        "Ananthapuramu",
        "Annamayya",
        "Bapatla",
        "Chittoor",
        "Dr. B.R. Ambedkar Konaseema",
        "East Godavari",
        "Eluru",
        "Guntur",
        "Kakinada",
        "Krishna",
        "Kurnool",
        "Nandyal",
        "NTR",
        "Palnadu",
        "Parvathipuram Manyam",
        "Prakasam",
        "Sri Potti Sriramulu Nellore",
        "Sri Sathya Sai",
        "Srikakulam",
        "Tirupati",
        "Visakhapatnam",
        "Vizianagaram",
        "West Godavari",
        "YSR Kadapa",
    ],

    "Arunachal Pradesh": [
        "Anjaw",
        "Bichom",
        "Changlang",
        "Dibang Valley",
        "East Kameng",
        "East Siang",
        "Kamle",
        "Keyi Panyor",
        "Kra Daadi",
        "Kurung Kumey",
        "Leparada",
        "Lohit",
        "Longding",
        "Lower Dibang Valley",
        "Lower Siang",
        "Lower Subansiri",
        "Namsai",
        "Pakke Kessang",
        "Papum Pare",
        "Shi Yomi",
        "Siang",
        "Tawang",
        "Tirap",
        "Upper Siang",
        "Upper Subansiri",
        "West Kameng",
        "West Siang",
    ],

    "Assam": [
        "Bajali",
        "Baksa",
        "Barpeta",
        "Biswanath",
        "Bongaigaon",
        "Cachar",
        "Charaideo",
        "Chirang",
        "Darrang",
        "Dhemaji",
        "Dhubri",
        "Dibrugarh",
        "Dima Hasao",
        "Goalpara",
        "Golaghat",
        "Hailakandi",
        "Hojai",
        "Jorhat",
        "Kamrup",
        "Kamrup Metropolitan",
        "Karbi Anglong",
        "Karimganj",
        "Kokrajhar",
        "Lakhimpur",
        "Majuli",
        "Morigaon",
        "Nagaon",
        "Nalbari",
        "Sivasagar",
        "Sonitpur",
        "South Salmara-Mankachar",
        "Tamulpur",
        "Tinsukia",
        "Udalguri",
        "West Karbi Anglong",
    ],

    "Bihar": [
        "Araria",
        "Arwal",
        "Aurangabad",
        "Banka",
        "Begusarai",
        "Bhagalpur",
        "Bhojpur",
        "Buxar",
        "Darbhanga",
        "East Champaran",
        "Gaya",
        "Gopalganj",
        "Jamui",
        "Jehanabad",
        "Kaimur",
        "Katihar",
        "Khagaria",
        "Kishanganj",
        "Lakhisarai",
        "Madhepura",
        "Madhubani",
        "Munger",
        "Muzaffarpur",
        "Nalanda",
        "Nawada",
        "Patna",
        "Purnia",
        "Rohtas",
        "Saharsa",
        "Samastipur",
        "Saran",
        "Sheikhpura",
        "Sheohar",
        "Sitamarhi",
        "Siwan",
        "Supaul",
        "Vaishali",
        "West Champaran",
    ],

    "Chhattisgarh": [
        "Balod",
        "Baloda Bazar",
        "Balrampur",
        "Bastar",
        "Bemetara",
        "Bijapur",
        "Bilaspur",
        "Dantewada",
        "Dhamtari",
        "Durg",
        "Gariaband",
        "Gaurela-Pendra-Marwahi",
        "Janjgir-Champa",
        "Jashpur",
        "Kabirdham",
        "Kanker",
        "Khairagarh-Chhuikhadan-Gandai",
        "Kondagaon",
        "Korba",
        "Koriya",
        "Mahasamund",
        "Manendragarh-Chirmiri-Bharatpur",
        "Mohla-Manpur-Ambagarh Chowki",
        "Mungeli",
        "Narayanpur",
        "Raigarh",
        "Raipur",
        "Rajnandgaon",
        "Sakti",
        "Sarangarh-Bilaigarh",
        "Sukma",
        "Surajpur",
        "Surguja",
    ],

    "Goa": [
        "North Goa",
        "South Goa",
    ],

    "Gujarat": [
        "Ahmedabad",
        "Amreli",
        "Anand",
        "Aravalli",
        "Banaskantha",
        "Bharuch",
        "Bhavnagar",
        "Botad",
        "Chhota Udaipur",
        "Dahod",
        "Dang",
        "Devbhoomi Dwarka",
        "Gandhinagar",
        "Gir Somnath",
        "Jamnagar",
        "Junagadh",
        "Kheda",
        "Kutch",
        "Mahisagar",
        "Mehsana",
        "Morbi",
        "Narmada",
        "Navsari",
        "Panchmahal",
        "Patan",
        "Porbandar",
        "Rajkot",
        "Sabarkantha",
        "Surat",
        "Surendranagar",
        "Tapi",
        "Vadodara",
        "Valsad",
    ],

    "Haryana": [
        "Ambala",
        "Bhiwani",
        "Charkhi Dadri",
        "Faridabad",
        "Fatehabad",
        "Gurugram",
        "Hisar",
        "Jhajjar",
        "Jind",
        "Kaithal",
        "Karnal",
        "Kurukshetra",
        "Mahendragarh",
        "Nuh",
        "Palwal",
        "Panchkula",
        "Panipat",
        "Rewari",
        "Rohtak",
        "Sirsa",
        "Sonipat",
        "Yamunanagar",
    ],

    "Himachal Pradesh": [
        "Bilaspur",
        "Chamba",
        "Hamirpur",
        "Kangra",
        "Kinnaur",
        "Kullu",
        "Lahaul and Spiti",
        "Mandi",
        "Shimla",
        "Sirmaur",
        "Solan",
        "Una",
    ],

    "Jharkhand": [
        "Bokaro",
        "Chatra",
        "Deoghar",
        "Dhanbad",
        "Dumka",
        "East Singhbhum",
        "Garhwa",
        "Giridih",
        "Godda",
        "Gumla",
        "Hazaribagh",
        "Jamtara",
        "Khunti",
        "Koderma",
        "Latehar",
        "Lohardaga",
        "Pakur",
        "Palamu",
        "Ramgarh",
        "Ranchi",
        "Sahibganj",
        "Seraikela-Kharsawan",
        "Simdega",
        "West Singhbhum",
    ],

    "Karnataka": [
        "Bagalkot",
        "Ballari",
        "Belagavi",
        "Bengaluru Rural",
        "Bengaluru Urban",
        "Bidar",
        "Chamarajanagar",
        "Chikkaballapur",
        "Chikkamagaluru",
        "Chitradurga",
        "Dakshina Kannada",
        "Davanagere",
        "Dharwad",
        "Gadag",
        "Hassan",
        "Haveri",
        "Kalaburagi",
        "Kodagu",
        "Kolar",
        "Koppal",
        "Mandya",
        "Mysuru",
        "Raichur",
        "Ramanagara",
        "Shivamogga",
        "Tumakuru",
        "Udupi",
        "Uttara Kannada",
        "Vijayapura",
        "Vijayanagara",
        "Yadgir",
    ],

    "Kerala": [
        "Alappuzha",
        "Ernakulam",
        "Idukki",
        "Kannur",
        "Kasaragod",
        "Kollam",
        "Kottayam",
        "Kozhikode",
        "Malappuram",
        "Palakkad",
        "Pathanamthitta",
        "Thiruvananthapuram",
        "Thrissur",
        "Wayanad",
    ],

    "Madhya Pradesh": [
        "Agar Malwa",
        "Alirajpur",
        "Anuppur",
        "Ashoknagar",
        "Balaghat",
        "Barwani",
        "Betul",
        "Bhind",
        "Bhopal",
        "Burhanpur",
        "Chhatarpur",
        "Chhindwara",
        "Damoh",
        "Datia",
        "Dewas",
        "Dhar",
        "Dindori",
        "Guna",
        "Gwalior",
        "Harda",
        "Indore",
        "Jabalpur",
        "Jhabua",
        "Katni",
        "Khandwa",
        "Khargone",
        "Maihar",
        "Mandla",
        "Mandsaur",
        "Mauganj",
        "Morena",
        "Narmadapuram",
        "Narsinghpur",
        "Neemuch",
        "Niwari",
        "Pandhurna",
        "Panna",
        "Raisen",
        "Rajgarh",
        "Ratlam",
        "Rewa",
        "Sagar",
        "Satna",
        "Sehore",
        "Seoni",
        "Shahdol",
        "Shajapur",
        "Sheopur",
        "Shivpuri",
        "Sidhi",
        "Singrauli",
        "Tikamgarh",
        "Ujjain",
        "Umaria",
        "Vidisha",
    ],

    "Maharashtra": [
        "Ahmednagar",
        "Akola",
        "Amravati",
        "Beed",
        "Bhandara",
        "Buldhana",
        "Chandrapur",
        "Chhatrapati Sambhajinagar",
        "Dharashiv",
        "Dhule",
        "Gadchiroli",
        "Gondia",
        "Hingoli",
        "Jalgaon",
        "Jalna",
        "Kolhapur",
        "Latur",
        "Mumbai City",
        "Mumbai Suburban",
        "Nagpur",
        "Nanded",
        "Nandurbar",
        "Nashik",
        "Palghar",
        "Parbhani",
        "Pune",
        "Raigad",
        "Ratnagiri",
        "Sangli",
        "Satara",
        "Sindhudurg",
        "Solapur",
        "Thane",
        "Wardha",
        "Washim",
        "Yavatmal",
    ],

    "Manipur": [
        "Bishnupur",
        "Chandel",
        "Churachandpur",
        "Imphal East",
        "Imphal West",
        "Jiribam",
        "Kakching",
        "Kamjong",
        "Kangpokpi",
        "Noney",
        "Pherzawl",
        "Senapati",
        "Tamenglong",
        "Tengnoupal",
        "Thoubal",
        "Ukhrul",
    ],

    "Meghalaya": [
        "East Garo Hills",
        "East Jaintia Hills",
        "East Khasi Hills",
        "Eastern West Khasi Hills",
        "North Garo Hills",
        "Ri Bhoi",
        "South Garo Hills",
        "South West Garo Hills",
        "South West Khasi Hills",
        "West Garo Hills",
        "West Jaintia Hills",
        "West Khasi Hills",
    ],

    "Mizoram": [
        "Aizawl",
        "Champhai",
        "Hnahthial",
        "Khawzawl",
        "Kolasib",
        "Lawngtlai",
        "Lunglei",
        "Mamit",
        "Saiha",
        "Saitual",
        "Serchhip",
    ],

    "Nagaland": [
        "Chumoukedima",
        "Dimapur",
        "Kiphire",
        "Kohima",
        "Longleng",
        "Mokokchung",
        "Mon",
        "Niuland",
        "Noklak",
        "Peren",
        "Phek",
        "Shamator",
        "Tseminyu",
        "Tuensang",
        "Wokha",
        "Zunheboto",
    ],

    "Odisha": [
        "Angul",
        "Balangir",
        "Balasore",
        "Bargarh",
        "Bhadrak",
        "Boudh",
        "Cuttack",
        "Deogarh",
        "Dhenkanal",
        "Gajapati",
        "Ganjam",
        "Jagatsinghpur",
        "Jajpur",
        "Jharsuguda",
        "Kalahandi",
        "Kandhamal",
        "Kendrapara",
        "Kendujhar",
        "Khordha",
        "Koraput",
        "Malkangiri",
        "Mayurbhanj",
        "Nabarangpur",
        "Nayagarh",
        "Nuapada",
        "Puri",
        "Rayagada",
        "Sambalpur",
        "Subarnapur",
        "Sundargarh",
    ],

    "Punjab": [
        "Amritsar",
        "Barnala",
        "Bathinda",
        "Faridkot",
        "Fatehgarh Sahib",
        "Fazilka",
        "Ferozepur",
        "Gurdaspur",
        "Hoshiarpur",
        "Jalandhar",
        "Kapurthala",
        "Ludhiana",
        "Malerkotla",
        "Mansa",
        "Moga",
        "Pathankot",
        "Patiala",
        "Rupnagar",
        "Sahibzada Ajit Singh Nagar",
        "Sangrur",
        "Shaheed Bhagat Singh Nagar",
        "Sri Muktsar Sahib",
        "Tarn Taran",
    ],

    "Rajasthan": [
        "Ajmer",
        "Alwar",
        "Banswara",
        "Baran",
        "Barmer",
        "Bharatpur",
        "Bhilwara",
        "Bikaner",
        "Bundi",
        "Chittorgarh",
        "Churu",
        "Dausa",
        "Dholpur",
        "Dungarpur",
        "Hanumangarh",
        "Jaipur",
        "Jaisalmer",
        "Jalore",
        "Jhalawar",
        "Jhunjhunu",
        "Jodhpur",
        "Karauli",
        "Kota",
        "Nagaur",
        "Pali",
        "Pratapgarh",
        "Rajsamand",
        "Sawai Madhopur",
        "Sikar",
        "Sirohi",
        "Sri Ganganagar",
        "Tonk",
        "Udaipur",
    ],

    "Sikkim": [
        "Gangtok",
        "Gyalshing",
        "Mangan",
        "Namchi",
        "Pakyong",
        "Soreng",
    ],

    "Tamil Nadu": [
        "Ariyalur",
        "Chengalpattu",
        "Chennai",
        "Coimbatore",
        "Cuddalore",
        "Dharmapuri",
        "Dindigul",
        "Erode",
        "Kallakurichi",
        "Kancheepuram",
        "Kanniyakumari",
        "Karur",
        "Krishnagiri",
        "Madurai",
        "Mayiladuthurai",
        "Nagapattinam",
        "Namakkal",
        "Nilgiris",
        "Perambalur",
        "Pudukkottai",
        "Ramanathapuram",
        "Ranipet",
        "Salem",
        "Sivaganga",
        "Tenkasi",
        "Thanjavur",
        "Theni",
        "Thoothukudi",
        "Tiruchirappalli",
        "Tirunelveli",
        "Tirupathur",
        "Tiruppur",
        "Tiruvallur",
        "Tiruvannamalai",
        "Tiruvarur",
        "Vellore",
        "Viluppuram",
        "Virudhunagar",
    ],

    "Telangana": [
        "Adilabad",
        "Bhadradri Kothagudem",
        "Hanumakonda",
        "Hyderabad",
        "Jagtial",
        "Jangaon",
        "Jayashankar Bhupalpally",
        "Jogulamba Gadwal",
        "Kamareddy",
        "Karimnagar",
        "Khammam",
        "Komaram Bheem Asifabad",
        "Mahabubabad",
        "Mahabubnagar",
        "Mancherial",
        "Medak",
        "Medchal-Malkajgiri",
        "Mulugu",
        "Nagarkurnool",
        "Nalgonda",
        "Narayanpet",
        "Nirmal",
        "Nizamabad",
        "Peddapalli",
        "Rajanna Sircilla",
        "Rangareddy",
        "Sangareddy",
        "Siddipet",
        "Suryapet",
        "Vikarabad",
        "Wanaparthy",
        "Warangal",
        "Yadadri Bhuvanagiri",
    ],

    "Tripura": [
        "Dhalai",
        "Gomati",
        "Khowai",
        "North Tripura",
        "Sepahijala",
        "South Tripura",
        "Unakoti",
        "West Tripura",
    ],

    "Uttar Pradesh": [
        "Agra",
        "Aligarh",
        "Ambedkar Nagar",
        "Amethi",
        "Amroha",
        "Auraiya",
        "Ayodhya",
        "Azamgarh",
        "Baghpat",
        "Bahraich",
        "Ballia",
        "Balrampur",
        "Banda",
        "Barabanki",
        "Bareilly",
        "Basti",
        "Bhadohi",
        "Bijnor",
        "Budaun",
        "Bulandshahr",
        "Chandauli",
        "Chitrakoot",
        "Deoria",
        "Etah",
        "Etawah",
        "Farrukhabad",
        "Fatehpur",
        "Firozabad",
        "Gautam Buddha Nagar",
        "Ghaziabad",
        "Ghazipur",
        "Gonda",
        "Gorakhpur",
        "Hamirpur",
        "Hapur",
        "Hardoi",
        "Hathras",
        "Jalaun",
        "Jaunpur",
        "Jhansi",
        "Kannauj",
        "Kanpur Dehat",
        "Kanpur Nagar",
        "Kasganj",
        "Kaushambi",
        "Kushinagar",
        "Lakhimpur Kheri",
        "Lalitpur",
        "Lucknow",
        "Maharajganj",
        "Mahoba",
        "Mainpuri",
        "Mathura",
        "Mau",
        "Meerut",
        "Mirzapur",
        "Moradabad",
        "Muzaffarnagar",
        "Pilibhit",
        "Pratapgarh",
        "Prayagraj",
        "Raebareli",
        "Rampur",
        "Saharanpur",
        "Sambhal",
        "Sant Kabir Nagar",
        "Shahjahanpur",
        "Shamli",
        "Shravasti",
        "Siddharthnagar",
        "Sitapur",
        "Sonbhadra",
        "Sultanpur",
        "Unnao",
        "Varanasi",
    ],

    "Uttarakhand": [
        "Almora",
        "Bageshwar",
        "Chamoli",
        "Champawat",
        "Dehradun",
        "Haridwar",
        "Nainital",
        "Pauri Garhwal",
        "Pithoragarh",
        "Rudraprayag",
        "Tehri Garhwal",
        "Udham Singh Nagar",
        "Uttarkashi",
    ],

    "West Bengal": [
        "Alipurduar",
        "Bankura",
        "Birbhum",
        "Cooch Behar",
        "Dakshin Dinajpur",
        "Darjeeling",
        "Hooghly",
        "Howrah",
        "Jalpaiguri",
        "Jhargram",
        "Kalimpong",
        "Kolkata",
        "Malda",
        "Murshidabad",
        "Nadia",
        "North 24 Parganas",
        "Paschim Bardhaman",
        "Paschim Medinipur",
        "Purba Bardhaman",
        "Purba Medinipur",
        "Purulia",
        "South 24 Parganas",
        "Uttar Dinajpur",
    ],


    # ========================================================
    # UNION TERRITORIES
    # ========================================================

    "Andaman and Nicobar Islands": [
        "Nicobar",
        "North and Middle Andaman",
        "South Andaman",
    ],

    "Chandigarh": [
        "Chandigarh",
    ],

    "Dadra and Nagar Haveli and Daman and Diu": [
        "Dadra and Nagar Haveli",
        "Daman",
        "Diu",
    ],

    "Delhi": [
        "Central Delhi",
        "East Delhi",
        "New Delhi",
        "North Delhi",
        "North East Delhi",
        "North West Delhi",
        "Shahdara",
        "South Delhi",
        "South East Delhi",
        "South West Delhi",
        "West Delhi",
    ],

    "Jammu and Kashmir": [
        "Anantnag",
        "Bandipora",
        "Baramulla",
        "Budgam",
        "Doda",
        "Ganderbal",
        "Jammu",
        "Kathua",
        "Kishtwar",
        "Kulgam",
        "Kupwara",
        "Poonch",
        "Pulwama",
        "Rajouri",
        "Ramban",
        "Reasi",
        "Samba",
        "Shopian",
        "Srinagar",
        "Udhampur",
    ],

    "Ladakh": [
        "Kargil",
        "Leh",
    ],

    "Lakshadweep": [
        "Lakshadweep",
    ],

    "Puducherry": [
        "Karaikal",
        "Mahe",
        "Puducherry",
        "Yanam",
    ],
}


# ============================================================
# 2. STATE / UT CAPITALS
# ============================================================

STATE_CAPITALS = {
    "Uttar Pradesh": "Lucknow",
    "Rajasthan": "Jaipur",
    "Maharashtra": "Mumbai",
    "Gujarat": "Gandhinagar",
    "Madhya Pradesh": "Bhopal",
    "Bihar": "Patna",
    "Jharkhand": "Ranchi",
    "Chhattisgarh": "Raipur",
    "Punjab": "Chandigarh",
    "Haryana": "Chandigarh",
    "Uttarakhand": "Dehradun",
    "Himachal Pradesh": "Shimla",
    "West Bengal": "Kolkata",
    "Odisha": "Bhubaneswar",
    "Assam": "Dispur",
    "Sikkim": "Gangtok",
    "Arunachal Pradesh": "Itanagar",
    "Nagaland": "Kohima",
    "Manipur": "Imphal",
    "Mizoram": "Aizawl",
    "Tripura": "Agartala",
    "Meghalaya": "Shillong",
    "Karnataka": "Bengaluru",
    "Kerala": "Thiruvananthapuram",
    "Tamil Nadu": "Chennai",
    "Telangana": "Hyderabad",
    "Andhra Pradesh": "Amaravati",
    "Goa": "Panaji",
    "Delhi": "New Delhi",
}


# ============================================================
# 3. MAJOR EV / HIGHWAY CORRIDORS
# ============================================================

INDIAN_EV_CORRIDORS = {

    "delhi_jaipur": {
        "name": "Delhi - Jaipur",
        "start": (28.6139, 77.2090),
        "end": (26.9124, 75.7873),
        "approx_distance_km": 280,
        "states": ["Delhi", "Haryana", "Rajasthan"],
    },

    "delhi_agra": {
        "name": "Delhi - Agra",
        "start": (28.6139, 77.2090),
        "end": (27.1767, 78.0081),
        "approx_distance_km": 230,
        "states": ["Delhi", "Uttar Pradesh"],
    },

    "agra_lucknow": {
        "name": "Agra - Lucknow",
        "start": (27.1767, 78.0081),
        "end": (26.8467, 80.9462),
        "approx_distance_km": 302,
        "states": ["Uttar Pradesh"],
    },

    "lucknow_varanasi": {
        "name": "Lucknow - Varanasi",
        "start": (26.8467, 80.9462),
        "end": (25.3176, 82.9739),
        "approx_distance_km": 320,
        "states": ["Uttar Pradesh"],
    },

    "delhi_meerut": {
        "name": "Delhi - Meerut",
        "start": (28.6139, 77.2090),
        "end": (28.9845, 77.7064),
        "approx_distance_km": 70,
        "states": ["Delhi", "Uttar Pradesh"],
    },

    "mumbai_pune": {
        "name": "Mumbai - Pune",
        "start": (19.0760, 72.8777),
        "end": (18.5204, 73.8567),
        "approx_distance_km": 150,
        "states": ["Maharashtra"],
    },

    "mumbai_nashik": {
        "name": "Mumbai - Nashik",
        "start": (19.0760, 72.8777),
        "end": (19.9975, 73.7898),
        "approx_distance_km": 170,
        "states": ["Maharashtra"],
    },

    "pune_bengaluru": {
        "name": "Pune - Bengaluru",
        "start": (18.5204, 73.8567),
        "end": (12.9716, 77.5946),
        "approx_distance_km": 840,
        "states": ["Maharashtra", "Karnataka"],
    },

    "bengaluru_mysuru": {
        "name": "Bengaluru - Mysuru",
        "start": (12.9716, 77.5946),
        "end": (12.2958, 76.6394),
        "approx_distance_km": 145,
        "states": ["Karnataka"],
    },

    "bengaluru_chennai": {
        "name": "Bengaluru - Chennai",
        "start": (12.9716, 77.5946),
        "end": (13.0827, 80.2707),
        "approx_distance_km": 350,
        "states": ["Karnataka", "Tamil Nadu"],
    },

    "chennai_coimbatore": {
        "name": "Chennai - Coimbatore",
        "start": (13.0827, 80.2707),
        "end": (11.0168, 76.9558),
        "approx_distance_km": 500,
        "states": ["Tamil Nadu"],
    },

    "hyderabad_bengaluru": {
        "name": "Hyderabad - Bengaluru",
        "start": (17.3850, 78.4867),
        "end": (12.9716, 77.5946),
        "approx_distance_km": 570,
        "states": ["Telangana", "Andhra Pradesh", "Karnataka"],
    },

    "ahmedabad_vadodara": {
        "name": "Ahmedabad - Vadodara",
        "start": (23.0225, 72.5714),
        "end": (22.3072, 73.1812),
        "approx_distance_km": 110,
        "states": ["Gujarat"],
    },

    "kolkata_bhubaneswar": {
        "name": "Kolkata - Bhubaneswar",
        "start": (22.5726, 88.3639),
        "end": (20.2961, 85.8245),
        "approx_distance_km": 440,
        "states": ["West Bengal", "Odisha"],
    },
}


# ============================================================
# 4. POPULAR EV MODELS IN INDIA
# ============================================================

INDIAN_EV_MODELS = [

    # Tata
    "Tata Nexon EV",
    "Tata Punch EV",
    "Tata Tiago EV",
    "Tata Tigor EV",
    "Tata Curvv EV",

    # Mahindra
    "Mahindra XUV400",
    "Mahindra BE 6",
    "Mahindra XEV 9e",

    # MG
    "MG Comet EV",
    "MG ZS EV",
    "MG Windsor EV",

    # Hyundai
    "Hyundai Ioniq 5",
    "Hyundai Creta Electric",

    # Kia
    "Kia EV6",

    # BYD
    "BYD Atto 3",
    "BYD Seal",
    "BYD eMAX 7",

    # BMW
    "BMW i4",
    "BMW i5",
    "BMW i7",
    "BMW iX",

    # Mercedes-Benz
    "Mercedes-Benz EQA",
    "Mercedes-Benz EQB",
    "Mercedes-Benz EQE SUV",
    "Mercedes-Benz EQS",

    # Audi
    "Audi Q8 e-tron",
    "Audi e-tron GT",

    # Volvo
    "Volvo EX40",
    "Volvo EC40",

    # Porsche
    "Porsche Taycan",
    "Porsche Macan Electric",
]


# ============================================================
# 5. VEHICLE CATEGORIES
# ============================================================

EV_VEHICLE_TYPES = {
    "car": "Electric Car",
    "suv": "Electric SUV",
    "two_wheeler": "Electric Two Wheeler",
    "three_wheeler": "Electric Three Wheeler",
    "bus": "Electric Bus",
    "truck": "Electric Truck",
    "commercial": "Commercial EV",
}


# ============================================================
# 6. CHARGING OPERATORS
# ============================================================

CHARGING_NETWORKS = {

    "tata_power": {
        "name": "Tata Power EZ Charge",
        "type": "Private",
    },

    "chargezone": {
        "name": "ChargeZone",
        "type": "Private",
    },

    "statiq": {
        "name": "Statiq",
        "type": "Private",
    },

    "bolt_earth": {
        "name": "Bolt.Earth",
        "type": "Private",
    },

    "jio_bp": {
        "name": "Jio-bp pulse",
        "type": "Private",
    },

    "shell": {
        "name": "Shell Recharge",
        "type": "Private",
    },

    "iocl": {
        "name": "IndianOil EV Charging",
        "type": "PSU",
    },

    "bpcl": {
        "name": "BPCL EV Charging",
        "type": "PSU",
    },

    "hpcl": {
        "name": "HPCL EV Charging",
        "type": "PSU",
    },
}


# ============================================================
# 7. CHARGER / CONNECTOR TYPES
# ============================================================

CHARGER_TYPES = {

    "ac_slow": {
        "name": "AC Slow Charger",
        "typical_power_kw": 3.3,
    },

    "ac_fast": {
        "name": "AC Fast Charger",
        "typical_power_kw": 7.4,
    },

    "type2": {
        "name": "Type 2 AC",
        "typical_power_kw": 22,
    },

    "ccs2": {
        "name": "CCS2 DC Fast Charger",
        "typical_power_kw": 60,
    },

    "high_power_ccs2": {
        "name": "High-Power CCS2",
        "typical_power_kw": 150,
    },

    "chademo": {
        "name": "CHAdeMO",
        "typical_power_kw": 50,
    },

    "bharat_ac001": {
        "name": "Bharat AC-001",
        "typical_power_kw": 3.3,
    },

    "bharat_dc001": {
        "name": "Bharat DC-001",
        "typical_power_kw": 15,
    },
}


# ============================================================
# 8. SAMPLE INDIA CHARGING STATIONS
# ============================================================

SAMPLE_CHARGING_STATIONS = [

    {
        "name": "Delhi EV Charging Hub",
        "state": "Delhi",
        "district": "New Delhi",
        "lat": 28.6139,
        "lon": 77.2090,
        "charger_type": "ccs2",
        "power_capacity": 120,
    },

    {
        "name": "Noida EV Charging Hub",
        "state": "Uttar Pradesh",
        "district": "Gautam Buddha Nagar",
        "lat": 28.5355,
        "lon": 77.3910,
        "charger_type": "ccs2",
        "power_capacity": 120,
    },

    {
        "name": "Aligarh EV Charging Hub",
        "state": "Uttar Pradesh",
        "district": "Aligarh",
        "lat": 27.8974,
        "lon": 78.0880,
        "charger_type": "ccs2",
        "power_capacity": 60,
    },

    {
        "name": "Lucknow EV Charging Hub",
        "state": "Uttar Pradesh",
        "district": "Lucknow",
        "lat": 26.8467,
        "lon": 80.9462,
        "charger_type": "ccs2",
        "power_capacity": 120,
    },

    {
        "name": "Jaipur EV Charging Hub",
        "state": "Rajasthan",
        "district": "Jaipur",
        "lat": 26.9124,
        "lon": 75.7873,
        "charger_type": "ccs2",
        "power_capacity": 120,
    },

    {
        "name": "Mumbai EV Charging Hub",
        "state": "Maharashtra",
        "district": "Mumbai City",
        "lat": 19.0760,
        "lon": 72.8777,
        "charger_type": "high_power_ccs2",
        "power_capacity": 150,
    },

    {
        "name": "Pune EV Charging Hub",
        "state": "Maharashtra",
        "district": "Pune",
        "lat": 18.5204,
        "lon": 73.8567,
        "charger_type": "ccs2",
        "power_capacity": 120,
    },

    {
        "name": "Ahmedabad EV Charging Hub",
        "state": "Gujarat",
        "district": "Ahmedabad",
        "lat": 23.0225,
        "lon": 72.5714,
        "charger_type": "ccs2",
        "power_capacity": 120,
    },

    {
        "name": "Bengaluru EV Charging Hub",
        "state": "Karnataka",
        "district": "Bengaluru Urban",
        "lat": 12.9716,
        "lon": 77.5946,
        "charger_type": "high_power_ccs2",
        "power_capacity": 150,
    },

    {
        "name": "Chennai EV Charging Hub",
        "state": "Tamil Nadu",
        "district": "Chennai",
        "lat": 13.0827,
        "lon": 80.2707,
        "charger_type": "ccs2",
        "power_capacity": 120,
    },

    {
        "name": "Hyderabad EV Charging Hub",
        "state": "Telangana",
        "district": "Hyderabad",
        "lat": 17.3850,
        "lon": 78.4867,
        "charger_type": "ccs2",
        "power_capacity": 120,
    },

    {
        "name": "Kolkata EV Charging Hub",
        "state": "West Bengal",
        "district": "Kolkata",
        "lat": 22.5726,
        "lon": 88.3639,
        "charger_type": "ccs2",
        "power_capacity": 120,
    },
]


# ============================================================
# 9. WEATHER EFFECT ON EV RANGE
# ============================================================

WEATHER_BATTERY_IMPACT = {

    "extreme_heat": {
        "temperature_min": 40,
        "range_factor": 0.88,
        "message": "Extreme heat may reduce EV efficiency.",
    },

    "hot": {
        "temperature_min": 32,
        "range_factor": 0.94,
        "message": "High temperature may slightly reduce range.",
    },

    "normal": {
        "temperature_min": 18,
        "range_factor": 1.0,
        "message": "Temperature is suitable for efficient EV operation.",
    },

    "cold": {
        "temperature_max": 10,
        "range_factor": 0.90,
        "message": "Cold conditions may reduce battery range.",
    },
}


# ============================================================
# 10. TERRAIN FACTORS
# ============================================================

TERRAIN_TYPES = {

    "plain": {
        "energy_factor": 1.0,
    },

    "urban": {
        "energy_factor": 1.05,
    },

    "hilly": {
        "energy_factor": 1.20,
    },

    "mountain": {
        "energy_factor": 1.30,
    },

    "expressway": {
        "energy_factor": 1.08,
    },
}


# ============================================================
# 11. TRAFFIC FACTORS
# ============================================================

TRAFFIC_LEVELS = {

    "clear": {
        "energy_factor": 1.0,
        "delay_factor": 1.0,
    },

    "moderate": {
        "energy_factor": 1.05,
        "delay_factor": 1.20,
    },

    "heavy": {
        "energy_factor": 1.12,
        "delay_factor": 1.50,
    },

    "severe": {
        "energy_factor": 1.20,
        "delay_factor": 2.0,
    },
}


# ============================================================
# 12. INDIA-SPECIFIC CHARGING PRICE CONFIGURATION
# ============================================================

# Demo/default prices only.
# Real prices should come from the selected charging operator/station.

DEFAULT_CHARGING_PRICING = {

    "ac_slow": 8.00,

    "ac_fast": 10.00,

    "type2": 12.00,

    "dc_fast": 15.00,

    "high_power_dc": 18.00,
}


# ============================================================
# 13. PAYMENT METHODS
# ============================================================

INDIAN_PAYMENT_METHODS = [

    "UPI",

    "Credit Card",

    "Debit Card",

    "Net Banking",

    "Wallet",

    "RFID",

    "Charging Network Wallet",
]


# ============================================================
# 14. ROAD TYPES
# ============================================================

INDIAN_ROAD_TYPES = {

    "national_highway": "National Highway",

    "state_highway": "State Highway",

    "expressway": "Expressway",

    "city": "City Road",

    "rural": "Rural Road",

    "mountain": "Mountain Road",
}


# ============================================================
# 15. AI RECOMMENDATION TYPES
# ============================================================

AI_RECOMMENDATION_TYPES = {

    "best_route": "Best Route",

    "eco_route": "Energy Efficient Route",

    "fastest_route": "Fastest Route",

    "nearest_charger": "Nearest Charging Station",

    "cheapest_charger": "Cheapest Charging Station",

    "fastest_charger": "Fastest Charging Station",

    "low_traffic_route": "Low Traffic Route",

    "battery_saving": "Battery Saving Recommendation",

    "weather_warning": "Weather Warning",

    "maintenance": "Maintenance Recommendation",
}


# ============================================================
# 16. INDIA-SPECIFIC ALERT MESSAGES
# ============================================================

ALERT_MESSAGES = {

    "low_battery":
        "Battery level is low. Please locate a nearby charging station.",

    "critical_battery":
        "Critical battery level. Charging is strongly recommended.",

    "maintenance_due":
        "Vehicle maintenance is due.",

    "charging_available":
        "A charging station is available nearby.",

    "route_suggestion":
        "A more efficient route is available.",

    "heavy_traffic":
        "Heavy traffic detected on your current route.",

    "weather_warning":
        "Weather conditions may affect battery range.",

    "overheating":
        "Battery temperature is high. Reduce load and check vehicle status.",

    "charging_queue":
        "The selected charging station currently has a queue.",

    "insurance_expiry":
        "Vehicle insurance is approaching its expiry date.",
}


# ============================================================
# 17. HINDI UI TRANSLATIONS
# ============================================================

HINDI_TRANSLATIONS = {

    "dashboard": "डैशबोर्ड",

    "vehicle": "वाहन",

    "battery": "बैटरी",

    "battery_health": "बैटरी स्वास्थ्य",

    "charging": "चार्जिंग",

    "charging_station": "चार्जिंग स्टेशन",

    "route": "मार्ग",

    "traffic": "यातायात",

    "weather": "मौसम",

    "driving": "चल रहा है",

    "idle": "निष्क्रिय",

    "maintenance": "रखरखाव",

    "status": "स्थिति",

    "location": "स्थान",

    "speed": "गति",

    "distance": "दूरी",

    "range": "रेंज",

    "energy": "ऊर्जा",

    "cost": "लागत",

    "available": "उपलब्ध",

    "unavailable": "अनुपलब्ध",

    "book": "बुक करें",

    "payment": "भुगतान",

    "trip": "यात्रा",

    "profile": "प्रोफ़ाइल",

    "notification": "सूचना",

    "emergency": "आपातकाल",

    "insurance": "बीमा",

    "rupees": "₹",

    "km_per_hour": "किमी/घंटा",
}


# ============================================================
# 18. UTILITY FUNCTIONS
# ============================================================

def get_states():
    """Return all Indian states and union territories."""
    return list(INDIA_STATES_DISTRICTS.keys())


def get_districts(state):
    """Return districts for a selected state/UT."""
    return INDIA_STATES_DISTRICTS.get(state, [])


def is_valid_district(state, district):
    """Check whether district belongs to selected state."""
    return district in INDIA_STATES_DISTRICTS.get(state, [])


def get_ev_corridor(corridor_id):
    """Return information about a configured EV corridor."""
    return INDIAN_EV_CORRIDORS.get(corridor_id)


def get_charging_operator(operator_id):
    """Return charging operator configuration."""
    return CHARGING_NETWORKS.get(operator_id)


def get_default_charging_price(charger_type):
    """Return demo/default price for a charger category."""
    return DEFAULT_CHARGING_PRICING.get(charger_type, 12.0)
