$(document).ready(function () {
    directory_redidect();
    create_directory();
    upload_file();
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
    $('#new_directory').click(function (e) { 
        e.preventDefault(); 
        let path = $(this).parent().parent().children().last();
        path.after('<td><input id="new_file"type="text" placeholder="New directory"></td>');
        $(this).after('<button class="btn btn-success">Save</button>');
        $('.btn').click(function (e) { 
            create_directory_call();
        });
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


function upload_file(){
    $('#upload_file').click(function (e) { 
        e.preventDefault(); 
        let path = $(this).parent().parent().children().last();
        path.after('<td><input id="new_file"type="file" placeholder="New file"></td>');
        $(this).after('<button class="btn btn-success">Save</button>');
        $('.btn').click(function (e) { 
            upload_file_call();
        });
    });
}
function upload_file_call(){
    let file = $('#new_file').prop('files')[0];
    console.log(file);
    let parent_id = $('#actual_directory').val();
    $.ajax({
        url: "http://"+window.location.host+"/upload_file",
        type: "POST",
        data: {
            file: file,
            parent_id: parent_id,
        },
        processData: false,
        contentType: false,
        cache: false,
        success: function(response){
            // window.location.reload();
        }
    });
}
