from prometheus_client import start_http_server, Metric, REGISTRY
import json
import requests
import sys
import time
import os

class JsonCollector(object):
  def __init__(self, endpoints):
    self._endpoints = endpoints
  def collect(self):
    for endpoint in self._endpoints:
      # Fetch the JSON
      response = json.loads(requests.get(endpoint).content.decode('UTF-8'))

      # Shares
      metric = Metric('xmr_stak_shares', 
          'Shares published to the pool', 'counter')
      metric.add_sample('xmr_stak_shares_processed', 
        value=response['results']['shares_total'], labels={'xmr_stak_instance': endpoint})
      metric.add_sample('xmr_stak_shares_accepted', 
        value=response['results']['shares_good'], labels={'xmr_stak_instance': endpoint})
      yield metric

      # Total hashes
      metric = Metric('xmr_stak_hashes',
          'Total hashrate for xmr-stak', 'counter')
      metric.add_sample('xmr_stak_hashes_count',
        value=response['results']['hashes_total'], labels={'xmr_stak_instance': endpoint})
      yield metric

      # Connection Uptime
      metric = Metric('xmr_stak_connection_uptime',
          'Connection uptime for xmr-stak', 'counter')
      metric.add_sample('xmr_stak_uptime_count',
        value=response['connection']['uptime'], labels={'xmr_stak_instance': endpoint})
      yield metric

      # Difficulty
      metric = Metric('xmr_stak_difficulty',
          'Difficulty', 'gauge')
      metric.add_sample('xmr_stak_difficulty',
        value=response['results']['diff_current'], labels={'xmr_stak_instance': endpoint})
      yield metric

      # Thread hashrate
      metric = Metric('xmr_stak_threads',
          'Hashrate info for each thread', 'gauge')
      for index, thread in enumerate(response['hashrate']['threads']):
        metric.add_sample('xmr_stak_thread_hashrate', 
          value=thread[1], 
          labels={'thread_id' : str(index),
                  'xmr_stak_instance': endpoint})
      yield metric

if __name__ == '__main__':

  # Get config options via env vars
  port = os.environ.get('XMR_STAK_EXPORTER_PORT', 6132)

  hosts = os.environ.get('XMR_STAK_EXPORTER_HOSTS', 'http://localhost:5555').split(',')

  interval = os.environ.get('XMR_STAK_EXPORTER_INTERVAL', 5)

  # Usage: json_exporter.py port endpoint
  start_http_server(int(port))
  REGISTRY.register(JsonCollector(hosts))

  while True: time.sleep(interval)
