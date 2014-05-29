
puppet analytics
================

A web application to collect and display stats on puppet modules


Requires an elasticsearch running on localhost:9200



Viewing data
------------

Click around in the web gui


Adding data
-----------


To submit a module deploy event to puppet analytics, send a curl request like this:


```
[nibz@nexus ~]$ curl -XPOST 'localhost:5000/api/1/module_send' 
-H "Content-Type: ication/json" -d '{
"author": "nibz",
"name": "liesboard",
"tags": "test,ci,awesome"
}'
True[nibz@nexus ~]$
```
