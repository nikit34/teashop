$(document).ready(function () {

  var decrementBtn = $('.decrement-btn')
  decrementBtn.click(function(event) {
    event.preventDefault();
    var thisBtn = $(this);
    var productId = thisBtn.data('product-id');
    var actionEndpoint = thisBtn.attr("data-endpoint");
    var method = thisBtn.data('method');
    var currentQuantity = parseInt($('.currentQuantity[data-product-id="' + productId + '"]').val());

    var newQuantity = currentQuantity - 1;
    $.ajax({
      type: method,
      url: actionEndpoint,
      data: {
        'product_id': productId,
        'new_quantity': newQuantity
      },
      success: function(data) {
        $('.currentQuantity[data-product-id="' + productId + '"]').val(newQuantity);
      },
      error: function(xhr, errmsg, err) {
        console.log(xhr.status + ': ' + xhr.responseText);
      }
    });
  });

  var incrementBtn = $('.increment-btn')
  incrementBtn.click(function(event) {
    event.preventDefault();
    var thisBtn = $(this);
    var productId = thisBtn.data('product-id');
    var actionEndpoint = thisBtn.attr("data-endpoint");
    var method = thisBtn.data('method');
    var currentQuantity = parseInt($('.currentQuantity[data-product-id="' + productId + '"]').val());

    var newQuantity = currentQuantity + 1;
    $.ajax({
      type: method,
      url: actionEndpoint,
      data: {
        'product_id': productId,
        'new_quantity': newQuantity
      },
      success: function(data) {
        $('.currentQuantity[data-product-id="' + productId + '"]').val(newQuantity);
      },
      error: function(xhr, errmsg, err) {
        console.log(xhr.status + ': ' + xhr.responseText);
      }
    });
  });
});