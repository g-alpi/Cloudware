$(document).ready(function () {
    directory_redidect();
    event_click_resources();
    right_click_upload_resources();
    right_click_edit_resources();
    event_click_upload_file_icon();
    event_click_uplaod_directory_icon();


});

function directory_redidect(){
    $('[data-type="directory"] p, [data-type="directory"] i').click(function (e) { 
        e.preventDefault();
        let id = $(this).parent().attr('data-id');
        console.log(id);
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

function event_click_upload_file_icon() {
    $(".upload-file-icon").click(function(){
        cerate_file();
    });
}
function event_click_uplaod_directory_icon() {
    $(".upload-directory-icon").click(function(){
        create_directory();
    });
}


function event_click_resources() {
    $( ".resources" ).click(function() {
        $('.resources').removeClass('active');
        $( this ).toggleClass("active");

    });
}
function edit_source_name(source_pk,source_name,source_type) {

    let container = $('[data-id="'+source_pk+'"][data-type="'+source_type+'"]');
    console.log(container);
    container.children().last().remove();
    container.append('<input type="text" id="new_source_name" value="'+source_name+'" class="m-2" >');
    detect_enter_key_update_source('new_source_name',source_pk,source_type);

}

function detect_enter_key_update_source(input,source_pk,source_type) {
    $('#'+input).keypress(function (e) { 
        var keycode = (e.keyCode ? e.keyCode : e.which);
        if(keycode == '13'){
            $.ajax({
                url: "http://"+window.location.host+"/edit_"+source_type,
                type: "POST",
                data: {
                    id: source_pk,
                    name: $('#'+input).val(),
                },
                success: function(response){
                    console.log(response);
                    window.location.reload();
                }
            });
        }
    });
};



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
    let source_pk;
    let source_name;
    let source_type;
    $(".resources" ).bind("contextmenu", function (event) {
        
        // Avoid the real one
        event.preventDefault();
        event.stopPropagation();

        source_pk= $(this).attr("data-id");
        source_name = $(this).attr("data-name");
        source_type = $(this).attr("data-type");

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
            case "second": edit_source_name(source_pk,source_name,source_type); break;
        }

        // Hide it AFTER the action was triggered
        $(".file-menu").hide(100);
    });
}   