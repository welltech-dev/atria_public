/* scroll reveal */

const reveals = document.querySelectorAll(".reveal");

function revealOnScroll(){

const windowHeight = window.innerHeight;

reveals.forEach(element => {

const elementTop = element.getBoundingClientRect().top;

if(elementTop < windowHeight - 120){

element.classList.add("active");

}

});

}

window.addEventListener("scroll", revealOnScroll);



/* scroll suave */

document.querySelectorAll("a[href^='#']").forEach(anchor => {

anchor.addEventListener("click", function(e){

e.preventDefault();

document.querySelector(this.getAttribute("href")).scrollIntoView({

behavior:"smooth"

});

});

});