//
// Lightpad - Layer.cpp
// ©2017 Nightwave Studios: Vinyl Darkscratch, Light Apacha, Origami1105, WhoovesPON3.
// Additional support from LaunchpadFun (http://www.launchpadfun.com/en/).
// https://www.nightwave.co/lightpad
//

#include "Layer.h"

#include <sys/time.h>
#include <string>
#include <sstream>
#include <iostream>
#include <iomanip>
#include <algorithm>
#include <vector>
#include <map>
#include <cmath>

#include <wx/wxprec.h>
#ifndef WX_PRECOMP
	#include <wx/wx.h>
#endif

#include <wx/dcbuffer.h>

#include "Helpers.h"

Keyframe::Keyframe() {

}

Keyframe::Keyframe(std::string name, double time) {
	this->name = name;
	this->time = time;
	this->smoother = SMOOTH_LINEAR;
}

std::string Keyframe::serialize() {
	return "";
}

void Keyframe::toBuffer(char *outbuf, int len) {
//	snprintf(outbuf, len, "keyframe %s %f %s %s %d\n", this->parent->description.c_str(), this->time, this->name.c_str(), this->serialize().c_str(), this->smoother);
}

DoubleKeyframe::DoubleKeyframe(std::string name, double time, double value) : Keyframe(name, time) {
	this->value = value;
};

DoubleKeyframe::DoubleKeyframe(std::string name, double time, float value) : Keyframe(name, time) {
	this->value = (double)value;
};

DoubleKeyframe::DoubleKeyframe(std::string name, double time, int value) : Keyframe(name, time) {
	this->value = (double)value;
};

std::string DoubleKeyframe::serialize() {
	std::stringstream stream;
	stream << value;
	return stream.str();
}

StringKeyframe::StringKeyframe(std::string name, double time, std::string *value) : Keyframe(name, time) {
	this->value = value;
	this->smoother = SMOOTH_HOLD;
};

StringKeyframe::StringKeyframe(std::string name, double time, const char *value) : Keyframe(name, time) {
	this->value = new std::string(value);
	this->smoother = SMOOTH_HOLD;
};

std::string StringKeyframe::serialize() {
	return *value;
}

//KeyframeSet::KeyframeSet() {
//	this->parent = NULL;
//}

KeyframeSet::KeyframeSet(Layer *parent) {
	this->parent = parent;
//	seek();
}

void KeyframeSet::AddKeyframe(Keyframe *f) {
	KeyframeIterator it = keyframes.begin();
	
	for (; it != keyframes.end(); ++it) {
		if ( f->time < (*it)->time ) {
			keyframes.insert(it, f);
			break;
		}
	}
	
	if (it == keyframes.end()) {
		keyframes.push_back(f);
	}
}

void KeyframeSet::seek() {
	prevKF = keyframes.begin();
	if (prevKF != keyframes.end()) {
		nextKF = std::next(prevKF, 1);
	} else {
		nextKF = keyframes.end();
	}
	advanceFrame();
}

void KeyframeSet::advanceFrame() {
	while (nextKF != keyframes.end() && parent->currentTime >= (*nextKF)->time) {
		++prevKF;
		++nextKF;
	}
}

double KeyframeSet::smoother_fraction() {
	// XXX Only does Linear smoothing, add other smoother types
	if (nextKF == keyframes.end()) return 0.0;
	
	assert(parent->currentTime >= (*prevKF)->time);
	assert((*nextKF)->time >= parent->currentTime);
	
	double dur = ((*nextKF)->time - (*prevKF)->time);
	if (dur == 0.0) return 0.0; // Avoid divide-by-zero crash
	return (parent->currentTime - (*prevKF)->time) / dur;
}

Keyframe *KeyframeSet::getFirst() {
	if (prevKF == keyframes.end()) return NULL;
	return *prevKF;
}

Keyframe *KeyframeSet::getSecond() {
	if (nextKF == keyframes.end()) return NULL;
	return *nextKF;
}

Layer::Layer() {
	description = "";
};

Layer::Layer(std::string d) {
	description = d;
}

void Layer::AddKeyframe(Keyframe *f) {
	std::string type = f->name;
	if (keyframes.find(type) == keyframes.end()) {
		keyframes[type] = new KeyframeSet(this);
	}
	keyframes[type]->AddKeyframe(f);
}

void Layer::seek(double newTime) {
	currentTime = newTime;
	for (auto it = keyframes.begin(); it != keyframes.end(); ++it) {
		it->second->seek();
	}
	
}

void Layer::advanceFrame(double increment) {
	currentTime += increment;
	for (auto it = keyframes.begin(); it != keyframes.end(); ++it) {
		it->second->advanceFrame();
	}
}

double Layer::getDouble(std::string type) {
	KeyframeSet *set = keyframes[type];
	DoubleKeyframe *KF1 = (DoubleKeyframe *)(set->getFirst());
	DoubleKeyframe *KF2 = (DoubleKeyframe *)(set->getSecond());
	
	if (KF1 == NULL) return 0.0;
	if (KF2 == NULL) return KF1->value;
	double pos = set->smoother_fraction();
	return KF1->value - (KF1->value * pos) + (KF2->value * pos); // XXX Simplify me (to get a good grade)!
}

std::string *Layer::getString(std::string type) {
	if (keyframes[type]->getFirst() == NULL) return new std::string("");
	return ((StringKeyframe *)(keyframes[type]->getFirst()))->value;
}