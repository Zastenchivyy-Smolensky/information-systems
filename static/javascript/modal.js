(() => {
  const open = document.getElementById("modal-open");
  const modalBg = document.getElementById("modal-bg");
  const container = document.getElementById("modal-container");
  const close = document.getElementById("modal-close");
  open.addEventListener("click", function () {
    container.classList.add("active");
    modalBg.classList.add("active");
  });
  close.addEventListener("click", function () {
    container.classList.remove("active");
    modalBg.classList.remove("active");
  });
  modalBg.addEventListener("click", function () {
    container.classList.remove("active");
    modalBg.classList.remove("active");
  });
})();
