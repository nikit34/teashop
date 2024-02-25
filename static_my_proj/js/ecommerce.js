$(document).ready(function () {
  // contact handler
  var contactForm = $(".contact-form");
  var contactFormMethod = contactForm.attr("method");
  var contactFormEndpoint = contactForm.attr("action");
  let lang = localization();
  function displaySubmitting(submitBtn, defaultText, doSubmit) {
    if (doSubmit) {
      submitBtn.addClass("disabled");
      var fragment;
      switch (lang) {
        case "en":
          fragment = '<i class="fa fa-spin fa-spinner"></i>Sending...';
          break;
        case "ru":
          fragment = '<i class="fa fa-spin fa-spinner"></i>Отправление...';
          break;
        case "pt":
          fragment = '<i class="fa fa-spin fa-spinner"></i>Enviando...';
          break;
        default:
          fragment = '<i class="fa fa-spin fa-spinner"></i>Undefined langueges in js';
      }
      searchBtn.html(fragment);
    } else {
      submitBtn.removeClass("disabled");
      submitBtn.html(defaultText);
    }
  }
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
  // search-form
  var searchForm = $(".search-form");
  var searchInput = searchForm.find('[name="q"]');
  var typingTimer;
  var typingInterval = 1500;
  var searchBtn = searchForm.find('[type="submit"]');
  searchInput.keyup(function (event) {
    clearTimeout(typingTimer);
    typingTimer = setTimeout(perfomSearch, typingInterval);
  });
  searchInput.keydown(function (event) {
    clearTimeout(typingTimer);
  });
  function displaySearching() {
    let lang = localization();
    searchBtn.addClass("disabled");
    var fragment;
    switch (lang) {
      case "en":
        fragment = '<i class="fa fa-spin fa-spinner"></i>Searching...';
        break;
      case "ru":
        fragment = '<i class="fa fa-spin fa-spinner"></i>Поиск...';
        break;
      case "pt":
        fragment = '<i class="fa fa-spin fa-spinner"></i>Procurando...';
        break;
      default:
        fragment = '<i class="fa fa-spin fa-spinner"></i>Undefined langueges in js';
    }
    searchBtn.html(fragment);
  }
  function perfomSearch() {
    displaySearching();
    var query = searchInput.val();
    setTimeout(function () {
      window.location.href = "/search/?q=" + query;
    }, 1000);
  }
  // product-cart
  var productForm = $(".form-product-ajax");

  productForm.submit(function (event) {
    event.preventDefault();
    var thisForm = $(this);
    var actionEndpoint = thisForm.attr("data-endpoint");
    var httpMethod = thisForm.attr("method");
    var formData = thisForm.serialize();
    let lang = localization();
    $.ajax({
      url: actionEndpoint,
      method: httpMethod,
      data: formData,
      success: function (data) {
        var submitSpan = thisForm.find(".submit-span");
        var fragment;
        if (data.added) {
          switch (lang) {
            case "en":
              fragment = "<div class='btn-group'> <a class='btn btn-success' href='/cart/'>In cart</a> <button type='submit' class='btn btn-outline-danger'>Remove?</button></div>";
              break;
            case "ru":
              fragment = "<div class='btn-group'> <a class='btn btn-success' href='/cart/'>Корзина</a> <button type='submit' class='btn btn-outline-danger'>Удалить?</button></div>";
              break;
            case "pt":
              fragment = "<div class='btn-group'> <a class='btn btn-success' href='/cart/'>No carrinho</a> <button type='submit' class='btn btn-outline-danger'>Remover?</button></div>";
              break;
            default:
              fragment = "<div class='btn-group'>Undefined langueges in js</div>";
          }
        } else {
          switch (lang) {
            case "en":
              fragment = '<button type="submit" class="btn btn-success">Add to cart</button>';
              break;
            case "ru":
              fragment = '<button type="submit" class="btn btn-success">Добавить в корзину</button>';
              break;
            case "pt":
              fragment = '<button type="submit" class="btn btn-success">Adicionar ao carrinho</button>';
              break;
            default:
              fragment = "<div class='btn-group'>Undefined langueges in js</div>";
          }
        }
        submitSpan.html(fragment);
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
      },
    });
  });

  $(".carousel").carousel({
    interval: 2000,
  });

  function refreshCart() {
    var cartTable = $(".cart-table");
    var cartBody = cartTable.find(".cart-body");
    var productRows = cartBody.find(".cart-product");
    var correntUrl = window.location.href;

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
          i = data.products.length;
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
          window.location.href = correntUrl;
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

  $('#form_comments').on('submit', function(event){
    event.preventDefault();
    let serializedData = $(this).serialize();
    $.ajax({
      url: window.location.href,
      type: "POST",
      data: serializedData,
      success: function(){
        $('#id_msg').val('');
        location.reload();
      },
      error: function(error){
        $.alert({
          title: "Break!",
          content: "An error occurred",
          theme: "modern",
        });
      }
    });
  });
});

function localization(){
  let localizations = document.getElementsByName("language");
  let i_attr_value, lang;
  for (let i = 0; i < localizations.length; i++) {
    if (localizations[i].outerHTML.includes("selected")) {
      i_attr_value = localizations[i].outerHTML.indexOf("value=");
      lang = localizations[i].outerHTML.slice(
        i_attr_value + 7,
        i_attr_value + 9
      );
    }
  }
  return lang;
}
