from utils import request
from config import base_url, params, country_codes, documentTypes


for documentType, documentType_code in documentTypes.items():
  params['documentType'] = documentType_code
  for country_name, country_code in country_codes.items():
      params['in_Domain'] = country_code
      filename = f'data/raw/Actual_{documentType}_{country_name}.xml'
      description = f'Actual {documentType} in {country_name}'
      request(base_url, params, filename, description)