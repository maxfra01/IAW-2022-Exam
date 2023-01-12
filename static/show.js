"use strict";

//Modale nuovo commento
const newCommentModal = document.getElementById('new-comment-modal');
newCommentModal.addEventListener('show.bs.modal', event => {
  
  const button = event.relatedTarget;
  const episodeId = button.getAttribute('data-bs-episodeid');
  const episodeTitle=button.getAttribute('data-bs-episodetitle');
  const showId=button.getAttribute('data-bs-showid');
  const form=document.getElementById('new-comment-form');
  const episodeName =document.getElementById('episode-field-new');
  episodeName.value=episodeTitle;
  form.action= "/new-comment/" +showId + "_" + episodeId;
})

//modale per modifica commento
const editCommentModal = document.getElementById('edit-comment-modal');
editCommentModal.addEventListener('show.bs.modal', event => {
  
  const button = event.relatedTarget;
  const episodeTitle=button.getAttribute('data-bs-edit-comment-episodetitle');
  const commentId=button.getAttribute('data-bs-commentid');
  const oldText=button.getAttribute('data-bs-commenttext');
  const showId=button.getAttribute('data-bs-showid');
  const form=document.getElementById('edit-comment-form');
  const episodeName=document.getElementById('episode-field-edit');
  const textArea=document.getElementById('old-comment-text');
  textArea.value=oldText;
  episodeName.value=episodeTitle;
  form.action= "/edit-comment/"+ showId +"_" + commentId;
})

//Modale conferma eliminazione commento
const confirmDeleteCommentModal = document.getElementById('delete-comment-modal');
confirmDeleteCommentModal.addEventListener('show.bs.modal', event => {
  
  const button = event.relatedTarget;
  const commentId = button.getAttribute('data-bs-delete-commentid');
  const showId = button.getAttribute('data-bs-showid');
  const form= document.getElementById('delete-comment-form');
  form.action= "/delete-comment/" + showId+ "_" +commentId ;
})

//modale modifica episodio
const editEpisodeModal = document.getElementById('edit-episode-modal');
editEpisodeModal.addEventListener('show.bs.modal', event => {
  
  const button = event.relatedTarget;

  const episodeTitle = button.getAttribute('data-bs-edit-episodetitle');
  const episodeId = button.getAttribute('data-bs-edit-episodeid');
  const episodeDate = button.getAttribute('data-bs-edit-date')
  const episodeDescription = button.getAttribute('data-bs-edit-description')
  const showId = button.getAttribute('data-bs-showid');

  const form= document.getElementById('edit-episode-form');
  const titolo=document.getElementById('title-input')
  titolo.value=episodeTitle

  const descrizione=document.getElementById('description-input')
  descrizione.value=episodeDescription

  const data=document.getElementById('date-input')
  data.value=episodeDate
  
  form.action= "/edit-episode/"+ showId + "_" + episodeId;
})

//modale conferma eliminazione epiosodio
const confirmDeleteEpisodeModal = document.getElementById('delete-episode-modal');
confirmDeleteEpisodeModal.addEventListener('show.bs.modal', event => {
  
  const button = event.relatedTarget;
  const episodeId = button.getAttribute('data-bs-del-episode-id');
  const showId = button.getAttribute('data-bs-showid');
  const form= document.getElementById('delete-episode-form');
  form.action= "/delete-episode/" + showId+ "_" +episodeId ;
})

//TOGLI CATEGORIA
const cat=document.getElementById('cat-dropdown')
cat.style.display= 'none'

//BARRA DI RICERCA
const searchButton=document.getElementById('search-button')
const searchBar=document.getElementById('search-bar')
searchBar.removeAttribute('hidden')
searchButton.removeAttribute('hidden')
searchButton.addEventListener('click', event => {
  const key= searchBar.value
  console.log('RICERCA DI '+key)
  
  const episodes= document.querySelectorAll('.episode-container')
  for (let i = 0; i < episodes.length; i++) {
    const element = array[i];
    
    
  }
})