import pandas as pd
from prometheus_api_client import PrometheusConnect


class MDSMetricQuery(object):

    def __init__(self):
        conf = {
            "url": "http://<prometheus_server>",
            "disable_ssl": True
        }
        self._metrics = PrometheusConnect(**conf)

    @property
    def metrics(self):
        return self._metrics

    def get_metric_value(self, base_df=None,  *metric_names):
        for metric_name in metric_names:
            metric_data = self.metrics.get_metric_range_data(
                metric_name=metric_name['metric_name']
            )

            metric = [
                {
                    'instance': x['metric']['instance'],
                    metric_name['metric_name'].replace(
                        'mds_', ''
                    ): x['values'][0][1],
                    metric_name['column_name']: x['values'][-1][1]
                } for x in metric_data
            ]
            metric = pd.DataFrame.from_dict(metric)
            base_df = base_df.merge(metric, on='instance', how='inner')
        return base_df
