# import elasticsearch
from ned.producer import Producer
from ned.records import DNSRecordRequest, DNSRecordResponse, NetflowRecord

# from ned.output import generate_to_elastic
# from testcontainers.elasticsearch import ElasticSearchContainer
# import os


def test_generation_netflow():
    producer = Producer(record_type="netflow")
    generator = producer.generate_records(amount=10, anomalous=False)
    generator_anomalies = producer.generate_records(amount=10, anomalous=True)
    generated_netflows = [record for record in generator]
    generated_anomalies = [record for record in generator_anomalies]
    assert type(generated_netflows[0]) is NetflowRecord
    assert type(generated_anomalies[0]) is NetflowRecord
    assert len(generated_netflows) == 10
    # if "DOCKER" not in os.environ:
    #     with ElasticSearchContainer(image="docker.elastic.co/elasticsearch/elasticsearch:7.15.0") as es:
    #         connection_url = es.get_url()
    #         es_client = elasticsearch.Elasticsearch(connection_url)
    #         generate_to_elastic(es_client, generated_netflows, "netflow", "netflow")


def test_generation_dns():
    producer = Producer(record_type="dns")
    generator = producer.generate_records(amount=10, anomalous=False)
    generator_anomalies = producer.generate_records(amount=10, anomalous=True)
    generated_dns = [record for record in generator]
    generated_anomalies = [record for record in generator_anomalies]
    assert type(generated_dns[0][0]) is DNSRecordRequest
    assert type(generated_dns[0][1]) is DNSRecordResponse
    assert type(generated_anomalies[0][0]) is DNSRecordRequest
    assert type(generated_anomalies[0][1]) is DNSRecordResponse
    assert len(generated_dns) == 10
    # if "DOCKER" not in os.environ:
    #     with ElasticSearchContainer(image="docker.elastic.co/elasticsearch/elasticsearch:7.15.0") as es:
    #         connection_url = es.get_url()
    #         es_client = elasticsearch.Elasticsearch(connection_url)
    #         generate_to_elastic(es_client, generated_dns, "dns", "dns")
