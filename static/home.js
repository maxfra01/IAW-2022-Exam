"use strict";

const cat= document.getElementById('js-active-category')
console.log(cat.innerText)
const catLabel=document.getElementById('js-category-'+ cat.innerText)
catLabel.classList.add('fw-bold')