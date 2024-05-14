const menu_btn = document.getElementById('sidebarToggle');
const sidebar = document.getElementById('sidebar');

menu_btn.addEventListener('click',function()  {
    if (sidebar.style.transform === "translateX(-300px)") {
        sidebar.style.transform = "translateX(0px)";
        menu_btn.style.transform = "rotate(90deg)";
    } 
    else if(sidebar.style.transform === "translateX(0px)"){
        sidebar.style.transform = "translateX(-300px)"
        menu_btn.style.transform = "rotate(0deg)"
    }
    else {
        sidebar.style.transform = "translateX(0px)";
    }
});

menu_btn.addEventListener('mouseover',function()  {
    if (sidebar.style.transform === "translateX(-300px)") {
        sidebar.style.transform = "translateX(0px)";
        menu_btn.style.transform = "rotate(90deg)";
    } 
    else if(sidebar.style.transform === "translateX(0px)"){
        sidebar.style.transform = "translateX(-300px)"
        menu_btn.style.transform = "rotate(0deg)";
    }
    else {
        sidebar.style.transform = "translateX(0px)";
    }
});





const profile = document.getElementById('profile');
const profile_menu = document.querySelector('.profile_menu');

profile.addEventListener('click',function(){
    if(profile_menu.style.right === "-160px"){
        profile_menu.style.right = "30px";
    }
    else {
        profile_menu.style.right = "-160px";
    }
});

profile.addEventListener('mouseover',function(){
    if(profile_menu.style.right === "-160px"){
        profile_menu.style.right = "30px";
    }
    else {
        profile_menu.style.right = "-160px";
    }
});


const profile_btn = document.getElementById('profile_btn');
profile_btn.addEventListener('click',function(){
    window.location.href = "Profile.html";
})







const Upgrade_btn = document.getElementById('Upgrade_btn');
const upgrade_menu = document.getElementById('upgrade_monthly');
const close_btn = document.getElementById('upgrade_close_btn');
const body = document.querySelector('body');

Upgrade_btn.addEventListener('click',function(){
    upgrade_menu.style.display = "block";
    body.style.backgroundColor = "";
});

close_btn.addEventListener('click',function(){
    upgrade_menu.style.display = "none";
});




const plan_btns = document.querySelectorAll('.plan_btn');
const Monthly_plan = document.getElementById('Monthly_plan');
const Yearly_plan = document.getElementById('Yearly_plan'); 
const monthly_info = document.getElementById('priceInfo');
const price_tag = document.getElementById('price_tag');
const time_p = document.getElementById('time_p');
const elements = document.querySelectorAll('.upgrade_main > .plans> button');


plan_btns.forEach(function(plan_btn) { 
    plan_btn.addEventListener('click', function() { 
       elements.style.Color = "#F65434";   
    });
});

Monthly_plan.addEventListener('click',function(){
    price_tag.textContent = "5";
    time_p.textContent = "per month";
});

Yearly_plan.addEventListener('click',function(){
    price_tag.textContent = "60";
    time_p.textContent = "annually, billed $5 per month";
});





