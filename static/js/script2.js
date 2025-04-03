window.addEventListener("DOMContentLoaded", () => {
  const flashData = JSON.parse(document.getElementById("flash-data").textContent);
  
  flashData.forEach(([category, message]) => {
      alert(message); 
  });
});

function toggleDropdown() {
  const dropdown = document.getElementById("myDropdown");
  dropdown.classList.toggle("show");
}