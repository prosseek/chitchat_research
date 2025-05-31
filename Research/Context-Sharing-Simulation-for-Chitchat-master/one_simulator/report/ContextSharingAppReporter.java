package report;

import applications.ContextSharingApplication;
import applications.PingApplication;
import core.*;
import smcho.ContextMessage;
import smcho.Database;
import smcho.DatabaseWithStrategy;

import java.util.List;

/**
 * Reporter for the <code>PingApplication</code>. Counts the number of pings
 * and pongs sent and received. Calculates success probabilities.
 *
 * @author teemuk
 */
public class ContextSharingAppReporter extends Report implements ApplicationListener, ConnectionListener, MessageListener {

    public static Database database = null;

    public void report(int from, int to, String event, int hostAddress)
    {
        System.out.printf("From:%d To:%d - %s (%d)\n", from, to, event, hostAddress);
    }
    public void report(int from, int to, String event)
    {
        System.out.printf("Host (%d) To (%d) - %s\n", from, to, event);
    }

    public static void setup(String directory, String strategy, String initialSummaryType, String hostSizes)
    {
        // application invokes setup function
        // application can be instantiated multiple times, so this checking code will
        // prevent creating database everytime application is instantiated
        if (database == null) {
            database = new DatabaseWithStrategy(strategy, directory, initialSummaryType, hostSizes);
            //database.load(directory, hostSize);
        }
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
        }
    }


    @Override
    public void done() {
        String directory = ContextSharingApplication.directory;

        smcho.Storage storage = database.getStorage();

        System.out.println(storage.repr());
        String name = "result_" + ContextSharingApplication.strategy + "_" + ContextSharingApplication.summaryType + ".json";
        storage.save(directory + "/results/" + name);
        super.done();
    }

    @Override
    public void newMessage(Message m) {
        System.out.printf("%5.2f: New message %d -> %d (%s)\n", SimClock.getTime(), m.getFrom().getAddress(), m.getTo().getAddress(), m.getId());
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
    public void messageTransferred(Message msg, DTNHost from, DTNHost to, boolean firstDelivery) {

        String type = (String)msg.getProperty("type");
        if (type == "context") { // message transferred
            if (msg.getTo().getAddress() == to.getAddress()) {
                System.out.printf("%5.2f: message transferred (%s) at %d\n", SimClock.getTime(), msg.getId(), to.getAddress());
                ContextMessage contextMessage = messageToContextMessage(msg);
                database.add(to.getAddress(), contextMessage);
            }
        }

        //System.out.printf("Tranferred message %d -> %d (%s) %b\n", from.getAddress(), to.getAddress(), m.getId(), firstDelivery);
    }

    /**
     * 2.3 When hosts are connected, the created context at 2.2 is made into message.
     *
     * @param host1 Host that initiated the connection
     * @param host2 Host that was connected to
     */
    @Override
    public void hostsConnected(DTNHost host1, DTNHost host2) {
        // Show message
        System.out.printf("%5.2f: Connected: %d <-> %d\n", SimClock.getTime(), host1.getAddress(), host2.getAddress());

        // get Context
        int h1 = host1.getAddress();
        int h2 = host2.getAddress();
        double simTime = SimClock.getTime();

        ContextMessage c1 = database.get(h1);
        c1.setHost1(h1); c1.setHost2(h2); c1.setTime(simTime);
        ContextMessage c2 = database.get(host2.getAddress());
        c2.setHost1(h2); c2.setHost2(h1); c2.setTime(simTime);

        // Message is created from the context
        // todo:: Better exception handling than printing the trace
        try {
            Message m1 = contextMessageToMessage(host1.getAddress(), host2.getAddress(), c1);
            Message m2 = contextMessageToMessage(host2.getAddress(), host1.getAddress(), c2);
            host1.createNewMessage(m1);
            host2.createNewMessage(m2);
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Override
    public void hostsDisconnected(DTNHost host1, DTNHost host2) {
        System.out.printf("%5.2f: Disconnected %d <-> %d\n", SimClock.getTime(), host1.getAddress(), host2.getAddress());
    }
    //endregion

    //region PRIVATE METHODS
    private DTNHost getHost(int id) throws Exception {
        SimScenario sim = SimScenario.getInstance();
        List<DTNHost> hosts = sim.getHosts();

        for (DTNHost h: hosts) {
            if (h.getAddress() == id) return h;
        }
        throw new Exception(String.format("No matching host id %d", id));
    }

    private Message contextMessageToMessage(int host1, int host2, ContextMessage contextMessage) throws Exception {
        contextMessage.setHost1(host1);
        contextMessage.setHost2(host2);
        return contextMessageToMessage(contextMessage);
    }

    private Message contextMessageToMessage(ContextMessage contextMessage) throws Exception {
        int host1 = contextMessage.host1();
        int host2 = contextMessage.host2();
        DTNHost dtnhost1 = getHost(host1);
        DTNHost dtnhost2 = getHost(host2);
        int size = contextMessage.size();
        double simTime = contextMessage.time();
        String message = contextMessage.nameTypesString(); //String.format(MESSAGE_FORMAT, host1, host2, size, simTime) + contextMessage.getContent();

        Message m1 = new Message(dtnhost1, dtnhost2, message, size);
        m1.addProperty("type", "context");
        //m1.setAppID(APP_ID);
        return m1;
    }

    /**
     *
     * Given a message, make it into a context
     *
     * @param msg
     * @return
     */
    public static ContextMessage messageToContextMessage(Message msg) {
        double clock = SimClock.getTime();
        return new ContextMessage(
                msg.getFrom().getAddress(),
                msg.getTo().getAddress(),
                clock,
                msg.getId(),
                msg.getSize());
    }
    //endregion
}
