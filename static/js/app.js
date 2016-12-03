String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
};
//TODO REFACTOR
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

function setUpEditQuizQuestion(){
    var options = $("#options");

    $("#addOption").click(function(e) {
        e.preventDefault();
        var newOption = $('<input style="display:none;" name="option[]" type="text" value="" placeholder="Option" />');
        options.find(".newQuestions").append(newOption);
        newOption.show("fast");
    });

    $("#deleteOption").click(function(e) {
        e.preventDefault();
        options.find(".newQuestions input:last-child").hide("fast").remove();
    });

    $(".deleteOption").click(function(e){
          e.preventDefault();
          $(this).parents(".current_option").remove();
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


function setUpDeleteQuizQuestion() {
    $("a.deleteQuizQuestion").click(function (e) {
        e.preventDefault();
        if (window.confirm("Do you really want to Delete The Question?")) {
            $.post($(this).attr("href"), function (res) {
                if(res.result == "success"){
                    window.location.search += '&time='+new Date().getTime();
                }
            });
        }
    });
}

$(document).ready(function(){
    if($("#createQuiz").length > 0 || $("#createPoll").length > 0 ){
        setUpCreateNewQuestion();
    }

    if($("#editQuizQuestion").length > 0 ){
        setUpEditQuizQuestion();
    }



    setUpDeleteQuizQuestion();

    $(document).foundation();

    if(('.timer-quick').length > 0){
        $('.timer-quick').startTimer({
            onComplete: function(){
                alert("Time is UP...");
                $("#submit").click();
            }
        });
    }

    var input = $('#refresh');
    input.val() == 'yes' ? location.reload(true) : input.val('yes');
});










