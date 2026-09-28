import { localization } from './base.js';


$(document).ready(function () {
  let lang = localization();

  var thisForm = $('.form');
  thisForm.on('click', '.add-to-cart-btn', function() {
    var thisForm = $(this).closest('form');
    var productIdInput = thisForm.find('input[name="product_id"]');
    var newQuantity = 1;

    $.ajax({
      url: thisForm.data('endpoint'),
      type: thisForm.attr('method'),
      data: {
        'product_id': productIdInput.val(),
        'new_quantity': newQuantity
      },
      dataType: 'json',
      success: function(data) {
        var submitSpan = thisForm.find(".submit-span");
        submitSpan.html("<div class='btn-group'> <a class='btn btn-general' href='/" + lang + "/cart/'>" + gettext('In cart') +
          "</a> <button type='button' class='btn btn-default remove-btn'>" + gettext('Remove') + "?</button></div>");
        var navbarCount = $(".navbar-cart-count");
        navbarCount.text(data.cartItemsCount);
      },
      error: function (errorData) {
        $.alert({
          title: gettext("Error"),
          content: gettext("An error occurred. Please try again."),
          theme: "modern",
        });
      }
    });
  });

  thisForm.on('click', '.remove-btn', function() {
    var thisForm = $(this).closest('form');
    var productIdInput = thisForm.find('input[name="product_id"]');
    var newQuantity = 0;
    var actionEndpoint = thisForm.data('endpoint');
    var method = thisForm.attr('method');

    $.ajax({
      type: method,
      url: actionEndpoint,
      data: {
        'product_id': productIdInput.val(),
        'new_quantity': newQuantity
      },
      dataType: 'json',
      success: function(data) {
        var submitSpan = thisForm.find(".submit-span");
        submitSpan.html('<button type="button" class="btn btn-general add-to-cart-btn">' + gettext('Add to cart') + "</button>");
        var navbarCount = $(".navbar-cart-count");
        navbarCount.text(data.cartItemsCount);
      },
      error: function (errorData) {
        $.alert({
          title: gettext("Error"),
          content: gettext("An error occurred. Please try again."),
          theme: "modern",
        });
      }
    });
  });
});
