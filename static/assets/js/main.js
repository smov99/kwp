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

  // Ajax requests
  function eventsAjax(event_type, event_name, time_spent, message) {
    var _path = window.location.origin + '/events/';
    $.ajax({
      headers: {"X-CSRFToken": csrftoken},
      url: _path,
      method: "POST",
      data: {"event_type":event_type, "event_name":event_name, "time_spent": time_spent, "message":message},
      dataType: "json"
    });
  }

  function formAjax (email) {
    var _path = window.location.href
    $.ajax({
      headers: {"X-CSRFToken": csrftoken},
      url: _path,
      method: "POST",
      data: {'email': email},
      dataType: "json",
      error: function () {
        $('#form-error').removeClass('d-none')
      }
    });
  }

  function pdfAjax () {
    var _path = window.location.href;
    $.ajax({
      headers: {"X-CSRFToken": csrftoken},
      url: _path,
      method: "POST",
      data: {"url": _path},
      dataType: "json"
    });
  }

  // Progress bar
  $(window).scroll(function() {
    let docElem = document.documentElement,
        docBody = document.body,
        scrollTop = docElem['scrollTop'] || docBody['scrollTop'],
        scrollBottom = (docElem['scrollHeight'] || docBody['scrollHeight']) - window.innerHeight,
        scrollPercent = scrollTop / scrollBottom * 100 + '%';

    document.getElementById('progress-bar').style.setProperty('--scrollAmount', scrollPercent);
  });

  // Preloader
  $(window).on('load', function () {
    let preloader = document.getElementById('preloader');
    setTimeout(function () {
      preloader.classList.add('loaded')
    }, 1000)
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
      if ($(this).scrollTop() > 50) {
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

  //Events
  let vh = window.innerHeight * 0.01,
    vw = window.innerWidth * 0.01;

  document.documentElement.style.setProperty('--vh', `${vh}px`)
  document.documentElement.style.setProperty('--vw', `${vw}px`)

  $(window).on('resize', function () {
    vh = window.innerHeight * 0.01;
    vw = window.innerWidth * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`)
    document.documentElement.style.setProperty('--vw', `${vw}px`)
  });

  $("#proposal-pdf-link").click(function (e) {
    var pdf_url = window.location.href + 'pdf',
      modal_width = screen.width,
      modal_height = screen.height;
    e.preventDefault();

    eventsAjax('Interaction with Proposal', 'Open');

    if ($(window).width()) {
      window.open(pdf_url,"", 'width='+modal_width+',height='+modal_height);
    }
  });

  if (window.location.href.includes('proposal')) {
    if (window.location.href.includes('pdf')) {
      $(window).on('load', function () {
        $(window).on('unload', function () {
          eventsAjax('Interaction with Proposal', 'Close');
        });
      });
    } else {
      $(window).on('load', function () {
        $(window).on('unload', function () {
          pdfAjax();
        });
      });
    }
  }

  function checkCheckbox () {
    return !!$('#flexCheckIntro').is(':checked');
  }

  $(window).on('load', function () {
    var spentTime,
      valDict = {},
      endSection,
      endQuestion;

    $('.section-title .collapsed').on('click', function (e) {
      e = e || window.event;
      e.preventDefault();
      var sectionName = $(e.target).closest('h2').text();
      if ($(this).hasClass('opened')) {
        endSection = new Date().getTime();
        spentTime = (endSection - valDict[sectionName]) / 1000;
        eventsAjax('Interaction with FAQ', 'Section ' + sectionName + ' close', '' + spentTime);
        $(this).removeClass('opened');
      } else {
        valDict[sectionName] = new Date().getTime();
        eventsAjax('Interaction with FAQ', 'Section ' + sectionName + ' open');
        $(this).addClass('opened');
      }
    });

    $('.faq-list .collapsed').on('click', function (e) {
      e = e || window.event;
      e.preventDefault();
      let questionText = $(e.target).closest('a').text(),
        l = questionText.length;
      questionText = 'Question ' + questionText;
      if (l > 50) {
        questionText = questionText.substring(0, 20) + ' ... ' + questionText.substring(l - 19, l);
      }
      if ($(this).hasClass('opened')) {
        endQuestion = new Date().getTime();
        spentTime = (endQuestion - valDict[questionText]) / 1000;
        eventsAjax('Interaction with FAQ', questionText + ' close', '' + spentTime);
        $(this).removeClass('opened');
      } else {
        valDict[questionText] = new Date().getTime();
        eventsAjax('Interaction with FAQ', questionText + ' open');
        $(this).addClass('opened');
      }
    });
  });

  $('#contact form button').on('click', function (e) {
    e.preventDefault();
    let message = $(this).closest("form").find('textarea'),
      _value = message,
      sentMessage = $(this).closest('form').find('.sent-message');
    if (_value.val().replace(/ /g,'').length) {
      eventsAjax('Interaction with Message Box', 'Question submitted ' + $(this).closest("form").attr('id'), '', '' + message.val());
      message.val('');
      $(sentMessage).slideDown(250).fadeIn(100, function () {
        $(sentMessage).css({'display': 'flex'});
      });
      setTimeout(function () {
        $(sentMessage).slideUp(250, 'linear').fadeOut(100, function () {
          $(sentMessage).css({'display':'none'});
        })
      }, 4000);
    }
  });

  // Email validation
  $('#introduction form input[type="submit"]').on('click', function (e) {
    if (checkCheckbox()) {
      let email = $(this).closest("form").find('input[type="email"]').val(),
        re = /[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?/;
      if (!re.test(String(email).toLowerCase())) {
        e.preventDefault();
        formAjax(email);
      }
    } else {
      e.preventDefault();
    }
  });



})(jQuery);