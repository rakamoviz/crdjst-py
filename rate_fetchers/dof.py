import os
from dateutil.parser import parse as parse_date
import requests
from scrapy.selector import Selector

class RateFetcher:
  def __init__ (self, logger):
    self.logger = logger

  def _fetch_from_site (self, date_str):
    formated_date = parse_date(date_str).strftime("%d/%m/%Y")
    response = requests.post(
      os.environ['DOF_URL'], data={
        'idioma': "sp",
        'fechaInicial': formated_date,
        'fechaFinal': formated_date,
        'salida': 'HTML'
      }, timeout=float(os.environ.get('DOF_TIMEOUT') or 30)
    )

    if (response.status_code != 200):
      raise Exception(f"rate-provider error ({response.status_code}) from dof")

    return response.text

  def obtain_rate (self, date_str):
    html_str = self._fetch_from_site(date_str)

    ratePath = Selector(text=html_str).xpath("/html/body/table/tr[2]/td[1]/table/tr[2]/td[4]/table/tr/td/text()").get()
    
    if (ratePath is None):
      return 'n/a'
    
    return ratePath.strip()