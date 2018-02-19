class CMoog extends Chubgraph {
  // Make a synthesizer to respond to incoming messages/parameters
  Moog moog => dac;
  0.90 => moog.gain;

  fun int strike(int note) {
      Std.mtof(note) => moog.freq;
      0.7 * note => moog.noteOn;
      return 1;
  }
}

class CMando extends Chubgraph {
  // Make a synthesizer to respond to incoming messages/parameters
  Mandolin m => JCRev r => dac;
  .75 => r.gain;
  .015 => r.mix;

  fun int strike(int note) {
      note + 24 => note;
      Std.mtof(note) => m.freq;
      0.7 => m.pluck;
      return 1;
  }
  fun void off(){
      m.noteOff;
  }
}

class CBWG extends Chubgraph {
  // Make a synthesizer to respond to incoming messages/parameters
  BandedWG band => dac;
  1.09 => band.gain;

  ["Uniform Bar","Tuned Bar",
  "Glass Harmonica","Tibetan Bowl"] @=> string presets[];


  fun int strike(int note) {
      Math.random2(0,3) => int preset;
      preset => band.preset;
      Math.random2f(100,1500) => float freq;
      freq => band.freq;
      0.9 => band.noteOn;
      second => now;
      return 1;
  }
}

class CBar extends Chubgraph {
  // Make a synthesizer to respond to incoming messages/parameters
  ModalBar bar => JCRev r => dac;
  // set the gain
  .80 => r.gain;
  // set the reverb mix
  .025 => r.mix;

  fun int strike(int note) {
      Std.mtof(note) => bar.freq;
      // go
      0.8  => bar.noteOn;
  }
}

class CStar extends Chubgraph {
  // Make a synthesizer to respond to incoming messages/parameters
  Sitar sit => PRCRev r => dac;
  .05 => r.mix;

  fun int strike(int note) {
    Math.random2( 0, note) => float winner;
    Std.mtof( 57 + Math.random2(0,3) * 12 + winner ) => sit.freq;

    // pluck!
    Math.random2f( 0.4, 0.9 ) => sit.noteOn;

    // advance time
    // note: Math.randomf() returns value between 0 and 1
    if( Math.randomf() > .5 ) {
        .5::second => now;
    } else { 
        0.25::second => now;
    }
  }
}

OscIn oin;        // make an OSC receiver
6448 => oin.port;  // set port #
oin.listenAll();  //   any message at all

OscMsg msg;   // message holder
CMoog moog;   // moog used for 12 tone melody
CMando m;     // sinister mandolin used to double the melody
CBar bar;     // modal rim shot to signify the end of a day.
CBWG bwg;     // banded waveguide used for "sunny" non-rainy days.
CStar str;    // sitar pluck to also signify the end of a day.

fun void doMoog(int note) {
  moog.strike(note);
}

fun void doMando(int note) {
  m.strike(note);
}

fun void doEOD(int note) {
  bar.strike(note);
  if (maybe) {
      str.strike(note);
  }
  <<< "EOD:", note, "EOD !!!!!!">>>;
}

fun void doZero(int note) {
  bwg.strike(note);
  <<< "ZERO:", note, "ZERO !!!!!!">>>;

}

while(true)
{
    oin => now;   // wait for any OSC
    
    while(oin.recv(msg))
    {
        msg.getInt(0) => int note;
        if (note == 0) {
            spork ~ doZero(note);
        } else {
            if (note == 24) {
                spork ~ doEOD(note);
            } else {
                spork ~ doMoog(note);
                spork ~ doMando(note);            
            }
        }
        <<< "got message:", note, msg.address >>>;
        // sonify our success with music!!
    }
}