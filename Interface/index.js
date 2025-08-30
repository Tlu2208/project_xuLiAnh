document.querySelectorAll(".button").forEach(item =>{
    item.addEventListener("click", lightBackground);
});

function rgbToHex(rgb) {
    const rgbArray = rgb.match(/\d+/g).map(Number);
    return "#" + rgbArray.slice(0, 3).map(x => x.toString(16).padStart(2, '0')).join('');
}

function lightBackground()
{
    //lay class container va mau nen cua container
    const container = document.querySelector(".container");
    const background = window.getComputedStyle(container).backgroundColor;

    //lay class cua button va icon
    const button = document.querySelectorAll(".button");
    const moon = document.querySelectorAll(".moon");
    const sun = document.querySelectorAll(".sun");

    //lay class va doi mau logo
    const logo = document.querySelector(".logo");

    const navbar = document.querySelector(".navbar");
    navbar.style.color = "black";
    const menu = document.querySelector(".menu");
    if(rgbToHex(background) === "#f2f9fe")
    {
        container.style.backgroundColor = "#111729";

        button.forEach(item => {
            item.style.backgroundColor = "#223344";
        });
        
        moon.forEach(item =>{
            item.style.backgroundColor = "rgb(255, 255, 255)";
            item.innerHTML = '<img src ="img/Moon_fill.svg">';
        });

        sun.forEach(item =>{
            item.style.background = "#111729";
            item.style.color = "rgb(255, 255, 255)";
        })

        logo.innerHTML = '<img src="img/logo-dark.svg">';

        container.style.color = "rgb(255, 255, 255)";

        menu.innerHTML = '<img src ="img/menu_24dp_FFFFFF_FILL0_wght400_GRAD0_opsz24.svg">';
    }

    else{
        container.style.background = "#f2f9fe";

        button.forEach(item => {
            item.style.backgroundColor = "#111729";
        });
        
        moon.forEach(item =>{
            item.style.backgroundColor = "#111729";
            item.innerHTML = '<img src ="img/Moon_fill_light.svg">';
        });

         sun.forEach(item =>{
            item.style.background = "rgb(255, 255, 255)";
            item.style.color = "#111729";
        })

        logo.innerHTML = '<img src="img/logo-light.svg">';

        container.style.color = "#000";

         menu.innerHTML = '<img src ="img/menu_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg">';
    }

}


//menu
function shownavbar() {
    const navbar = document.getElementsByClassName("navbar")[0];
    navbar.style.display = "flex";
}

function closeNavbar() {
    const navbar = document.getElementsByClassName("navbar")[0];
    navbar.style.display = "none";
}

document.getElementsByClassName("menu")[0].addEventListener("click", shownavbar);

document.querySelector(".close img").addEventListener("click", closeNavbar);


const fileInput = document.getElementById('fileInput');
const btnChoose = document.querySelector(".choice-img");
const showBox = document.querySelector(".show-img");

btnChoose.addEventListener('click', () => fileInput.click())

fileInput.addEventListener('change', () => {
    const file = fileInput.files && fileInput.files[0];
    if(!file) return;
    const url = URL.createObjectURL(file);
    showBox.innerHTML = `<img src="${url}" alt="preview" style="max-width:100%;height:auto;display:block;">`;
});


