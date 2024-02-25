$(document).ready(function () {
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

export { localization };