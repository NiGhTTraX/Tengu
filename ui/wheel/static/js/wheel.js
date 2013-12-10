function UnknownRack(message) { this.message = message; }
UnknownRack.prototype = new Error();

function RackFullError(message) { this.message = message; }
RackFullError.prototype = new Error();

function HardpointsFull(message) { this.message = message; }
HardpointsFull.prototype = new Error();


$.widget("tengu.rack", {
		options: {
				size: undefined,
				startAngle: undefined,
				endAngle: undefined,
				className: "slots"
		},

		_create: function() {
				var o = this.options;

				this.element.addClass(o.className);

				// Create Wavy.
				var size = o.size || this.element.data("size"),
						startAngle = o.startAngle || this.element.data("startAngle"),
						endAngle = o.endAngle || this.element.data("endAngle");
				this.element.wavy();
		},

		addModule: function(module, index) {
		},

		removeModule: function(index) {
		},

		capacity: function() {
		}
});


$.widget("tengu.bar", {
		options: {
				startAngle: undefined,
				endAngle: undefined,
				size: undefined,
				className: "slots",
				overlayClass: "overlay",
				barRadius: 247,
				barWidth: 18,
				fillStyle: "#ccc",
				counter: undefined
		},

		_create: function() {
				var container, overlay, bar,
						w, h, cx, cy, barOffset, containerOffset,
						o = this.options;

				var size = o.size || this.element.data("size"),
						startAngle = o.startAngle !== undefined ? o.startAngle : this.element.data("start-angle"),
						endAngle = o.endAngle !== undefined ? o.endAngle : this.element.data("end-angle"),
						counter = o.counter !== undefined ? o.counter : endAngle < startAngle;

				container = this.element.addClass(o.className);
				overlay = $("<div></div>").addClass(o.overlayClass);
				bar = $("<div></div>");

				bar.appendTo(container);
				overlay.appendTo(container);

				containerOffset = container.position();
				w = container.parent().width();
				h = container.parent().height();
				cx = w / 2 - containerOffset.left;
				cy = h / 2 - containerOffset.top;

				bar.statsbar({
						centerX: cx,
						centerY: cy,
						radius: o.barRadius,
						width: o.barWidth,
						size: size,
						startAngle: startAngle,
						endAngle : endAngle,
						fillStyle: o.fillStyle,
						counterClockwise: counter
				});
		},

		current: function(value) {
				if (value === undefined)
					return $(".statsbar", this.element).statsbar("current");

				if (value > this._size)
					return;

				$(".statsbar", this.element).statsbar("current", value);
		}
});


$.widget("tengu.hardpoints", {
		options: {
				size: undefined
		},

		_create: function() {
				this._size = this.options.size || this.element.data("size");
				this.element.bar({ size: 8 });
		},

		current: function(value) {
				if (value === undefined)
					return $(".statsbar", this.element).statsbar("current");

				if (value > this._size)
					return;

				$(".statsbar", this.element).statsbar("current", value);
		}
});


$.widget("tengu.wheel", {
		options: {
				highs: 8,
				meds: 8,
				lows: 8,
				rigs: 3,
				subs: 5,
				missiles: 8,
				turrets: 8,
				calibration: 400,
				cpu: 100,
				pg: 100,

				slotsRadius: 230,

				fillstyleTurrets: "#d7d7d7",
				fillstyleMissiles: "#d7d7d7",
				fillstyleCalibration: "#d7d7d7",
				fillstyleCPU: "#d7d7d7",
				fillstylePG: "red",
		},

		_create: function() {
			var o = this.options;

			this.element.addClass("wheel");

			// Initialize racks.
			this._rackHigh = $(".highs", this.element).rack();
			this._rackMed = $(".meds", this.element).rack();
			this._rackLow = $(".lows", this.element).rack();
			this._rackRig = $(".rigs", this.element).rack();
			this._rackSub = $(".subs", this.element).rack();

			// Initialize bars.
			this._barCPU = $(".cpu", this.element).bar();
			this._barPG = $(".pg", this.element).bar();
			this._barCalibration = $(".calibration", this.element).bar();

			// Initialize hardpoints.
			this._hardpointsMissiles = $(".missiles", this.element).hardpoints();
			this._hardpointsTurrets = $(".turrets", this.element).hardpoints();
		},

		addModule: function(module, index) {
			var rack, weapon;

			// Figure out on what rack should the module go.
			if (module.hasClass("high"))
				rack = this._rackHigh;
			else if (module.hasClass("med"))
				rack = this._rackMid;
			else if (module.hasClass("low"))
				rack = this._rackLow;
			else if (module.hasClass("rig"))
				rack = this._rackRig;
			else if (module.hasClass("sub"))
				rack = this._rackSub;

			if (!rack)
				throw new UnknownRack("Unknown rack");

			// Is there space on that rack?
			if (rack.hasClass("full"))
				throw new RackFullError("Rack full");

			// Figure out if the module is a weapon.
			if (module.hasClass("missile"))
				weapon = this._hardpointsMissiles;
			else if (module.hasClass("turret"))
				weapon = this._hardpointsTurrets;

			// Are there any free slots of that weapon type?
			if (weapon && weapon.hasClass("full"))
				throw new HardpointsFull("No available hardpoints");

			// Add the module to the rack.
			rack.wavy("addItem", module);

			// Did we fill up the hardpoints?
			if (weapon && weapon.data("current") == weapon.data("size"))
				weapon.addClass("full");
		},

		removeModule: function(module, rack, index) {
		},

		cpu: function(value) {
		},

		pg: function(value) {
		},

		calibration: function(value) {
		}
});


$(document).ready(function() {
	// Attach handlers for items.
	$("#items-box").on("dblclick", ".item", function() {
		// Get visible fitting.
		var fitting = $(".fittingWheel:visible", "#fitting-window");

		// Add the item.
		fitting.wheel("addModule", $(this));
	});

	// Initialize any existing fitting wheels.
	$("#fitting-window .fittingWheel").each(function() {
			$(this).wheel({
			});
	});
});

