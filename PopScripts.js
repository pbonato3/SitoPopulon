 
var selectedRazza = document.getElementById('SelRazza'); 
 
selectedRazza.addEventListener('change', function() { 
  document.getElementById('immagineRazza').src = selezionaImg(this.value); 
}); 
 
function selezionaimg(razza){ 
  return "img/"+razza+".jpg" 
} 
