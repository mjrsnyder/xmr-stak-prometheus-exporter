# xmr-stak-prometheus-exporter
A [prometheus exporter](https://prometheus.io/docs/instrumenting/exporters/) for the [xmr-stak](https://github.com/fireice-uk/xmr-stak) [Monero](https://getmonero.org/) mining application

xmr-stak-prometheus-exporter makes metrics from the json api in xmr-stak availible to prometheus for one or more instances of xmr-stak.  Once the metrics are in prometheus you can configure alerts and make cool dashboards in [Grafana](https://grafana.com/)

### Features:

 * Supports xmr-stak (_other flavors of xmr-stak-* may work but haven't been tested_)
 * Monitor multiple instances of xmr-stak with a single instance of the exporter
 * Easy to run using Docker

### Quick Start:

Make sure your xmr-stak instances have the http server enabled by setting the `httpd_port` config option to an availible port.

```bash
docker run -d \
    --restart always \
    -p 6132:6132 \
    -e XMR_STAK_EXPORTER_HOSTS="http://<xmr-stak hostname or IP>:<httpd_port>/api.json" \
    mjrsnyder/xmr-stak-prometheus-exporter:latest
```

More than one host can be specified by setting `XMR_STAK_EXPORTER_HOSTS` to a coma separated list of instances.

Add the following to your `scrape_configs:` section in your prometheus configuration:
```yaml
  - job_name: 'xmr-stak'
    static_configs:
      - targets: ['<hostname or IP of the exporter>:6132']
```
Reload your prometheus config and you should be getting new metrics.

A Grafana dashboard is also included 

![Grafana Dashboard](https://i.imgur.com/Ld36GaZ.png)

### Contributing:

Feedback and pull requests are welcome! 