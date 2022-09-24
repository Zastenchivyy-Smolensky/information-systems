(() => {
  const $tabs = document.querySelectorAll("[data-tab]");
  const $contents = document.querySelectorAll("[data-content]");
  //初期表示で最初の要素以外は非表示
  $contents.forEach(($content, index) => {
    if (!index) {
      return;
    }
    $content.style.display = "none";
  });
  //たぶをクリック時に対象の要素を表示
  const onClick = (event) => {
    const tabIndex = event.target.dataset.tab;
    const $content = document.querySelector(`[data-content="${tabIndex}"]`);
    //一旦すべてのコンテンツを非表示
    $contents.forEach(($content) => {
      $content.style.display = "none";
    });
    //いったんすべてのたぶを初期化
    $tabs.forEach(($tab) => {
      $tab.classList.remove("is-active");
    });
    $content.style.display = "block";
    event.target.classList.add("is-active");
  };
  $tabs.forEach(($tab) => {
    $tab.addEventListener("click", onClick);
  });
})();
