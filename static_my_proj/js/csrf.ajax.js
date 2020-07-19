$(document).ready(function(){
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
          }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

  // PayPal
  if (window.location.href.includes("/cart/checkout/")) {
    let csrftoken = getCookie('csrftoken');
    let url = "/cart/create-paypal-transaction/";

    paypal.Buttons({
      style: {
        color:  'blue',
        shape:  'pill',
        label:  'pay',
        height: 50
      },
      createOrder: function() {
        return fetch(url, {
          method: 'post',
          headers: {
            'content-type': 'application/json',
            "X-CSRFToken": csrftoken,
          }
        }).then(function(data) {
          let orderID = data.url.split('/')[7];
          location.replace(data.url);
          return orderID;
        });
      },
    }).render('#paypal-button-container');
  }
})