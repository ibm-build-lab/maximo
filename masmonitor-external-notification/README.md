# Send alerts to external system from Maximo Monitor

Maximo Monitor, a powerful asset management monitoring tool, provides a comprehensive solution for monitoring various business processes, but sometimes, it's necessary to extend its capabilities to integrate with other systems. This is where a custom function that sends alerts to external systems by making REST calls comes into play.

This custom function enables organizations to configure high or low alerts and URLs to external systems, allowing them to receive notifications when alerts are generated in Maximo Monitor. This integration is particularly useful when external systems need to take action based on the alerts generated in Maximo Monitor. For instance, if an organization uses ServiceNow for incident management, they can configure the custom function to send alerts to ServiceNow, which will then trigger the appropriate incident management process.

## Configuration
Refer https://developer.ibm.com/tutorials/awb-send-alerts-external-system-maximo-monitor/ for configuration steps and installment.


## Prerequisite
1. [Python 3.9.x](https://www.python.org/downloads/release/python-390/)
2. [GitHub](https://github.com/)
3. Maximo Monitor instance
