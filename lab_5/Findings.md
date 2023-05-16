# Lab 5 Findings - Giovanni Mola

- [Lab 5 Findings - \[Giovanni Mola\]](#lab-5-findings---Giovanni-Mola)
  - [Findings Summary](#findings-summary)
    - [Finding 1](#Finding-1-Request-volume-increase-with-increase-in-cache-rate)
    - [Finding 2](#Finding-2-Increase-cache-leads-to-decrease-in-request-duration)
    - [Finding 3](#Finding-3-Increase-in-cache-affects-sidecars-CPU-and-Memory)
  - [Conclusion](#conclusion)

---


## Findings Summary

This document provides an in depth summary of tests that were run to determine the most optimal cache rate for our application's rest endpoint. The out of the box ISTIO dashboards in Grafana provide out of the box metrics like resource utilization, network traffic and request latency. 

### Finding 1 Request volume increase with increase in cache rate
![Alt text](istio_workload_2.png?raw=true "Istio Workload Request Volume")
Here we can see that as our cache rate was increased from the range of 0, .25, .5 and 1 our endpoint was able to increase the amount of requests. 
### Finding 2 Increase cache leads to decrease in request duration
The corresponding increase in cache rate led to a decrease in the request duration times. 
![Alt text](istio_workload_3.png?raw=true "Istio Workload Request Duration")

### Finding 3 Increase in cache affects sidecars CPU and Memory
Increaseing our cache unsurprisingly increases the memory used by our sidecar while the cpu utilization starts high and planes off as more of the responses are stored in memory
![Alt text](sidecar_cpu_mem.png?raw=true "CPU Usage")


## Conclusion

From the above findings we can see that at increase in cache rate helps the performance of our endpoint by increasing the amount of requests our endpoint can process, lowering the request duration of the requests and increasing the overall load that our applicaion can handle. 

### Appendix additional dashboard views
![Alt text](istio_service_1.png?raw=true "CPU Usage")
![Alt text](istio_workload_1.png?raw=true "CPU Usage")
