/* 
 * Copyright 2010 Aalto University, ComNet
 * Released under GPLv3. See LICENSE.txt for details. 
 */

package report;

import applications.PingApplication;
import core.*;

/**
 * Reporter for the <code>PingApplication</code>. Counts the number of pings
 * and pongs sent and received. Calculates success probabilities.
 * 
 * @author teemuk
 */
public class PingAppReporter extends Report implements ApplicationListener, MessageListener {

    private int pingsSent=0, pingsReceived=0;
    private int pongsSent=0, pongsReceived=0;

    public void report(int from, int to, String event, int hostAddress)
    {
        System.out.printf("From:%d To:%d - %s (%d)\n", from, to, event, hostAddress);
    }
    public void report(int from, int to, String event)
    {
        System.out.printf("Host (%d) To (%d) - %s\n", from, to, event);
    }

    public void gotEvent(String event, Object params, Application app,
            DTNHost host) {
        // Check that the event is sent by correct application type
        if (!(app instanceof PingApplication)) return;

        // params contain Address, which can be sender or receiver
        // This should not be null
        assert (params != null);

        if (params instanceof Message) {
            Message msg = (Message) params;
            //report(msg.getFrom().getAddress(), msg.getTo().getAddress(), event, host.getAddress());
        }
        else {
            assert (params instanceof Integer);
            int toAddress = (int) params;
            //report(host.getAddress(), toAddress, event);

            // Increment the counters based on the event type
            if (event.equalsIgnoreCase("GotPing")) {
                pingsReceived++;
            }
            if (event.equalsIgnoreCase("SentPong")) {
                pongsSent++;
            }
            if (event.equalsIgnoreCase("GotPong")) {
                pongsReceived++;
            }
            if (event.equalsIgnoreCase("SentPing")) {
                pingsSent++;
            }
        }
    }


    @Override
    public void done() {
        write("Ping stats for scenario " + getScenarioName() +
                "\nsim_time: " + format(getSimTime()));
        double pingProb = 0; // ping probability
        double pongProb = 0; // pong probability
        double successProb = 0;	// success probability

        if (this.pingsSent > 0) {
            pingProb = (1.0 * this.pingsReceived) / this.pingsSent;
        }
        if (this.pongsSent > 0) {
            pongProb = (1.0 * this.pongsReceived) / this.pongsSent;
        }
        if (this.pingsSent > 0) {
            successProb = (1.0 * this.pongsReceived) / this.pingsSent;
        }

        String statsText = "pings sent: " + this.pingsSent +
            "\npings received: " + this.pingsReceived +
            "\npongs sent: " + this.pongsSent +
            "\npongs received: " + this.pongsReceived +
            "\nping delivery prob: " + format(pingProb) +
            "\npong delivery prob: " + format(pongProb) +
            "\nping/pong success prob: " + format(successProb)
            ;

        write(statsText);
        super.done();
    }

    @Override
    public void newMessage(Message m) {
        //System.out.printf("New message %d -> %d (%s)\n", m.getFrom().getAddress(), m.getTo().getAddress(), m.getId());
    }

    @Override
    public void messageTransferStarted(Message m, DTNHost from, DTNHost to) {

    }

    @Override
    public void messageDeleted(Message m, DTNHost where, boolean dropped) {
        System.out.printf("Deleted message at %d (%s) %b\n", where.getAddress(), m.getId(), dropped);
    }

    @Override
    public void messageTransferAborted(Message m, DTNHost from, DTNHost to) {
        System.out.printf("Aborted message from %d to %d (%s)\n", from.getAddress(), to.getAddress(), m.getId());

    }

    @Override
    public void messageTransferred(Message m, DTNHost from, DTNHost to, boolean firstDelivery) {
        //System.out.printf("Tranferred message %d -> %d (%s) %b\n", from.getAddress(), to.getAddress(), m.getId(), firstDelivery);
    }
}
