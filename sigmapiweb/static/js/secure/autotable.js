$(document).ready(function () {
	// Initialize all datatable class elements to data table.
	$.fn.dataTableExt.oStdClasses["sFilter"] = "dataTable-filter"
	$.fn.dataTableExt.oStdClasses["sLength"] = "dataTable-length"
	$.fn.dataTableExt.oStdClasses["sInfo"] = "dataTable-message"
	$.fn.dataTableExt.oStdClasses["sPagePrevEnabled"] = "btn btn-primary dataTable-button-left"
	$.fn.dataTableExt.oStdClasses["sPagePrevDisabled"] = "btn btn-primary disabled dataTable-button-left"
	$.fn.dataTableExt.oStdClasses["sPageNextEnabled"] = "btn btn-primary dataTable-button-right"
	$.fn.dataTableExt.oStdClasses["sPageNextDisabled"] = "btn btn-primary disabled dataTable-button-right"

	// Initialize all data table instances.

	$(".dataTable").DataTable();

	// NOTE: THIS IS A CUSTOM CLASS BECAUSE WE DO NOT WANT AUTOSORTING
	// MOST OF THE TIME
	// TAGS: dataTable DataTable bSort sorting tablesort data-table
	$(".dataTable-nosort").DataTable({
		"bSort": false // false to disable sorting
	});
});