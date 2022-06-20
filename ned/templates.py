suricata_template_netflow = {
    "timestamp": "",
    "flow_id": 0,
    "event_type": "flow",
    "src_ip": "",
    "src_port": 0,
    "dest_ip": "",
    "dest_port": 0,
    "proto": "TCP",
    "app_proto": "dcerpc",
    "flow": {
        "pkts_toserver": 0,
        "pkts_toclient": 0,
        "bytes_toserver": 0,
        "bytes_toclient": 0,
        "start": "",
        "end": "",
        "age": "0",
        "state": "established",
        "reason": "timeout",
        "alerted": "false",
    },
    "tcp": {
        "tcp_flags": "da",
        "tcp_flags_ts": "da",
        "tcp_flags_tc": "5a",
        "syn": "true",
        "psh": "true",
        "ack": "true",
        "ecn": "true",
        "cwr": "true",
        "state": "established",
    },
}

suricata_dns_template_request = {
    "timestamp": "",
    "flow_id": 0,
    "in_iface": "ens224",
    "event_type": "dns",
    "vlan": 510,
    "src_ip": "",
    "src_port": 0,
    "dest_ip": "",
    "dest_port": 0,
    "proto": "UDP",
    "metadata": {"flowbits": ["MSS.not_whitelisted_dnsdomains"]},
    "dns": {
        "type": "query",
        "id": "0",
        "rrname": "",
        "rrtype": "A",
        "tx_id": "249162",
    },
}

suricata_dns_template_response = {
    "timestamp": "",
    "flow_id": 0,
    "in_iface": "ens224",
    "event_type": "dns",
    "vlan": 510,
    "src_ip": "",
    "src_port": 0,
    "dest_ip": "",
    "dest_port": 0,
    "proto": "UDP",
    "metadata": {"flowbits": ["MSS.not_whitelisted_dnsdomains"]},
    "dns": {
        "version": 2,
        "type": "answer",
        "id": 39037,
        "flags": "8180",
        "qr": "true",
        "rd": "true",
        "ra": "true",
        "rrname": "",
        "rrtype": "A",
        "rcode": "NOERROR",
        "answers": [
            {
                "rrname": "",
                "rrtype": "CNAME",
                "ttl": 0,
                "rdata": "",
            }
        ],
        "grouped": {
            "A": [""],
            "CNAME": [""],
        },
    },
}
