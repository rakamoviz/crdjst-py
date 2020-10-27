import glob
import functools
import re
import importlib

glob.glob('rate_fetchers/*.py')

def _filename_to_rate_fetchers(rate_fetchers, filename):
  key = re.match("^rate_fetchers/(.+)\.py$", filename).groups(0)[0]
  rate_fetcher = importlib.import_module(f"rate_fetchers.{key}")
  rate_fetchers[key] = rate_fetcher

  return rate_fetchers

rate_fetchers = functools.reduce(
  _filename_to_rate_fetchers, 
  glob.glob('rate_fetchers/*.py'), {}
)

for key in rate_fetchers:
  rate_fetchers[key].print_func("", "")