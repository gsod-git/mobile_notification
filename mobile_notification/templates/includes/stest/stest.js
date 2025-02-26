
// $("#course").hide();
$(".phoenix-tile--test").hide();


$( "#program" ).change(function() {

	$("#course").html('<option disabled="disabled" selected="selected" value="">Select Course</option>');
	var program = $('#program option:selected').text()
		$("#course").show();

		$(".phoenix-tile--test").show();

		frappe.call({
				method: "frappe.client.get_list",
				args: {
					doctype: "Course",
					fields: ["course_name"],
					filters: {
						"program_name": program
					}
					
				},

				callback: function(r) {

					for (var i=0; i<r.message.length; i++) 
					{	
						$("#course").append("<option value="+r.message[i].course_name+"}>"+r.message[i].course_name+"</option>")
					}

				}
	
			});	

});



$( "#course" ).change(function() {
var program = $("#program option:selected").text();
var course = $("#course option:selected").text();

$(".examitem").hide(); 

$('[data-course='+course+']').toggle(); 


});


$( "#program" ).change(function() {
var program = $("#program option:selected").text();
var course = $("#course option:selected").text();

$(".examitem").hide(); 

$('[data-program='+program+']').toggle(); 


});
