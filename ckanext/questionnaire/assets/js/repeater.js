$("select").on("change", function () {
  var max_fields = 10; //maximum input boxes allowed
  var wrapper = $(".input_fields_wrap"); //Fields wrapper
  var add_button = $(".add_field_button"); //Add button ID
  var x = 1; //initlal text box count
  $(".remove_field").remove();
  $(".show").attr("class", "hidden");

  if (this.value !== "text") {
    $(".hidden").attr("class", "show");
    $(add_button).click(function (e) {
      //on add input button click
      e.preventDefault();
      if (x < max_fields) {
        //max input box allowed
        x++; //text box increment
        $(wrapper).append(
          '<div class="controls show"><input id="question-option" type="text" name="question-option" class="form-control"><button class="remove_field">-</button></div>'
        ); //add input box
      }
    });
  }

  $(wrapper).on("click", ".remove_field", function (e) {
    //user click on remove text
    e.preventDefault();
    $(this).parent("div").remove();
    x--;
  });
});
