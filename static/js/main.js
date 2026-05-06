document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".alert").forEach((alert) => {
    setTimeout(() => alert.remove(), 5000);
  });

  document.querySelectorAll(".password-toggle").forEach((button) => {
    button.addEventListener("click", () => {
      const input = button.parentElement.querySelector("input");
      const isPassword = input.type === "password";
      input.type = isPassword ? "text" : "password";
      button.textContent = isPassword ? "Hide" : "Show";
      button.setAttribute("aria-label", isPassword ? "Hide password" : "Show password");
    });
  });

  document.querySelectorAll("form[data-confirm]").forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (!window.confirm(form.dataset.confirm)) {
        event.preventDefault();
      }
    });
  });
});
