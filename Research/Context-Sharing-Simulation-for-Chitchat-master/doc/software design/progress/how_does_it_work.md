### [2015/08/15] When and what update() works?

![p](pic/update1.png)

1. runSim() updates world
2. world updates hosts
3. hosts updates router (this.router.update())
4. epimedic router updates

update() method.

    @Override
    public void update() {
        super.update();
        if (isTransferring() || !canStartTransfer()) {
            return; // transferring, don't try other connections yet
        }
        
        // Try first the messages that can be delivered to final recipient
        if (exchangeDeliverableMessages() != null) {
            return; // started a transfer, don't try others (yet)
        }
        
        // then try any/all message to any/all connection
        this.tryAllMessagesToAllConnections(); <-- 
    }
    
ActiveRouter -> MessageRouter

    protected Connection exchangeDeliverableMessages() {
        List<Connection> connections = getConnections();

        if (connections.size() == 0) {
            return null;
        }
        
        @SuppressWarnings(value = "unchecked")
        Tuple<Message, Connection> t =
            tryMessagesForConnected(sortByQueueMode(getMessagesForConnected()));
 
 Now, messages are beginning to be transferred:
            
    protected Tuple<Message, Connection> tryMessagesForConnected(
            List<Tuple<Message, Connection>> tuples) {
        if (tuples.size() == 0) {
            return null;
        }
        
        for (Tuple<Message, Connection> t : tuples) {
            Message m = t.getKey();
            Connection con = t.getValue();
            if (startTransfer(m, con) == RCV_OK) {
                return t;
            }
        }
        
        return null;
    }

### host.sendMessage()

startTransfer and sendMessage: they need not to be directly related. 

    public void sendMessage(String id, DTNHost to) {
        this.router.sendMessage(id, to);
    }

router uses only the id for sending the message, so the message should be stored. 

    public void sendMessage(String id, DTNHost to) {
        Message m = getMessage(id);
        Message m2;
        if (m == null) throw new SimError("no message for id " +
                id + " to send at " + this.host);
 
        m2 = m.replicate(); // send a replicate of the message
        to.receiveMessage(m2, this.host);
    }