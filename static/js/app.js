String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
};

$(document).ready(function(){
    $(".submitButton").click(function(){
        $(this).parents("form").submit();
    });

    $(document).foundation();
});


