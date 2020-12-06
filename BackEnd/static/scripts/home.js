function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        
        reader.onload = function(e) {
          $('#actualImage').attr('src', e.target.result);
        }
        
        reader.readAsDataURL(input.files[0]); // convert to base64 string

        //Used to hide background are for uploading image
        //Makes the uploaded picture visible
        var element = document.getElementById('uploadedImage');
        element.style.display = 'none'
        element = document.getElementById('actualImage')
        element.style.display = 'flex'
        element = document.getElementById('pictureText')
        element.style.display = 'none'
        element = document.getElementById('pictureBox')
        element.style.backgroundColor = 'white'
    }
}    

$("#uploadImage").change(function() {
    readURL(this);
  });