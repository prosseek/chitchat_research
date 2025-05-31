### Active Router << MessageRouter [2015/08/15]

#### startTransfer

#### update

In update(), it invokes finalize transfer() in the connection. 

    public void update() {      
        super.update(); // << MessageRouter's update
        
        /* in theory we can have multiple sending connections even though
          currently all routers allow only one concurrent sending connection */
        for (int i=0; i<this.sendingConnections.size(); ) {
            boolean removeCurrent = false;
            Connection con = sendingConnections.get(i);
            
            /* finalize ready transfers */
            if (con.isMessageTransferred()) {
                if (con.getMessage() != null) {
                    transferDone(con);
                    con.finalizeTransfer();
                } /* else: some other entity aborted transfer */
                removeCurrent = true;
            }

### Message Router [2015/08/15]

In `MessageRouter`, update() always calls the update in the app. 

    /**
     * Updates router.
     * This method should be called (at least once) on every simulation
     * interval to update the status of transfer(s). 
     */
    public void update(){
        for (Collection<Application> apps : this.applications.values()) {
            for (Application app : apps) {
                app.update(this.host);
            }
        }
    }
    
#### sendMessage(String id, DTNHost to)

Host's sendMessage is invoking `this.router.sendMessage()`

    public void sendMessage(String id, DTNHost to) {
        Message m = getMessage(id);
        Message m2;
        if (m == null) throw new SimError("no message for id " +
                id + " to send at " + this.host);
 
        m2 = m.replicate(); // send a replicate of the message
        to.receiveMessage(m2, this.host);
    }
    
### Connection [2015/08/15]

It's a connection between nodes, it uses "MessageRouter".


#### finalizeTransfer

When a connection finalizes the transfer, the host is invoked. 

    public void finalizeTransfer() {
        assert this.msgOnFly != null : "Nothing to finalize in " + this;
        assert msgFromNode != null : "msgFromNode is not set";
        
        this.bytesTransferred += msgOnFly.getSize();

        getOtherNode(msgFromNode).messageTransferred(this.msgOnFly.getId(),
                msgFromNode);
        clearMsgOnFly();
    }