$('.update_review_button').click(function (event){
    event.preventDefault();
    $(this).hide();
    $(this).next('.update_review_form').fadeToggle();
    $(this).parent().next('.current_review').hide();
});


$('.update').click(function (){
    $(this).parent().parent().prev().fadeToggle();
    $(this).parent().parent().hide();
    $(this).parent().parent().parent().next().fadeToggle();
});