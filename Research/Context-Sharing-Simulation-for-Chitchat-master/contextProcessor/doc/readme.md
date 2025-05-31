* [2015/08/17]

### Q & A
* How do you define context in this project?
    * context is a bridge between ContextSummary (ContextSummary project, referred as CS) and a Message (ONE simulator). A CS that contains real contextual information has a link to this context. These contexts are represented as Message to be transferred between hosts. 

* How each host contains contexts?
    * Each host has a map (string, context) that has all the contexts to be shared. 
        * ??? I may need another map to separate between storage and sharing. 
        
* What is the key to the map?
    * The key is automatically generated from getId() method.
    * ??? Do I really need this map? Can't I just use the index in the database?
    