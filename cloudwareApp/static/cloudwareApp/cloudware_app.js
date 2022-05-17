$(document).ready(function () {
    directory_redidect();
    event_click_resources();
    right_click_upload_resources();
    right_click_edit_resources();
    event_click_upload_file_icon();
    event_click_uplaod_directory_icon();
    event_click_shared_files();

});

function directory_redidect(){
    $('[data-type="directory"] p, [data-type="directory"] i').click(function (e) { 
        e.preventDefault();
        let id = $(this).parent().attr('data-id');
        $.ajax({
            type: "GET",
            url: "http://"+window.location.host+"/cloudware-app/"+id,
            success: function (response) {
                window.location.href = "http://"+window.location.host+"/cloudware-app/"+id;
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

function create_file() {
    form_file_toogle();
    click_outside_file_form();
}

function share_source(source_pk,source_type) {
    form_share_toogle();
    click_outside_share_form();

    $('.btn').click(function (e) { 
        link_share_sorces(source_pk,source_type);
    });
}

function form_directory_toogle() {
    $('.form-directory-container').toggle();
    $('.dark-background').toggle();
}
function form_file_toogle() {
    $('.form-file-container').toggle();
    $('.dark-background').toggle();
}
function form_share_toogle() {
    $('.form-share-container').toggle();
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

function click_outside_share_form() {
    $('.dark-background').click(function (e) { 
        e.preventDefault();
        $('.form-share-container').hide();
        $('.dark-background').hide();
    });
}

function event_click_upload_file_icon() {
    $("#add-file").click(function(){
        create_file();
    });
}
function event_click_uplaod_directory_icon() {
    $("#add-directory").click(function(){
        create_directory();
    });
}


function event_click_resources() {
    $( ".resources" ).click(function() {
        $('.resources').removeClass('active');
        $( this ).toggleClass("active");

    });
}

function event_click_shared_files(){
    $('.shared_files').click(function (e) { 
        e.preventDefault();
        window.location.href = "http://"+window.location.host+"/cloudware-app/shared-files";
    });
}


function edit_source_name(source_pk,source_name,source_type) {

    let container = $('[data-id="'+source_pk+'"][data-type="'+source_type+'"]');
    container.children().last().remove();
    container.append('<input type="text" id="new_source_name" value="'+source_name+'" class="m-2" >');
    detect_enter_key_update_source('new_source_name',source_pk,source_type);
    click_outside_edit_source(container);

}

function delete_source(source_pk,source_type) { 
    $.ajax({
        url: "http://"+window.location.host+"/delete_"+source_type,
        type: "POST",
        data: {
            id: source_pk,
        },
        success: function(response){
            console.log(response);
            location.reload();
        }
        
    });
}

function download_file (source_pk) {
    $.ajax({
        url: "http://"+window.location.host+"/download_file/"+source_pk,
        type: "POST",
        success: function(response){
            window.location.href = "http://"+window.location.host+"/download_file/"+source_pk;
        }
        
    });
}

function link_share_sorces(source_pk,source_type) {
    emails = $('#share-emails').val();
    $.ajax({
        url: "http://"+window.location.host+"/share-"+source_type +"/"+source_pk,
        type: "POST",
        data: {
            id: source_pk,
            mails: emails,
            type: source_type,
        },
        success: function(response){
            console.log(response);
            location.reload();
        }
    });
}



function click_outside_edit_source(container) {
    $('#main_container').click(function (e) { 
        e.preventDefault();
        if(!$(e.target).is(container.children())){
            container.children().last().remove();
            if (container.attr('data-type') == 'file') {
                container.append('<p>'+container.attr('data-name')+container.attr('data-extension')+'</p>');
            }
            else{
                container.append('<p>'+container.attr('data-name')+'</p>');
            }
        }
    });
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
    $("#main_container" ).bind("contextmenu", function (event) {
    
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
            case "first": create_file(); break;
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
            case "first": download_file(source_pk); break;
            case "second": edit_source_name(source_pk,source_name,source_type); break;
            case "third": share_source(source_pk,source_type); break;
            case "fourth": delete_source(source_pk,source_type); break;
        }

        // Hide it AFTER the action was triggered
        $(".file-menu").hide(100);
    });
}   