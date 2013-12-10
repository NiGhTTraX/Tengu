

$.widget("tengu.statsbar", {
		options: {
				size: 8,
				width: 25,
				radius: 250,
				startAngle: 0,
				endAngle: 360,
				centerX: 256,
				centerY: 256,
				fillStyle: "red",
				counterClockwise: false,
		},

		_create: function() {
				this.element.addClass("statsbar");

				// The canvas element needs explicit width and height attributes.
				this._canvas = $("<canvas></canvas>").attr({
						width: this.element.width(),
						height: this.element.height()
				});
				this._canvas.appendTo(this.element);
				this._ctx = this._canvas[0].getContext("2d");
				this._ctx.strokeStyle = this.options.fillStyle;

				this._current = 0;
		},

		_destroy: function() {
				this._canvas.remove();
				this.element.removeClass("statsbar");
		},

		_setOption: function(key, value) {
				// Update the value and redraw the bar.
				this._super(key, value);
				this.current(this._current);
		},

		_drawBar: function(percent) {
				var o = this.options,
						cx = o.centerX,
						cy = o.centerY,
						w = o.width,
						r = o.radius,
						startAngle = o.startAngle * Math.PI / 180,
						endAngle = o.endAngle * Math.PI / 180;

				this._ctx.clearRect(0, 0, this._canvas[0].width, this._canvas[0].height);
				this._ctx.beginPath();
				this._ctx.arc(cx, cy, r - w / 4,
											startAngle,
											startAngle + (endAngle - startAngle) * percent,
											o.counterClockwise);
				this._ctx.lineWidth = w / 2;
				this._ctx.stroke();
		},

		current: function(value) {
				if (value === undefined)
					return this._current;

				if (value > this.options.size)
					return;

				// Redraw the bar.
				this._drawBar(value / this.options.size );

				this._current = value;
		}
});

