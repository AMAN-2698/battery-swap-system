function validateForm() {
  const inputs = document.querySelectorAll("input[required]");
  for (let input of inputs) {
    if (input.value.trim() === "") {
      alert("All fields are required!");
      return false;
    }
  }
  return true;
}

document.addEventListener("DOMContentLoaded", () => {
  const search = document.getElementById("search");
  if (search) {
    search.addEventListener("input", () => {
      const filter = search.value.toLowerCase();
      document.querySelectorAll("table tr").forEach((row, i) => {
        if (i === 0) return;
        row.style.display = row.innerText.toLowerCase().includes(filter) ? "" : "none";
      });
    });
  }
});
