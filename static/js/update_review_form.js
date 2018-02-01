$('.update_review_button').click(function (event){
    event.preventDefault();
    $(this).next('.update_review_form').fadeToggle(function () {
        $(this).parent().next('.current_review').fadeToggle();
    });
});
