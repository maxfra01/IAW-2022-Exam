"use strict";

//Modale nuovo commento
const newCommentModal = document.getElementById('new-comment-modal');
newCommentModal.addEventListener('show.bs.modal', event => {
  
  const button = event.relatedTarget;
  const episodeId = button.getAttribute('data-bs-episodeid');
  const episodeTitle=button.getAttribute('data-bs-episodetitle');
  const showId=button.getAttribute('data-bs-showid');
  const form=document.getElementById('new-comment-form');
  const episodeName =document.getElementById('episode-field');
  episodeName.value=episodeTitle;
  form.action= "/new-comment/" +showId + "_" + episodeId;
})

//modale per modifica commento
const editCommentModal = document.getElementById('edit-comment-modal');
editCommentModal.addEventListener('show.bs.modal', event => {
  
  const button = event.relatedTarget;
  const episodeTitle=button.getAttribute('data-bs-episodetitle');
  const commentId=button.getAttribute('data-bs-commentid');
  const oldText=button.getAttribute('data-bs-commenttext');
  const showId=button.getAttribute('data-bs-showid');
  const form=document.getElementById('edit-comment-form');
  const episodeName =document.getElementById('episode-field');
  const textArea=document.getElementById('old-comment-text');
  textArea.value=oldText;
  episodeName.value=episodeTitle;
  form.action= "/edit-comment/"+ showId +"_" + commentId;
})

//Modale conferma eliminazione commento
const confirmDeleteCommentModal = document.getElementById('delete-comment-modal');
confirmDeleteCommentModal.addEventListener('show.bs.modal', event => {
  
  const button = event.relatedTarget;
  const commentId = button.getAttribute('data-bs-commentid');
  const showId = button.getAttribute('data-bs-showid');
  const form= document.getElementById('delete-comment-form');
  form.action= "/delete-comment/" + showId+ "_" +commentId ;
})

//modale modifica episodio
const editEpisodeModal = document.getElementById('edit-episode-modal');
editEpisodeModal.addEventListener('show.bs.modal', event => {
  
  const button = event.relatedTarget;

  const episodeTitle = button.getAttribute('data-bs-episodetitle');
  const episodeId = button.getAttribute('data-bs-episodeid');
  const episodeDate = button.getAttribute('data-bs-date')
  const episodeDescription = button.getAttribute('data-bs-description')
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
  const episodeId = button.getAttribute('data-bs-episodeid');
  const showId = button.getAttribute('data-bs-showid');
  const form= document.getElementById('delete-episode-form');
  form.action= "/delete-episode/" + showId+ "_" +episodeId ;
})
