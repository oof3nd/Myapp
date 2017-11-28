$(document).ready(function(){
     $(".close").click(function(){
        $("#alert-solution").hide();
    });

    $( "#btn-solution" ).click(function() {
       $("#alert-solution").toggle('slow');
});

});