window.addStatement = function (intra_id) {
    event.preventDefault()
    $.ajax({
        type: 'POST',
        url: 'https://call_backend_add_statement',
        contentType: "application/json; charset=utf-8",
        dataType: 'json',
        data: JSON.stringify({
            intra_id: intra_id,
            all_results: all_results,
            origin: all_data['origin'][0],
            keywords: all_data['keywords']
        }),
        success: function(data) {
            console.log("add statement result")
            console.log(data);
            updateGraphAnalyze(data)
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.error('Error:', errorThrown);
        }
    });
}

window.removeStatement = function (intra_id) {
    console.log("REMOVE STATEMENT")
    event.preventDefault()
    $.ajax({
        type: 'POST',
        url: 'https://call_backend_Remove_statement',
        contentType: "application/json; charset=utf-8",
        dataType: 'json',
        data: JSON.stringify({
            intra_id: intra_id,
            all_results: all_results,
            origin: all_data['origin'][0],
            keywords: all_data['keywords']
        }),
        success: function(data) {
            console.log("add statement result")
            console.log(data);
            updateGraphAnalyze(data)
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.error('Error:', errorThrown);
        }
    });
}