# RGB<>HSL color conversion
def RGB2HSL(red, green, blue):
	max_val = max(red, green, blue)
	min_val = min(red, green, blue)
	luminosity = (max_val + min_val) / 2.0

	if max_val == min_val:
		hue = 0
		saturation = 0
	else:
		diff = max_val - min_val
		if luminosity > 127: saturation = diff * 255 / (510 - max_val - min_val)
		else: saturation = diff * 255 / (max_val + min_val)
		if max_val == red:
			hue = (green - blue) * 60 / diff
			if green < blue: hue += 6
		elif max_val == green: hue = (blue - red) * 60 / diff + 120
		elif max_val == blue: hue = (red - green) * 60 / diff + 240
	return [hue, saturation, luminosity]
	
def Hue2RGB(cc_p, cc_q, cc_t):
	if (cc_t < 0.0): cc_t += 1
	if (cc_t > 1.0): cc_t -= 1
	if (cc_t < 1 / 6.0): return cc_p + (cc_q - cc_p) * 6.0 * cc_t
	if (cc_t < 1 / 2.0): return cc_q
	if (cc_t < 2 / 3.0): return cc_p + (cc_q - cc_p) * (2 / 3.0 - cc_t) * 6.0
	return cc_p

def HSL2RGB(hue, saturation, luminosity):
	hue = hue / 360.0
	if (saturation == 0.0): red = green = blue = luminosity * 255
	else:
		if luminosity < 127: cc_q = luminosity * (1 + saturation) / 255
		else: cc_q = luminosity + (saturation / 255) - luminosity * (saturation / 255)
		cc_p = 2.0 * luminosity / 255 - cc_q
		red = round(max(0, Hue2RGB(cc_p, cc_q, hue + 1 / 3.0) * 255))
		green = round(max(0, Hue2RGB(cc_p, cc_q, hue) * 255))
		blue = round(max(0, Hue2RGB(cc_p, cc_q, hue - 1 / 3.0) * 255))
	return [int(red), int(green), int(blue)]

# RGB<>HSV color conversion
def RGB2HSV(red, green, blue):
	max_val = max(red, green, blue)
	min_val = min(red, green, blue)
	diff = max_val - min_val
	velocity = max_val
	if max_val == 0.0: saturation = 0.0
	else: saturation = diff / max_val

	if max_val == min_val: hue = 0.0
	else:
		if max_val == red:
			hue = (green - blue) / diff
			if green < blue: hue += 6.0
		elif max_val == green: hue = (blue - red) / diff + 2.0
		elif max_val == blue: hue = (red - green) / diff + 4.0
		hue = hue / 6.0

def HSV2RGB(hue, saturation, velocity):
	cc_i = hue * 6.0
	cc_is = (cc_i - floor(cc_i)) * saturation
	red = green = blue = velocity

	i = int(floor(cc_i)) % 6
	if i == 0:
		green = velocity * cc_is
		blue = velocity * (1.0 - saturation)
	elif i == 1:
		red = velocity * (1.0 - cc_is)
		blue = velocity * (1.0 - saturation)
	elif i == 2:
		red = velocity * (1.0 - saturation)
		blue = velocity * cc_is
	elif i == 3:
		red = velocity * (1.0 - saturation)
		green = velocity * (1.0 - cc_is)
	elif i == 4:
		red = velocity * cc_is
		green = velocity * (1.0 - saturation)
	elif i == 5:
		green = velocity * (1.0 - saturation)
		blue = velocity * (1.0 - cc_is)

# # RGB<>CMYK color conversion
# void ColorConverter::RGB2CMYK(double red, double green, double blue, double *cyan, double *magenta, double *yellow, double *black) {
# 	*black = 1.0 - threeway_max(red, green, blue);
# 	*cyan = (1.0 - red - *black) / (1.0 - *black);
# 	*magenta = (1.0 - green - *black) / (1.0 - *black);
# 	*yellow = (1.0 - blue - *black) / (1.0 - *black);
# }

# void ColorConverter::CMYK2RGB(double cyan, double magenta, double yellow, double black, double *red, double *green, double *blue) {
# 	*red = (1.0 - cyan) / (1.0 - black);
# 	*green = (1.0 - magenta) / (1.0 - black);
# 	*blue = (1.0 - yellow) / (1.0 - black);
# }

