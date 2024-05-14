const return_home = document.getElementById('retn_home_btn');

return_home.addEventListener('click',function(){
    window.location.href = "Home Screen.html";
});






const profile = document.getElementById('profile');
const profile_menu = document.querySelector('.profile_menu');

profile.addEventListener('click',function(){
    if(profile_menu.style.display === "none"){
        profile_menu.style.display = "block";
    }
    else {
        profile_menu.style.display = "none";
    }
});

profile.addEventListener('mouseover',function(){
    if(profile_menu.style.display === "none"){
        profile_menu.style.display = "block";
    }
    else {
        profile_menu.style.display = "none";
    }
});


const edit_btn = document.getElementById('edit_btn');
const cancel_btn = document.getElementById('Cancel_btn');
const done_btn = document.getElementById('Done_btn');

edit_btn.addEventListener('click',function(){
    edit_btn.style.display = "none";
    cancel_btn.style.display = "block";
    done_btn.style.display = "block";
});

cancel_btn.addEventListener('click',function(){
    edit_btn.style.display = "block";
    cancel_btn.style.display = "none";
    done_btn.style.display = "none";
});

done_btn.addEventListener('click',function(){
    edit_btn.style.display = "block";
    cancel_btn.style.display = "none";
    done_btn.style.display = "none";
});


