"use strict";

//Modale nuovo episodio
let currentDate = dayjs();
const newEpisodeModal=document.getElementById('add-episode-modal')
newEpisodeModal.addEventListener('show.bs.modal', event => {

  const date= document.getElementById('new-episode-date-input')
  date.value=currentDate.format('YYYY-MM-DD').toString()
})


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


//BARRA DI RICERCA
const searchButton=document.getElementById('search-button')
const searchBar=document.getElementById('search-bar')
searchButton.addEventListener('click', event => {
  const key= searchBar.value
  console.log('RICERCA DI '+key)
  
  const episodeTitles= document.querySelectorAll('#js-episode-title')
  const episodeDescriptions= document.querySelectorAll('#js-episode-description')

  for (let i = 0; i < episodeTitles.length; i++) {
    console.log(episodeDescriptions[i].innerHTML)
    console.log(episodeTitles[i].innerHTML)
    let match=0;
    if (episodeTitles[i].innerHTML.toLowerCase().includes(key.toLowerCase())){
      match=1;
    }
    if (episodeDescriptions[i].innerHTML.toLowerCase().includes(key.toLowerCase())){
      match=1;
    }

    if (!match){
      episodeTitles[i].parentElement.classList.add('visually-hidden')
    }
    else{
      episodeTitles[i].parentElement.classList.remove('visually-hidden')
    }
  }
})