function getCsrfToken() {
const name = "csrftoken";
const cookies = document.cookie.split(";");
for (let cookie of cookies) {
    cookie = cookie.trim();
    if (cookie.startsWith(name + "=")) {
    return cookie.substring(name.length + 1);
    }
}
return "";
}

const searchBox = document.getElementById("search-box");
const resultsList = document.getElementById("live-results");
let debounceTimer;

searchBox.addEventListener("input", function () {
clearTimeout(debounceTimer);
const query = this.value.trim();

if (query.length === 0) {
    resultsList.innerHTML = "";
    return;
}

debounceTimer = setTimeout(() => {
    fetch(`/search-ajax/?query=${encodeURIComponent(query)}`)
    .then(response => response.json())
    .then(data => {
        resultsList.innerHTML = "";
        data.results.forEach(game => {
        const li = document.createElement("li");

        const img = document.createElement("img");
        img.src = game.cover_image_url;
        img.alt = game.name;
        img.style.height = "60px";

        const text = document.createElement("span");
        text.textContent = " " + game.name;

        const addButton = document.createElement("button");
        addButton.textContent = "+";
        addButton.className = "add-button";
        addButton.setAttribute("aria-label", `Add ${game.name} to tracker`);
        addButton.title = "Add to tracker";
        addButton.addEventListener("click", () => {
            fetch("/add-game/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCsrfToken(),
            },
            body: JSON.stringify({
                title: game.name,
                cover_image_url: game.cover_image_url,
            }),
            })
            .then(() => {
                window.location.reload();
            });
        });

        li.appendChild(img);
        li.appendChild(text);
        li.appendChild(addButton);
        resultsList.appendChild(li);
        });
    });
}, 300);
});

document.querySelectorAll(".status-select").forEach(select => {
select.addEventListener("change", function () {
    const itemId = this.dataset.itemId;
    const newStatus = this.value;
    const colourMap = {
    "not_started": "secondary",
    "playing": "primary",
    "done": "success",
    "dropped": "danger"
    }
    this.className = `badge badge-pill badge-${colourMap[newStatus]} status-select`;
    fetch(`/update-status/${itemId}/`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),
    },
    body: JSON.stringify({ status: newStatus })
    });
});
});

document.querySelectorAll(".delete-button").forEach(button => {
button.addEventListener("click", function () {
    const itemId = this.dataset.itemId;

    fetch(`/delete-game/${itemId}/`, {
    method: "POST",
    headers: {
        "X-CSRFToken": getCsrfToken(),
    },
    })
    .then(response => response.json())
    .then(() => {
        // Remove this row from the page
        const row = this.closest("tr");
        row.remove();
    });
});
});

document.addEventListener("click", function (event) {
const clickedInsideSearch = event.target.closest(".search-wrapper");
if (!clickedInsideSearch) {
    resultsList.innerHTML = "";
}
});

const notesSidebar = document.getElementById("notes-sidebar");
const notesOverlay = document.getElementById("notes-overlay");
const notesTitle = document.getElementById("notes-title");
const notesCover = document.getElementById("notes-cover");
const notesTextarea = document.getElementById("notes-textarea");
let currentItemId = null;
document.querySelectorAll(".notes-button").forEach(button => {
  button.addEventListener("click", function () {
    currentItemId = this.dataset.itemId;
    notesTitle.textContent = this.dataset.title;
    notesCover.src = this.dataset.cover;
    fetch(`/get-notes/${currentItemId}/`)
      .then(response => response.json())
      .then(data => {
        notesTextarea.value = data.notes || "";
        notesSidebar.classList.add("open");
        notesOverlay.classList.add("open");
      });
  });
});
document.getElementById("notes-close").addEventListener("click", closeSidebar);
notesOverlay.addEventListener("click", closeSidebar);
function closeSidebar() {
  notesSidebar.classList.remove("open");
  notesOverlay.classList.remove("open");
}
document.getElementById("notes-save").addEventListener("click", function () {
  fetch(`/save-notes/${currentItemId}/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCsrfToken(),
    },
    body: JSON.stringify({ notes: notesTextarea.value }),
  }).then(() => {
    this.textContent = "Saved!";
    setTimeout(() => { this.textContent = "Save"; }, 1200);
  });
});