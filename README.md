This is an extended version of the Glances core integration.

This uses a modified version of the glances_api to also return the results from using the AMPS plugin and also adds in the container info per container.

I have a script that runs on the AMPS plugin to get the number of updates available for the package manager APT. This then stores the result and uploads it to HA via Glances2 integration

Next it lists the container images on the docker server and their Name, CPU, uptime, id and Mem use per container (running or not).