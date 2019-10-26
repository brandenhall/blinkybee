(function() {
  var patterns = {};
  
  function update(data) {
    console.log(data);
    $.ajax({
      url:"/update",
      type:"POST",
      data: JSON.stringify(data),
      contentType:"application/json; charset=utf-8",
      dataType:"json",
    });
  }

  function changeBrightness() {
    update({brightness: $("#brightness").val()});
  }

  function selectPattern() {
    var currentPattern = patterns[$("#pattern").val()];
    update({pattern: $("#pattern").val()});
    $("#settings").empty();

    currentPattern.settings.forEach(function(setting) {
      markup = '<div class="form-group">';
      markup += '<label for="'+setting.key+'">'+setting.label+'</label>';

      if (setting.type == "color") {
        markup += '<input type="color" class="form-control select-setting" name="'+setting.key+'" value="'+setting.default+'"></input>';
      
      } else if (setting.type == "select") {
        markup += '<select class="form-control color-setting" name="'+setting.key+'">';
        setting.options.forEach(function(option) {
          markup += '<option value="'+option[0]+'"';
          if (option[0] == setting.default) {
            markup += ' selected'
          }
          markup += '>'+option[1]+'</option>';
        });
        markup += '</select>'
      }
      markup += '</div>';
      $("#settings").append(markup);
    });
  }

  function changeOption(evt) {
    var name = evt.target.getAttribute("name");
    var value = $(evt.target).val();
    var options = {};
    options[name] = value;
    update({"options": options});
  }

  function init() {
    $("#brightness").change(changeBrightness);
    $("#pattern").change(selectPattern);
    $(document).on('input', '.color-setting', changeOption);
    $(document).on('change', '.select-setting', changeOption); 

    $.getJSON("patterns.json", function(data) {
      var $patternSelect = $("#pattern");
      patterns = data;
      for (patternKey in patterns) {
        var pattern = patterns[patternKey];
        $patternSelect.append('<option value="'+patternKey+'">' + pattern.name + '</option>');
      }
      selectPattern();
    });
  }

  $(document).ready(init);
})();