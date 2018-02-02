$('.update_quantity_button').click(function (event){
    event.preventDefault();
    $(this).next('.update_quantity').fadeToggle();
    $(this).hide();
});

$('.save').click(function (){
    $(this).parent().parent().prev().fadeToggle();
    $(this).parent().parent().hide();
});
