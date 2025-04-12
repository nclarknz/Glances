This is an extended version of the Glances core integration.

This uses a modified version of the glances_api to also return the results from using the AMPS plugin and also adds in the container info per container.

I have a script that runs on the AMPS plugin to get the number of updates available for the package manager APT. This then stores the result and uploads it to HA via Glances2 integration

Next it lists the container images on the docker server and their Name, CPU, uptime, id and Mem use per container (running or not).

Once the data is in HA, then the containers can be shown in a markup card to view the data of each single container converted to a table. The containers data is stoed in the attribute field (As this can store longer then 255 characters for the containers list entity)
In my case this is pointing at the localhost entity of the container slist, but change the name of the sensor to suit different setups.

This is the basic code, but can be prettified using HTML tag markup if required.

type: markdown
content: &gt;+
  &lt;table&gt;
  &lt;tr&gt;
  &lt;th&gt;ID&lt;/th&gt;&lt;th&gt;Name&lt;/th&gt;&lt;th&gt;Status&lt;/th&gt;&lt;th&gt;Cpu&lt;/th&gt;&lt;th&gt;Memory&lt;/th&gt;&lt;th&gt;Uptime&lt;/th&gt;&lt;th&gt;Engine&lt;/th&gt;
  &lt;/tr&gt;
  {% set e_list = state_attr('sensor.localhost_containerslist', 'ContainerInfo')
  | sort(attribute= 's') | list %}
  {% set l_count = e_list | count %}
  {% for x in e_list %}
    &lt;tr&gt;
    &lt;td&gt;{{x.i[:4]}}&lt;/td&gt;
    &lt;td&gt;{{x.n}}&lt;/td&gt;
   &lt;td&gt;{{x.s}}&lt;/td&gt;
    &lt;td&gt;{{x.c}}&lt;/td&gt;
    &lt;td&gt;{{x.m}}&lt;/td&gt;
    &lt;td&gt;{{x.u}}&lt;/td&gt;
    &lt;td&gt;{{x.e}}&lt;/td&gt;
    &lt;/tr&gt;
  {% endfor %}
  &lt;/table&gt;