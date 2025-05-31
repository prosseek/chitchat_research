# ContextSharingSimulation
Context Sharing Simulation on ONE Simulator, the results are used in the paper [CHITCHAT: Navigating Tradeoffs in Device-to-Device Context Sharing](https://www.researchgate.net/publication/287249098_CHITCHAT_Navigating_Tradeoffs_in_Device-to-Device_Context_Sharing)

## Simulation setup
* [2015/08/19] `ln -s ../experiment/ ./experiment` should be executed in the ONE simulator directory.
    * Database loads the contexts assuming the base directory is in ContextSharingSimulation directory, but with one simulator this becomes one_simulator.
    * This symbolic link solves this issue. 
* [2015/08/19] Contexts in `experiment/contexts/SimulationSimple/contexts` are loaded when the simulation starts. Refer to Database object in ContextProcessor package.

## Changes

Try to change as little as possible in the `one_simulator`.

### [2015/08/10] Project structure change

All the one simulator code is in one_simulator directory, all the settings should be in the one_simulator directory

The working direcgtory becomes PATH/one_simulator

### [2015/08/10] Applications are listeners.

core/SimScenario.java/createHosts() method: for each application, add them into listener list based on what types it implements.

    protoApp = (Application)t.createIntializedObject(
            APP_PACKAGE + t.getSetting(APPTYPE_S));
    // smcho added
    // If the application implements connectionListner, it should be added to the lister group
    if (protoApp instanceof ConnectionListener) {
        addConnectionListener((ConnectionListener) protoApp);
    }
    if (protoApp instanceof MessageListener) {
        addMessageListener((MessageListener) protoApp);
    }
    if (protoApp instanceof MovementListener) {
        addMovementListener((MovementListener) protoApp);
    }
    if (protoApp instanceof UpdateListener) {
        addUpdateListener((UpdateListener) protoApp);
    }
    if (protoApp instanceof ApplicationListener) {
        addApplicationListener((ApplicationListener) protoApp);
    }
    // smcho added end

## Message id as the names of context
[2015/08/24]

This is an example of message.

    0-Set(is0, is3(3->0[52]), is2(2->0[48]))
    1-Set(is1, is3(3->1[52]))
    2-Set(is2, is0(0->2[39]), is4(4->2[58]))
    3-Set(is3, is0(0->3[39]), is1(1->3[28]))
    4-Set(is4, is2(2->4[48]))
    
The format is `is\d+(\d+->\d+[\d+])?`. 

* `is\d+` shows the originator of the context.
* `\d+->\d+` shows the sender and receiver of the context.
* `[\d+]` shows the size of context.

We may be able to add more information (i.e., the type of context) to be further analyzed. 
