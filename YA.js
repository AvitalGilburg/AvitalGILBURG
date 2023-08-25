const yamenu = document.querySelector(".yamenu");
const navMenu = document.querySelector(".nav-menu");

yamenu.addEventListener("click", () => {yamenu.classList.toggle("active"); navMenu.classList.toggle("active");})
document.querySelector(".nav-link").forEach(n => n.addEventListener("click", () => {yamenu.classList.remove("active");navMenu.classList.remove("active");}))

if yamenu:
	window.open(