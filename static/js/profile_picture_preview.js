function selectPicture(pic) {
    document.getElementById('profile-picture-preview').src = "/static/img/" + pic;
    document.querySelector('input[name="profile_picture"][value="' + pic + '"]').checked = true;
  }
  