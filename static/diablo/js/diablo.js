function loadHero(that,pk) {
  $(".hero-tab").removeClass("active").removeClass("loading");
  if (!!$("#hero-"+pk).length) {
    showTab(pk);
    $(that).removeClass("loading").addClass("active");
    return;
  }
  $(that).addClass("loading");
  $.get(
    "/diablo/hero/"+pk+"/",
    function (data) {
      $("#diablo_armory").append($(data));
      showTab(pk)
      $(that).removeClass("loading").addClass("active");
    },
        "html"
  )
}
function showTab(pk) {
  $("#diablo_armory").children().hide();
  $("#hero-"+pk).show();
}
function showBonuses(that,pk) {
  $(".bonus-stat.active").removeClass("active");
  $(that).addClass("active");
  $(".bonus-value").hide();
  $(".bonus-type-"+pk).show();
}