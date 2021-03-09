# Sample commands

## Metric dumps

#### CPU usage

```
$ orca-tools dump-metrics cpu_usage \
    'sum(
        rate(
            container_cpu_usage_seconds_total{
                namespace="isotope"
            }[1m]
        )
    ) by (pod)' \
    --exp-start 1609927920 --exp-duration 120 \
    --ymin -0.1 --ymax 2 \
    --step 15 \
    --xmarker 1609927920
```

#### Memory usage in MB

```
$ orca-tools dump-metrics memory_usage \
    'sum(
        container_memory_working_set_bytes{
            namespace="isotope"
        }
    ) by (pod) / 1000 / 1000' \
    --exp-start 1609927920 --exp-duration 120 \
    --ymin -0.1 --ymax 2 \
    --step 15 \
    --xmarker 1609927920
```

#### Success rate

```
$ orca-tools dump-metrics success_rate \
    'sum(
        label_join(
            sum(
                rate(
                    istio_requests_total{
                        destination_service_namespace="isotope",
                        reporter="destination",
                        response_code!~"5.*"
                    }[1m]
                )
            ) by (destination_workload, destination_workload_namespace)
            /
            sum(
                rate(
                    istio_requests_total{
                        destination_service_namespace="isotope",
                        reporter="destination"
                    }[1m]
                )
            ) by (destination_workload, destination_workload_namespace),
            "series_name", ".", "destination_workload", "destination_workload_namespace"
        )
    ) by (series_name)' \
    --exp-start 1609927920 --exp-duration 120 \
    --ymin -0.1 --ymax 1.2 \
    --step 15 \
    --xmarker 1609927920
```

#### P90 latency

```
$ orca-tools dump-metrics p90_latency \
    'sum(
        label_join(
            histogram_quantile(
                0.90,
                sum(
                    rate(
                        istio_request_duration_milliseconds_bucket{
                            reporter="destination"
                        }[1m]
                    )
                ) by (le, destination_workload, destination_workload_namespace)
            )
            /
            1000,
            "series_name", ".", "destination_workload", "destination_workload_namespace"
        )
    ) by (series_name)' \
    --exp-start 1609927920 --exp-duration 120 \
    --ymin -0.5 --ymax 5 \
    --step 15 \
    --xmarker 1609927920
```

#### Incoming requests

```
$ orca-tools dump-metrics incoming_req \
    'sum(
        rate(
            istio_requests_total{
                destination_service_namespace="isotope",
                reporter="destination"
            }[1m]
        )
    ) by (destination_workload, destination_workload_namespace)' \
    --exp-start 1609927920 --exp-duration 120 \
    --step 15 \
    --xmarker 1609927920
```

#### Pod restarts

```
$ orca-tools dump-metrics kube_pod_restarts \
    'sum(
        rate(
            kube_pod_container_status_restarts_total{
             namespace="isotope"
            }[5m]
        )
    ) by (pod)' \
    --exp-start 1615293556 --exp-duration 120 \
    --step 15 \
    --xmarker 1615293556
```
