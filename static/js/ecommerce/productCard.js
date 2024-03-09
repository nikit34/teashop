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
        var fragment;
        switch (lang) {
          case "en":
            fragment = "In cart</a> <button type='button' class='btn btn-default remove-btn'>Remove?";
            break;
          case "ru":
            fragment = "Корзина</a> <button type='button' class='btn btn-default remove-btn'>Удалить?";
            break;
          case "pt":
            fragment = "No carrinho</a> <button type='button' class='btn btn-default remove-btn'>Remover?";
            break;
          default:
            fragment = "<div class='btn-group'>Undefined langueges in js</div>";
        }
        submitSpan.html("<div class='btn-group'> <a class='btn btn-general' href='/cart/'>" + fragment + "</button></div>");
        var navbarCount = $(".navbar-cart-count");
        navbarCount.text(data.cartItemsCount);
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
        submitSpan.html('<button type="button" class="btn btn-general add-to-cart-btn">' + fragment + "</button>");
        var navbarCount = $(".navbar-cart-count");
        navbarCount.text(data.cartItemsCount);
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
});
