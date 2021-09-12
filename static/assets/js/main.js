!(function($) {
  "use strict";

  // Get CSRF
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
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
    var _path = window.location.href;
    $.ajax({
      headers: {"X-CSRFToken": csrftoken},
      url: _path,
      method: "POST",
      data: {'email': email},
      dataType: "json",
      error: function () {
        let emailError = $('#form-email-error');
        $(emailError).slideDown(350).fadeIn(200, function () {
          $(emailError).removeClass('d-none');
        });
        setTimeout(function () {
          $(emailError).slideUp(350, 'linear').fadeOut(200, function () {
            $(emailError).addClass('d-none');
          })
        }, 4000);
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
      preloader.classList.add('loaded');
      if (!window.location.href.includes('pdf')) {
        $(document.body).addClass('loaded');
      }
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

  $(".proposal-pdf-link").click(function (e) {
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
      endQuestion,
      section = '.section-title .collapsed',
      question = '.faq-list .collapsed';

    function closeLastSection() {
      if (valDict['lastOpenedSection']) {
        let $lstOpenedSection = $(valDict['lastOpenedSection'].replace('#', '#link-'));
        if ($lstOpenedSection.hasClass('opened')) {
          $lstOpenedSection.click();
        }
      }
    }

    function closeLastQuestion() {
      if (valDict['lastOpenedQuestion']) {
        let $lstOpenedQuestion = $(valDict['lastOpenedQuestion'].replace('#', '#link-'));
        if ($lstOpenedQuestion.hasClass('opened')) {
          $lstOpenedQuestion.click();
        }
      }
    }

    $(section).on('click', function (e) {
      e.preventDefault();
      let sectionName = $(e.target).closest('h2').text(),
        sectionId = $(this).attr('href');
      if ($(this).hasClass('opened')) {
        endSection = new Date().getTime();
        spentTime = (endSection - valDict[sectionId]) / 1000;
        eventsAjax('Interaction with FAQ', 'Section ' + sectionName + ' close', '' + spentTime);
        $(this).removeClass('opened');
      } else {
        closeLastQuestion();
        closeLastSection();
        valDict[sectionId] = new Date().getTime();
        valDict['lastOpenedSection'] = sectionId;
        eventsAjax('Interaction with FAQ', 'Section ' + sectionName + ' open');
        $(this).addClass('opened');
      }
    });

    $(question).on('click', function (e) {
      e.preventDefault();
      let questionText = $(e.target).closest('a').text(),
        l = questionText.length,
        questionId = $(this).attr('href');
      questionText = 'Question ' + questionText;
      if (l > 150) {
        questionText = questionText.substring(0, 70) + ' ... ' + questionText.substring(l - 69, l);
      }
      if ($(this).hasClass('opened')) {
        endQuestion = new Date().getTime();
        spentTime = (endQuestion - valDict[questionId]) / 1000;
        eventsAjax('Interaction with FAQ', questionText + ' close', '' + spentTime);
        $(this).removeClass('opened');
      } else {
        closeLastQuestion();
        valDict[questionId] = new Date().getTime();
        valDict['lastOpenedQuestion'] = questionId;
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
  $('.introduction-form form').on('submit', function (e) {
    if (checkCheckbox()) {
      let email = $(this).find('input[type="email"]').val(),
        re = /[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?/;
      if (!re.test(String(email).toLowerCase())) {
        e.preventDefault();
        formAjax(email);
      } else {
        $(this).find('input[type="submit"]').attr("disabled", true);
        return true;
      }
    } else {
      let checkboxError = $('#form-checkbox-error');
      $(checkboxError).slideDown(350).fadeIn(200, function () {
        $(checkboxError).removeClass('d-none');
      });
      setTimeout(function () {
        $(checkboxError).slideUp(350, 'linear').fadeOut(200, function () {
          $(checkboxError).addClass('d-none');
        })
      }, 4000);
      e.preventDefault();
    }
  });

  // Carousel
  $(document).ready(function(){
  var itemsMainDiv = ('.rescarousel');
  var itemsDiv = ('.rescarousel-inner');
  var itemWidth = "";
    $('.leftLst, .rightLst').click(function () {
      var condition = $(this).hasClass("leftLst");
      if(condition)
        click(0,this);
      else
        click(1,this)
    });
    rescarouselSize();
  $(window).resize(function() {
    rescarouselSize();
  });
  function rescarouselSize()
  {
    var incno = 0;
    var dataItems = ("data-items");
    var itemClass = ('.item');
    var id = 0;
    var btnParentSb = '';
    var itemsSplit = '';
    var sampwidth = $(itemsMainDiv).width();
    var bodyWidth = $('.documents-main').width();
    $(itemsDiv).each(function() {
      id=id+1;
      var itemNumbers = $(this).find(itemClass).length;
        btnParentSb = $(this).parent().attr(dataItems);
        itemsSplit = btnParentSb.split(',');
        $(this).parent().attr("id","ResSlid"+id);
      if(bodyWidth>=375)
      {
        incno=itemsSplit[1];
        itemWidth = sampwidth/incno;
      }
      else
      {
        incno=itemsSplit[0];
        itemWidth = sampwidth/incno;
      }
      $(this).css({'transform':'translateX(0px)','width':itemWidth*itemNumbers});
      $(this).find(itemClass).each(function(){
        $(this).outerWidth(itemWidth);
      });

      $(".leftLst").addClass("d-none");
      $(".rightLst").removeClass("d-none");

    });
  }
  function rescarousel(e, el, s){
    var leftBtn = ('.leftLst');
    var rightBtn = ('.rightLst');
    var translateXval = '';
    var divStyle = $(el+' '+itemsDiv).css('transform');
    var values = divStyle.match(/-?[\d\.]+/g);
    var xds = Math.abs(values[4]);
      if(e==0){
        translateXval = parseInt(xds)-parseInt(itemWidth*s);
        $(el+' '+rightBtn).removeClass("d-none");

        if(translateXval<= itemWidth/2){
          translateXval = 0;
          $(el+' '+leftBtn).addClass("d-none");
        }
      }
      else if(e==1){
        var itemsCondition = $(el).find(itemsDiv).width()-$(el).width();
        translateXval = parseInt(xds)+parseInt(itemWidth*s);
        $(el+' '+leftBtn).removeClass("d-none");

        if(translateXval>= itemsCondition-itemWidth/2){
          translateXval = itemsCondition;
          $(el+' '+rightBtn).addClass("d-none");
        }
      }
      $(el+' '+itemsDiv).css('transform','translateX('+-translateXval+'px)');
  }
  function click(ell,ee){
    var Parent ="#"+$(ee).parent().attr("id");
    var slide = $(Parent).attr("data-slide");
    rescarousel(ell, Parent, slide);
  }

  });



})(jQuery);