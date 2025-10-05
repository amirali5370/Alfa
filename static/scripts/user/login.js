const starsContainer = document.getElementById('stars');
const divElement=document.querySelector('#content')
let width = divElement.offsetWidth;
let height = divElement.offsetHeight;
const numberOfStars = Math.ceil(width*height/2500);
for (let i = 0; i < numberOfStars; i++) {
  const star = document.createElement('div');
  star.classList.add('star');
  star.style.top = `${Math.random() * height}px`;
  star.style.left = `${Math.random() * (width-10)}px`;
  star.style.animationDelay = `${Math.random() * 2}s`;
  starsContainer.appendChild(star);
}