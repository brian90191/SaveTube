
function showModal(title, link)
    {
       link = link.replace("watch?v=","embed/");

        $("#youtubeModal").on('shown.bs.modal', function (e) {
            $("#youtubeModal .modal-title").html(title)
            $("#yt-player > iframe").attr('src', link);
        });

       $("#youtubeModal").modal();

       //close youtube on closing the modal
       $("#youtubeModal").on('hidden.bs.modal', function (e) {
            $("#youtubeModal .modal-title").html('');
            $("#yt-player > iframe").attr('src', '');
        });
    }

$(document).ready(function(){
    //footer_refresh();
    //$(window).resize(function() {
    //    footer_refresh();
    //});

     /*$(".dropdown").hover(
        function() {
            $('.dropdown-menu', this).not('.in .dropdown-menu').stop(true,true).slideDown("400");
            $(this).toggleClass('open');
        },
        function() {
            $('.dropdown-menu', this).not('.in .dropdown-menu').stop(true,true).slideUp("400");
            $(this).toggleClass('open');
        }
    );
*/


    $('[data-toggle="tooltip"]').tooltip();

    //to-top scroll button
    var scrollTop = $(window).scrollTop();
    if (scrollTop > 0){
        $('#to-top').show();
    }else{
        $('#to-top').hide();
    }
    $('#to-top').bind('click', function()
	{
		$('body,html').animate({
			scrollTop: 0},
			2500);
	});

    //Dialog mask when opening dialog (start)
    $('.DialogMask').hide();
    $('.dropdown').on('show.bs.dropdown', function () {
      $('.collapse').collapse('hide');
      $('.DialogMask').show();
    })

    $('.dropdown').on('hide.bs.dropdown', function () {
      $('.DialogMask').hide();
    })

    $('.collapse').on('show.bs.collapse', function () {
        //$(".dropdown").dropdown("toggle");
        $('.DialogMask').show();
    })

    $('.collapse').on('hide.bs.collapse', function () {
        $('.DialogMask').hide();
    })

    //close collapse when clicking outside of header
    $('.DialogMask').click(function(e) {
        $('.collapse').collapse('hide');
    });
    //Dialog mask when opening dialog (end)


    //login dialog
    $('#login-form-link > div').click(function(e) {
    	$("#login-form").delay(100).fadeIn(100);
 		$("#register-form").fadeOut(100);
		$('#register-form-link > div').removeClass('active-tab');
		$(this).addClass('active-tab');
		e.preventDefault();
	});
	$('#register-form-link > div').click(function(e) {
		$("#register-form").delay(100).fadeIn(100);
 		$("#login-form").fadeOut(100);
		$('#login-form-link > div').removeClass('active-tab');
		$(this).addClass('active-tab');
		e.preventDefault();
	});

	$('.dropdown-menu').click(function(e) {
		e.stopPropagation();
	});


    //favorite tag filter
    $('.favorite_tags > button').click(function(){
        $(this).toggleClass('active');
        var btn_tag = $(this).text();
        if($(this).hasClass('active')){
            $(".video-card[tag='"+btn_tag+"']").show();
        }
        else{
            $(".video-card[tag='"+btn_tag+"']").hide();
        }
    })

    //more videos button
    $('.lazyLoading').click(function(){
        var post_url = $('.lazyLoading').attr('postVal');
        $.ajax({
            url: post_url,
            //data: $('form').serialize(),
            type: 'POST',
            beforeSend: function (xhr) {
                $('.lazyLoading > img').show();
            },
            success: function(response) {
                var video_obj = $($.parseHTML(response)).find('.video-card');
                $(video_obj).appendTo('.result').addClass('video_animate');

                 var next_url = $($.parseHTML(response)).find('.lazyLoading').attr('postVal');
                $('.lazyLoading').attr('postVal', next_url);

                $('.lazyLoading > img').hide();
            },
            error: function(error) {
                alert(error);
            }
        });
    })

//    //Infinite Scrolling
//	var win = $(window);
//	// Each time the user scrolls
//	win.scroll(function() {
//		// End of the document reached?
//		if(win.scrollTop() + win.height() > $(document).height()-1) {
//            var current_page = parseInt($('#loading').attr("page"));  //to next page
//            var page_link = $('#loading').attr("page_link");
//            $("#loading[page='"+ current_page +"']").show();
//
//            var sp = getParameterByName("sp", page_link);
//            var q = getParameterByName("q", page_link);
//
//			$.ajax({
//			    type : "POST",
//				url : "/load_ajax",
//				data : {"current_page": current_page, "sp": sp, "q": q},
//				contentType: 'application/json;charset=UTF-8',
//				success: function(result) {
//					//$('#posts').append(result);
//					$("#loading[page='"+ current_page +"']").hide();
//
//                    current_page = current_page +1;
//
//					//$('#loading').attr("page",current_page);
//					//$('#loading').attr("page_link", "{{all_page.get('{}'.format("+ current_page +"))}}");
//				}
//			});
//		}
//	});
})


$(window).scroll(function (event) {
    var scrollTop = $(window).scrollTop();
    if (scrollTop > 0){
        $('#to-top').show();
    }else{
        $('#to-top').hide();
    }
});

function footer_refresh(){
    $('#footer').css(
        'margin-top',
        $(document).height() - $('#header').height() - $('#content').height() - $('#footer').height() - 67
    );
}

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}
