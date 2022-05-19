$(document).ready(function () {
    directory_redidect();
    event_click_resources();
    right_click_upload_resources();
    right_click_edit_resources();
    event_click_interact_icons();
    event_click_shared_files();
    click_outside_file_form();
    hide_modal_app();
});

function hide_modal_app(){
    $('.dark-background').click(function (e) {
        $('.form-container').hide();
        $('.dark-background').hide();
    });
}

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
    let name = $('#new_directory').val();
    if(validate_directory_name(name)){
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
    else{
        $('#new_directory').before('<div class="alert alert-danger alert-dismissible fade show" role="alert">Enter a name without /, \\, or *<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>');
    }
}
function validate_directory_name(name){
    let regex = /^[^\s^\x00-\x1f\\?*:"";<>|\/.][^\x00-\x1f\\?*:"";<>|\/]*[^\s^\x00-\x1f\\?*:"";<>|\/.]+$/g;
    if(regex.test(name)){
        return true;
    }else{
        return false;
    }
}

function create_file() {
    form_file_toogle();

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

function event_click_interact_icons() {
    $(".rounded-circle").click(function(e){
        e.preventDefault();
        switch (this.id) {
            case 'add-file':
                create_file();
                break;
            case 'remove-file':
                if($(".active").length === 1 && $('.active').attr('data-type')=='file'){
                    delete_confirmation($('.active').attr('data-id'),$(".active").attr("data-name"), $('.active').attr('data-type'));
                }
                else{
                    create_warning('You have to select a file to remove');
                }
                break;
            case 'share-file':
                if($('.active').attr('data-type')=='file'){
                    share_source($('.active').attr('data-id'),$('.active').attr('data-type'));
                }
                else{
                    create_warning('You have to select a file to share');
                }
                break;
            case 'add-directory':
                create_directory();
                break;
            case 'remove-directory':
                if($(".active").length === 1 && $('.active').attr('data-type') == 'directory'){
                    delete_confirmation($('.active').attr('data-id'),$(".active").attr("data-name"), $('.active').attr('data-type'));
                }
                else{
                    create_warning("You have to select a directory to remove")
                }
                break;
            case 'share-directory':
                if ($('.active').attr('data-type') == 'directory') {
                    share_source($('.active').attr('data-id'),$('.active').attr('data-type'));
                }
                else{
                    create_warning('You have to select a directory to share');
                }
                break;
            default:
                break;
        }
    });
    
}

function create_warning(message){
    main_div = $('<div class="alert alert-danger alert-dismissible fade show" role="alert"></div>')
    svg_symbol = $('<svg xmlns="http://www.w3.org/2000/svg" style="display: none;"><symbol id="exclamation-triangle-fill" fill="currentColor" viewBox="0 0 16 16"><path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/></symbol></svg>')
    close_symbol = $('<svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Danger:"><use xlink:href="#exclamation-triangle-fill"/></svg>')
    button = $('<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>')
    main_div.append(svg_symbol)
    main_div.append(close_symbol)
    main_div.append(message)
    main_div.append(button)     
    $(".user-messages").append(main_div)
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
            if (response['emailError'] != 'null'){
                $('#share-emails').before('<div class="alert alert-danger alert-dismissible fade show" role="alert">'+response['emailError']+'<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>');
            }
            else{
                $('#share-emails').before('<div class="alert alert-success alert-dismissible fade show" role="alert">'+response['success']+'<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>');
                setTimeout(function(){
                    $('.alert').alert('close');
                    form_share_toogle();
                }, 2000);
            }
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
        if (source_type == 'directory') {
            $('[data-action="first"]').hide();
        }
        else{
            $('[data-action="first"]').show();
        }
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
            case "fourth": delete_confirmation(source_pk, source_name, source_type); break;
        }

        // Hide it AFTER the action was triggered
        $(".file-menu").hide(100);
    });
}   

function delete_confirmation(source_pk, source_name, source_type) {
    $(".form-delete-container").show();
    $(".dark-background").show();
    $("#delete-form p").text("Are you sure you want to delete " + source_name + "?");
    $("#resource_id").val(source_pk);
    $("#delete-form").attr("action", "http://"+window.location.host+"/delete_"+source_type);
}