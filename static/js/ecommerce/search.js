import { localization } from './base.js';


$(document).ready(function () {
  let lang = localization();

  var searchForm = $(".navbar-search-form");
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
    searchBtn.addClass("disabled");
    searchBtn.html('<i class="fa fa-spin fa-spinner"></i>' + gettext('Searching...'));
  }
  function perfomSearch() {
    displaySearching();
    var query = searchInput.val();
    setTimeout(function () {
      window.location.href = "/" + lang + "/search/?q=" + encodeURIComponent(query);
    }, 1000);
  }
});