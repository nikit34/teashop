import { localization } from './base.js';


$(document).ready(function () {
  let lang = localization();

  $('.form').on('click', '.add-to-cart-btn', function() {
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
            fragment = "In cart</a> <button type='button' class='btn btn-outline-danger remove-btn'>Remove?";
            break;
          case "ru":
            fragment = "Корзина</a> <button type='button' class='btn btn-outline-danger remove-btn'>Удалить?";
            break;
          case "pt":
            fragment = "No carrinho</a> <button type='button' class='btn btn-outline-danger remove-btn'>Remover?";
            break;
          default:
            fragment = "<div class='btn-group'>Undefined langueges in js</div>";
        }
        submitSpan.html("<div class='btn-group'> <a class='btn btn-success' href='/cart/'>" + fragment + "</button></div>");
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
});