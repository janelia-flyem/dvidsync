"""Main functionality for syncing dvid severs.
"""

from kafka import KafkaConsumer
from kafka import TopicPartition
import json
from libdvid import DVIDNodeService, ConnectionMethod

def sync(config):
    logdata = {}

    # parse log if it exists
    # (log is a dictionary of topic and current offset)
    try:
        with open(config["log"]) as log:
            logdata = json.load(log)
    except (IOError, OSError) as e:
        pass

    # open up new dvid connections for each write UUID
    dviddest = str(config["destination"])
    
    topics = []

    # maps topics to instance name (for convenience)
    topic2instname = {}

    for repo, repoinfo in config["repoinfo"].items():
        # TODO: support branch operations
        for datainfo in repoinfo["datauuids"]:
            topics.append("dvidrepo-"+str(repo)+"-inst-"+str(datainfo[1]))
            topic2instname["dvidrepo-"+str(repo)+"-inst-"+str(datainfo[1])] = datainfo[0]
    
    # create kafka consumer
    consumer = KafkaConsumer(bootstrap_servers=config["kafkaservers"])
   
    # assign topic partitions
    topicparts = []
    for topic in topics:
        topicparts.append(TopicPartition(topic=topic, partition=0))
    consumer.assign(topicparts)

    # set offset (default 0 if nothing yet synced)
    for topic in topics:
        if topic in logdata:
            consumer.seek(TopicPartition(topic=topic, partition=0), logdata[topic])
        else:
            consumer.seek(TopicPartition(topic=topic, partition=0), 0)

    # listen for kafka events (kill with keyboard interrupt)
    try:
        for msg in consumer:
            dvidmsg = json.loads(msg.value)
            # (currently only handles merges)
            # TODO: support splits and branch operations
            if dvidmsg["Action"] == "merge":
                # perform merge at uuid
                ns = DVIDNodeService(dviddest, dvidmsg["UUID"])
                mergejson = [dvidmsg["Target"]]
                mergelabels = dvidmsg["Labels"]
                mergejson.extend(mergelabels)

                # call merge
                ns.custom_request("/" + topic2instname[msg.topic] + "/merge", json.dumps(mergejson).encode(), ConnectionMethod.POST)

            else:
                # Should this be a fatal error?
                print("Not supported: ", msg.value)

            # set new offset in log
            logdata[msg.topic] = msg.offset + 1
            fout = open(config["log"], 'w')
            fout.write(json.dumps(logdata))
    except KeyboardInterrupt:
        fout = open(config["log"], 'w')
        fout.write(json.dumps(logdata))
        print("Quit syncing ... restart will resume syncing from queue")    

