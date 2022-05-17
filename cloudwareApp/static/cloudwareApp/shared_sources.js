$(document).ready(function () {
    directory_redidect();
    event_click_resources();
    right_click_edit_resources();
    event_click_my_files();
});

function directory_redidect(){
    $('[data-type="directory"] p, [data-type="directory"] i').click(function (e) { 
        e.preventDefault();
        let id = $(this).parent().attr('data-id');
        $.ajax({
            type: "GET",
            url: "http://"+window.location.host+"/cloudware-app/shared-files/"+id,
            success: function (response) {
                window.location.href = "http://"+window.location.host+"/cloudware-app/shared-files/"+id;
            }
        });
    });

}

function event_click_resources() {
    $( ".resources" ).click(function() {
        $('.resources').removeClass('active');
        $( this ).toggleClass("active");

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

function event_click_my_files(){
    $('.my_files').click(function (e) { 
        e.preventDefault();
        window.location.href = "http://"+window.location.host+"/cloudware-app";
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
        }

        // Hide it AFTER the action was triggered
        $(".file-menu").hide(100);
    });
}   