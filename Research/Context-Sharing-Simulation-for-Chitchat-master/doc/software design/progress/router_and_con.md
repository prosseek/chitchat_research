### [2015/08/15]

ActiveRouter uses con to start transfer. 

    protected int startTransfer(Message m, Connection con) {
        int retVal;
        
        if (!con.isReadyForTransfer()) {
            return TRY_LATER_BUSY;
        }
        
        if (!policy.acceptSending(getHost(), 
                con.getOtherNode(getHost()), con, m)) {
            return MessageRouter.DENIED_POLICY;
        }
        
        retVal = con.startTransfer(getHost(), m);
        if (retVal == RCV_OK) { // started transfer
            addToSendingConnections(con);
        }
        else if (deleteDelivered && retVal == DENIED_OLD && 
                m.getTo() == con.getOtherNode(this.getHost())) {
            /* final recipient has already received the msg -> delete it */
            this.deleteMessage(m.getId(), false);
        }
        
        return retVal;
    }

CBRConnection.startTransfer() uses the same receiveMessage() for data transfer. 
    
    public int startTransfer(DTNHost from, Message m) {
        assert this.msgOnFly == null : "Already transferring " + 
            this.msgOnFly + " from " + this.msgFromNode + " to " + 
            this.getOtherNode(this.msgFromNode) + ". Can't " + 
            "start transfer of " + m + " from " + from;

        this.msgFromNode = from;
        Message newMessage = m.replicate();
        int retVal = getOtherNode(from).receiveMessage(newMessage, from);

        if (retVal == MessageRouter.RCV_OK) {
            this.msgOnFly = newMessage;
            this.transferDoneTime = SimClock.getTime() + 
            (1.0*m.getSize()) / this.speed;
        }

        return retVal;
    }
