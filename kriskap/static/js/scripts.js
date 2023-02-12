// Preview Image Section Account and Section - Create/Edit Product
function selectImage() {
  const image_f = document.getElementById("image_f");
  const file_container = document.getElementById("file_container");
  const image_view = file_container.querySelector(".image_view");

  image_f.addEventListener("change", function () {
    const file = this.files[0];
    if (file) {
      const reader = new FileReader();

      reader.addEventListener("load", function () {
        image_view.setAttribute("src", this.result);
      });
      reader.readAsDataURL(file);
    } else {
      image_view.setAttribute("src", "static/img/product_pics/default.png");
    }
  });
}

// Section Cart - Increase and Decrease Items on Cart
$(document).ready(function () {
  $(".quantityChange").on("change", function () {
    var cart_id = $(this).attr("cart_id");
    var quantity = $("#quantityChange" + cart_id).val();
    if (quantity < 1) {
      $("#quantityChange" + cart_id).val(1);
      quantity = 1;
    }
    if (quantity) {
      req = $.ajax({
        url: "/cart/update",
        type: "POST",
        data: { cart_id: cart_id, quantity: quantity },
      });
      req.done(function (data) {
        if (quantity > data.max) {
          $("#quantityChange" + cart_id).val(data.max);
          alert(
            "You have reached the maximum quantity available for this item."
          );
        }
        $("#cartNumber" + cart_id).text(data.total);
        $("#cartTotal").text(data.cart_total);
        $("#cart_subtotal").text(data.cart_subtotal);
      });
    }
  });
});

// Section View Product - Increase and Decrease Item on Quantity Field
$(document).ready(function () {
  $("#quantity").on("change", function () {
    var quantity = $("#quantity").val();
    var product_id = $("#productId").val();
    if (quantity < 1) {
      $("#quantity").val(1);
      quantity = 1;
    }
    req = $.ajax({
      url: "/cart/check-stock",
      type: "POST",
      data: { quantity: quantity, product_id: product_id },
    });
    req.done(function (data) {
      if (quantity > data.available_stock) {
        $("#quantity").val(data.available_stock);
        alert("You have reached the maximum quantity available for this item.");
      }
    });
  });
});

// Section Address - Search Cities
$(document).ready(function () {
  $("#province").on("click", function () {
    $("#submit").attr("disabled", true);
    var city = $("#city");
    city.empty();
    city.prop("disabled", true);
    var barangay = $("#barangay");
    barangay.empty();
    barangay.prop("disabled", true);
    var province_code = $("#province").val();
    req = $.ajax({
      url: "/address/search-city",
      type: "POST",
      data: { province_code: province_code },
    });
    req.done(function (data) {
      city.empty();
      for (var i = 0; i < data.cities.length; i++) {
        city.append(
          "<option value=" +
            data.cities[i][0] +
            ">" +
            data.cities[i][1] +
            "</option>"
        );
      }
      city.prop("disabled", false);
    });
  });
});

// Section Address - Search Barangay
$(document).ready(function () {
  $("#city").on("click", function () {
    var city_code = $("#city").val();
    req = $.ajax({
      url: "/address/search-barangay",
      type: "POST",
      data: { city_code: city_code },
    });
    req.done(function (data) {
      var barangay = $("#barangay");
      barangay.empty();
      for (var i = 0; i < data.barangays.length; i++) {
        barangay.append(
          "<option value=" +
            data.barangays[i][0] +
            ">" +
            data.barangays[i][1] +
            "</option>"
        );
      }
      barangay.prop("disabled", false);
    });
  });
});

// Section Address - Submit Button
$(document).ready(function () {
  $("#barangay").on("click", function () {
    $("#submit").attr("disabled", false);
  });
});

// Section Address - Submit Button
$(document).ready(function () {
  $("#province-duplicate").on("click", function () {
    $("#province").attr("hidden", false);
    $("#province-duplicate").attr("hidden", true);
  });
});

// Section Address - Submit Button
$(document).ready(function () {
  $("#house").blur(function () {
    if (!$(this).val()) {
      $("#province").attr("hidden", true);
      $("#city").attr("disabled", true);
      $("#barangay").attr("disabled", true);
      $("#city").empty();
      $("#barangay").empty();
      $("#province-duplicate").attr("hidden", false);
      $("#submit").attr("disabled", true);
    } else {
      $("#province").attr("hidden", false);
      $("#province-duplicate").attr("hidden", true);
    }
  });
});
