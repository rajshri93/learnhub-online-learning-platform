document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".menu-toggle");
  const links = document.querySelector(".nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", () => {
      const open = links.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
    });
  }

  document.querySelectorAll(".complete-lesson").forEach((button) => {
    button.addEventListener("click", async () => {
      const lessonId = button.dataset.lessonId;
      button.disabled = true;
      button.textContent = "Saving...";
      try {
        const response = await fetch(`/lesson/${lessonId}/complete`, {
          method: "POST",
          headers: { "Accept": "application/json" }
        });
        const data = await response.json();
        if (!response.ok || !data.ok) throw new Error(data.error || "Could not save progress");
        button.textContent = "✓ Completed";
        button.classList.remove("btn-outline");
        button.classList.add("btn-completed");
        const navItem = document.querySelector(`.lesson-nav-item[href="#lesson-${lessonId}"]`);
        if (navItem) {
          navItem.classList.add("is-complete");
          const check = navItem.querySelector(".check-circle");
          if (check) check.textContent = "✓";
        }
        const bar = document.getElementById("progress-bar");
        const label = document.getElementById("progress-label");
        if (bar) bar.style.width = `${data.progress}%`;
        if (label) label.textContent = `${data.progress}% complete`;
      } catch (error) {
        button.disabled = false;
        button.textContent = "Try again →";
        window.alert(error.message);
      }
    });
  });
});
