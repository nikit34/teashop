import { localization } from './base.js';


$(document).ready(function () {
  let lang = localization();

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
      success: refreshCart(),
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
      success: refreshCart(),
      error: function(xhr, errmsg, err) {
        console.log(xhr.status + ': ' + xhr.responseText);
      }
    });
  });

  $('.form').on('click', '.remove-btn', function() {
    var thisForm = $(this).closest('form');
    var productIdInput = thisForm.find('input[name="product_id"]');
    var newQuantity = 0;

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
        var fragment;
        switch (lang) {
          case "en":
            fragment = 'Add to cart';
            break;
          case "ru":
            fragment = 'Добавить в корзину';
            break;
          case "pt":
            fragment = 'Adicionar ao carrinho';
            break;
          default:
            fragment = "<div class='btn-group'>Undefined langueges in js</div>";
        }
        submitSpan.html('<button type="button" class="btn btn-success add-to-cart-btn">' + fragment + "</button>");
        var navbarCount = $(".navbar-cart-count");
        navbarCount.text(data.cartItemCount);
        var currentPath = window.location.href;
        if (currentPath.indexOf("cart") != -1) {
          refreshCart();
        }
      },
      error: function (errorData) {
        $.alert({
          title: "Break!",
          content: "An error occurred",
          theme: "modern",
        });
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
        var productsLength = data.products.length;
        if (productsLength > 0) {
          productRows.remove();
          var i = productsLength;
          $.each(data.products, function (index, productItem) {
            var newCartItemRemove = hiddenCartItemRemoveForm.clone();
            newCartItemRemove.css("display", "block");
            newCartItemRemove.find(".cart-item-product-id").val(productItem.id);
            cartBody.prepend(
              '<tr class="cart-product">' +
                '<th scope="row">' + i + '</th>' +
                '<td><a href="' + productItem.url + '">' + productItem.title + '</a>' +
                  newCartItemRemove.html() +
                '</td><td>' +
                  productItem.quantity + '&nbsp;' +
                '</td><td>' +
                  '<div class="input-group text-center">' +
                    '<button class="input-group-text decrement-btn" data-method="POST" data-endpoint="/' + lang + '/cart/update" data-product-id="' + productItem.id + '">-</button>' +
                    '<input type="text" name="quantity" class="form-control currentQuantity text-center" data-product-id="' + productItem.id + '" value="' + productItem.quantity + '" min="1">' +
                    '<button class="input-group-text increment-btn" data-method="POST" data-endpoint="/' + lang + '/cart/update" data-product-id="' + productItem.id + '">+</button>' +
                  '</div>' +
                '</td><td>' +
                  productItem.price +
                '</tb>' +
              '</tr>'
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
});
