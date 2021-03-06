//
// Lightpad - MidiLayer.h
// ©2018 Gooborg Studios: Vinyl Darkscratch, Light Apacha.
// Additional support from LaunchpadFun (http://www.launchpadfun.com/en/).
// http://www.gooborg.com/lightpad
//

#pragma once

#include <wx/wxprec.h>
#ifndef WX_PRECOMP
	#include <wx/wx.h>
#endif

#include <string>

#include "GooCore/Colors.h"
#include "HOWL/Layer.h"

class NoteKeyframe: public HOWL::Keyframe {
	public:
		unsigned char velocity;
		NoteKeyframe(int name, long time, unsigned char velocity);
		std::string serialize();
		void render(wxDC &canvas, wxRect bounding_box);
};

class MidiLayer: public HOWL::Layer {
	public:
		unsigned char getVelocity(int position);
		unsigned char getVelocity(std::string position);
		void setVelocity(int position, unsigned char velocity);
};

const int COLORCOUNT = 128;
extern Color velocitycolors[COLORCOUNT];

unsigned char get_closest_velocity(Color c);
char get_color_velocity(Color c);
