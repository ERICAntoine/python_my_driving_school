function parseObject(json){
    for(let i = 0; i < json.length; i++){
        for(let key in json[i]){
            if(key === 'pk'){
                console.log()
                json[i]["fields"]["idPlanning"] = json[i][key];
            }
        }
        json[i] = json[i]["fields"];
    }
    return json;
}

function updatePlanning(json){
    const csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    $.ajaxSetup({headers: { "X-CSRFToken": csrftoken }});
    $.post('/app/planning/update', json)
    .done(function() {
        alert( "second success" );
    })
    .fail(function() {
      alert( "error" );
    })
    .always(function() {
      alert( "finished" );
    });
}