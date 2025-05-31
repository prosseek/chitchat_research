package applications;

import core.*;
import report.ContextSharingAppReporter;

public class ContextSharingApplication extends Application {
/**
 * An application to share contexts when hosts are connected in a DTN.
 *
 * 1. The corresponding <code>ContextSharingAppReporter</code> class can be used to record
 * information about the application behavior.
 *
 * 2. The mechanism is as follows:
 *    2.1 Each host makes their own context to be shared.
 *    2.2 When a message (context) is received, the context database is updated, and the next set of contexts
 *        are calculated.
 *    2.3 When hosts are connected, the created context at 2.2 is made into message.
 *
 * @see ContextSharingAppReporter
 * @author smcho
 */
    /** Size of the ping message */
    //public static final String CONTEXT_SIZE = "contextSize";
    public static final String SUMMARYTYPE = "summaryType";
    public static final String CONTEXTSUMMARY = "ContextSummary";
    public static final String STRAGETY = "strategy";
    public static final String DIRECTORY = "directory";

    /** Application ID */
    public static final String APP_ID = "edu.texas.mpc.ContextSharingApplication";

    //private static final String MESSAGE_FORMAT = "%d->%d/%d/%5.2f/";

    // Private vars
    //private int     contextSize = 0;
    public static String   summaryType = "";
    public static String   strategy = "";
    public static String   directory = "";

    //region CONSTRUCTORS
    /**
     * Creates a new ping application with the given settings.
     *
     * @param s	Settings to use for initializing the application.
     */
    public ContextSharingApplication(Settings s) {
        Settings s2 = new Settings(CONTEXTSUMMARY);
        summaryType = s2.getSetting(SUMMARYTYPE);
        strategy = s2.getSetting(STRAGETY);
        directory = s2.getSetting(DIRECTORY);

        // Scenario.nrofHostGroups = 2
        String NROF_GROUPS_S = "nrofHostGroups";
        Settings s3 = new Settings("Scenario");
        int nrofGroups = s3.getInt(NROF_GROUPS_S);

        String hostSizes = "";
        for (int i = 1; i <= nrofGroups; i++) {
            Settings t = new Settings("Group" + i);
            int hostSize = t.getInt("nrofHosts");
            hostSizes += String.format("%d:", hostSize);
        }
        hostSizes = hostSizes.substring(0, hostSizes.length() - 1);

        ContextSharingAppReporter.setup(this.directory + "/contexts", this.strategy, summaryType, hostSizes);
        super.setAppID(APP_ID);
    }

    /**
     * Copy-constructor
     *
     * @param a the input object
     */
    public ContextSharingApplication(ContextSharingApplication a) {
        super(a);
        //this.contextSize = a.getContextSize();
    }
    //endregion

    //region OVERRIDE METHODS
    /**
     * Handles an incoming message. If the message is a ping message replies
     * with a pong message. Generates events for ping and pong messages.
     *
     *  handle() implements the 2.2 in the description
     *  2.2 When a message (context) is received, the context database is updated, and the next set of contexts
     *      are calculated.
     *
     * @param msg	message received by the router
     * @param host	host to which the application instance is attached
     */
    @Override
    public Message handle(Message msg, DTNHost host) {
//        String type = (String)msg.getProperty("type");
//        if (type==null) return msg;
//
//        if (type == "context") { // message transferred
//            if (msg.getTo().getAddress() == host.getAddress()) {
//                System.out.printf("%5.2f: message transferred (%s) at %d\n", SimClock.getTime(), msg.getId(), host.getAddress());
//                ContextMessage contextMessage = ContextSharingAppReporter.messageToContextMessage(msg);
//                ContextSharingAppReporter.add(host.getAddress(), contextMessage);
//
//                // I'm not 100% sure, but it's OK to delete the delete message to avoid the "message drop" in the GUI
//                //msg.getFrom().deleteMessage(msg.getId(), true);
//                return null;
//            }
//        }

        return msg;
    }

    @Override
    public Application replicate() {
        return new ContextSharingApplication(this);
    }

    /**
     * This method is invoked when 
     *
     * @param host to which the application instance is attached
     */
    @Override
    public void update(DTNHost host) {
        double curTime = SimClock.getTime();
    }

    //region PROPERTIES
    //endregion
}