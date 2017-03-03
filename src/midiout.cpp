//
// Lightpad - midiout.cpp
// ©2017 Nightwave Studios: Vinyl Darkscratch, Light Apacha, Eric Busch (Origami1105), WhoovesPON3.
// Additional support from LaunchpadFun (http://www.launchpadfun.com/en/).
// https://www.nightwave.co/lightpad
//

#include <iostream>
#include <iomanip>
#include <cstdlib>
#include <cstdarg>
#include <csignal>
#include <ctime>
#include <unistd.h>

#include <wx/wxprec.h>
#ifndef WX_PRECOMP
	#include <wx/wx.h>
#endif

#include "RtMidi.h"
#include "MidiFile.h"

#include "Helpers.h"

int BPM = 120;

bool done;
static void finish(int ignore){ done = true; std::cout << std::endl; }

int main() {
	MidiFile midifile;
	MidiEvent* mev;
	std::vector<unsigned char> message_in;
	int nBytes, color, deltatick;
	double stamp;
	LaunchpadPro *lp = new LaunchpadPro();
	int lp_status = lp->connect();
	if (lp_status < 0) {
		std::cout << "Launchpad not found!  Is it plugged in and turned on?\n";
		return 1;
	}

	srand(time(NULL));

	// Pulse side LED
	lp->setPulse(LAUNCHPAD_PRO_SIDE_LED_ID, 53);

	midifile.read("../references/Light_Output_Test.mid");
	midifile.joinTracks();

	std::cout << "Playing MIDI File..." << std::endl;
	
	for (int event=0; event < midifile[0].size(); event++) {
		mev = &midifile[0][event];
		if (event == 0) {
			deltatick = mev->tick;
		} else {
			deltatick = mev->tick - midifile[0][event-1].tick;
		}
		if ((int)(*mev)[0] == 128 || (int)(*mev)[0] == 144) {
			color = (int)(*mev)[2];
			if ((int)(*mev)[0] == 128) color = 0;
			if (deltatick > 0) {
				usleep(60000 * 1000 / (BPM * deltatick));
			}

			lp->setColor(note_to_button((int)(*mev)[1]), color);

		}
	}

	std::cout << "Completed MIDI file playback!" << std::endl << std::endl;

	// Install an interrupt handler function.
	done = false;
	(void) signal(SIGINT, finish);
	// Periodically check input queue.
	std::cout << "Reading MIDI from port ... quit with Ctrl-C." << std::endl;
	while (!done) {
		stamp = lp->getMessage(&message_in);
		nBytes = message_in.size();
		if (nBytes > 0) {
			if ((message_in[0] == 144) || (message_in[0] == 176)) {
				color = rand() % 126 + 1;
				if (message_in[2] > 0) {
					lp->setColor(message_in[1], color);
				} else {
					lp->setPulse(message_in[1], color);
				}
			}
		}

		if ( nBytes > 0 ) {
			std::cout << std::fixed << std::setprecision(7) << stamp << " |   ";
			for ( int i=0; i<nBytes; i++ )
				std::cout << std::setw(4) << (int)message_in[i];
			std::cout << std::endl;
		}
		
		usleep( 10000 ); // Sleep for 10 milliseconds ... platform-dependent.
	}

	// delete midiin;
	// delete midiout;
	lp->disconnect();
	return 0;
}