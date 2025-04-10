This is an extended version of the Glances core integration.

This uses a modified version of the glances_api to also return the results from using the AMPS plugin.

I have a script that runs on the AMPS plugin to ge the number of updates available for the package manager APT. This then stores teh result and uploads it to HA via Glances2 integration

Next is to list the available dockers running and their CName, CPU and Mem use per container (running or not)