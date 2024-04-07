import { displaySubmitting } from './base.js';

$(document).ready(function () {
  var formCheckout = $('#form_checkout')
  formCheckout.on('submit', function(event){
    event.preventDefault();
    let serializedData = $(this).serialize();
    var checkoutFormSubmitBtn = formCheckout.find('[type="submit"]');
    var checkoutFormSubmitBtnTxt = checkoutFormSubmitBtn.text();
    displaySubmitting(checkoutFormSubmitBtn, "", true);
    $.ajax({
      url: '/api/checkout/',
      type: "POST",
      data: serializedData,
      success: function() {
        $('#id_msg').val('');
        setTimeout(function () {
          displaySubmitting(
            checkoutFormSubmitBtn,
            checkoutFormSubmitBtnTxt,
            false
          );
        }, 500);
      },
      error: function(error){
        $.alert({
          title: "Break!",
          content: "An error occurred",
          theme: "modern",
        });
      }
    });
  });
});