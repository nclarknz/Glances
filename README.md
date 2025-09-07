This is an extended version of the Glances core integration in Home Assistant. It provides more data for the containers and also the output for any amps plugins that are configured (inlcuding custom). It shows a list of all containers installed on the system and its id, name, cpu usage, mem usuage, uptime and engine per each container.

This also uses a modified version of the glances_api to also return the results from using the AMPS plugin and also adds in the container info per container. In the glances2b_api directory, will need to copy the contents of this to the /usr/local/lib/python/site-packages/glances_api folder (May need to put the version number of python as well.) and overwite the existing ones (After taking a a backup of course) Everytime that HA is updated you may need to copy this over again. To this exec a bash shell on the homeassisstant docker image (If using a docker version of HA). 
e.g. docker exec -it {HA container id} bash
Then in the bash shell do the following at the command prompt.
cd
git clone https://github.com/nclarknz/Glances.git
cd Glances
cd glances2b_api
cp * /usr/local/lib/python3.13/site-packages/glances_api

Make sure the custom_components has been installed in HA through the HACS interface. (The github for glances2 needs to be added to the list of custom repositries for HACS as an integration)
Then goto Settings | Devies and click Add integration.
Search for glances2 as add this. Enter teh relevant details to connect to the host you have installed HA on.
This won't need to be updated when you update the HA docker image.

Then restart HA to get all of above working.

I have a script that runs on a custom AMPS plugin to get the number of updates available for the package manager APT. This then stores the result and uploads it to HA via Glances2 integration. So the api also returns all AMPs plugin results, as both the result text (results entity) and if a number is at the start of the result then it will return this as resultcount entity. I use this resultscount entity to return the number of packages available to be updated so I can then run automations based on this.

Once the data is in HA, then the containers can be shown in a markup card to view the data of each single container converted to a table. The containers data is stored in the attribute field (As this can store longer then 255 characters for the containers list entity)
In my case this is pointing at the localhost entity of the containers list, but change the name of the sensor to suit different setups.

This is the basic code for the markup card, but can be prettified using HTML tag markup if required.

<div>type: markdown</div>
<div>content: &gt;+</div>
<div>&lt;table&gt;</div>
<div>  &lt;tr&gt;</div>
<div>  &lt;th&gt;ID&lt;/th&gt;&lt;th&gt;Name&lt;/th&gt;&lt;th&gt;Status&lt;/th&gt;&lt;th&gt;Cpu&lt;/th&gt;&lt;th&gt;Memory&lt;/th&gt;&lt;th&gt;Uptime&lt;/th&gt;&lt;th&gt;Engine&lt;/th&gt;</div>
<div>  &lt;/tr&gt;</div>
<div>  {% set e_list = state_attr('sensor.localhost_containerslist', 'ContainerInfo')</div>
<div>  | sort(attribute= 's') | list %}</div>
<div>  {% set l_count = e_list | count %}</div>
<div>  {% for x in e_list %}</div>
<div>    &lt;tr&gt;</div>
<div>    &lt;td&gt;{{x.i[:4]}}&lt;/td&gt;</div>
<div>    &lt;td&gt;{{x.n}}&lt;/td&gt;</div>
<div>   &lt;td&gt;{{x.s}}&lt;/td&gt;</div>
<div>    &lt;td&gt;{{x.c}}&lt;/td&gt;</div>
<div>    &lt;td&gt;{{x.m}}&lt;/td&gt;</div>
<div>    &lt;td&gt;{{x.u}}&lt;/td&gt;</div>
<div>    &lt;td&gt;{{x.e}}&lt;/td&gt;</div>
<div>    &lt;/tr&gt;</div>
<div>  {% endfor %}</div>
<div>  &lt;/table&gt;</div>
