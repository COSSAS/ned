# NED: The NEtwork Data producer v0.6.0

* python package to quickly generate large amount of network data for all intents and purposes
* can push data to elasticsearch

usage(docker)
```
cp deployment/config-defaults.env deployment/config.env
nano deployment/config.env
docker run --env deployment/config.env registry.gitlab.com/notno/ned:v0.6.0 --to-elastic --type netflow
```

types & formats:
* netflows (suricata)
* dns (suricata)
