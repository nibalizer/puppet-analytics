[![Build Status](https://travis-ci.org/nibalizer/puppet-analytics.png?branch=master)](https://travis-ci.org/nibalizer/puppet-analytics)

puppet analytics
================

A web application to collect and display statistics on puppet modules.
See it live at [http://puppet-analytics.org](http://puppet-analytics.org)



Note
----

Puppet Analytics is Super Beta. It is by no means done, and it needs work. It is best labeled as an experiment.



Goals
-----

The overall goal of this project is to enhance visibility into use of Puppet modules. Module maintainers need to know which versions of their software are being used. Users want to identify the most popular modules. The download numbers on the forge are insufficient for this: broken modules have hundreds or thousands of downloads, and some modules have artificially high download rate because of ci systems.


This effort borrows from the Debian Popularity Contest model. Instead of tracking which packages are downloaded from some server, we ask our users to report on their use. Puppet analytics introduces the concept of a 'deploy'. Ideally whenever a site updates their Puppet manifests, they run a script that runs through their modulepath reporting which modules and what versions are in use to puppet analytics. Thus we track 'deploys' of modules. There is a tagging system. Puppet analytics will split the tags field on commas and store all the tags that each deployment has used. This is an easy way for the community to feel out which tags make sense to report and keep track of.

Since the puppet analytics reporting script can be run as part of a git post-receive hook, reporting module statistics should integrate well into the dynamic branching model.


Viewing data
------------

Click around in the web gui


Adding data
-----------


To submit a module deploy event to puppet analytics, send a curl request like this:


```
[nibz@nexus ~]$ curl -XPOST 'http://puppet-analytics.org/api/1/module_send' -H "Content-Type: application/json" -d '{
"author": "puppetlabs",
"name": "stdlib",
"tags": "version=2.1.0,purpose=test,science"
}'
True[nibz@nexus ~]$
```


Or use a client from: https://github.com/nibalizer/puppet-analytics-client



Development
-----------

We congregate on freenode irc in ##puppet-analytics

Contributing is easy! Just send in a github pull request!



License
-------

Apache 2



Contributors
------------

Spencer Krum
Greg Haynes
William Hopper
Colleen Murphy
William Van Hevelingen

Special thanks to Ben Kero and Alan Sherman for making delicious burgers at our hackathon



Integration with r10k, puppet module tool, $THING
-------------------------------------------------


If this takes off, then likely we will try to integrate it with those tools. For now, puppet-analytics, is best labeled as an experiment. Until it's usefulness has been established and its api stabilized, it doesn't make sense to harass the authors of those tools.
