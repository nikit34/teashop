import { localization } from './base.js';


$(document).ready(function () {
  let lang = localization();

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
});