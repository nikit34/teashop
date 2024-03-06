$(document).ready(function () {
  $(".carousel").carousel({
    interval: 2000,
  });

  var formComment = $('#form_comments')
  formComment.on('submit', function(event){
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