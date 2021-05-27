let sheet = (function() {
    let style = document.createElement("style");
    style.appendChild(document.createTextNode(""));
    document.head.appendChild(style);
    return style.sheet;
   })();
   initialBookmark = "page=1";
   function editToolBar(){
    //when the page is resized, the viewer hides and move some buttons around.
    //this function forcibly show all buttons so none of them disappear or re-appear on page resize
    removeGrowRules();
  
    /* Reorganizing the UI */
    // the 'addElemFromSecondaryToPrimary' function moves items from the secondary nav into the primary nav
    // there are 3 primary nav regions (toolbarViewerLeft, toolbarViewerMiddle, toolbarViewerRight)
  
    //adding elements to left part of toolbar
    
    addElemFromSecondaryToPrimary('zoomIn', 'toolbarViewerLeft')
    addElemFromSecondaryToPrimary('zoomOut', 'toolbarViewerLeft')
  
    //adding elements to middle part of toolbar
    addElemFromSecondaryToPrimary('previous', 'toolbarViewerMiddle')
    addElemFromSecondaryToPrimary('next', 'toolbarViewerMiddle')
    addElemFromSecondaryToPrimary('pageNumber', 'toolbarViewerMiddle')
    addElemFromSecondaryToPrimary('numPages', 'toolbarViewerMiddle')
  
    //adding elements to right part of toolbar
    addElemFromSecondaryToPrimary('download', 'toolbarViewerRight')
    addElemFromSecondaryToPrimary('documentProperties', 'toolbarViewerRight')
  
    /* Hiding elements */
    removeElement('secondaryToolbarToggle')
    removeElement('scaleSelectContainer')
    removeElement('presentationMode')
    removeElement('openFile')
    removeElement('print')
    removeElement('viewOutline')
    removeElement('viewAttachments')
    removeElement('viewLayers')
    removeElement('viewBookmark')
    removeElement('viewFind')
    removeElement('splitToolbarButton')
   }
  function addElemFromSecondaryToPrimary(elemID, parentID){
      let element = $('#'+elemID);
      let parent = $('#'+parentID);
      $(element).css('min-width', '0px');
      $(element).empty();
      $(parent).append(element);
  }
  function removeElement(elemID){
      $('#'+elemID).remove();
  }
  function removeGrowRules(){
      addCSSRule(sheet, '.hiddenSmallView *', 'display:block !important');
      addCSSRule(sheet, '.hiddenMediumView', 'display:block !important');
      addCSSRule(sheet, '.hiddenLargeView', 'display:block !important');
      addCSSRule(sheet, '.visibleSmallView', 'display:block !important');
      addCSSRule(sheet, '.visibleMediumView', 'display:block !important');
      addCSSRule(sheet, '.visibleLargeView', 'display:block !important');
  }
  function addCSSRule(sheet, selector, rules, index) {
      if("insertRule" in sheet) {
          sheet.insertRule(selector + "{" + rules + "}", index);
      }
      else if("addRule" in sheet) {
          sheet.addRule(selector, rules, index);
      }
  }
  $(document).ready(editToolBar);