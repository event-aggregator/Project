/**
 * Chosen: Multiple Dropdown
 */
window.WDS_Chosen_Multiple_Dropdown = {};
( function( window, $, that ) {

	// Constructor.
	that.init = function() {
		that.cache();

		if ( that.meetsRequirements ) {
			that.bindEvents();
		}
	};

	// Cache all the things.
	that.cache = function() {
		that.$c = {
			window: $(window),
			theDropdown: $( '.dropdown' ),
		};
	};

	// Combine all events.
	that.bindEvents = function() {
		that.$c.window.on( 'load', that.applyChosen );
	};

	// Do we meet the requirements?
	that.meetsRequirements = function() {
		return that.$c.theDropdown.length;
	};

	// Apply the Chosen.js library to a dropdown.
	that.applyChosen = function() {
		that.$c.theDropdown.chosen({
			inherit_select_classes: true,
			width: '300px',
		});
	};

	// Engage!
	$( that.init );

})( window, jQuery, window.WDS_Chosen_Multiple_Dropdown );