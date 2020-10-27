import glob
import functools
import re
import importlib

class CoreBusiness:
  def __init__ (self, logger):
    self.logger = logger
    self.rate_fetchers = functools.reduce(
      lambda rate_fetchers, filename: CoreBusiness._filename_to_rate_fetchers(
        logger, rate_fetchers, filename
      ), glob.glob('rate_fetchers/*.py'), {}
    )

  @staticmethod
  def _filename_to_rate_fetchers (logger, rate_fetchers, filename):
    key = re.match("^rate_fetchers/(.+)\.py$", filename).groups(0)[0]
    rate_fetcher = importlib.import_module(f"rate_fetchers.{key}")
    rate_fetchers[key] = rate_fetcher.RateFetcher(logger)

    return rate_fetchers

  def obtain_rates (self, date_str):
    return [{item[0]: item[1].obtain_rate(date_str)} for item in self.rate_fetchers.items()]