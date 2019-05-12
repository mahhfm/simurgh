$(function(){
     $(".table").on("click", "tr[role=\"button\"]", function (e) {
          window.location = $(this).data("href");
     });
});