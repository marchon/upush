import pybloomfilter
import uuid
import random

InitialArray = []
storage = []
sentitems = []
receiveditems = []
for i in range(1000):
    InitialArray.append(str(uuid.uuid4()))

#print InitialArray

sendqueue = pybloomfilter.BloomFilter(1024, 0.0011, '/tmp/words1')
sentqueue = pybloomfilter.BloomFilter(1024, 0.0011, '/tmp/words2')

HOLDINGCELL = []
for Packet in range(1000):
  ElementValue = InitialArray.pop()
  sendqueue.update(ElementValue)
  storage.append(ElementValue)
  if random.randrange(1000) > 970:
      print "%s %s LOST IN TRANSIT"  % (' '*60,ElementValue)
      continue
  sentitems.append(ElementValue)
  sentqueue.update(ElementValue)
  #print "SENT %s " % ElementValue

NN1 = sendqueue.to_base64()

receivedqueue = pybloomfilter.BloomFilter(1024, 0.0011, '/tmp/words3')
for item in sentitems:
        receiveditems.append(item)
        receivedqueue.update(item)
if receivedqueue.to_base64() <> NN1:
    print "Checksum does not match -- QUEUE MISMATCH"
    print "returning received Checksum %s " % receivedqueue.to_base64()

    FindMissingFromChecksumID = receivedqueue.to_base64()

MNM = sentitems[:]

print FindMissingFromChecksumID

#BloomFilter(1024, 0.1, '/tmp/words4')
verifyqueue = pybloomfilter.BloomFilter.from_base64('/tmp/words5', FindMissingFromChecksumID)
for item in MNM:
    QueueBeforeAdd = verifyqueue.to_base64()
    verifyqueue.update(item)
    QueueAfterAdd = verifyqueue.to_base64()
    print
    if QueueAfterAdd[:] == QueueBeforeAdd[:]:
        storage.remove(item)
        print "REMOVED ITEM AS SENT %s " % item.strip()

QueueAfterAdd = verifyqueue.to_base64()
if QueueAfterAdd[:] == NN1[:]:
   print "All Packetes Found"
else:
   for item in storage:
        print "packet missing %s  RETRANSMITTING" % item.strip()
        sentitems.append(item)
        sentqueue.update(item)

MNM = storage[:]
for item in MNM:
    QueueBeforeAdd = verifyqueue.to_base64()
    verifyqueue.update(item)
    QueueAfterAdd = verifyqueue.to_base64()
    print
    if QueueAfterAdd[:] == QueueBeforeAdd[:]:
        try:
             storage.remove(item)
        except:
            pass # Item may have already been removed

        print "REMOVED ITEM AS SENT %s " % item.strip()


print "Storage %s" % storage
