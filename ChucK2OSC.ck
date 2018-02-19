//  Listen for all incoming messages on port

OscIn oin;        // make an OSC receiver
6449 => oin.port;  // set port #
oin.listenAll();  //   any message at all

OscOut xmit;    // Make a new OSC sender object
6448 => int port;
xmit.dest ( "localhost", port ); // open on local host

OscMsg msg;   // message holder

fun void pass_msg(int note) {
    xmit.start( "/realDSPOSCSender/OSCNote" );
    note => xmit.add;           // add integer note# to message
    //velocity => xmit.add;    // add float velocity to message
    //message => xmit.add;    // add string to message
    xmit.send();             // Ship it!!
}

while(true)
{
    oin => now;   // wait for any OSC
    
    while(oin.recv(msg))
    {
        msg.getInt(0) => int note;
        pass_msg(note);
        <<< "got message:", note, msg.address >>>;
        // sonify our success with music!!
    }
}

