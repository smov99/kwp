!(function($) {
  "use strict";

  // Get CSRF
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  const csrftoken = getCookie('csrftoken')

  // Ajax request
  function eventsAjax(event_type, event_name, time_spent, message) {
    var events_path = window.location.href.replace('proposal/', 'events/')
    $.ajax({
      headers: {"X-CSRFToken": csrftoken},
      url: events_path,
      method: "POST",
      data: {"event_type":event_type, "event_name":event_name, "time_spent": time_spent, "message":message},
      dataType: "json"
    });

  }

  // Process bar
  $(window).scroll(function() {
    let docElem = document.documentElement,
        docBody = document.body,
        scrollTop = docElem['scrollTop'] || docBody['scrollTop'],
        scrollBottom = (docElem['scrollHeight'] || docBody['scrollHeight']) - window.innerHeight,
        scrollPercent = scrollTop / scrollBottom * 100 + '%';

    document.getElementById('progress-bar').style.setProperty('--scrollAmount', scrollPercent);
  });

  // Smooth scroll for the navigation menu and links with .scrollto classes
  var scrolltoOffset = $('#header').outerHeight() - 5;
  $(document).on('click', '.nav-menu a, .mobile-nav a, .scrollto', function(e) {
    if (location.pathname.replace(/^\//, '') === this.pathname.replace(/^\//, '') && location.hostname === this.hostname) {
      var target = $(this.hash);
      if (target.length) {
        e.preventDefault();

        var scrollto = target.offset().top - scrolltoOffset;

        $('html, body').animate({
          scrollTop: scrollto
        }, 1500, 'easeInOutExpo');

        return false;
      }
    }
  });

  // Activate smooth scroll on page load with hash links in the url
  $(document).ready(function() {
    if (window.location.hash) {
      var initial_nav = window.location.hash;
      if ($(initial_nav).length) {
        var scrollto = $(initial_nav).offset().top - scrolltoOffset;
        $('html, body').animate({
          scrollTop: scrollto
        }, 1500, 'easeInOutExpo');
      }
    }
  });

  // Navigation active state on scroll
  var nav_sections = $('section');
  var main_nav = $('.nav-menu, .mobile-nav');

  $(window).on('scroll', function() {
    var cur_pos = $(this).scrollTop() + 400;

    nav_sections.each(function() {
      var top = $(this).offset().top,
        bottom = top + $(this).outerHeight();

      if (cur_pos >= top && cur_pos <= bottom) {
        if (cur_pos <= bottom) {
          main_nav.find('li').removeClass('active');
        }
        main_nav.find('a[href="#' + $(this).attr('id') + '"]').parent('li').addClass('active');
      }
      if (cur_pos < 300) {
        $(".nav-menu ul:first li:first, .mobile-menu ul:first li:first").addClass('active');
      }
    });
  });

  // Mobile Navigation
  if ($('.nav-menu').length) {
    var $mobile_nav = $('.nav-menu').clone().prop({
      class: 'mobile-nav d-none'
    });
    $('body').append($mobile_nav);
    $('body').prepend('<button type="button" class="mobile-nav-toggle d-lg-none collapsed" data-toggle="collapse" data-target="#mobile-nav"><i class="far fa-bars"></i></button>');

    $(document).on('click', '.mobile-nav-toggle', function(e) {
      $('body').toggleClass('mobile-nav-active');
      $('.mobile-nav-toggle i').toggleClass('fa-bars fa-times');
    });

    $("#mobile-nav").on('show.bs.collapse', function() {
        $('a.nav-link').click(function() {
            $('.mobile-nav-toggle i').toggleClass('fa-bars fa-times');
            $("#mobile-nav").collapse('hide');
        });
    });

   $(document).click(function (event) {
     var clickover = $(event.target);
     var _opened = $(".navbar-collapse").hasClass("show");
     if (_opened === true && !clickover.hasClass("mobile-nav-toggle")) {
       $(".mobile-nav-toggle").click();
     }
   });

  } else if ($(".mobile-nav, .mobile-nav-toggle").length) {
    $(".mobile-nav, .mobile-nav-toggle").hide();
  }

  // Toggle .header-scrolled class to #header when page is scrolled
  $(window).scroll(function() {
    if ($(window).width() > 992) {
      if ($(this).scrollTop() > 100) {
        $('#header').addClass('header-scrolled');
      } else {
        $('#header').removeClass('header-scrolled');
      }}
  });

  // Init AOS
  function aos_init() {
    AOS.init({
      duration: 1000,
      once: true
    });
  }
  $(window).on('load', function() {
    aos_init();
  });

  //PDF preview and events
  $("#proposal-pdf-link").click(function (e) {
    var pdf_url = window.location.href + 'pdf',
      modal_width = screen.width,
      modal_height = screen.height,
      pdfWindow;
    e.preventDefault();

    eventsAjax('open_pdf', 'Open PDF document');
    eventsAjax('page_opened', 'Opened page number: 1');

    if ($(window).width()) {
      pdfWindow = window.open(pdf_url,"", 'width='+modal_width+',height='+modal_height);}

    $(pdfWindow).on('load', function () {
      var downloadBtn = this.document.getElementById('proposal-download-btn'),
        timeTracker = {},
        iframe = this.document.getElementById('pdf-iframe').contentWindow;
    $(iframe).ready(function (){
      $(iframe).scroll(function() {
        let docElem = iframe.document.documentElement,
            docBody = iframe.document.body,
            scrollTop = docElem['scrollTop'] || docBody['scrollTop'],
            scrollBottom = (docElem['scrollHeight'] || docBody['scrollHeight']) - iframe.innerHeight,
            scrollPercent = scrollTop / scrollBottom * 100 + '%';

        document.getElementById('progress-bar').style.setProperty('--scrollAmount', scrollPercent);
      });
    })

    timeTracker['pageStart'] = new Date();

    // Copy tracking
    this.document.addEventListener('copy', function (e) {
        let selected_text = pdfWindow.getSelection().toString().replace("\n", ' '),
          l = selected_text.length;
        if (l > 50) {
            selected_text = selected_text.substring(0, 20) + ' ... ' + selected_text.substring(l-20, l);
        }
        eventsAjax('copying_in_pdf', 'Copied text: '+selected_text);
    });

    // Download button
    downloadBtn.href = url

    downloadBtn.addEventListener('click', () => {
      eventsAjax('download', 'PDF downloaded');
    })
    $(pdfWindow).on('unload', () => {
      eventsAjax('closing_preview', 'Closing modal preview');
    });
  });

  });

  $('#flexCheckIntro').on('click', function () {
    if ($(this).is(':checked')) {
      $('.introduction-form input[type="submit"]').removeAttr('disabled');
    } else {
      $('.introduction-form input[type="submit"]').attr('disabled', 'disabled');
    }
  });

  $('.section-title .collapsed').on('click', function (e) {
    e.preventDefault();
    eventsAjax('opening_of_section','Opening of section: '+e.target.innerText);
  });

  $('.faq-list .collapsed').on('click', function (e) {
    e.preventDefault();
    eventsAjax('opening_of_sections_line', 'Opening of line: '+e.target.innerText);
  });

  $('#contact form button').on('click', function (e) {
    e.preventDefault();
    let message = $(this).closest("form").find('textarea'),
      val = message;
    if (val.val().replace(/ /g,'').length) {
      eventsAjax('click_on_submit_button', 'Click on submit button in ' + $(this).closest("form").attr('id'), '', '' + message.val());
      message.val('')
    }
  });



})(jQuery);