addEventListener("load", function () {
  const src1 = "static/images/69681.jpg";
  const src2 = "static/images/69678.jpg";
  const src3 = "static/images/04.png";
  const img_src = [src1, src2, src3];
  const menu = document.querySelectorAll(".js-menu");
  let num = -1;
  function toggle() {
    const content = this.nextElementSibling;
    this.classList.toggle("is-active");
    content.classList.toggle("is-open");
  }

  function slide_time() {
    if (num === 2) {
      num = 0;
    } else {
      num++;
    }
    document.getElementById("slide_img").src = img_src[num];
  }

  setInterval(slide_time, 3000);

  for (let i = 0; i < menu.length; i++) {
    menu[i].addEventListener("click", toggle);
  }
});
