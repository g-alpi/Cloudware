$(document).ready(function(){
    activate_edit();
    delete_file();
    create_directory();
});

function delete_file() {
    $('.delete').click(function () { 
        let id = $(this).parent().parent().children().first().text();
        console.log(id);
        const csrftoken = $('[name=csrfmiddlewaretoken]').val();
        $.ajax({
            url: "http://"+window.location.host+"/delete_file",
            type: "POST",
            data: {
                id: id,
                csrfmiddlewaretoken: csrftoken
            },
            success: function(response){
                console.log(response);
                location.reload();
            }
        });
        
    });
}


function activate_edit(){
    $(".edit").click(function(){
        let path = $(this).parent().parent().children().first().next().next();
        path.after('<td><input id="new_file"type="file" value="'+path.text()+'"></td>');
        path.remove();
        $(this).after('<button class="btn btn-success">Save</button>');
        $('.btn').click(function (e) { 
            edit_file(this);
            
        });
        
    });
}

function edit_file(event){
    let id = $(event).parent().parent().children().first().text();
    let file = $('#new_file').val();
    console.log(id);
    let csrftoken = $('[name=csrfmiddlewaretoken]').val();
    $.ajax({
        url: "http://"+window.location.host+"/edit_file",
        type: "POST",
        data: {
            id: id,
            file: file,
            csrfmiddlewaretoken: csrftoken
        },
        success: function(response){
            console.log(response);
            window.location.reload();
        }
    });
}
