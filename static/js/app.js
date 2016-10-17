String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
};

$(document).ready(function(){
    $("#loginButton").click(function(){
        $("#login").find("form").submit();
    });


    $(document).foundation();

});