# # RGB<>YIQ color conversion
# void ColorConverter::RGB2YIQ(double red, double green, double blue, double *yluma, double *inphase, double *quadrature) {
# 	*yluma = 0.299 * red + 0.587 * green + 0.114 * blue;
# 	*inphase = 0.569 * red - 0.275 * green - 0.322 * blue;
# 	*quadrature = 0.211 * red - 0.523 * green + 0.312 * blue;
# }

# void ColorConverter::YIQ2RGB(double yluma, double inphase, double quadrature, double *red, double *green, double *blue) {
# 	*red = yluma + 0.956 * inphase + 0.621 * quadrature;
# 	*green = yluma - 0.272 * inphase - 0.647 * quadrature;
# 	*blue = yluma - 1.106 * inphase + 1.703 * quadrature;
# }

# double ColorConverter::XYZ2H(double cc_q) {
# 	if (cc_q > 0.008856) return pow(cc_q, 0.333333);
# 	return 7.787 * cc_q + 0.137931;
# }

# # RGB<>XYZ color conversion
# void ColorConverter::RGB2XYZ(int red, int green, int blue, double *xresponse, double *yluminance, double *zblue) {
# 	double adapt = 0.003922;
# 	*xresponse = (0.412424 * red + 0.357579 * green + 0.180464 * blue) * adapt;
# 	*yluminance = (0.212656 * red + 0.715158 * green + 0.072186 * blue) * adapt;
# 	*zblue = (0.019332 * red + 0.119193 * green + 0.950444 * blue) * adapt;
# }

# void ColorConverter::XYZ2RGB(double xresponse, double yluminance, double zblue, int *red, int *green, int *blue) {
# 	*red = xresponse * 3.080342  - yluminance * 1.537399 - zblue * 0.542943;
# 	*green = xresponse * -0.921178 + yluminance * 1.87593  + zblue * 0.045248;
# 	*blue = xresponse * 0.052881  - yluminance * 0.204011 + zblue * 1.15113;
# }

# # XYZ<>LAB color conversion
# void ColorConverter::XYZ2LAB(double xresponse, double yluminance, double zblue, double *luminosity, double *apoint, double *bpoint) {
# 	*luminosity = 116 * ColorConverter::XYZ2H(yluminance) - 16;
# 	*apoint = 500 * (ColorConverter::XYZ2H(xresponse / 0.950467) - ColorConverter::XYZ2H(yluminance));
# 	*bpoint = 200 * (ColorConverter::XYZ2H(yluminance) - ColorConverter::XYZ2H(zblue / 1.088969));
# }

# void ColorConverter::LAB2XYZ(double luminosity, double apoint, double bpoint, double *xresponse, double *yluminance, double *zblue) {
# 	double XRESPONSE, YLUMINANCE, ZBLUE;
# 	YLUMINANCE = luminosity * (0.00862) + 0.137931;
# 	XRESPONSE = apoint * (0.002) + YLUMINANCE;
# 	ZBLUE = bpoint * (-0.005) + YLUMINANCE;

# 	*xresponse = XRESPONSE > 0.206897 ? pow(XRESPONSE, 3) : XRESPONSE * (0.128419) - 0.017713;
# 	*yluminance = luminosity > 8 ? pow(YLUMINANCE, 3) : luminosity * (0.00110705646);
# 	*zblue = ZBLUE > 0.206897 ? pow(ZBLUE, 3) : ZBLUE * (0.128419) - 0.017713;
# }

# # RGB<>XYZ<>LAB color conversion
# void ColorConverter::RGB2LAB(int red, int green, int blue, double *luminosity, double *apoint, double *bpoint) {
# 	double xresponse, yluma, zblue;
# 	RGB2XYZ(red, green, blue, &xresponse, &yluma, &zblue);
# 	XYZ2LAB(xresponse, yluma, zblue, luminosity, apoint, bpoint);
# }

# void ColorConverter::LAB2RGB(double luminosity, double apoint, double bpoint, int *red, int *green, int *blue) {
# 	double xresponse, yluma, zblue;
# 	LAB2XYZ(luminosity, apoint, bpoint, &xresponse, &yluma, &zblue);
# 	XYZ2RGB(xresponse, yluma, zblue, red, green, blue);
# }

