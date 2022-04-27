const dictionary = {
    'main': 'home',
    'me': 'about', 
    'proj': 'projects', 
    'res': 'resume', 
    'talk': 'contact'
}

$(document).ready(function() {

    $(document).on('scroll', function(event) {
        var scrollPosition = $(document).scrollTop();
        var lastID = 'main';
        
        $('#menu a').each(function() {

            var currentLink = $(this)[0].id;
            var id = dictionary[currentLink];
            var idPosition = $("#"+id).offset().top - 60;

            if (scrollPosition >= idPosition) {
                lastID = currentLink;
            }
        });

        changeText(lastID)
    });

    // change underline when new menu link is clicked
    $('#menu a').on('click', function(event) {
         event.preventDefault();
         // changeText(event.target.id);
         myScroll(event.target.id);

        // hides menu after link has been clicked
         var label = $('.hide-menu-btn');
         var label_id = $(label).attr('for');
         $('#'+label_id).trigger('click');

         return false;
    });


    $('#send').on('click', function() {
        var name = $('.input-name').val();
        var email = $('.input-email').val();
        var message = $('.input-message').val()
        var name_check, email_check, message_check = 0;

        // hide error messages
        $('#name').addClass('sent');
        $('#email').addClass('sent');
        $('#message').addClass('sent');

        // checks that all input fields are filled
        if (name.length == 0) {
           $('.input-name').css('border-color', 'red');
           name_check = 1;
        }
        else {
           $('.input-name').css('border-color', '#888');
           name_check = 0;
        }

        if (email.length == 0 || !email.match('@')) {
           $('.input-email').css('border-color', 'red');
           email_check = 1;
        }
        else {
           $('.input-email').css('border-color', '#888');
           email_check = 0;
        }

        if (message.length == 0) {
           $('.input-message').css('border-color', 'red');
           message_check = 1;
        }
        else {
           $('.input-message').css('border-color', '#888');
           message_check = 0;
        }


        if (name_check) {
           $('#name').removeClass('sent');
           return;
        }

        else if (email_check) {
           $('#email').removeClass('sent');
           return;
        }

        else if (message_check) {
           $('#message').removeClass('sent');
        }

        else {

           // hide error messages
           $('#name').addClass('sent');
           $('#email').addClass('sent');
           $('#message').addClass('sent');
        
           $.ajax({
              type: 'POST',
              data: {name, email, message},
              url: '/send_email',
              success: function(response) {

                 if (response === 'OK') {
                    // remove error response
                    $('#error').addClass('sent');

                    $('#alert').removeClass('sent');
                 }
                 else {
                    // remove success response
                    $('#alert').addClass('sent');

                    $('#error').removeClass('sent');
                 }
              },
           });
        }
        
        return false;
     });
});

function changeText(target) {
    const ids = ['main', 'me', 'proj', 'res', 'talk'];

    for (let i = 0; i < ids.length; i++) {
        id = ids[i];

        var link = document.getElementById(id);

        if (target === id) {
            $(link).addClass('active');
        }
        else {
            $(link).removeClass('active');
        }
    }

    return false;
}

function myScroll(id) {
    var target = dictionary[id];
    $('html,body').animate({scrollTop: $("#"+target).offset().top-50},'slow');

    return false;
}
