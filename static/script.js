const themeBtn = document.getElementById("theme-toggle");

if(themeBtn){

    if(localStorage.getItem("theme")==="dark"){

        document.body.classList.add("dark");
        themeBtn.innerHTML="☀️";

    }

    themeBtn.onclick=function(){

        document.body.classList.toggle("dark");

        if(document.body.classList.contains("dark")){

            localStorage.setItem("theme","dark");
            themeBtn.innerHTML="☀️";

        }

        else{

            localStorage.setItem("theme","light");
            themeBtn.innerHTML="🌙";

        }

    }

}

const dropArea=document.querySelector(".drop-area");
const input=document.querySelector("input[type='file']");

if(dropArea && input){

dropArea.addEventListener("dragover",(e)=>{

e.preventDefault();
dropArea.style.background="#efe8ff";

});

dropArea.addEventListener("dragleave",()=>{

dropArea.style.background="";

});

dropArea.addEventListener("drop",(e)=>{

e.preventDefault();

input.files=e.dataTransfer.files;

dropArea.style.background="";

if(input.files.length>0){

dropArea.querySelector("p").innerHTML=input.files[0].name;

}

});

input.addEventListener("change",()=>{

if(input.files.length>0){

dropArea.querySelector("p").innerHTML=input.files[0].name;

}

});

}