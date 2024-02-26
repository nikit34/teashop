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

  function refreshCart() {
    var cartTable = $(".cart-table");
    var cartBody = cartTable.find(".cart-body");
    var productRows = cartBody.find(".cart-product");
    var currentUrl = window.location.href;

    var refreshCartUrl = "/api/cart/";
    var refreshCartMethod = "GET";
    var data = {};
    $.ajax({
      url: refreshCartUrl,
      method: refreshCartMethod,
      data: data,
      success: function (data) {
        var hiddenCartItemRemoveForm = $(".cart-item-remove-form");
        if (data.products.length > 0) {
          productRows.html(" ");
          var i = data.products.length;
          $.each(data.products, function (index, value) {
            var newCartItemRemove = hiddenCartItemRemoveForm.clone();
            newCartItemRemove.css("display", "block");
            newCartItemRemove.find(".cart-item-product-id").val(value.id);
            cartBody.prepend(
              '<tr><th scope="row">' +
                i +
                '</th><td><a href="' +
                value.url +
                '">' +
                value.name +
                "</a>" +
                newCartItemRemove.html() +
                "</td><td>" +
                value.price +
                "</tb></tr>"
            );
            i--;
          });
          cartBody.find(".cart-subtotal").text(data.subtotal);
          cartBody.find(".cart-total").text(data.total);
        } else {
          window.location.href = currentUrl;
        }
      },
      error: function (errorData) {
        $.alert({
          title: "Break!",
          content: "An error occurred",
          theme: "modern",
        });
      },
    });
  }

  window.refreshCart = refreshCart;
});
