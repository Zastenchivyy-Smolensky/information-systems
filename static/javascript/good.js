$(function () {
  var $good = $(".good-btn"),
    reviewId;
  $good.on("click", function (e) {
    e.stopPropagation();
    var $this = $(this);
    var data = JSON.stringify({ review_id: $this.data("review_id") });
    $.ajax({
      type: "POST",
      url: "/good",
      data: data,
      contentType: "application/json",
    })
      .done(function (data) {
        $this.next().text(data);
        $this.toggleClass("good-btn-active");
      })
      .fail(function (msg) {
        console.log("エラー");
      });
  });
});
