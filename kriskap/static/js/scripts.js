function selectImage() {
  const image_f = document.getElementById("image_f");
  const file_container = document.getElementById("file_container");
  const image_view = file_container.querySelector(".image_view");

  image_f.addEventListener("change", function() {
      const file = this.files[0];
      if (file) {
          const reader = new FileReader();

          reader.addEventListener("load", function() {
              image_view.setAttribute("src", this.result);
          });
          reader.readAsDataURL(file);
      } else {
          image_view.setAttribute("src", "static/img/product_pics/default.png");
      }
  });
}
function validateForms() {
  // Example starter JavaScript for disabling form submissions if there are invalid fields
  (() => {
    'use strict'

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation')

    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
      form.addEventListener('submit', event => {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      }, false)
    })
  })()
}
