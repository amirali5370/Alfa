const side_bar = document.querySelector("#side");
function open_side(){
    side_bar.classList.add("open")
}
function close_side(){
    side_bar.classList.remove("open")
}

svg = document.querySelector("#x_side")
svg.addEventListener('click', () => {
  close_side()
});