$(document).ready(function () {

  var decrementBtn = $('.decrement-btn')
  decrementBtn.click(function(event) {
    event.preventDefault();
      var currentQuantity = $('.currentQuantity').val();
      var thisBtn = $(this);
      var productId = thisBtn.data('product-id');
      var actionEndpoint = thisBtn.attr("data-endpoint");
      var method = thisBtn.data('method');

      $.ajax({
          type: method,
          url: actionEndpoint,
          data: {
              'product_id': productId,
              'quantity': currentQuantity + 1
          },
          success: function(data) {
            if (data.added) {
              $('#quantity-display').text(data.new_quantity);
                console.log('Quantity updated successfully');
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
      var currentQuantity = $('.currentQuantity').val();
      var thisBtn = $(this);
      var productId = thisBtn.data('product-id');
      var actionEndpoint = thisBtn.attr("data-endpoint");
      var method = thisBtn.data('method');

      $.ajax({
          type: method,
          url: actionEndpoint,
          data: {
              'product_id': productId,
              'quantity': currentQuantity - 1
          },
          success: function(data) {
            if (data.success) {
              $('#quantity-display').text(data.new_quantity);
                console.log('Quantity updated successfully');
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