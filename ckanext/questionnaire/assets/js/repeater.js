var max_fields = 10; //maximum input boxes allowed
var wrapper = $(".input_fields_wrap"); //Fields wrapper
var add_button = $(".add_field_button"); //Add button ID
var x = 1; //initlal text box count

$("#field-question-type").on("change", function () {
  var remove_field = $("._show");

  $(".show").attr("class", "hidden");
  $(remove_field).remove();

  if (this.value !== "text") {
    _button = $(":button.hidden");
    $(_button).attr("class", "show btn btn-primary add_field_button");
    $(".hidden").attr("class", "show form-group");

    add_button_event;
  }
});

add_button_event = $(add_button).click(function (e) {
  //on add input button click
  e.preventDefault();
  if (x < max_fields) {
    //max input box allowed
    x++; //text box increment
    $(wrapper).append(
      '<div style="display:flex; gap:10px" class="form-group _show"><input id="question-option" type="text" name="question-option" class="form-control"><button class="btn btn-danger remove_field">-</button></div>'
    ); //add input box
  }
});

$(wrapper).on("click", ".remove_field", function (e) {
  //user click on remove text
  console.log(this);
  e.preventDefault();
  $(this).parent("div").remove();
  x--;
});
