# dvidsync [![Picture](https://raw.github.com/janelia-flyem/janelia-flyem.github.com/master/images/HHMI_Janelia_Color_Alternate_180x40.png)](http://www.janelia.org)

**Status: Under Development**

This package syncs a subset of operations between two [DVID](https://github.com/janelia-flyem/dvid.git") repositories.  This package assumes two DVID servers pointing to copies of the same database.  The sync service will ensure that certain operations on the source server (like merge, split) will be performed on the destination server.

Potential applications:

* Enable a separate DVID server to be used exclusively for proofreading training (so as not to interfere with the production server).  The segmentation from the master branch could sync with this training server enabling practice sessions to be performed off of up-to-date segmentation.  The training data does not get synced back to the production server.
* Keep an up-to-date cloud-snapshot of a local DVID reconstruction to facilitate real-time data release and collaboration.

## Installation

Dependencies:

* kafka-python
* libdvid-python

Requirements:

* Kafka server where DVID produced events
* DVID servers for source and destination

Install:

% python setup.py build
% python setup.py install
 
This package must have access to two DVID servers and a Kafka server.

## Running

To start syncing between two running DVIDs:

% dvidsync config.json

which will listen to events on a Kafka server produced by DVID and apply supported actions on the destination server.  This program will ensure that a event is read once and only once.

Sample config json:

```python
{
    "source": "DVIDSERVER1",
    "destination": "DVIDSERVER2",
    "repoinfo": {
        "REPOUUID" : {
            "branches" : ["all"] or [BRANCH LIST]
            "datauuids": [[LABELNAME, DATAUUID]...]
        }
    },
    "kafkaservers": [KAFKASERVERS],
    "log": "LOGLOC"
}
```

## TODO

* support split and branching operations
* support google bucket destinations
* improve robustness of kafka interface
