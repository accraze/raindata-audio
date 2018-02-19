class CMoog extends Chubgraph {
  // Make a synthesizer to respond to incoming messages/parameters
  Moog moog => dac;
  0.5 => moog.gain;

  fun int strike(int note) {
      if (maybe) note + 5 => note;
      Std.mtof(note) => moog.freq;
      0.5 * note => moog.noteOn;
      return 1;
  }
}

class CFlute extends Chubgraph {
  // Make a synthesizer to respond to incoming messages/parameters
  Flute flute => dac;
  0.5 => flute.gain;

  fun int strike(int note) {
      if (maybe) note + 55 => note;
      Std.mtof(note) => flute.freq;
      0.5 * note => flute.noteOn;
      return 1;
  }
}

OscIn oin;        // make an OSC receiver
6448 => oin.port;  // set port #
oin.listenAll();  //   any message at all

OscMsg msg;   // message holder
CMoog moog;
CFlute flute;

while(true)
{
    oin => now;   // wait for any OSC
    
    while(oin.recv(msg))
    {
        msg.getInt(0) => int note;
        moog.strike(note);
        flute.strike(note);
        <<< "got message:", note, msg.address >>>;
        // sonify our success with music!!
    }
}

