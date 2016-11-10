String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
};

function setUpCreateNewQuestion(){
    var options = $("#options");

    $("#addOption").click(function(e) {
        e.preventDefault();
        var newOption = $('<input style="display:none;" name="option[]" type="text" value="" placeholder="Option" />');
        options.append(newOption);
        newOption.show("fast");
    });

    $("#deleteOption").click(function(e) {
        e.preventDefault();
        options.find("input:last-child").hide("fast").remove();
    });

    $("input[name=answer_type]").change(function(){
        if(this.value == "yes_no" || this.value == "free_text"){
            options.hide();
            $("#optionsActions").hide();
        }else{
            options.show();
            $("#optionsActions").show();
        }
    });
}

$(document).ready(function(){

    if($("#createQuiz").length > 0 || $("#createPoll").length > 0){
        setUpCreateNewQuestion();
    }

    $(document).foundation();
    if(('.timer-quick').length > 0){
        $('.timer-quick').startTimer({
          onComplete: function(){
                alert("Time is UP...");
                $("#submit").click();
          }
        });
    }
});










