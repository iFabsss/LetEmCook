$(document).ready(function () {
    $("#create-recipe-btn").click(function () {
        $("#recipe-form-container").toggleClass("visible");
    });

    $("#recipe-form-container").click(function (e) {
        if (e.target.id === "recipe-form-container") {
            $("#recipe-form-container").removeClass("visible");
            $("#recipe-form")[0].reset();
        }
    }
    );

    $(".recipe-container").click(function (e) {
        const href = $(this).data("href");
        if (href) {
            window.location.href = href;
        }
    });

    $("#logout-btn").click(function () {
        if (confirm("Are you sure you want to logout?")) {
            $.ajax({
                url: "/logout",
                type: "POST",
                data: {
                    csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
                },
                success: function () {
                    location.href = "/";
                },
                error: function () {
                    alert("Something went wrong while deleting the comment.");
                }
            })
        }
    });

    window.deleteComment = function (commentId) {
        if (confirm("Are you sure you want to delete your comment?")) {
            $.ajax({
                url: "/deleteComment/" + commentId,
                type: "POST",
                data: {
                    csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
                },
                success: function () {
                    location.reload();
                },
                error: function () {
                    alert("Something went wrong while deleting the comment.");
                }
            })
        }
    }

    window.deleteRecipe = function (recipeId) {
        if (confirm("Are you sure you want to delete this recipe?")) {
            $.ajax({
                url: "/deleteRecipe/" + recipeId,
                type: "POST",
                data: {
                    csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
                },
                success: function () {
                    // Check if the previous page was home
                    if (document.referrer.endsWith("/home")) {
                        location.href = document.referrer; // This reloads the home page
                    } else {
                        window.history.back(); // Go back to the previous page
                    }
                },
                error: function () {
                    alert("Error deleting recipe.");
                }
            });
        }
    }

    window.generateDescription = function () {
        const title = $("input[name='title']").val();
        const ingredients = $("input[name='ingredients']").val();

        if (!title || !ingredients) {
            alert("Please enter both title and ingredients first.");
            return;
        }

        $.ajax({
            url: "generateDescription",
            type: "POST",
            data: {
                title: title,
                ingredients: ingredients,
                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
            },
            success: function (response) {
                if (response.description) {
                    $("textarea[name='description']").val(response.description);
                } else {
                    alert("Failed to generate description.");
                }
            },
            error: function () {
                alert("Error occurred while generating description.");
            }
        });
    };

    window.generateTags = function () {
        const title = $("input[name='title']").val();
        const ingredients = $("input[name='ingredients']").val();
        const description = $("textarea[name='description']").val();
        if (!title || !ingredients || !description) {
            alert("Please enter title, ingredients, and description first.");
            return;
        }

        $.ajax({
            url: "generateTags",
            type: "POST",
            data: {
                title: title,
                ingredients: ingredients,
                description: description,
                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
            },
            success: function (response) {
                if (response.tags) {
                    $("input[name='tags']").val(response.tags);
                } else {
                    alert("Failed to generate tags.");
                }
            },
            error: function () {
                alert("Error occurred while generating tags.");
            }
        });

    }



});
