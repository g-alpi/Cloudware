$(document).ready(function () {
    directory_redidect();
    event_click_resources();
    right_click_upload_resources();
    right_click_edit_resources();
    
    


});

function directory_redidect(){
    $('.parent').click(function (e) { 
        e.preventDefault();
        let id = $(this).next().val();
        $.ajax({
            type: "GET",
            url: "http://"+window.location.host+"/directory/"+id,
            success: function (response) {
                window.location.href = "http://"+window.location.host+"/directory/"+id;
            }
        });
    });

}

function create_directory() {

    form_directory_toogle();
    click_outside_directory_form();
    
    $('.btn').click(function (e) { 
        create_directory_call();
    });

}
function create_directory_call(){
    let name = $('#new_file').val();
    let parent_id = $('#actual_directory').val();
    $.ajax({
        url: "http://"+window.location.host+"/create_directory",
        type: "POST",
        data: {
            name: name,
            parent_id: parent_id,
        },
        success: function(response){
            window.location.reload();
        }
    });
}


function cerate_file() {
    form_file_toogle();
    click_outside_file_form();
}

function form_directory_toogle() {
    $('.form-directory-container').toggle();
    $('.dark-background').toggle();
}
function form_file_toogle() {
    $('.form-file-container').toggle();
    $('.dark-background').toggle();
}
function click_outside_directory_form() {
    $('.dark-background').click(function (e) {
        $('.form-directory-container').hide();
        $('.dark-background').hide();
    });
}
function click_outside_file_form() {
    $('.dark-background').click(function (e) {
        $('.form-file-container').hide();
        $('.dark-background').hide();
    });
}


function event_click_resources() {
    $( ".resources" ).click(function() {
        $('.resources').removeClass('active');
        $( this ).toggleClass("active");

    });
}



function right_click_upload_resources() {
    $(".box-shadow" ).bind("contextmenu", function (event) {
    
        // Avoid the real one
        event.preventDefault();
        
        // Show contextmenu
        $(".upload-menu").finish().toggle(100).
        
        // In the right position (the mouse)
        css({
            top: event.pageY + "px",
            left: event.pageX + "px"
        });
    });

    // If the document is clicked somewhere
    $(document ).bind("mousedown", function (e) {
        
        // If the clicked element is not the menu
        if (!$(e.target).parents(".upload-menu").length > 0) {
            
            // Hide it
            $(".upload-menu").hide(100);
        }
    });


    // If the menu element is clicked
    $(".upload-menu li").click(function(){
        
        // This is the triggered action name
        switch($(this).attr("data-action")) {
            
            // A case for each action. Your actions here
            case "first": cerate_file(); break;
            case "second": create_directory(); break;
        }
    
        // Hide it AFTER the action was triggered
        $(".upload-menu").hide(100);
    });

}

function right_click_edit_resources() {
    $(".resources" ).bind("contextmenu", function (event) {
        
        // Avoid the real one
        event.preventDefault();
        event.stopPropagation();
        
        // Show contextmenu
        $(".file-menu").finish().toggle(100).
        
        // In the right position (the mouse)
        css({
            top: event.pageY + "px",
            left: event.pageX + "px"
        });
    });

    // If the document is clicked somewhere
    $(document).bind("mousedown", function (e) {
        
        // If the clicked element is not the menu
        if (!$(e.target).parents(".file-menu").length > 0) {
            
            // Hide it
            $(".file-menu").hide(100);
        }
    });
    // If the menu element is clicked
    $(".file-menu li").click(function(){
        
        // This is the triggered action name
        switch($(this).attr("data-action")) {
            
            // A case for each action. Your actions here
            case "first": alert("first"); break;
            case "second": alert("second"); break;
        }

        // Hide it AFTER the action was triggered
        $(".file-menu").hide(100);
    });
}
    