$(document).ready(function () {

  var decrementBtn = $('.decrement-btn')
  decrementBtn.click(function(event) {
    event.preventDefault();
    var currentQuantity = parseInt($('.currentQuantity').val());
    var thisBtn = $(this);
    var productId = thisBtn.data('product-id');
    var actionEndpoint = thisBtn.attr("data-endpoint");
    var method = thisBtn.data('method');

    var newQuantity = currentQuantity - 1;
    $.ajax({
      type: method,
      url: actionEndpoint,
      data: {
        'product_id': productId,
        'new_quantity': newQuantity
      },
      success: function(data) {
        if (data.removed) {
          $('.currentQuantity[data-product-id="' + productId + '"]').val(newQuantity);
          console.log('Quantity decrement successfully');
        } else {
          console.log('Failed to update quantity:', data.error);
        }
      },
      error: function(xhr, errmsg, err) {
        console.log(xhr.status + ': ' + xhr.responseText);
      }
    });
  });

  var incrementBtn = $('.increment-btn')
  incrementBtn.click(function(event) {
    event.preventDefault();
    var currentQuantity = parseInt($('.currentQuantity').val());
    var thisBtn = $(this);
    var productId = thisBtn.data('product-id');
    var actionEndpoint = thisBtn.attr("data-endpoint");
    var method = thisBtn.data('method');

    var newQuantity = currentQuantity + 1;
    $.ajax({
      type: method,
      url: actionEndpoint,
      data: {
        'product_id': productId,
        'new_quantity': newQuantity
      },
      success: function(data) {
        if (data.added) {
          $('.currentQuantity[data-product-id="' + productId + '"]').val(newQuantity);
          console.log('Quantity increment successfully');
        } else {
          console.log('Failed to update quantity:', data.error);
        }
      },
      error: function(xhr, errmsg, err) {
        console.log(xhr.status + ': ' + xhr.responseText);
      }
    });
  });
});