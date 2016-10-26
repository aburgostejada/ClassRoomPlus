String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
};

$(document).ready(function(){
    $(".submitButton").click(function(){
        $(this).parents("form").submit();
    });

    $(document).foundation();
});


function add_option() {
    document.getElementById('options').innerHTML += '<input name="option[]" type="text" value="" placeholder="Option" />';
}


function delete_option() {
    document.getElementById('options').lastChild.remove();
}


