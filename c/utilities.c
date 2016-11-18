double coerce(double val, double min, double max) {
	return val > max ? max : (val < min ? min : val);
}
