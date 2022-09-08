(function () {
  var menu = document.getElementById("tab_menu1");
  var content = document.getElementById("tab_content1");
  var menus = menu.getElementsByTagName("a");
  var current;
  for (var i = 0, l = menus.length; i < l; i++) {
    tab_init(menus[i], i);
  }

  function tab_init(link, index) {
    var id = link.hash.slice(1);
    var page = document.getElementById(id);
    if (!current) {
      // 状態の初期化
      current = { page: page, menu: link };
      page.style.display = "block";
      link.className = "active";
    } else {
      page.style.display = "none";
    }
    link.onclick = function () {
      current.page.style.display = "none";
      current.menu.className = "";
      page.style.display = "block";
      link.className = "active";
      current.page = page;
      current.menu = link;
      return false;
    };
  }
})();
