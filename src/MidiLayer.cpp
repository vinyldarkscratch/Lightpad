//
// Lightpad - MidiLayer.cpp
// ©2017 Nightwave Studios: Vinyl Darkscratch, Light Apacha, Origami1105, WhoovesPON3.
// Additional support from LaunchpadFun (http://www.launchpadfun.com/en/).
// https://www.nightwave.co/lightpad
//

#include "MidiLayer.h"

#include <wx/wxprec.h>
#ifndef WX_PRECOMP
	#include <wx/wx.h>
#endif

#include <string>

#include "Layer.h"

NoteKeyframe::NoteKeyframe(int name, double time, unsigned char velocity) : Keyframe(std::to_string(name), time) {
	this->velocity = velocity;
}

std::string NoteKeyframe::serialize() {
	return std::string("");
}

unsigned char MidiLayer::getVelocity(int position) {
	std::string type = std::to_string(position);
	if (keyframes[type]->getFirst() == NULL) return NULL;
	return ((NoteKeyframe *)(keyframes[type]->getFirst()))->velocity;
}

void MidiLayer::setVelocity(int position, unsigned char velocity) {
	std::string type = std::to_string(position);
	NoteKeyframe *kf = (NoteKeyframe *)(keyframes[type]->getFirst());
	if (kf == NULL) {
		AddKeyframe(new NoteKeyframe(position, currentTime, velocity));
	} else {
		kf->velocity = velocity;
	}
}