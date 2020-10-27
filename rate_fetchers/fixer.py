import os
from dateutil.parser import parse as parse_date
import requests
import json

class RateFetcher:
  def __init__ (self, logger):
    self.logger = logger

  def _fetch_from_site (self, date_str):
    formated_date = parse_date(date_str).strftime("%Y-%m-%d")
    url = f"http://{os.environ['FIXER_HOST']}/api/{formated_date}?access_key={os.environ['FIXER_API_KEY']}&base=USD&symbols=MXN"
    
    response = requests.get(
      url, timeout=float(os.environ.get('FIXER_TIMEOUT') or 30)
    )

    if (response.status_code != 200):
      raise Exception(f"rate-provider error ({response.status_code}) from fixer")

    return response.text

  def obtain_rate (self, date_str):
    json_str = self._fetch_from_site(date_str)

    fixer_rates = json.loads(json_str)
    
    if (fixer_rates.get('rates') is None):
      return "n/a"

    rate = fixer_rates.get('rates').get('MXN')
    if (rate is None):
      return "n/a"  

    return rate