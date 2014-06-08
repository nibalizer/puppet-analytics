[![Build Status](https://travis-ci.org/nibalizer/puppet-analytics.png?branch=master)](https://travis-ci.org/nibalizer/puppet-analytics)

puppet analytics
================

A web application to collect and display statistics on puppet modules.
See it live at [http://puppet-analytics.org](http://puppet-analytics.org)



Viewing data
------------

Click around in the web gui


Adding data
-----------


To submit a module deploy event to puppet analytics, send a curl request like this:

```shell
curl -XPOST '127.0.0.1:5000/api/2/bulk_update' -H "Content-Type: application/json" -d '[
{
"author": "nibz",
"name": "liesboard",
"tags": "test,ci,awesome"
},
{
"author": "nibz",
"name": "liesboard",
"tags": "test,ci,awesome"
}]'
```



Development
-----------

We congregate on freenode irc in ##puppet-analytics

