$(".bg-semi-transparent-black").on("click", function(){
    $(this).hide();
    $(".modify-form").hide();
});
$("#edit-username").on("click", function(){
    $("#modal-transparent-background").show();
    $("#modify-username").show();
});
$("#edit-email").on("click", function(){
    $("#modal-transparent-background").show();
    $("#modify-email").show();
});
$("#edit-password").on("click", function(){
    $("#modal-transparent-background").show();
    $("#modify-password").show();
});
$("#delete-account").on("click", function(){
    $("#modal-transparent-background").show();
    $("#delete-account-modal").show();
});
$("dismiss-delete-account").on("click", function(event){
    event.preventDefault();
    $("#modal-transparent-background").hide();
    $(".modify-form").hide();
});