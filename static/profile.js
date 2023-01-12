"use strict";

//Modale conferma eliminazione serie
const confirmDeleteModal = document.getElementById('delete-show-modal');
confirmDeleteModal.addEventListener('show.bs.modal', event => {
  
  const button = event.relatedTarget;
  
  const showId = button.getAttribute('data-bs-showid');
  const form= document.getElementById('delete-show-form');
  form.action= "/delete-show/" + showId;
})

//TOGLI CATEGORIA
const cat=document.getElementById('cat-dropdown')
cat.style.display= 'none'
