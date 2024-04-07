import { localization, displaySubmitting } from './base.js';


$(document).ready(function () {
  let lang = localization();

  var contactForm = $(".contact-form");
  var contactFormMethod = contactForm.attr("method");
  var contactFormEndpoint = contactForm.attr("action");
  contactForm.submit(function (event) {
    event.preventDefault();
    var contactFormSubmitBtn = contactForm.find('[type="submit"]');
    var contactFormSubmitBtnTxt = contactFormSubmitBtn.text();
    var contactFormData = contactForm.serialize();
    var thisForm = $(this);
    displaySubmitting(contactFormSubmitBtn, "", true);
    let lang = localization();
    $.ajax({
      method: contactFormMethod,
      url: contactFormEndpoint,
      data: contactFormData,
      success: function (data) {
        contactForm[0].reset();
        $.alert({
          title: "Success!",
          content: data.message,
          theme: "modern",
        });
        setTimeout(function () {
          displaySubmitting(
            contactFormSubmitBtn,
            contactFormSubmitBtnTxt,
            false
          );
        }, 500);
      },
      error: function (error) {
        var jsonData = error.responseJSON;
        var msg = "";
        $.each(jsonData, function (key, value) {
          msg += key + ": " + value[0].message + "<br/>";
        });
        $.alert({
          title: "Break!",
          content: msg,
          theme: "modern",
        });
        setTimeout(function () {
          displaySubmitting(
            contactFormSubmitBtn,
            contactFormSubmitBtnTxt,
            false
          );
        }, 500);
      },
    });
  });
});