# # HSL<>RGB<>HSV color conversion
# void ColorConverter::HSL2HSV(double hue, double saturation, double luminosity, double *_hue, double *_saturation, double *velocity) {
# 	double red, green, blue;
# 	HSL2RGB(hue, saturation, luminosity, &red, &green, &blue);
# 	RGB2HSV(red, green, blue, _hue, _saturation, velocity);
# }

# void ColorConverter::HSV2HSL(double hue, double saturation, double velocity, double *_hue, double *_saturation, double *luminosity) {
# 	double red, green, blue;
# 	HSV2RGB(hue, saturation, velocity, &red, &green, &blue);
# 	RGB2HSL(red, green, blue, _hue, _saturation, luminosity);
# }

# # HSL<>RGB<>CMYK color conversion
# void ColorConverter::HSL2CMYK(double hue, double saturation, double luminosity, double *cyan, double *magenta, double *yellow, double *black) {
# 	double red, green, blue;
# 	HSL2RGB(hue, saturation, luminosity, &red, &green, &blue);
# 	RGB2CMYK(red, green, blue, cyan, magenta, yellow, black);
# }

# void ColorConverter::CMYK2HSL(double cyan, double magenta, double yellow, double black, double *hue, double *saturation, double *luminosity) {
# 	double red, green, blue;
# 	CMYK2RGB(cyan, magenta, yellow, black, &red, &green, &blue);
# 	RGB2HSL(red, green, blue, hue, saturation, luminosity);
# }

# # HSV<>RGB<>CMYK color conversion
# void ColorConverter::HSV2CMYK(double hue, double saturation, double velocity, double *cyan, double *magenta, double *yellow, double *black) {
# 	double red, green, blue;
# 	HSV2RGB(hue, saturation, velocity, &red, &green, &blue);
# 	RGB2CMYK(red, green, blue, cyan, magenta, yellow, black);
# }

# void ColorConverter::CMYK2HSV(double cyan, double magenta, double yellow, double black, double *hue, double *saturation, double *velocity) {
# 	double red, green, blue;
# 	CMYK2RGB(cyan, magenta, yellow, black, &red, &green, &blue);
# 	RGB2HSV(red, green, blue, hue, saturation, velocity);
# }

# # HSL<>RGB<>YIQ color conversion
# void ColorConverter::HSL2YIQ(double hue, double saturation, double luminosity, double *yluma, double *inphase, double *quadrature) {
# 	double red, green, blue;
# 	HSL2RGB(hue, saturation, luminosity, &red, &green, &blue);
# 	RGB2YIQ(red, green, blue, yluma, inphase, quadrature);
# }

# void ColorConverter::YIQ2HSL(double yluma, double inphase, double quadrature, double *hue, double *saturation, double *luminosity) {
# 	double red, green, blue;
# 	YIQ2RGB(yluma, inphase, quadrature, &red, &green, &blue);
# 	RGB2HSL(red, green, blue, hue, saturation, luminosity);
# }

# # HSV<>RGB<>YIQ color conversion
# void ColorConverter::HSV2YIQ(double hue, double saturation, double velocity, double *yluma, double *inphase, double *quadrature) {
# 	double red, green, blue;
# 	HSV2RGB(hue, saturation, velocity, &red, &green, &blue);
# 	RGB2YIQ(red, green, blue, yluma, inphase, quadrature);
# }

# void ColorConverter::YIQ2HSV(double yluma, double inphase, double quadrature, double *hue, double *saturation, double *velocity) {
# 	double red, green, blue;
# 	YIQ2RGB(yluma, inphase, quadrature, &red, &green, &blue);
# 	RGB2HSV(red, green, blue, hue, saturation, velocity);
# }

# # CMYK<>RGB<>YIQ color conversion
# void ColorConverter::CMYK2YIQ(double cyan, double magenta, double yellow, double black, double *yluma, double *inphase, double *quadrature) {
# 	double red, green, blue;
# 	CMYK2RGB(cyan, magenta, yellow, black, &red, &green, &blue);
# 	RGB2YIQ(red, green, blue, yluma, inphase, quadrature);
# }

# void ColorConverter::YIQ2CMYK(double yluma, double inphase, double quadrature, double *cyan, double *magenta, double *yellow, double *black) {
# 	double red, green, blue;
# 	YIQ2RGB(yluma, inphase, quadrature, &red, &green, &blue);
# 	RGB2CMYK(red, green, blue, cyan, magenta, yellow, black);
# }