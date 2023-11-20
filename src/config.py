base_url = "https://web-api.tp.entsoe.eu/api"

security_token = '1d9cd4bd-f8aa-476c-8cc1-3442dc91506d'

params = {
    "securityToken": security_token,
    "processType": "A16", 
    "periodStart": "202201010000", 
    "periodEnd": "202301010000" 
}

country_codes = {
    'Spain': '10YES-REE------0',
    'United Kingdom': '10Y1001A1001A92E',
    'Germany': '10Y1001A1001A83F',
    'Denmark': '10Y1001A1001A65H',
    'Hungary': '10YHU-MAVIR----U',
    'Sweden': '10YSE-1--------K',
    'Italy': '10YIT-GRTN-----B',
    'Poland': '10YPL-AREA-----S',
    'Netherlands': '10YNL----------L',
}

documentTypes = {
  "Generation": "A75",
  "Load": "A65"
}