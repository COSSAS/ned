# """
# prints random dga logs using suricata format
# """

# import datetime
# import json
# import logging
# import os
# import random
# import time
# from datetime import timedelta
# from random import randint

# from elasticsearch import Elasticsearch

# logging.basicConfig(
#     format="%(levelname)s: %(message)s",
#     level=os.environ.get(key="LOG_LEVEL", default="ERROR").upper(),
# )

# example_dns_query = {
#     "timestamp": "2021-03-04T14:44:23.464363+0100",
#     "flow_id": 645842343577326,
#     "in_iface": "ens224",
#     "event_type": "dns",
#     "vlan": 510,
#     "src_ip": "10.142.10.2",
#     "src_port": 47856,
#     "dest_ip": "94.127.57.66",
#     "dest_port": 53,
#     "proto": "UDP",
#     "metadata": {"flowbits": ["MSS.not_whitelisted_dnsdomains"]},
#     "dns": {
#         "type": "query",
#         "id": 39037,
#         "rrname": "avupdate.fireeye.com",
#         "rrtype": "A",
#         "tx_id": 249162,
#     },
# }
# example_dns_reply = {
#     "timestamp": "2021-03-04T14:44:23.471363+0100",
#     "flow_id": 645842343577326,
#     "in_iface": "ens224",
#     "event_type": "dns",
#     "vlan": 510,
#     "src_ip": "94.127.57.66",
#     "src_port": 53,
#     "dest_ip": "10.142.10.2",
#     "dest_port": 47856,
#     "proto": "UDP",
#     "metadata": {"flowbits": ["MSS.not_whitelisted_dnsdomains"]},
#     "dns": {
#         "version": 2,
#         "type": "answer",
#         "id": 39037,
#         "flags": "8180",
#         "qr": "true",
#         "rd": "true",
#         "ra": "true",
#         "rrname": "avupdate.fireeye.com",
#         "rrtype": "A",
#         "rcode": "NOERROR",
#         "answers": [
#             {
#                 "rrname": "avupdate.fireeye.com",
#                 "rrtype": "CNAME",
#                 "ttl": 0,
#                 "rdata": "wpc.2d7dd.alphacdn.net",
#             },
#             {
#                 "rrname": "wpc.2d7dd.alphacdn.net",
#                 "rrtype": "CNAME",
#                 "ttl": 0,
#                 "rdata": "dual46.gs1.wpc.v2cdn.net",
#             },
#             {
#                 "rrname": "dual46.gs1.wpc.v2cdn.net",
#                 "rrtype": "A",
#                 "ttl": 3420,
#                 "rdata": "68.232.34.73",
#             },
#         ],
#         "grouped": {
#             "A": ["68.232.34.73"],
#             "CNAME": ["wpc.2d7dd.alphacdn.net", "dual46.gs1.wpc.v2cdn.net"],
#         },
#     },
# }

# src_ip = ["192.168.0.1", "192.168.0.2", "192.168.0.3"]
# dest_ip = ["192.168.0.4", "192.168.0.5", "192.168.0.6"]

# if __name__ == "__main__":
#     OUTPUT_MODE = os.environ.get(key="OUTPUT_MODE", default="stdout")
#     AMOUNT = int(os.environ.get(key="AMOUNT", default=10000))

#     if OUTPUT_MODE == "elasticsearch":
#         ES_HOST = os.environ.get(key="ES_HOST", default="http://localhost:9200")
#         ES_INDEX = os.environ.get(key="ES_INDEX", default="dns")
#         ES_USER = os.environ.get(key="ES_USER", default="elastic")
#         ELASTIC_PASSWORD = os.environ.get(key="ELASTIC_PASSWORD", default="changeme")
#         connected = False
#         while not connected:
#             try:
#                 es_client = Elasticsearch(
#                     hosts=[ES_HOST], http_auth=(ES_USER, ELASTIC_PASSWORD)
#                 )
#                 es_client.indices.create(index=ES_INDEX, ignore=400)
#                 connected = True
#                 print(f"connected to elasticsearch at {ES_HOST}")
#             except Exception:  # quick and really dirty
#                 logging.error("can't reach elasticsearch at %s, retrying...", ES_HOST)
#                 time.sleep(2)

#     for i in range(AMOUNT):
#         query = example_dns_query.copy()
#         reply = example_dns_reply.copy()

#         query["src_ip"] = src_ip[randint(0, 2)]  # nosec
#         query["dest_ip"] = dest_ip[randint(0, 2)]  # nosec
#         query["timestamp"] = (
#             datetime.datetime.now() + timedelta(seconds=i)
#         ).isoformat()
#         reply["src_ip"] = query["dest_ip"]
#         reply["dest_ip"] = query["src_ip"]
#         reply["timestamp"] = (
#             datetime.datetime.now() + timedelta(seconds=i + 1)
#         ).isoformat()

#         # add a DGA randomly
#         if random.randint(1, 10) % 10 == 0:  # nosec
#             query["dns"]["rrname"] = "adsfhasdlkjfhasdlkj.ru"
#             reply["dns"]["rrname"] = "adsfhasdlkjfhasdlkj.ru"

#         if OUTPUT_MODE == "stdout":
#             print(json.dumps(query))
#             print(json.dumps(reply))
#         elif OUTPUT_MODE == "elasticsearch":
#             print(query)
#             es_client.index(
#                 index=ES_INDEX, ignore=400, body=json.loads(json.dumps(query))
#             )
#             print(reply)
#             es_client.index(
#                 index=ES_INDEX, ignore=400, body=json.loads(json.dumps(reply))
#             )

#     if OUTPUT_MODE == "elasticsearch":
#         print(f"inserted {AMOUNT} entries in index {ES_INDEX}")
