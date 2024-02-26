$(document).ready(function () {
  var subtotalField = $('.cart-subtotal');
  var totalField = $('.cart-total');

  var decrementBtn = $('.decrement-btn');
  decrementBtn.click(function(event) {
    event.preventDefault();
    var thisBtn = $(this);
    var productId = thisBtn.data('product-id');
    var actionEndpoint = thisBtn.attr("data-endpoint");
    var method = thisBtn.data('method');
    var inputField = $('.currentQuantity[data-product-id="' + productId + '"]');
    var currentQuantity = parseInt(inputField.val());

    var newQuantity = currentQuantity - 1;
    $.ajax({
      type: method,
      url: actionEndpoint,
      data: {
        'product_id': productId,
        'new_quantity': newQuantity
      },
      success: function(data) {
        inputField.val(data.currentQuantity);
        subtotalField.text(data.subtotal);
        totalField.text(data.total);
      },
      error: function(xhr, errmsg, err) {
        console.log(xhr.status + ': ' + xhr.responseText);
      }
    });
  });

  var incrementBtn = $('.increment-btn');
  incrementBtn.click(function(event) {
    event.preventDefault();
    var thisBtn = $(this);
    var productId = thisBtn.data('product-id');
    var actionEndpoint = thisBtn.attr("data-endpoint");
    var method = thisBtn.data('method');
    var inputField = $('.currentQuantity[data-product-id="' + productId + '"]');
    var currentQuantity = parseInt(inputField.val());

    var newQuantity = currentQuantity + 1;
    $.ajax({
      type: method,
      url: actionEndpoint,
      data: {
        'product_id': productId,
        'new_quantity': newQuantity
      },
      success: function(data) {
        inputField.val(data.currentQuantity);
        subtotalField.text(data.subtotal);
        totalField.text(data.total);
      },
      error: function(xhr, errmsg, err) {
        console.log(xhr.status + ': ' + xhr.responseText);
      }
    });
  });
});