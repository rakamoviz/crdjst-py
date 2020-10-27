import os
from dateutil.parser import parse as parse_date
import requests
from lxml import etree

class RateFetcher:
  def __init__ (self, logger):
    self.logger = logger

  def _fetch_from_site (self, date_str):
    formated_date = parse_date(date_str).strftime("%Y-%m-%d")
    url = f"{os.environ['BANXICO_URL']}/SieAPIRest/service/v1/series/SF43718/datos/{formated_date}/{formated_date}?mediaType=xml"
    
    response = requests.get(
      url, headers={'Bmx-Token': os.environ['BANXICO_TOKEN']}, 
      timeout=float(os.environ.get('BANXICO_TIMEOUT') or 30)
    )

    if (response.status_code != 200):
      raise Exception(f"rate-provider error ({response.status_code}) from banxico")

    return response.text

  def obtain_rate (self, date_str):
    xml_str = self._fetch_from_site(date_str)

    banxico_rates = etree.fromstring(xml_str.encode())

    datoElms = banxico_rates.xpath("/series/serie/Obs/dato")
    if (len(datoElms) < 1):
      return "n/a"

    return datoElms[0].text