$(".action_form").on("submit", function(event){
          event.preventDefault();
          console.log("form submitted!");
          $.ajax({
            type : "POST",
            data : $(this).serializeArray(),
            success : function(json) {console.log(json)}, // log the returned json to the console
          });
        });